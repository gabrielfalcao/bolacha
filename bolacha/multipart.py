#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

# some parts of the code below were took from Django Web Framework test client:
# http://code.djangoproject.com/browser/django/tags/releases/1.1/django/test/client.py
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

def encode_multipart(boundary, data):
    lines = []

    for key, value in data.items():
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
