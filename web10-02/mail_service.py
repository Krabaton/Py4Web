import smtplib
#
port = 1025  # For SSL


def send_email(sender, receiver, message):
    with smtplib.SMTP("localhost", port) as server:

        server.sendmail(sender, receiver, message)


send_email('test@test.com', 'test@api.com', 'Hello world')