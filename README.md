# jsonformatter
A slow Python 3 module/program for producing somewhat clean JSON strings made because I was bored<br>
The documentation is pretty bad.

Requirements
--------------
- Python 3 (preferably 3.6.2 or later)

Installation
--------------
Download and extract the ZIP file and move the jsonformatter.py file to wherever you want. (other steps are needed to use it as a module)

Exceptions
--------------
- `CircularReferenceError`: raised when a circular reference is detected
- `TypeError`
- `ValueError`

Functions
--------------
`def obj_to_json(obj, *, mode='compact', sort_keys=True, item_sep=None, indent=None, line_sep=None, max_line_len=None, str_keys=True, allow_nan_inf=True, char_subs=_char_subs)`
returns a json string
- `obj`: the object (string, number, boolean, None, list, or dict) to be converted to json
- `mode`: the preset to use. This affects `item_sep`, `indent`, `line_sep`, and `max_line_len`. If this value isn't set to a valid preset, it is ignored. 
  Set this value to any of the below to use a preset:
  - `standard`
  - `compact`
  - `clean`
  - `clean compact`
  - `short lines`
<br>Arguments that are manually set will override the preset.
- `sort_keys`: whether dictionary keys are sorted or not
- `item_sep`: the string that comes after `,` (for values) and `:` (for keys) in both lists and dicts
- `indent`: the string determining the indent
- `line_sep`: the string that separates lines
- `max_line_len`: the max length (usually) of a line not including indentation
- `str_keys`: if this is True, keys will always be casted to strings
- `allow_nan_inf`: if this is False, `nan`, `inf`, and `-inf` values will be converted to strings to conform to the official json spec
- `char_subs`: a list of tuples of character substitutions that are applied to strings (this is used to escape characters by default)

Usage (test)
--------------
1. Using terminal or command prompt, navigate to the directory of jsonformatter.py
2. Enter the following command: `python jsonformatter.py [json filename]`
3. Open the json file to see the formatting
