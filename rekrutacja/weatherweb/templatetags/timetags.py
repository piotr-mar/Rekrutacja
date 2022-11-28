from datetime import datetime, timedelta

from django import template

register = template.Library()


def convert_timestamp(timestamp):
    time = datetime.utcfromtimestamp(timestamp) + timedelta(hours=1)
    time = time.strftime("%d/%m/%Y")
    return time


register.filter(convert_timestamp)
