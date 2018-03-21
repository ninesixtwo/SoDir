import tornado.web
import tornado.httpserver
from tornado.log import enable_pretty_logging
import logging
import os.path

import dbhandler

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
            user_name = dbhandler.getUserNameFromSessionID(self.get_secure_cookie("session_id").decode("utf-8"))['user_name']
            if user_name != None:
                info = dbhandler.getSocials(user_name)
                socials = []
                if info != False:
                    for social in info:
                        url = social['url']
                        user_name = social['url'].split("/")[-1]
                        name = social['social_name']
                        social_id = social['ID']
                        socials.append([name, url, user_name, social_id])
                self.render("edit.html", user_name = user_name, socials = socials)
    def post(self):
        # Edit form submits hidden values. Action tells wether deleting or adding.
        action = self.get_argument("action")
        if action == "delete":
            # Hidden value social_id submits the id of the social to be deleted.
            social_id = int(self.get_argument("social_id"))
            # session_id is a cookie set when the user logs in, can be used to
            # determine which user is logged in.
            session_id = self.get_secure_cookie("session_id").decode("utf-8")
            social_ids_from_sess_id = dbhandler.getSocialIDsFromSessionID(session_id)
            if social_ids_from_sess_id != False:
                for s_id in social_ids_from_sess_id:
                    if s_id['ID'] == social_id:
                        # Delete the social link from the directory.
                        dbhandler.deleteSocial(social_id)
            self.redirect("/me/edit")
        if action == "add_new":
            social_name = self.get_argument("social_name_select")
            user_name = self.get_argument("user_name")
            user_id = dbhandler.getUserID(user_name)


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
