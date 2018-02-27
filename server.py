import tornado.web
import tornado.httpserver
from tornado.log import enable_pretty_logging
import logging
import os.path

import dbhandler

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        info = dbhandler.getSocials("sam-drew")
        socials = []
        for social in info:
            url = social['url']
            user_name = social['url'].split("/")[-1]
            name = social['social_name']
            socials.append([name, url, user_name])
        user_name = info[0]['user_name']
        self.render("index.html", user_name = user_name, socials = socials)

class DirectoryHandler(tornado.web.RequestHandler):
    def get(self, url):
        req_user_name = url.split("/")[-1]
        info = dbhandler.getSocials(req_user_name)
        print(info)
        socials = []
        for social in info:
            url = social['url']
            user_name = social['url'].split("/")[-1]
            name = social['social_name']
            socials.append([name, url, user_name])
        user_name = info[0]['user_name']
        self.render("index.html", user_name = user_name, socials = socials)

enable_pretty_logging()
app = tornado.web.Application(
    [(r"/", RootHandler), (r"/(.*)", DirectoryHandler),],
    # Set the path where tornado will find the html templates
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "secret",
    xsrf_cookies = True,
    autoreload = True,
)

# CODE TO MAKE MAKE SERVER SSL TRAFFIC

#ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#ssl_ctx.load_cert_chain(os.path.join("ssl", "cert.pem"),
                        #os.path.join("ssl", "key.pem"))
# http_server = tornado.httpserver.HTTPServer(app, ssl_options = ssl_ctx)

http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(8080)

# Start the asynchronous IO loop
tornado.ioloop.IOLoop.instance().start()
