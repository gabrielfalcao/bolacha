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
from os.path import dirname, abspath, join
from nose.tools import assert_equals
from bolacha import Bolacha

LOCAL_FILE = lambda *x: join(abspath(dirname(__file__)), *x)

def test_get():
    b = Bolacha()
    head, body = b.request('http://localhost:5050/', 'GET')
    assert_equals(body, 'You are not authenticated!')

def test_post_with_login():
    b = Bolacha()
    head, body = b.request('http://localhost:5050/', 'POST',
                           body={'username': 'foo',
                                 'password': 'bar'})

    assert_equals(body, 'Welcome to the website!')
    head, body = b.request('http://localhost:5050/', 'GET')
    assert_equals(body, 'Welcome to the website!')

def test_upload_after_login():
    b = Bolacha()

    head, body = b.request('http://localhost:5050/', 'GET')
    assert_equals(body, 'You are not authenticated!')

    b.request('http://localhost:5050/', 'POST',
              body={'username': 'foo',
                    'password': 'bar'})

    gpl2 = open(LOCAL_FILE('data', 'gpl-2.0.tex'))
    head, body = b.request('http://localhost:5050/upload', 'POST',
                           body={'file': gpl2})

    assert_equals(head['status'], '200')
    gpl2.seek(0)
    assert_equals(body, gpl2.read())
