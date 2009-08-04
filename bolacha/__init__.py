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
from urllib import urlencode
from httplib2 import Http as HTTPClass

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

        if isinstance(body, dict):
            rbody = urlencode(body)
        else:
            rbody = unicode(body)

        if headers is None:
            headers = {}

        if not isinstance(headers, dict):
            raise TypeError, 'Bolacha.request, parameter headers must be ' \
                  'a dict or NoneType. Got %s' % repr(headers)

        rheaders = self.headers.copy()
        rheaders.update(headers)

        response, content = self.http.request(url, method, rbody, rheaders)

        self.headers.update(response)

        return response, content
