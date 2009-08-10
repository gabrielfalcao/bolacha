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

from bolacha import Bolacha, BOUNDARY
from httplib2 import Http

base_header = {'Content-type': 'application/x-www-form-urlencoded'}
def prepare_header(h):
    z = h.copy()
    z.update(base_header)
    return z

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
                      prepare_header(response_headers)). \
        AndReturn((response_headers, response_body))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    got = b.request('http://somewhere.com', 'GET',
                    response_body,
                    prepare_header(response_headers))
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

def test_request_keep_sending_last_cookies():
    mocker = Mox()

    http_mock = mocker.CreateMockAnything()

    response_headers1 = {'set-cookie': 5}
    response_headers2 = {'good': 10}
    response_headers3 = {'set-cookie': 20}

    request_headers1 = {}
    request_headers2 = {'Cookie': 5}
    request_headers3 = {'Cookie': 5}
    request_headers4 = {'Cookie': 20}

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

def test_request_when_persistent():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    response_headers = {'connection': 'close'}

    http_mock.request('http://somewhere.com', 'GET', '', {}). \
        AndReturn((response_headers, ''))

    http_mock.request('http://somewhere.com', 'GET', '', {}).AndReturn(({}, ''))

    mocker.ReplayAll()

    b = Bolacha(klass_mock, persistent=True)
    b.request('http://somewhere.com', 'GET')
    b.request('http://somewhere.com', 'GET')
    mocker.VerifyAll()

def test_request_when_not_persistent():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    response_headers = {'connection': 'close', 'set-cookie': 'blabla'}
    request_headers = {'connection': 'close'}

    http_mock.request('http://somewhere.com', 'GET', '', {}). \
        AndReturn((response_headers, ''))

    http_mock.request('http://somewhere.com', 'GET', '', request_headers). \
        AndReturn((response_headers, ''))

    mocker.ReplayAll()

    b = Bolacha(klass_mock, persistent=False)
    b.request('http://somewhere.com', 'GET')
    b.request('http://somewhere.com', 'GET')
    mocker.VerifyAll()

def test_set_content_type_urlencoded_when_body_dict_and_none_was_given():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    request_headers = {'Content-type': 'application/x-www-form-urlencoded'}

    http_mock.request('http://somewhere.com', 'GET', '', request_headers). \
        AndReturn(({}, ''))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    b.request('http://somewhere.com', 'GET', body={})
    mocker.VerifyAll()

def test_when_body_dict_and_content_type_is_specified():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    request_headers = {'Content-type': 'text/plain'}

    http_mock.request('http://somewhere.com', 'GET', '', request_headers). \
        AndReturn(({}, ''))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    b.request('http://somewhere.com', 'GET', body={}, headers=request_headers)
    mocker.VerifyAll()

def test_post_shortcut():
    mocker = Mox()

    b = Bolacha()
    b.request = mocker.CreateMockAnything()

    b.request('host', 'POST', body={'name': 'foo', 'age': 30}, headers=None)
    mocker.ReplayAll()

    b.post('host', {'name': 'foo', 'age': 30})

    mocker.VerifyAll()

def test_get_shortcut():
    mocker = Mox()

    b = Bolacha()
    b.request = mocker.CreateMockAnything()

    b.request('host', 'GET', body={'name': 'foo', 'age': 30}, headers=None)
    mocker.ReplayAll()

    b.get('host', {'name': 'foo', 'age': 30})

    mocker.VerifyAll()

def test_put_shortcut():
    mocker = Mox()

    b = Bolacha()
    b.request = mocker.CreateMockAnything()

    b.request('host', 'PUT', body={'name': 'foo', 'age': 30}, headers=None)
    mocker.ReplayAll()

    b.put('host', {'name': 'foo', 'age': 30})

    mocker.VerifyAll()

def test_delete_shortcut():
    mocker = Mox()

    b = Bolacha()
    b.request = mocker.CreateMockAnything()

    b.request('host', 'DELETE', body={'name': 'foo', 'age': 30}, headers=None)
    mocker.ReplayAll()

    b.delete('host', {'name': 'foo', 'age': 30})

    mocker.VerifyAll()

def test_head_shortcut():
    mocker = Mox()

    b = Bolacha()
    b.request = mocker.CreateMockAnything()

    b.request('host', 'HEAD', body={'name': 'foo', 'age': 30}, headers=None)
    mocker.ReplayAll()

    b.head('host', {'name': 'foo', 'age': 30})

    mocker.VerifyAll()

def test_request_with_file_will_upload_multipart():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    http_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(http_mock)

    class FileStub(object):
        name = '/path/to/file'
        def read(self):
            return 'FileStubContent'

    request_headers = {}
    body = {
        'name': 'John Doe',
        'picture': FileStub(),
    }

    expected_body = '--%(boundary)s\r\nContent-Disposition: form-data; ' \
                    'name="picture"; filename="file"\r\nContent-Type: ' \
                    'application/octet-stream\r\n\r\nFileStubContent\r\n' \
                    '--%(boundary)s\r\nContent-Disposition: form-data; ' \
                    'name="name"\r\n\r\nJohn Doe\r\n' \
                    '--%(boundary)s--\r\n' % {'boundary': BOUNDARY}
    expected_header = {'content-length': '291',
                       'Content-type': 'multipart/form-data; ' \
                       'boundary=%s' % BOUNDARY}

    http_mock.request('http://somewhere.com', 'POST',
                      expected_body, expected_header). \
        AndReturn(({}, ''))

    mocker.ReplayAll()

    b = Bolacha(klass_mock)
    b.request('http://somewhere.com', 'POST', body=body, headers=request_headers)
    mocker.VerifyAll()

