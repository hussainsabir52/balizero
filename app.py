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
        time = formone.time.data 
        purpose = formone.purpose.data
        if time == "Less than 30 days":
            if purpose == "Tourism":
                messages = "SINCE MARCH 2020 COMING FOR TOURISM PORPOSE IS POSSIBEL ONLY WITH A B211A ENTRY VISA"
                url = "APPLY FOR SINGLE ENTRY VISA"
            elif purpose == "Business/Other":
                messages = "YOU CAN APPLY WITH US. WE WILL BE YOUR SPONSOR TO APPLY FOR A B211A ENTRY VISA"
                url = "APPLY FOR SINGLE ENTRY VISA"
            else:
                messages = "NO SERVICES WAS FOUND"    
                url = "GET HELP"

        elif time == "More than 1 month and less than 6 month":
            if purpose == "Staycation/Business/Work Remotely":
                messages = "YOU CAN APPLY WITH US AND STAY IN INDONESIA UP TO 180 DAYS WE WILL BE YOUR SPONSOR TO APPLY FOR A B211A ENTRY VISA"
                url = "APPLY FOR SINGLE ENTRY VISA"
            elif purpose == "Work":
                messages = "TO WORK AND GENERATE INCOME IN INDONESIA YOU MUST HAVE A WORKING PERMIT AND BE HIRED BY AN INDONESIAN COMPANY (WORKING VISA) OR WORK INDIPENENTLY AS A FREELANCE (FREELANCE VISA)"
                url = "WANT TO KNOW MORE ABOUT WORKING VISA"
            elif purpose == "Investment":
                messages = "IF YOU WANT TO START YOUR BUSINESS IN INDONESIAYOU CAN OPEN YOUR OWN FOREIGN COMPANY (PT PMA) AND APPLY FOR AN INVESTOR VISA"
                url = "APPLY FOR INVESTOR KITAS"    
            else:
                messages = "NO SERVICES WAS FOUND"    
                url = "GET HELP"

        elif time == "Long term more than 6 month":
            if purpose == "I'm Retired":
                messages = "IF YOU HAVE MORE THAN 55 YEARS OLD YOU CAN APPLY FOR A LONG TERM STAY PERMIT"
                url = "APPLY FOR RETIREMENT VISA"

            elif purpose == "I'm Married With Indonesian Citizen":
                messages = "IF YOU MERRIED AND INDONESIAN CITIZEN YOU CANAPPLY FOR A LONG TERM STAY PERMIT"
                url = "APPLY FOR MARRIAGE VISA"

            elif purpose == "Investment":
                messages = "IF YOU WANT TO START YOUR BUSINESS IN INDONESIAYOU CAN OPEN YOUR OWN FOREIGN COMPANY (PT PMA) AND APPLY FOR AN INVESTOR VISA"
                url = "APPLY FOR INVESTOR KITAS"    

            elif purpose == "Staycation/Business/Work Remotely":
                messages = "YOU CAN APPLY WITH US AND STAY IN INDONESIA UP TO 180 DAYS WE WILL BE YOUR SPONSOR TO APPLY FOR A B211A ENTRY VISA"
                url = "APPLY FOR SINGLE ENTRY VISA"
            elif purpose == "Work":
                messages = "TO WORK AND GENERATE INCOME IN INDONESIA YOU MUST HAVE A WORKING PERMIT AND BE HIRED BY AN INDONESIAN COMPANY (WORKING VISA) OR WORK INDIPENENTLY AS A FREELANCE (FREELANCE VISA)"
                url = "WANT TO KNOW MORE ABOUT WORKING VISA"
            elif purpose == "Investment":
                messages = "IF YOU WANT TO START YOUR BUSINESS IN INDONESIAYOU CAN OPEN YOUR OWN FOREIGN COMPANY (PT PMA) AND APPLY FOR AN INVESTOR VISA"
                url = "APPLY FOR INVESTOR KITAS"        

            else:
                messages = "NO SERVICES WAS FOUND"    
                url = "GET HELP"        
                    
        return redirect(url_for("Result",messages=messages,url=url)) 
    return render_template("index.html",formone=formone,formtwo=formtwo)    



@app.route("/two",methods=["GET","POST"])
def Index2():
    formone = FormOne()
    formtwo = FormTwo()
    if formtwo.validate_on_submit():
        messages = "YOU EGLIBED TO APPLY"    
        url = "APPLY NOW"    
        return redirect(url_for("Result",messages=messages,url=url))   
                    
    return render_template("bali.html",formone=formone,formtwo=formtwo)   



@app.route("/result/<messages>/<url>",methods=["GET","POST"])
def Result(messages,url):
    formone = FormOne()
    formtwo = FormTwo() 
    return render_template("result.html",formone=formone,formtwo=formtwo,messages=messages,url=url)   



@app.route("/services/<name>",methods=["GET","POST"])
def Services(name):
    if name == "investor-kitas" :
        return render_template("investor.html") 
    elif name == "retirment-kitas"  :  
        return render_template("retirment.html") 
    elif name == "spouse-kitas"  :  
        return render_template("spouse.html")     
    elif name == "working-kitas"  :  
        return render_template("working.html")     
    elif name == "freelance-kitas"  :  
        return render_template("freelance.html")
    elif name == "social-visa-onshore":
        return render_template("social.html")
    elif name == "business-visa-onshore":
        return render_template("business.html")
    elif name == "set-up-pt-pma":
        return render_template("pma.html")    
                         
                     
    
















if __name__ == "__main__":
	#manager.run()
	app.jinja_env.cache = {}
	app.run(host='0.0.0.0',threaded=True)	






