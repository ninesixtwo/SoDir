# SoDir Documentation.  

## server.py

server.py is the main body of code that provides I/O and serves content when a request is made. It relies heavily upon the Tornado library for many of these actions.  

Because of the way that Tornado works, generally speaking for each piece of functionality that the website has, a handler class defines how SoDir should repspond to a given action. For example, when a request is made to the root URL, the RootHandler defines how SoDir will respond to that request.

```python
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
```

As we can see, this handler clearly defines that when a GET request is made, the server should render the template "index.html".  

Defining which handler responds to which URL is done when defining the server as a whole.

```python
app = tornado.web.Application(
   	[(r"/", RootHandler),],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "",
    xsrf_cookies = True,
)
```

This clearly defines that when a request is made to "/" (i.e. the root of the website), the response is defined by the RootHandler handler.