# -*- coding: utf-8 -*-
"""
templatetags.layout
-------------------
"""
from django import template

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

