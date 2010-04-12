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
from httplib2 import Http as HTTPClass
from bolacha.multipart import BOUNDARY
from bolacha.multipart import encode_multipart
from bolacha.multipart import urlencode
from bolacha.multipart import is_file
from bolacha.meta import __version__
from bolacha.meta import __release__

HTTP_METHODS = (
    'OPTIONS',
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'TRACE',
    'CONNECT',
)

RFC_LOCATION = 'Take a look at http://www.w3.org/Protocols/rfc2616/' \
               'rfc2616-sec9.html to see valid method definitions'

class Bolacha(object):
    headers = None
    def __init__(self, http=None, persistent=True, **kw):
        if http is not None and not isinstance(http, type) and not callable(http):
            raise TypeError, 'Bolacha takes a class or callable as parameter, ' \
                  'got %s' % repr(http)

        if http is not None:
            self.http = http(**kw)
        else:
            self.http = HTTPClass(**kw)

        self.persistent = persistent
        self.headers = {}

    def post(self, url, body=None, headers=None):
        return self.request(url, 'POST', body=body, headers=headers)

    def get(self, url, body=None, headers=None):
        return self.request(url, 'GET', body=body, headers=headers)

    def put(self, url, body=None, headers=None):
        return self.request(url, 'PUT', body=body, headers=headers)

    def delete(self, url, body=None, headers=None):
        return self.request(url, 'DELETE', body=body, headers=headers)

    def head(self, url, body=None, headers=None):
        return self.request(url, 'HEAD', body=body, headers=headers)

    def request(self, url, method, body=None, headers=None):
        if not isinstance(url, basestring):
            raise TypeError, 'Bolacha.request, parameter url must be ' \
                  'a string. Got %s' % repr(url)

        if not isinstance(method, basestring):
            raise TypeError, 'Bolacha.request, parameter method must be ' \
                  'a string. Got %s' % repr(method)

        if method not in HTTP_METHODS:
            raise TypeError, 'Bolacha.request, parameter method must be ' \
                  'a valid HTTP method. Got %s. %s' % (method,
                                                        RFC_LOCATION)

        if body is None:
            body = ''

        if not isinstance(body, (basestring, dict)):
            raise TypeError, 'Bolacha.request, parameter body must be ' \
                  'a string or dict. Got %s.' % (repr(body))

        is_urlencoded = False

        body_has_file = isinstance(body, dict) and any([is_file(fobj)
                                                        for fobj in body.values()])

        if isinstance(body, dict):
            if body_has_file:
                rbody = encode_multipart(BOUNDARY, body)
            else:
                rbody = urlencode(body)
                is_urlencoded = True
        else:
            rbody = body

        if headers is None:
            headers = {}

        if not isinstance(headers, dict):
            raise TypeError, 'Bolacha.request, parameter headers must be ' \
                  'a dict or NoneType. Got %s' % repr(headers)

        rheaders = self.headers.copy()
        rheaders.update(headers)

        if self.persistent:
            if 'set-cookie' in self.headers:
                rheaders['Cookie'] = self.headers['set-cookie']

        if 'set-cookie' in rheaders:
            del rheaders['set-cookie']

        if is_urlencoded and not 'Content-type' in rheaders:
            rheaders['Content-type'] = 'application/x-www-form-urlencoded'
        elif body_has_file:
            rheaders['Content-type'] = 'multipart/form-data; boundary=%s' % BOUNDARY
            rheaders['content-length'] = '%d' % len(rbody)

        response, content = self.http.request(url, method, rbody, rheaders)

        if self.persistent and 'set-cookie' in response:
            self.headers['set-cookie'] = response['set-cookie']

        if not self.persistent:
            if 'connection' in response:
                self.headers['connection'] = response['connection']

        return response, content
