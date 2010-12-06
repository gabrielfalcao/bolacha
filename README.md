# Bolacha

Bolacha is a simple http client that allows you testing http requests,
handling cookies and file upload.

# Why "Bolacha" ?

"Bolacha" means "cookie" in Brazillian Portuguese.

Since one of the killer features of Bolacha is dealing with cookies
and session for you, I took very fair to name the project as "Bolacha".

# Installation

     pip install bolacha >= 0.6.0

# BASIC USAGE

Will authenticate, and make a upload:

    from bolacha import Bolacha

    b = Bolacha()

    login_data = {'username': 'admin', 'password': 'qwerty'}

    b.request('http://my-website.com/login', 'POST', body=login_data)

    data = {
        'title': 'Some pictures of my vacations at Rio de Janeiro',
        'year': '2009',
        'pictures': [
            open('/home/some_user/sugar-loaf.jpg'),
            open('/home/some_user/christ-redeemer.jpg'),
        ]
    }
    b.post('http://my-website.com/upload', body=data)

    headers, body = b.get('http://my-website.com/pictures/2009')

    assert 'vacations at Rio de Janeiro' in body
    assert 'text/html' in headers['Content-Type']
