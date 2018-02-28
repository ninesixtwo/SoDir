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
