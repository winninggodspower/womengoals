from flask import Flask, redirect, url_for, render_template, request, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from blog import blog
from blog import db, DbConfig

from blog.blog import BlogConfig

app = Flask(__name__)
mail = Mail(app)



#configuration of mail
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.environ.get("EMAIL_ID"),
    MAIL_PASSWORD = os.environ.get("EMAIL_PW"),
))
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
mail = Mail(app)


def send_volunteer_email(user_info):
    msg = Message(
        f"{user_info['username']} volluntered to womensgoal",
        sender = os.environ.get("EMAIL_ID"),
        recipients= [os.environ.get("EMAIL_ID"),]
    )

    msg.html = render_template("volunteer_email.html", user = user_info)
    mail.send(msg)
    return
    
def send_contact_email(user_info):
    msg = Message(
        f"{user_info['username']} contacted womensgoal",
        sender = user_info["email"],
        recipients= [os.environ.get("EMAIL_ID"),]
    )

    msg.html = render_template("contact_email.html", user = user_info)
    mail.send(msg)
    return


app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user_info = dict(
            username = request.form.get("username"),
            email = request.form.get("email"),
            message = request.form.get("message"),
        )
        
        send_contact_email(user_info)
        flash("Youv've successfully contacted womensgoal. We'll reply your message soon. ", "Success")
        return render_template('index.html')

    return render_template('index.html')

@app.route('/volunteer',methods=['GET','POST'])
def volunteer():
    if request.method == 'POST':
        user_info = dict(
            username = request.form.get("username"),
            phone = request.form.get("phone"),
            country = request.form.get("country"),
            state = request.form.get("state"),
            department = request.form.get("department"),
            note = request.form.get("note"),
        )
        print(user_info)
        
        send_volunteer_email(user_info)
        return render_template('thanks.html')

    return render_template('volluteer.html')

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


@app.route("/sponsor")
def sponsor():
    return render_template("sponsor.html")


DbConfig(app)
db.init_app(app)
BlogConfig(app)

#DEBUG is SET to TRUE. CHANGE FOR PROD
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get("SECRET_KEY")
print(app.config.get('SECRET_KEY'))
app.register_blueprint(blog)


if __name__ == '__main__':
    app.run(port=5000,debug=False)