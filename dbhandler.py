import pymysql
import yaml

# Function to make connection to the database. Reads the parameters out of a
# configuration file. Returns the connection object for use by other functions.
def makeConnection():
    with open("dbconfig.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
            connection = pymysql.connect(host = config['MySQL']['hostname'],
                                        user = config['MySQL']['user'],
                                        password = config['MySQL']['password'],
                                        db = config['MySQL']['database'],
                                        charset = "utf8mb4",
                                        cursorclass = pymysql.cursors.DictCursor)
            return(connection)
        except Exception as e:
            return("Error: {0}".format(e))

# getSocials returns all socials for a given user name.
def getSocials(user_name):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM socials INNER JOIN users ON socials.user_id = users.ID WHERE users.user_name = '{}'")
            sql_f = sql.format(user_name)
            cursor.execute(sql_f)
            result = cursor.fetchall()
            if len(result) == 0:
                return(False)
            else:
                return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getSocialIDsFromSessionID(session_id):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT socials.ID FROM socials INNER JOIN users ON socials.user_id = users.ID WHERE users.session_id = '{}'")
            sql_f = sql.format(session_id)
            cursor.execute(sql_f)
            result = cursor.fetchall()
            if len(result) == 0:
                return(False)
            else:
                return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def deleteSocial(social_id):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("DELETE FROM socials WHERE ID = '{}'")
            sql_f = sql.format(social_id)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def addNewSocial(user_id, url, social_name):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO socials (user_id, social_name, url) VALUES ('{0}', '{1}', '{2}')")
            sql_f = sql.format(user_id, social_name, url)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getUserID(user_name):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT ID FROM users WHERE user_name = '{0}'")
            sql_f = sql.format(user_name)
            cursor.execute(sql_f)
            result = cursor.fetchone()
            return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getUserNameFromSessionID(session_id):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT user_name FROM users WHERE session_id = '{0}'")
            sql_f = sql.format(session_id)
            cursor.execute(sql_f)
            result = cursor.fetchone()
            return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getUserIDFromSessionID(session_id):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT ID FROM users WHERE session_id = '{0}'")
            sql_f = sql.format(session_id)
            cursor.execute(sql_f)
            result = cursor.fetchone()
            return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def updateSessionID(user_name, session_id):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("UPDATE users SET session_id = '{0}' WHERE user_name = '{1}'")
            sql_f = sql.format(session_id, user_name)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getUserName(email):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT user_name FROM users WHERE email = '{0}'")
            sql_f = sql.format(email)
            cursor.execute(sql_f)
            result = cursor.fetchone()
            if result ==  None:
                return(False)
            else:
                return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def setLoginKey(user_name, login_key):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("UPDATE users SET login_key = '{0}' WHERE user_name = '{1}'")
            sql_f = sql.format(login_key, user_name)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def clearLoginKey(user_name):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("UPDATE users SET login_key = NULL WHERE user_name = '{0}'")
            sql_f = sql.format(user_name)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def getUserNameFromLoginKey(login_key):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT user_name FROM users WHERE login_key = '{0}'")
            sql_f = sql.format(login_key)
            cursor.execute(sql_f)
            result = cursor.fetchone()
            return(result)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def addNewUser(user_name, user_email):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO users (email, user_name) VALUES ('{0}', '{1}')")
            sql_f = sql.format(user_email, user_name)
            cursor.execute(sql_f)
            connection.commit()
            return(True)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()

def checkUserNameInUse(user_name):
    connection = makeConnection()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM users WHERE user_name = '{0}'")
            sql_f = sql.format(user_name)
            cursor.execute(sql_f)
            result = cursor.fetchall()
            if len(result) > 0:
                return(True)
            else:
                return(False)
    except Exception as e:
        return("Error: {0}. Error code is {1}".format(e, e.args[0]))
    finally:
        connection.close()
