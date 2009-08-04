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

def test_bolacha_creation_takes_class():
    msg = r'Bolacha takes a class or callable as parameter, got %r'
    assert_raises(TypeError,
                  Bolacha, 5,
                  exc_pattern=msg % 5)
    assert_raises(TypeError,
                  Bolacha, 'blabla',
                  exc_pattern=msg % 'blabla')

def test_bolacha_instantiate_class_with_kwargs():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    klass_mock(cache_path='/some/path', other_param=10)

    mocker.ReplayAll()
    Bolacha(klass_mock, cache_path='/some/path', other_param=10)
    mocker.VerifyAll()

def test_bolacha_keeps_http_instance_after_instantiation():
    mocker = Mox()

    klass_mock = mocker.CreateMockAnything()
    instance_mock = mocker.CreateMockAnything()
    klass_mock().AndReturn(instance_mock)

    mocker.ReplayAll()
    b = Bolacha(klass_mock)
    assert_equals(b.http, instance_mock)
    mocker.VerifyAll()

def test_bolacha_uses_httplib2_Http_as_default_http_class():
    b = Bolacha()
    assert isinstance(b.http, Http), 'Bolacha().http should be instance of ' \
           'httplib2.Http, got %s' % repr(b.http)

def test_bolacha_is_persistent_by_default():
    b = Bolacha()
    assert b.persistent is True, 'Bolacha should be persistent by default'

def test_bolacha_can_be_not_persistent():
    b = Bolacha(persistent=False)
    assert b.persistent is False, 'Bolacha should be persistent by default'

def test_bolacha_is_persistent_by_default():
    b = Bolacha()
    assert b.persistent
