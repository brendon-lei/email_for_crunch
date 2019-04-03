from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib, ssl, email
import os

app = Flask(__name__)
app.debug = True

UPLOAD_FOLDER = '/Users/blei941/Documents/GitProjects/Testing' #change to fit where the code is located
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','.doc','.docx','.java','.py'])#add more if needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/') #starter page, would request subject/message body
def index():
    return render_template('email.html')

@app.route('/result', methods = ['POST', 'GET']) #will take the data and input it into the program
def result():
    if request.method == 'POST':
        result = request.form
        receiver_email = ["crunchtest@kwesi.info"] #gotta fill this up with the list of emails from the database
        # db.email_list.queryAll();

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        subject = result['subject']
        email = result['email']#message of the email

        for x in receiver_email: #allows to send emails to the array/list of emails
            sender_email = "crunch+test@kwesi.info"#this is our tester email for now
            
            message = MIMEMultipart()
            text = """%s""" %(email)
            message.attach(MIMEText(text,'plain'))

            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)
            message.attach(part)

            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = x

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, 'crunch123')#'crunch123' is the password for our email, change it if you change sender email
                server.sendmail(sender_email, receiver_email, message.as_string())
        os.remove(file.filename) 
        return render_template('result.html')


if __name__ == '__main__':
    app.run()
