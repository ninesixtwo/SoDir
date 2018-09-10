import tornado.web
import tornado.httpserver
from tornado.log import enable_pretty_logging

import logging
import os.path
import uuid
import threading
import time
import boto3
from botocore.exceptions import ClientError

import dbhandler
import sodir_utils

class DirectoryHandler(tornado.web.RequestHandler):
    def get(self, url):
        req_user_name = url.split("/")[-1]
        info = dbhandler.getSocials(req_user_name)
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
            self.redirect("/sodir/login")
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
        social_urls = {
            "Twitter": "https://twitter.com/",
            "Instagram": "https://instagram.com/",
            "Github": "https://github.com/"
        }
        # If the user is not logged in, redirect to homepage.
        if not self.get_secure_cookie("session_id"):
            self.redirect("/")
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
        elif action == "add_new":
            # First collect all information that is neccessary for action.
            social_name = self.get_argument("social_name_select")
            social_user_name = self.get_argument("user_name")
            session_id = self.get_secure_cookie("session_id").decode("utf-8")
            user_id = dbhandler.getUserIDFromSessionID(session_id)['ID']
            social_url = (social_urls[social_name] + social_user_name)
            # Execute using dbhandkler function.
            dbhandler.addNewSocial(user_id, social_url, social_name)
        self.redirect("/sodir/edit")

class LoginSignupHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login_signup.html", message = "")

    def post(self):
        supplied_user_name = self.get_argument("username")
        supplied_email = self.get_argument("email")
        # Check if account is associated with email supplied.
        # This implicitly checks if the email is in use, but does not confirm
        # that the supplied user name is not associated with another email.
        user_name = dbhandler.getUserName(supplied_email)
        if user_name == False:
            logging.info("Email not registered, signing user up.")
            # Email is not registered. Sign user up.
            # Check that the user_name is also not in use elsewhereself.
            if dbhandler.checkUserNameInUse(supplied_user_name) == False:
                # Trigger add user function, creates new database records.
                response = dbhandler.addNewUser(supplied_user_name, supplied_email)
                if response != True:
                    logging.error(response)
                # Now send an email allowing them to trigger the login process.
                login_key = str(uuid.uuid4())
                dbhandler.setLoginKey(supplied_user_name, login_key)
                # Send the email containing the login key.
                sodir_utils.loginEmailSender(supplied_email, login_key)
                # Start the login key timeout worker thread.
                t = threading.Thread(target = sodir_utils.loginKeyTimeout_worker, args=(supplied_user_name,))
                logging.info("Starting loginkey timeout worker.")
                t.start()
                self.redirect("/sodir/checkuremail")
            else:
                # Email is unique but user name is already in use. Feedback this
                # to user.
                self.render("login_signup.html", message = "Username already in use, please select a different one.")
        elif user_name['user_name'] != supplied_user_name:
            # Incorrect username / email combination.
            self.render("login_signup.html", message = "Incorrect username or email.")
        else:
            # User is registered, log them in.
            # Generate login key
            login_key = str(uuid.uuid4())
            dbhandler.setLoginKey(user_name['user_name'], login_key)
            # Send the email containing the login key.
            sodir_utils.loginEmailSender(supplied_email, login_key)
            # Start the login key timeout worker thread.
            t = threading.Thread(target = sodir_utils.loginKeyTimeout_worker, args=(user_name['user_name'],))
            logging.info("Starting loginkey timeout worker.")
            t.start()
            self.redirect("/sodir/checkuremail")

class LoginVerificationHandler(tornado.web.RequestHandler):
    def get(self, url):
        # TODO regex to check if valid login key.
        if len(url) != 36:
            self.redirect("/")
        else:
            # Check if login key is valid.
            user_name = dbhandler.getUserNameFromLoginKey(url)
            if user_name != None:
                user_name = user_name['user_name']
                # Generate session id.
                session_id = str(uuid.uuid4())
                # Save session id to database and as cookie to users browser.
                dbhandler.updateSessionID(user_name, session_id)
                self.set_secure_cookie("session_id", session_id)
                self.redirect("/sodir/edit")
            else:
                self.redirect("/sodir/login")

# Define what should be done when a user clicks the exit button.
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("_xsrf")
        self.clear_cookie("session_id")
        self.redirect("/")

# Static handlers.
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class CheckEmailHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("checkuremail.html")

class PrivacyPolicyHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("privacy_policy.html")

class TermsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("terms.html")

enable_pretty_logging()

app = tornado.web.Application(
    [(r"/", RootHandler), (r"/sodir/login", LoginSignupHandler), (r"/sodir/exit", LogoutHandler), (r"/sodir/checkuremail", CheckEmailHandler),
    (r"/sodir/edit", EditDirectoryHandler), (r"/sodir/privacy", PrivacyPolicyHandler), (r"/sodir/terms", TermsHandler),
    (r"/sodir/v/(.*)", LoginVerificationHandler), (r"/(.*)", DirectoryHandler),],
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
http_server.listen(8888)

# Start the asynchronous IO loop
tornado.ioloop.IOLoop.instance().start()
