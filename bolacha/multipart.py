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

from uuid import uuid4
from urllib import quote_plus, urlencode
from glob import glob
from os.path import basename
from mimetypes import guess_type

BOUNDARY = uuid4().hex

def is_file(obj):
    return hasattr(obj, 'read') and callable(obj.read)

def to_str(s):
    if not isinstance(s, basestring):
        s = unicode(s)
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    return quote_plus(s)

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
