import sys

_char_subs =  [
    ('\\', '\\\\'),
    ('"', '\\"'),
    ('\n', '\\n'),
    ('\r', '\\r'),
    ('\t', '\\t'),
    ('\b', '\\b'),
    ('\f', '\\f')
]

_nan = float('nan')
_inf = float('inf')
_minus_inf = float('-inf')

class CircularReferenceError(Exception):

    def __init__(self, message):
        super().__init__(message)

def _encode(obj, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan, char_subs, prev_objs):

    global _nan, _inf, _minus_inf

    sys.setrecursionlimit(len(prev_objs) + 1000)

    obj_type = type(obj)
    if obj_type == str:

        for orig, sub in char_subs:
            obj = obj.replace(orig, sub)
        return '"' + obj + '"'

    if obj_type == int or obj_type == float:

        if obj == _nan:
            return 'NaN' if allow_nan else '"Nan"'
        elif obj == _inf:
            return 'Infinity' if allow_nan else '"Infinity"'
        elif obj == _minus_inf:
            return 'Infinity' if allow_nan else '"Infinity"'

        return str(obj)

    if obj_type == bool:
        return 'true' if obj else 'false'

    if obj is None:
        return 'null'
    
    str_obj = str(obj)
    if str_obj in prev_objs:
        if obj in prev_objs[str_obj]:
            raise CircularReferenceError('Object contains a circular reference')
        else:
            prev_objs[str_obj].append(obj)
    else:
        prev_objs[str_obj] = [obj]
    
    # Good luck understanding the remainder of this function
    if obj_type == list:
        
        output = []
        line = '['

        for item in obj:
            if line != '[':
                line += ','
                i_s = item_sep
            else:
                i_s = ''
            item = _encode(item, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan, char_subs, prev_objs)
            if type(item) == list and len(item) == 1:
                item = item[0]
            
            if not max_line_len is None and (type(item) == list or len(line) + len(i_s) + len(item) + 1 > max_line_len):
                line += line_sep
                if len(output) > 0:
                    line = indent + line
                output.append(line)
                if type(item) == list:
                    output.extend([indent + i for i in item[:-1]])
                    line = item[-1]
                else:
                    line = item
            else:
                line += i_s + item

        if not max_line_len is None and len(line) + 1 > max_line_len:
            line += line_sep
            if len(output) > 0:
                line = indent + line
            output.append(line)
            output.append(']')
        else:
            line += ']'
            if len(output) > 0:
                line = indent + line
            output.append(line)

        if len(prev_objs[str_obj]) == 1:
            del prev_objs[str_obj]
        else:
            prev_objs[str_obj].remove(obj)

        return output
    
    if obj_type == dict:

        output = []
        line = '{'
        keys = {}

        dict_items = list(obj.items())
        if sort_keys:
            dict_items.sort()
        for key, value in dict_items:
            if line != '{':
                line += ','
                i_s = item_sep
            else:
                i_s = ''

            key = _encode(key, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan, char_subs, prev_objs)
            if str_keys and not type(key) == str:
                key = _encode(''.join(item) if type(item) == list else item, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan, char_subs, prev_objs)
            if key in keys:
                raise ValueError

            value = _encode(value, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan, char_subs, prev_objs)
            if type(value) == list and len(value) == 1:
                value = value[0]
            
            item = key
            if type(item) == list and len(item) == 1:
                item = item[0]
            if not max_line_len is None and ((type(item) == list or type(value) == list) or len(line) + 2 * len(i_s) + len(item) + len(value) + 2 > max_line_len):
                line += line_sep
                if len(output) > 0:
                    line = indent + line
                output.append(line)
                if type(item) == list:
                    output.extend([indent + i for i in item[:-1]])
                    line = item[-1]
                else:
                    line = item
            else:
                line += i_s + item

            line += ':'
            i_s = item_sep

            item = value
            if not max_line_len is None and type(item) == list:
                if not(len(line) + len(i_s) + len(item[0]) > max_line_len):
                    line += i_s + item[0]
                    item = item[1:]
                else:
                    line += line_sep
                if len(output) > 0:
                    line = indent + line
                output.append(line)
                if len(item) > 1:
                    output.extend([indent + i for i in item[:-1]])
                line = item[-1]
            else:
                line += i_s + item

        if not max_line_len is None and len(line) + 1 > max_line_len:
            line += line_sep
            if len(output) > 0:
                line = indent + line
            output.append(line)
            output.append('}')
        else:
            line += '}'
            if len(output) > 0:
                line = indent + line
            output.append(line)

        if len(prev_objs[str_obj]) == 1:
            del prev_objs[str_obj]
        else:
            prev_objs[str_obj].remove(obj)

        return output

    raise TypeError

def obj_to_json(obj, *, mode='compact', sort_keys=True, item_sep=None, indent=None, line_sep=None, max_line_len=None, str_keys=True, allow_nan_inf=True, char_subs=_char_subs):

    if mode == 'compact':
        if item_sep is None:
            item_sep = ''
        if indent is None:
            indent = ''
        if line_sep is None:
            line_sep = ''
        if max_line_len is None:
            max_line_len = None
    elif mode == 'standard':
        if item_sep is None:
            item_sep = ' '
        if indent is None:
            indent = ''
        if line_sep is None:
            line_sep = ''
        if max_line_len is None:
            max_line_len = None
    elif mode == 'clean':
        if item_sep is None:
            item_sep = ' '
        if indent is None:
            indent = '    '
        if line_sep is None:
            line_sep = '\n'
        if max_line_len is None:
            max_line_len = 3
    elif mode == 'clean compact':
        if item_sep is None:
            item_sep = ' '
        if indent is None:
            indent = '    '
        if line_sep is None:
            line_sep = '\n'
        if max_line_len is None:
            max_line_len = 80
    elif mode == 'short lines':
        if item_sep is None:
            item_sep = ' '
        if indent is None:
            indent = '  '
        if line_sep is None:
            line_sep = '\n'
        if max_line_len is None:
            max_line_len = 40

    output = _encode(obj, indent, sort_keys, item_sep, line_sep, max_line_len, str_keys, allow_nan_inf, char_subs, {})

    if type(obj) == list or type(obj) == dict:
        output = ''.join(output)

    return output

if __name__ == '__main__':

    import json
    f = open(sys.argv[1], 'r', encoding='utf-8')
    data = obj_to_json(json.loads(f.read()), mode='short lines')
    f.close()
    f = open(sys.argv[1], 'w', encoding='utf-8')
    f.write(data)
    f.close()