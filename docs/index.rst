====================
Bolacha Documentation
====================


Bolacha is a simple http client that allows you testing http requests,
handling cookies and file upload.

Authenticating in a cookie-based website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bolacha handles cookies per instance, so you just need to instantiate
it once, and make successive requests::

     >>> from bolacha import Bolacha
     >>> b = Bolacha()
     >>> login_data = {'username': 'admin', 'password': 'qwerty'}
     >>> b.request('http://my-website.com/login', 'POST', body=login_data)
     ({'content-type': 'text/html; charset=UTF-8' ...},
      'successfully logged in')

Notice that a Bolacha.request returns a 2-item tuple: a dict with headers, and a string body.

Uploading a file
~~~~~~~~~~~~~~~~

Bolacha detects when you put a python file object within its body
dict, and automatically makes a multipart/form-data request::

     >>> from bolacha import Bolacha
     >>> b = Bolacha()
     >>> data = {'title': 'A picture of my vacations at Rio de Janeiro',
     ...         'year': '2009',
     ...         'picture': open('/home/some_user/vacations.jpg')}
     >>> b.request('http://my-website.com/upload', 'POST', body=data)

Shortcuts
~~~~~~~~~

Bolacha has methods providing shortcuts to GET, POST, PUT, DELETE and
HEAD::

     >>> from bolacha import Bolacha
     >>> b = Bolacha()
     >>>
     >>> b.post('http://my-website.com/login', {'name': 'User'})
     >>> b.get('http://my-website.com/list_by', {'topic': 'Medicine'})
     >>> b.put('http://my-website.com/add', {'person': 'Foo Bar'})
     >>> b.delete('http://my-website.com/person/1')
     >>> b.head('http://my-website.com/info/person/1')

Putting all together
~~~~~~~~~~~~~~~~~~~~

Logging in a website and making a upload::

     >>> from bolacha import Bolacha
     >>> b = Bolacha()
     >>>
     >>> b.post('http://my-website.com/login', {'username': 'foo', 'password': 'bar'})
     >>> b.post('http://my-website.com/upload', {'profile_pic': open('/home/user/me.jpg')})
