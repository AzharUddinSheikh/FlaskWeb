import os 
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail

# we just saved our picture to our path here (why random_hex if user enter same image name it ll cause problem)
# _ means not using it 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    path = 'C:/Users/azhar/Desktop/Flask-Rest and Api/Flask-api-2/flaskblog'
    picture_path = os.path.join(path,'static/img',picture_fn)

#  to resize our images to save in static so that our web page work faster with saving tons of space
    # output_size = (125,125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    form_picture.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    
    msg  = Message('Password Reset Request', sender='noreply@gmail.com',recipients=["user.email"])
    
    msg.body  = f'''To reset your password visit the following link:
{url_for('users.reset_password',token=token, _external=True)}
if you didnot make this request then simply ignore this email and no changes has been done'''
    mail.send(msg)
