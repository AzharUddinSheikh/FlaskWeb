import os

class Config:
     SECRET_KEY  = '642c24502769cd43fb7953e17b1e173f'
     SQLALCHEMY_DATABASE_URI  = 'sqlite:///site.db'
     MAIL_SERVER  = 'smtp.googlemail.com'
     MAIL_PORT  = 465
     MAIL_USE_TLS  = False
     MAIL_USE_SSL  = True
     MAIL_USERNAME  = 'noreply@gmail.com'
     MAIL_PASSWORD  = 'password'