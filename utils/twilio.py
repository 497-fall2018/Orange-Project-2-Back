from twilio.rest import Client

def send_notification(phone_num, name, status):

    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC001d428747f459acf98d736285ac1ba9'
    auth_token = 'd61a7a610d338e673f0333b556fc4f63'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+16317063866',
        body='Hello! Courts at ' + name + ' is now ' + status,
        to='+1' + phone_num
    )
