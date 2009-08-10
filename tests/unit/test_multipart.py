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
from mox import Mox
from nose.tools import assert_equals
from utils import assert_raises
from bolacha import multipart

def test_to_str_with_nonstring():
    got = multipart.to_str(5)
    assert_equals(got, u'5')

def test_to_str_with_latin_unicode():
    wee = u'áéíóção@#'.decode('latin')
    got = multipart.to_str(wee)
    assert_equals(got, '\xc3\x83\xc2\xa1\xc3\x83\xc2\xa9\xc3\x83\xc2\xad\xc3' \
                  '\x83\xc2\xb3\xc3\x83\xc2\xa7\xc3\x83\xc2\xa3o@#')


def test_guess_mime_guessed():
    mocker = Mox()

    old_guess_type = multipart.guess_type
    multipart.guess_type = mocker.CreateMockAnything()
    multipart.guess_type('should-be-a-path').AndReturn(('some-mimetype', None))

    mocker.ReplayAll()
    try:
        assert_equals(multipart.guess_mime('should-be-a-path'), 'some-mimetype')
        mocker.VerifyAll()
    finally:
        multipart.guess_type = old_guess_type

def test_guess_mime_fallsback_to_octet_stream():
    mocker = Mox()

    old_guess_type = multipart.guess_type
    multipart.guess_type = mocker.CreateMockAnything()
    multipart.guess_type('should-be-a-path').AndReturn((None, None))

    mocker.ReplayAll()
    try:
        assert_equals(multipart.guess_mime('should-be-a-path'),
                      'application/octet-stream')
        mocker.VerifyAll()
    finally:
        multipart.guess_type = old_guess_type

def test_encode_file():
    mocker = Mox()

    expected_list = ['--my-boundary',
                     'Content-Disposition: form-data; name="my_file"; ' \
                                                     'filename="file.pdf"',
                     'Content-Type: application/octet-stream',
                     '',
                     'Gabriel Falc\xc3\x83\xc2\xa3o']

    old_guess_type = multipart.guess_type
    multipart.guess_type = mocker.CreateMockAnything()
    multipart.guess_type('/path/to/file.pdf').AndReturn((None, None))
    file_mock = mocker.CreateMockAnything()
    file_mock.name = '/path/to/file.pdf'
    file_mock.read().AndReturn(u'Gabriel Falcão'.decode('latin1'))

    mocker.ReplayAll()
    try:
        got = multipart.encode_file('my-boundary', 'my_file', file_mock)
        assert_equals(got, expected_list)
        mocker.VerifyAll()
    finally:
        multipart.guess_type = old_guess_type

def test_encode_multipart_single_data():
    my_data = {
        'name': u'Gabriel Falcão',
    }
    got = multipart.encode_multipart('some-boundary', my_data)
    assert_equals(got, '--some-boundary\r\nContent-Disposition: ' \
                       'form-data; name="name"\r\n\r\nGabriel Falc\xc3\xa3o\r\n' \
                       '--some-boundary--\r\n')

def test_encode_multipart_without_files():
    my_data = {
        'foo': u'bar',
        'age': 21
    }
    got = multipart.encode_multipart('wee', my_data)
    assert_equals(got, '--wee\r\nContent-Disposition: form-data; ' \
                       'name="age"\r\n\r\n21\r\n--wee\r\nContent-Disposition: ' \
                       'form-data; name="foo"\r\n\r\nbar\r\n--wee--\r\n')

def test_encode_multipart_without_files():
    mocker = Mox()
    file_path = '/path/to/file.pdf'

    old_guess_type = multipart.guess_type
    multipart.guess_type = mocker.CreateMockAnything()
    multipart.guess_type(file_path).AndReturn(('some-mimetype', None))

    file_mock = mocker.CreateMockAnything()
    file_mock.name = file_path
    file_mock.read().AndReturn('MY_FILE_CONTENT')

    mocker.ReplayAll()
    try:
        my_data = {
            'foo': u'bar',
            'age': 21,
            'my_file': file_mock,
        }
        got = multipart.encode_multipart('fakeboundary', my_data)
        assert_equals(got, '--fakeboundary\r\nContent-Disposition: form-data; ' \
                           'name="age"\r\n\r\n21\r\n--fakeboundary\r\nContent-' \
                           'Disposition: form-data; name="foo"\r\n\r\nbar\r\n-' \
                           '-fakeboundary\r\nContent-Disposition: form-data; ' \
                           'name="my_file"; filename="file.pdf"\r\nContent-Type: ' \
                           'some-mimetype\r\n\r\nMY_FILE_CONTENT\r\n--' \
                           'fakeboundary--\r\n')
        mocker.VerifyAll()
    finally:
        multipart.guess_type = old_guess_type

def test_is_file_true():
    class FakeFile(object):
        def read(self):
            pass

    assert multipart.is_file(FakeFile())

def test_is_file_no_attr_read():
    class FakeFile(object):
        pass

    assert not multipart.is_file(FakeFile())

def test_is_file_attr_read_not_callable():
    class FakeFile(object):
        read = 'not a callable'

    assert not multipart.is_file(FakeFile())
