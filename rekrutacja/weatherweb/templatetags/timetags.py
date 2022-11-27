from datetime import datetime

from django import template

register = template.Library()


def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')


register.filter(convert_timestamp)
