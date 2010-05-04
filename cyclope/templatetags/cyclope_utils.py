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
            self.alias = alias

    def render(self, context):
        if isinstance(self.alias, template.Variable):
            context[self.alias.resolve(context)] = self.value.resolve(context)
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
