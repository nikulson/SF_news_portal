from django import template


register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    Stop_List = ['Пайтон', 'Зенит', 'текст', 'футбол']
    sentence = value.split()
    for i in Stop_List:
        for words in sentence:
            if i in words:
                pos = sentence.index(words)
                sentence.remove(words)
                sentence.insert(pos, '*' * len(i))
    return " ".join(sentence)