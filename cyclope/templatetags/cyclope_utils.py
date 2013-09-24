#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
templatetags.cyclope_utils
-------------------

General utility helper tags.
"""

from django import template
from django.utils.safestring import mark_safe
from django.contrib.markup.templatetags import markup

import cyclope.settings as cyc_settings
from cyclope.utils import nohang, get_object_name, get_app_label
from cyclope.utils.lru_cache import LRULimitedSizeDict


MARKUP_RENDERER_WAIT = 5
MARKUP_CACHE_SIZE = 250

register = template.Library()

class JoinedStrings(template.Node):
    """Join a list of strings and put the result in the given template variable.

    The list can be of strings or template variables holding string values.
    """
    def __init__(self, element_list, var_name):
        self.data = []
        for element in element_list:
            if element[0] not in ['"', "'"]:
                self.data.append(template.Variable(element))
            else:
                self.data.append(element[1:-1])
        self.var_name = var_name

    def render(self, context):
        strings = []
        for item in self.data:
            if isinstance(item, template.Variable):
                strings.append(item.resolve(context))
            else:
                strings.append(item)

        context[self.var_name] = "".join(strings)
        return ''

@register.tag('join')
def do_join(parser, token):
    bits = token.contents.split()
    if bits[-2] != 'as':
        raise template.TemplateSyntaxError, "Missing 'as' argument for '%s' tag" % bits[0]
    return JoinedStrings(bits[1:-2], bits[-1])


class Alias(template.Node):
    def __init__(self, origin, alias):
        self.value = template.Variable(origin)

        if alias[0] not in ['"', "'"]:
            self.alias = template.Variable(alias)
        else:
            self.alias = alias[1:-1]

    def render(self, context):
        if isinstance(self.alias, template.Variable):
            context[unicode(self.alias.resolve(context))] = self.value.resolve(context)
        else:
            context[self.alias] = self.value.resolve(context)
        return ''

@register.tag('alias')
def do_alias(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "'%s' tag takes exactly four arguments" % bits[0]
    if bits[-2] != 'as':
        raise template.TemplateSyntaxError, "Missing 'as' argument for '%s' tag" % bits[0]
    return Alias(bits[1], bits[3])


# code from http://djangosnippets.org/snippets/539/
class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

@register.tag('assign')
def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

# based on http://djangosnippets.org/snippets/1627/
class AppendGetNode(template.Node):
    """
    Append paramaters to a GET querystring
    """
    def __init__(self, extra_context=None):
        self.extra_context = extra_context or {}

    def render(self, context):
        get = context['request'].GET.copy()
        for key, val in self.extra_context.iteritems():
            get[key] = val.resolve(context)

        get_encoded = ""
        if len(get):
            get_encoded = "%s" % get.urlencode()
        return get_encoded

@register.tag('append_to_get')
def do_append_to_get(parser, token):
    from django.template.base import token_kwargs
    kwargs = token_kwargs(token.split_contents()[1:], parser)
    return AppendGetNode(kwargs)


def admin_list_filter_without_all(cl, spec):
    choices = list(spec.choices(cl))
    choices.pop(0) # Remove "all" option
    return {'title': spec.title, 'choices' : choices}
admin_list_filter_without_all = register.inclusion_tag('admin/filter.html')(admin_list_filter_without_all)


lru_cache = LRULimitedSizeDict(size_limit=MARKUP_CACHE_SIZE)

@register.filter
def smart_style(value):
    value_hash = hash(value)
    result = lru_cache.get(value_hash, None)
    if result is not None:
        return result

    style = cyc_settings.CYCLOPE_TEXT_STYLE
    styles = {"wysiwyg": mark_safe,
              "markdown": markup.markdown,
              "textile": markup.textile,
              "raw": mark_safe}
    renderer = styles.get(style, None)
    if renderer is None:
        raise ValueError("Bad TEXT_STYLE option: %s" % style)
    else:
        result, success = nohang.run(renderer, args=(value,), wait=MARKUP_RENDERER_WAIT)
        if not success:
            result = value
        lru_cache[value_hash] = result
        return result

smart_style.is_safe = True


class PdbNode(template.Node):
    def render(self, context):
        # These imports are here because ipython creates a temporary dir and files
        # each time in /tmp if the user has no homedir.
        try:
            import ipdb as pdb
        except ImportError:
            import pdb
        # Access vars at the prompt for an easy reference to
        # variables in the context
        vars = []
        for dict in context.dicts:
            for k, v in dict.items():
                vars.append(k)
                locals()[k] = v
        pdb.set_trace()
        # You may access all context variables directly (they are stored in locals())
        return ''

@register.tag("pdb_debug")
def pdbdebug_tag(parser, token):
    """Tag that inspects template context.

    Usage:
    {% pdb_debug %}

    You can then access your context variables directly at the prompt.

    The vars variable additonally has a reference list of keys
    in the context.
    """
    return PdbNode()


@register.filter
def inline_template(obj, inline_view_name):
    """
    Returns the name of the requested inline template for the object obj.

    Eg: {{ article|inline_template:"teaser" }} -> "articles/article_teaser.html"
    """
    return "%s/%s_%s.html" % (get_app_label(obj), get_object_name(obj),
                              inline_view_name)

from django.utils.encoding import force_unicode
from django.utils.html import (conditional_escape, escapejs, fix_ampersands,
    escape, urlize as urlize_impl, linebreaks, strip_tags)

@register.filter(is_safe=True, needs_autoescape=True)
def unordered_list_css(value, autoescape=None):
    """
    Recursively takes a self-nested list and returns an HTML unordered list --
    WITHOUT opening and closing <ul> tags.

    The list is assumed to be in the proper format. For example, if ``var``
    contains: ``[('States', 'states'), [('Kansas', 'knss'), [('Lawrence', 'lw'), ('Topeka', 'tk')]]]``,
    then ``{{ var|unordered_list }}`` would return::

        <li class="states">States
        <ul>
                <li class="knss">Kansas
                <ul>
                        <li class="lw">Lawrence</li>
                        <li class="tk">Topeka</li>
                </ul>
                </li>
        </ul>
        </li>
    """
    if autoescape:
        escaper = conditional_escape
    else:
        escaper = lambda x: x
    def _helper(list_, tabs=1):
        indent = u'\t' * tabs
        output = []

        list_length = len(list_)
        i = 0
        while i < list_length:
            title, css_class = list_[i]
            sublist = ''
            sublist_item = None
            if isinstance(title, (list, tuple)):
                sublist_item = title
                title = ''
            elif i < list_length - 1:
                next_item = list_[i+1]
                if next_item and isinstance(next_item[0], (list, tuple)):
                    # The next item is a sub-list.
                    sublist_item = next_item
                    # We've processed the next item now too.
                    i += 1
            if sublist_item:
                sublist = _helper(sublist_item, tabs+1)
                sublist = '\n%s<ul>\n%s\n%s</ul>\n%s' % (indent, sublist,
                                                         indent, indent)
            output.append('%s<li class="%s">%s%s</li>' % (indent, css_class,
                    escaper(force_unicode(title)), sublist))
            i += 1
        return '\n'.join(output)
    return mark_safe(_helper(value))
