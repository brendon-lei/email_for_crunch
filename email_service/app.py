from flask import Flask, render_template, request #gotta download the request package "pip install requests"
from email.mime.text import MIMEText
import smtplib, ssl

app = Flask(__name__)
app.debug = True

@app.route('/') #starter page, would request subject/message body
def index():
    return render_template('email.html')

@app.route('/result', methods = ['POST', 'GET']) #will take the data and input it into the program
def result():
    if request.method == 'POST':
        result = request.form
        receiver_email = ["crunch@kwesi.info"] #gotta fill this up with the list of emails from the database
        #gotta add a for loop to add emails


        subject = result['subject']
        email = result['email']#message of the email

        for x in receiver_email: #allows to send emails to the array/list of emails
            sender_email = "crunch+test@kwesi.info"#this is our tester email for now

            text = """%s""" %(email)

            message = MIMEText(text)
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = x

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, 'crunch123')#'crunch123' is the password for our email, change it if you change sender email
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )

        return render_template('result.html')


if __name__ == '__main__':
    app.run()
