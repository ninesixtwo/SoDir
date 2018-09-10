# SoDir Documentation.  

## How we use Tornado (a brief intro).

This is a very brief introduction into Tornado and how we use it, with the intention of making the code a little easier to understand if you've never used Tornado before. If you need more detail, or more examples, there's a wealth of docs on the [Tornado website](http://tornadoweb.org).  

*All examples shown within this document are drawn from SoDir code, but are simplified, and do not represent how the program works in real life.*

Because of the way that Tornado works, for each page within the site a handler class defines how SoDir should repspond to a given action. For example, when a request is made to the root URL, the RootHandler defines how SoDir will respond to that request.

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

Templates define how each webpage should look. From the Tornado website:
>A Tornado template is just HTML (or any other text-based format) with Python control sequences and expressions embedded within the markup.  

A very basic example of this is shown in the head of the *directory.html* template:  

```html
<head>
    <title>SoDir | {{ user_name }}</title>
</head>
```

When this template is rendered, the *user_name* of the user whose directory you are viewing is inserted dynamically into the page title. This can be rendered using a handler like this:  

```python
Class DirectoryHandler(tornado.web.RequestHandler):
    def get(self):
        usrnm = getUserName()
        self.render("directory.html", user_name = usrnm)
```

Where 'getUserName()' is a function that finds the string name of the user whose page you are viewing.  

The templating language is also used to insert fragments that are repeated on many pages across the site and it's templates, for example: the footer. The footer is on every page on the site, and is the exact same on all of these pages. Hence, it can be defined as a fragment in its own file and then inserted with a one line tag at the bottom of every template, like so:  


```html
<div id="footer">
    <p><a href="/">About</a> | <a href="/sodir/privacy">Privacy Policy</a> | <a href="/sodir/terms">Terms and Conditions</a></p>
    <p>Made with &lt;3 by <a href="http://labs.ninesixtwo.xyz">NINESIXTWO</a> in the UK.</p>
</div>
```

```html
<body>
    <div id="content">
        <div id="navbar">
            <a class="title" href="/">SoDir</a>
            <a id="login_link" href="/sodir/login">Login/Signup</a>
        </div>
        <div id="socials">
            SoDir allows you to easily create a sharable directory of your social media accounts.
        </div>
        {% include footer.html %}
    </div>
</body>
```

This ensures that if any changes are made to the footer, they are instantly made site wide.