import json
from collections import OrderedDict
from .models import Plan
def date_handler(obj):
    """
    Handles JSON serialization for datetime values
    """
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def convert_field_names(event_list):
    """
    Converts atribute names from Python code convention to the
    attribute names used by FullCalendar 
    """
    for event in event_list:
        for key in event.keys():
            event[snake_to_camel_case(key)] = event.pop(key)
    return event_list


def snake_to_camel_case(s):
    """
    Converts strings from 'snake_case' (Python code convention)
    to CamelCase
    """
    new_string = s

    leading_count = 0
    while new_string.find('_') == 0:
        new_string = new_string[1:]
        leading_count +=1
    
    trailing_count = 0
    while new_string.rfind('_') == len(new_string) - 1:
        new_string = new_string[:-1]
        trailing_count +=1
    
    new_string = ''.join([word.title() for word in new_string.split('_')])
    leading_underscores = '_' * leading_count
    trailing_underscores = '_' * trailing_count
    return leading_underscores + new_string[0].lower() + new_string[1:] + trailing_underscores


def plans_to_json(plans_queryset):
    events_values = list(plans_queryset.values('plan', 'plan_type', 'begin', 'end', 'id'))
    events_values = convert_field_names(events_values)
    gantt_chart = create_gantt_chart(json.dumps(events_values, default=date_handler, sort_keys=False))
    return gantt_chart

def create_gantt_chart(json_string):
    chart_data = json.loads(json_string)
    dicts = []
    for c in chart_data:
        json_data = OrderedDict()
        plan = Plan.objects.get(pk=c['plan'])
        if c['planType'] == 'P':
            json_data['id'] = str(c['id']) 
            json_data['name'] = 'Propagation -'+str(plan.crop)
            json_data['start'] = c['begin']
            json_data['end'] = c['end']
            json_data['custom_class'] = 'milestone-orange'
        elif c['planType'] == 'PL':
            json_data['id'] = str(c['id']) 
            json_data['name'] = 'Plantation'
            json_data['start'] = c['begin']
            json_data['end'] = c['end']
            json_data['dependencies'] = str(c['id']-1)
            json_data['custom_class'] = 'milestone-blue'
        elif c['planType'] == 'V':
            json_data['id'] = str(c['id']) 
            json_data['name'] = 'Vegetative'
            json_data['start'] = c['begin']
            json_data['end'] = c['end']
            json_data['dependencies'] = str(c['id']-1)
            json_data['custom_class'] = 'milestone-green'
        elif c['planType'] == 'H':
            json_data['id'] = str(c['id']) 
            json_data['name'] = 'Harvest'
            json_data['start'] = c['begin']
            json_data['end'] = c['end']
            json_data['dependencies'] = str(c['id']-1)
            json_data['custom_class'] = 'milestone-khaki'
        elif c['planType'] == 'C':
            json_data['id'] = str(c['id']) 
            json_data['name'] = 'Cleaning'
            json_data['start'] = c['begin']
            json_data['end'] = c['end']
            json_data['dependencies'] = str(c['id']-1)
            json_data['custom_class'] = 'milestone-brown'
        dicts.append(json_data)
    return json.dumps(dicts, indent=4, sort_keys=False)