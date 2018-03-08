import tornado.web
import tornado.httpserver
from tornado.log import enable_pretty_logging
import logging
import os.path

import dbhandler

# This is a demo dict that has a session cookie : user_name.
sessions = {
    "sampleSession": "sam-drew"
}

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class DirectoryHandler(tornado.web.RequestHandler):
    def get(self, url):
        req_user_name = url.split("/")[-1]
        info = dbhandler.getSocials(req_user_name)
        print(info)
        if info == False:
            self.render("no-account.html")
        else:
            socials = []
            for social in info:
                url = social['url']
                user_name = social['url'].split("/")[-1]
                name = social['social_name']
                socials.append([name, url, user_name])
            user_name = info[0]['user_name']
            self.render("directory.html", user_name = user_name, socials = socials)

class EditDirectoryHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie("session_id"):
            self.set_secure_cookie("session_id", "sampleSession")
            self.redirect("/me/edit")
        else:
            user_name = sessions[self.get_secure_cookie("session_id").decode("utf-8")]
            if user_name != None:
                info = dbhandler.getSocials(user_name)
                socials = []
                for social in info:
                    url = social['url']
                    user_name = social['url'].split("/")[-1]
                    name = social['social_name']
                    social_id = social['ID']
                    socials.append([name, url, user_name, social_id])
                self.render("edit.html", user_name = user_name, socials = socials)
    def post(self):
        action = self.get_argument("action")
        if action == "delete":
            social_id = self.get_argument("social_id")
            session_id = self.get_secure_cookie("session_id").decode("utf-8")
            social_ids_from_sess_id = dbhandler.getSocialIDsFromSessionID(session_id)
            for s_id in social_ids_from_sess_id:
                if s_id['ID'] == social_id:
                    # Delete the social link from the directory.
                    dbhandler.deleteSocial(social_id)
            self.redirect("/me/edit")

enable_pretty_logging()
app = tornado.web.Application(
    [(r"/", RootHandler), (r"/me/edit", EditDirectoryHandler), (r"/(.*)", DirectoryHandler),],
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
