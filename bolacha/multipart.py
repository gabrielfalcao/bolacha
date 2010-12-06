# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bolacha - http library for python, with cookies and upload support>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import types
from uuid import uuid4
from urllib import quote_plus, urlencode
from glob import glob
from os.path import basename
from mimetypes import guess_type

BOUNDARY = uuid4().hex

def is_file(obj):
    return hasattr(obj, 'read') and callable(obj.read)

def to_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """ took from django smart_str """

    if strings_only and isinstance(s, (types.NoneType, int)):
        return s

    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def expand_items(dictionary):
    """
    Given a dict like {'key': ('value1', 'value2')} returns
    a list like [('key','value1'), ('key', 'value2')]
    """
    items = []
    for key, value in dictionary.items():
        if isinstance(value, (list, tuple)):
            items.extend([(key, item) for item in value])
        else:
            items.append((key, value))
    return items

def encode_multipart(boundary, data):
    lines = []

    for key, value in expand_items(data):
        if is_file(value):
            lines.extend(encode_file(boundary, key, value))
        else:
            if is_file(value):
                lines.extend(encode_file(boundary, key, value))
            else:
                lines.extend([
                    '--' + boundary,
                    'Content-Disposition: form-data; name="%s"' % to_str(key),
                    '',
                    to_str(value)
                ])

    lines.extend([
        '--' + boundary + '--',
        '',
    ])
    return '\r\n'.join(lines)

def guess_mime(path):
    mime, x = guess_type(path)
    return mime or 'application/octet-stream'

def encode_file(boundary, key, file):
    return [
        '--' + boundary,
        'Content-Disposition: form-data; name="%s"; filename="%s"' \
            % (to_str(key), to_str(basename(file.name))),
        'Content-Type: %s' % guess_mime(file.name),
        '',
        to_str(file.read())
    ]
