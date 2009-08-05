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
import types
from mox import Mox
from nose.tools import assert_equals
from utils import assert_raises

from bolacha import Bolacha
from httplib2 import Http

def test_creation_takes_class():
    msg = r'Bolacha takes a class or callable as parameter, got %r'
    assert_raises(TypeError,
                  Bolacha, 5,
                  exc_pattern=msg % 5)
    assert_raises(TypeError,
                  Bolacha, 'blabla',
                  exc_pattern=msg % 'blabla')

def test_instantiate_class_with_kwargs():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    klass_mock(cache_path='/some/path', other_param=10)

    mocker.ReplayAll()
    Bolacha(klass_mock, cache_path='/some/path', other_param=10)
    mocker.VerifyAll()

def test_keeps_http_instance_after_instantiation():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    instance_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(instance_mock)

    mocker.ReplayAll()
    b = Bolacha(klass_mock)
    assert_equals(b.http, instance_mock)
    mocker.VerifyAll()

def test_uses_httplib2_Http_as_default_http_class():
    b = Bolacha()
    assert isinstance(b.http, Http), 'Bolacha().http should be instance of ' \
           'httplib2.Http, got %s' % repr(b.http)

def test_is_persistent_by_default():
    b = Bolacha()
    assert b.persistent is True, 'Bolacha should be persistent by default'

def test_can_be_not_persistent():
    b = Bolacha(persistent=False)
    assert b.persistent is False, 'Bolacha should be persistent by default'

def test_is_persistent_by_default():
    b = Bolacha()
    assert b.persistent

def test_has_headers_attribute():
    b = Bolacha()
    assert hasattr(b, 'headers'), 'Bolacha should be "headers"'
    assert isinstance(b.headers, dict), \
           'Bolacha.headers should be a dict, got %s' % repr(b.headers)

def test_headers_are_instance_scoped():
    b1 = Bolacha()
    b2 = Bolacha()
    b1.headers['foo'] = 'foo foo'
    b2.headers['bar'] = 'bar bar'

    b3 = Bolacha()

    assert_equals(b1.headers, {'foo': 'foo foo'})
    assert_equals(b2.headers, {'bar': 'bar bar'})
    assert_equals(b3.headers, {})

def test_request_calls_http_request():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    response_headers = {}
    response_body = "should be my html content"

    http_mock.request('http://somewhere.com', 'GET', '', {}). \
        AndReturn((response_headers, response_body))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    assert_equals(b.request('http://somewhere.com', 'GET'), (response_headers,
                                                             response_body))
    mocker.VerifyAll()

def test_request_fails_with_headers_non_dict():
    b = Bolacha()
    assert_raises(TypeError, b.request, 'http://somewhere', 'GET', headers=5,
                  exc_pattern=r'Bolacha.request, parameter headers must be ' \
                  'a dict or NoneType. Got 5')
    assert_raises(TypeError, b.request, 'http://somewhere', 'GET', headers='bla',
                  exc_pattern=r'Bolacha.request, parameter headers must be ' \
                  'a dict or NoneType. Got \'bla\'')

def test_request_fails_url_non_string():
    b = Bolacha()
    assert_raises(TypeError, b.request, None, None,
                  exc_pattern=r'Bolacha.request, parameter url must be ' \
                  'a string. Got None')
    assert_raises(TypeError, b.request, 99, None,
                  exc_pattern=r'Bolacha.request, parameter url must be ' \
                  'a string. Got 99')

def test_request_fails_method_non_string():
    b = Bolacha()
    assert_raises(TypeError, b.request, 'http://gnu', None,
                  exc_pattern=r'Bolacha.request, parameter method must be ' \
                  'a string. Got None')
    assert_raises(TypeError, b.request, 'http://gnu', 99,
                  exc_pattern=r'Bolacha.request, parameter method must be ' \
                  'a string. Got 99')

def test_request_fails_inexistent_method():
    b = Bolacha()
    assert_raises(TypeError, b.request, 'http://gnu', 'FOOBAR',
                  exc_pattern=r'Bolacha.request, parameter method must be ' \
                  'a valid HTTP method. Got FOOBAR. ' \
                  'Take a look at http://www.w3.org/Protocols/rfc2616/' \
                  'rfc2616-sec9.html to see valid method definitions')
    assert_raises(TypeError, b.request, 'http://gnu', 'GOOSFRABA',
                  exc_pattern=r'Bolacha.request, parameter method must be ' \
                  'a valid HTTP method. Got GOOSFRABA. ' \
                  'Take a look at http://www.w3.org/Protocols/rfc2616/' \
                  'rfc2616-sec9.html to see valid method definitions')

def test_request_with_body_dict():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    response_headers = {'header1': 'value of header'}
    response_body = {'param1': 'value1', 'foo': 'bar'}

    http_mock.request('http://somewhere.com', 'GET',
                      'foo=bar&param1=value1',
                      response_headers). \
        AndReturn((response_headers, response_body))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    got = b.request('http://somewhere.com', 'GET',
                    response_body,
                    response_headers)
    assert_equals(got, (response_headers,
                        response_body))
    mocker.VerifyAll()

def test_request_with_invalid_body():
    b = Bolacha()
    assert_raises(TypeError, b.request, 'http://gnu', 'GET',
                  body=['a list'],
                  exc_pattern=r'Bolacha.request, parameter body must be ' \
                  'a string or dict. Got .\'a list\'.')
    assert_raises(TypeError, b.request, 'http://gnu', 'GET',
                  body=5,
                  exc_pattern=r'Bolacha.request, parameter body must be ' \
                  'a string or dict. Got 5')

def test_request_keep_sending_last_headers():
    mocker = Mox()

    http_mock = mocker.CreateMockAnything()

    response_headers1 = {'normal': 5}
    response_headers2 = {'good': 10}
    response_headers3 = {'awesome': 20}

    request_headers1 = {}
    request_headers2 = {'normal': 5}
    request_headers3 = {'normal': 5, 'good': 10}
    request_headers4 = {'normal': 5, 'good': 10, 'awesome': 20}

    # 1st request
    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers1). \
        AndReturn((response_headers1, ''))

    # 2nd request
    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers2). \
        AndReturn((response_headers2, ''))

    # 3rd request
    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers3). \
        AndReturn((response_headers3, ''))

    # 4th request
    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers4). \
        AndReturn(({}, ''))

    mocker.ReplayAll()
    bol = Bolacha()
    bol.http = http_mock
    for x in range(4):
        bol.request('http://somewhere.com', 'GET')

    mocker.VerifyAll()

def test_request_handle_cookies():
    mocker = Mox()

    http_mock = mocker.CreateMockAnything()
    request_headers1 = {}
    response_headers1 = {'set-cookie': 'Will log in'}

    request_headers2 = {'Cookie': 'Will log in'}
    response_headers2 = {'set-cookie': 'Already logged as root'}

    request_headers3 = {'Cookie': 'Already logged as root'}
    response_headers3 = {'set-cookie': 'Just logged out'}

    request_headers4 = {'Cookie': 'Just logged out'}
    response_headers4 = {'set-cookie': 'Will log in'}

    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers1). \
        AndReturn((response_headers1, ''))

    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers2). \
        AndReturn((response_headers2, ''))

    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers3). \
        AndReturn((response_headers3, ''))

    http_mock.request('http://somewhere.com', 'GET',
                      '', request_headers4). \
        AndReturn((response_headers4, ''))

    mocker.ReplayAll()
    bol = Bolacha()
    bol.http = http_mock
    for x in range(4):
        bol.request('http://somewhere.com', 'GET')

    mocker.VerifyAll()
