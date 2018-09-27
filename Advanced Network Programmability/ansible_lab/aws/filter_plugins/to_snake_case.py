from jinja2.utils import soft_unicode

'''
USAGE:
  - debug:
      msg: '{{RegularExpressionsAreFunky | to_snake_case}}'
'''


class FilterModule(object):
    def filters(self):
        return {
            'to_snake_case': to_snake_case
        }


def to_snake_case(not_snake_case):
    final = ''
    for i in xrange(len(not_snake_case)):
        item = not_snake_case[i]
        if i < len(not_snake_case) - 1:
            next_char_will_be_underscored = (
                not_snake_case[i+1] == "_" or
                not_snake_case[i+1] == " " or
                not_snake_case[i+1].isupper()
            )
        if (item == " " or item == "_") and next_char_will_be_underscored:
            continue
        elif (item == " " or item == "_"):
            final += "_"
        elif item.isupper():
            final += "_"+item.lower()
        else:
            final += item
    if final[0] == "_":
        final = final[1:]
    return final
