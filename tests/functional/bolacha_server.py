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
import socket
import cherrypy

class TestController:
    @cherrypy.expose
    def index(self, username=None, password=None):
        if username == 'foo' and password == 'bar':
            cherrypy.session['is_authenticated'] = True

        if cherrypy.session.get('is_authenticated'):
            return 'Welcome to the website!'

        cherrypy.response.status = 403 # forbidden
        return 'You are not authenticated!'

    @cherrypy.expose
    def logout(self):
        if cherrypy.session.get('is_authenticated'):
            cherrypy.session['is_authenticated'] = False
            return 'Logged out successfully!'

        return 'You are not logged in!'

def port_is_free(server, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        connection.bind((server, port))
        connection.close()
        del connection
        return True
    except socket.error, e:
        if e.args[0] is 98:
            return False
        else:
            raise e

if __name__ == '__main__':
    if not port_is_free('localhost', 5050):
        print 'The port 5050 in localhost is not free, Bolacha ' \
        'functional tests can not proceed'
        raise SystemExit(1)

    cherrypy.config['server.socket_port'] = 5050
    c = {
        '/': {
            'tools.sessions.on': True,
        }
    }
    cherrypy.quickstart(TestController(), '/', config=c)

