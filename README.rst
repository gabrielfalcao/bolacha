Bolacha
~~~~~~~

Bolacha is a simple http client that allows you testing http requests,
handling cookies and file upload.

Why "Bolacha" ?
~~~~~~~~~~~~~~~

"Bolacha" means "cookie" in Brazillian Portuguese.

Since one of the killer features of Bolacha is dealing with cookies
and session for you, I took very fair to name the project as "Bolacha".

BASIC USAGE
~~~~~~~~~~~

Will authenticate, and make an upload::

     >>> from bolacha import Bolacha
     >>> b = Bolacha()
     >>> login_data = {'username': 'admin', 'password': 'qwerty'}
     >>> b.request('http://my-website.com/login', 'POST', body=login_data)
     >>>
     >>> data = {'title': 'A picture of my vacations at Rio de Janeiro',
     ...         'year': '2009',
     ...         'picture': open('/home/some_user/vacations.jpg')}
     >>> b.request('http://my-website.com/upload', 'POST', body=data)

