from django import template

register = template.Library()

censor_list = ['редис']


@register.filter(name='censor_func')
def censor_func(value: str):
    for word in value.split():
        for censor in censor_list:
            if censor in word.lower():
                value = value.replace(word, word[0] + '*'*(len(word)-2) + word[-1])
    return f'{value}'
