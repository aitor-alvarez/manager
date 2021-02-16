from django import template
import datetime

register = template.Library()

@register.filter
def check_class_name(value):
	return value.__class__.__name__



@register.filter(name='subtract')
def subtract_dates(date1, date2):
	if date1>date2:
		dif = datetime.datetime.combine(datetime.date(1, 1, 1), date1)-datetime.datetime.combine(datetime.date(1, 1, 1), date2)
	else:
		dif = datetime.datetime.combine(datetime.date(1, 1, 1), date2) - datetime.datetime.combine(
			datetime.date(1, 1, 1), date1)
	return dif

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""

@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])