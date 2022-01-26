 # -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, flash,jsonify,Response, session
import json
from flask_sqlalchemy import SQLAlchemy 
from config import database, secret
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from dateutil.rrule import rrule, DAILY
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message 
from functools import wraps
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from form import FormOne,FormTwo
from sqlalchemy.sql import func
from sqlalchemy import extract
import random
from flask_compress import Compress
from werkzeug.utils import secure_filename
import os




app = Flask(__name__) 
COMPRESS_MIMETYPES = ["text/html", "text/css", "application/json"]
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app) 
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret 
db = SQLAlchemy(app)
app.debug = True 




migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


#fungsi Upload
#mengatur image
UPLOAD_FOLDER = 'static/images/'
images = UploadSet("images",IMAGES)
app.config["UPLOADED_IMAGES_DEST"] = "static/images/"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
configure_uploads(app,images)




#################################################### Decorator ##############################################################################



#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")





@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.errorhandler(500)
def internal_server(error):
    return 'Opps something bad happen,try again', 500



####################################################### Model #############################################
@app.route("/",methods=["GET","POST"])
def Index():
    formone = FormOne()
    formtwo = FormTwo()
    if formone.validate_on_submit():
        return redirect(url_for("Result",status="one"))
    return render_template("bali.html",formone=formone,formtwo=formtwo)

@app.route("/two",methods=["GET","POST"])
def Index2():
    formone = FormOne()
    formtwo = FormTwo()
    if formtwo.validate_on_submit():
        return redirect(url_for("Result",status="two"))
    return render_template("bali.html",formone=formone,formtwo=formtwo)    

@app.route("/result/<status>",methods=["GET","POST"])
def Result(status):
    formone = FormOne()
    formtwo = FormTwo()
    if status == "one":
        return render_template("result_one.html",formone=formone,formtwo=formtwo)
    else:
        return render_template("result_two.html",formone=formone,formtwo=formtwo)   



@app.route("/services/<name>",methods=["GET","POST"])
def Services(name):
    if name == "investor-kitas" :
        return render_template("services/investor.html") 
    elif name == "retirment-kitas"  :  
        return render_template("services/retirment.html") 
    elif name == "spouse-kitas"  :  
        return render_template("services/spouse.html")     
    elif name == "working-kitas"  :  
        return render_template("services/working.html")     
    elif name == "freelance-kitas"  :  
        return render_template("services/freelance.html")
    elif name == "social-visa-onshore":
        return render_template("services/social.html")
    elif name == "business-visa-onshore":
        return render_template("services/business.html")
    elif name == "set-up-pt-pma":
        return render_template("services/pma.html")    
                         
                     
    
















if __name__ == "__main__":
	#manager.run()
	app.jinja_env.cache = {}
	app.run(host='0.0.0.0',threaded=True)	






