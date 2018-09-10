def loginEmailSender(email, loginKey):
    logging.info("Attempting to send login email.")
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "SoDir Login <donotreply@ninesixtwo.xyz>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-1"

    # The subject line for the email.
    SUBJECT = "Login to SoDir"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("An attempt has been made to login to your SoDir account.\r\n\
                Please click here or copy the link below into the address bar of your web browser\n\
                http://sodir.xyz/sodir/v/{0}".format(loginKey))

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Login to SoDir</h1>
      <p>An attempt has been made to login to your SoDir account.</p>
      <p>Please click <a href="http://sodir.xyz/sodir/v/{0}">here</a> or copy the link below into the address bar of your web browser.</p>
      <p>http://sodir.xyz/sodir/v/{0}</p>
    </body>
    </html>
                """.format(loginKey)
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    # The boto3 client uses the file /.aws/credentials for authenticating.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logging.error((e.response['Error']['Message']))
    else:
        logging.info(("Email sent! Message ID:{}".format(response['MessageId'])))

def loginKeyTimeout_worker(user_name):
    time.sleep(1200)
    dbhandler.clearLoginKey(user_name)
    logging.info("Clearing a login key.")
