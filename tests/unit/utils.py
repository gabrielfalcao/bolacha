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

import re
import sys

def assert_raises(exception, callable, *args, **kwargs):
    '''
    Discussion
       assert_raises() adds two optional arguments: "exc_args"
       and "exc_pattern". "exc_args" is a tuple that is expected
       to match the .args attribute of the raised exception.
       "exc_pattern" is a compiled regular expression that the
       stringified raised exception is expected to match.

    Original url: http://code.activestate.com/recipes/307970/
    Author: Trent Mick

    Usage: assert_raises(ExceptionType, method_to_execute,
                          arguments_to_method, kwargs_to_method,
                          exc_pattern=r'^.+$')
    Please note that exc_pattern is not required, but if passed
    matches the exception message.

    Fail Conditions
    Fails on exception not raised, wrong exception type or
    invalid exception message.
    '''

    if "exc_args" in kwargs:
        exc_args = kwargs["exc_args"]
        del kwargs["exc_args"]
    else:
        exc_args = None
    if "exc_pattern" in kwargs:
        exc_pattern = kwargs["exc_pattern"]
        if isinstance(exc_pattern, basestring):
            exc_pattern = re.compile(exc_pattern)

        del kwargs["exc_pattern"]
    else:
        exc_pattern = None

    argv = [repr(a) for a in args]\
           + ["%s=%r" % (k,v)  for k,v in kwargs.items()]
    callsig = "%s(%s)" % (callable.__name__, ", ".join(argv))

    try:
        callable(*args, **kwargs)
    except exception, exc:
        if exc_args is not None:
            assert exc.args != exc_args, \
                        "%s raised %s with unexpected args: "\
                        "expected=%r, actual=%r"\
                        % (callsig, exc.__class__, exc_args, exc.args)
        if exc_pattern is not None:
            assert exc_pattern.search(str(exc)), \
                            "%s raised %s, but the exception "\
                            "does not match '%s': %r"\
                            % (callsig, exc.__class__, exc_pattern.pattern,
                               str(exc))
    except Exception, e:
        exc_info = sys.exc_info()
        print exc_info
        assert False, "%s raised an unexpected exception type: "\
                  "expected=%s, actual=%s (%s)"\
                  % (callsig, exception, exc_info[0], unicode(e))
    else:
        assert False, "%s did not raise %s" % (callsig, exception)
