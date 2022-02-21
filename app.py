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
from form import StepOneSocialForm,StepOneBusinessForm,StepTwoForm,StepThreeForm,StepFourForm,UploadForm




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
UPLOAD_FOLDER = 'static/document/'
ALLOWED_EXTENSIONS = {'jpeg','jpg','png','pdf'}
images = UploadSet("images",IMAGES)
app.config["UPLOADED_IMAGES_DEST"] = "static/document/"
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


####################################################### Model #############################################
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(200))   
    password = db.Column(db.String(500))        
    role = db.Column(db.String(100))    


class Booking(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(200))  
    services = db.Column(db.String(200))
    paymentmethod = db.Column(db.String(200))
    fullname = db.Column(db.String(200))
    gender =  db.Column(db.String(200))
    birthplace = db.Column(db.String(200))
    birthdate = db.Column(db.DateTime())
    martial =  db.Column(db.String(200))
    nationality =  db.Column(db.String(200))
    email =  db.Column(db.String(200))
    phone =  db.Column(db.String(200))
    original_address =  db.Column(db.Text())
    original_city = db.Column(db.String(200))
    original_state =  db.Column(db.String(200))
    original_zip =  db.Column(db.String(200))
    original_country =  db.Column(db.String(200))
    indo_address =  db.Column(db.Text())
    indo_city = db.Column(db.String(200))
    indo_state =  db.Column(db.String(200))
    indo_zip =  db.Column(db.String(200))
    emergency_name =  db.Column(db.String(200))
    emergency_status =  db.Column(db.String(200))
    emergency_address =  db.Column(db.Text())
    emergency_city = db.Column(db.String(200))
    emergency_state =  db.Column(db.String(200))
    emergency_zip =  db.Column(db.String(200))
    emergency_country =  db.Column(db.String(200))
    emergency_email =  db.Column(db.String(200))
    emergency_phone =  db.Column(db.String(200))
    visit_purpose = db.Column(db.String(200))
    activities = db.Column(db.Text())
    deported = db.Column(db.String(200))
    overstay = db.Column(db.String(200))    
    created_date = db.Column(db.DateTime())
    status = db.Column(db.String(200))   
    tipe = db.Column(db.String(200))
    pricing = db.Column(db.String(200)) 
    services = db.Column(db.String(200))
    traveldocumentowner = db.relationship("TravelDocument",backref="traveldocumentowner") 
    documentowner = db.relationship("Document",backref="documentowner") 

class TravelDocument(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tipe = db.Column(db.String(200))
    document_number = db.Column(db.String(200))
    place_issued = db.Column(db.String(200))
    date_issued = db.Column(db.DateTime())
    date_expired = db.Column(db.DateTime())
    traveldocumentowner_id =  db.Column(db.Integer(), db.ForeignKey("booking.id"))

class Document(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tipe = db.Column(db.String(200))
    filename = db.Column(db.Text())
    documentowner_id =  db.Column(db.Integer(), db.ForeignKey("booking.id"))






























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
    elif name == "cozero-living":  
        return render_template("cozero-living.html")  
                         
                     
    

@app.route("/sub/order/<tipe>",methods=["GET","POST"])
def CreateOrder(tipe):
    string = []
    chars = 'abccdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    finished = False
    while not finished:
        for x in range(1, 6+1):
            string.append(random.choice(chars))
        string = "".join(string)
        check = Booking.query.filter_by(url=string).all()
        if len(check) < 1:
            finished = True

    today = datetime.today()         
    order = Booking(url=string,created_date=today,status="uncomplete data",tipe=tipe)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for("StepOne",url=order.url))



@app.route("/sub/step1/<url>",methods=["GET","POST"])
def StepOne(url):
    booking = Booking.query.filter_by(url=url).first()
    if booking.tipe == "business visa offshore":
        form = StepOneBusinessForm()  
    else:    
        form = StepOneSocialForm()
      
    if form.validate_on_submit():
        checked = request.form.getlist("vehicle")
        if len(checked) == 10:
            services = form.services.data 
            if services == "E-Visa Service":
                booking.pricing = 3300000
                db.session.commit()
            elif services == "E-Visa Service + Visa Extention":
                booking.pricing = 6500000
                db.session.commit()
            elif services == "E-Visa Regular Proccess Service":
                booking.pricing = 2999000
                db.session.commit() 
            elif services == "E-Visa Express Proccess Service":
                booking.pricing = 3800000
                db.session.commit() 
            else:
                booking.pricing = 7000000
                db.session.commit()    
                
                           

            booking.paymentmethod = form.payment.data 
            booking.services = form.services.data 
            db.session.commit()          

            return redirect(url_for("StepTwo",url=url))
    return render_template("submission/stepone.html",form=form,tipe=booking.tipe)



@app.route("/sub/step2/<url>",methods=["GET","POST"])
def StepTwo(url):
    booking = Booking.query.filter_by(url=url).first()
    form = StepTwoForm()    
    if form.validate_on_submit():
        booking.fullname =   form.fullname.data
        booking.gender =  form.gender.data   
        booking.birthplace =   form.birthplace.data
        booking.birthdate =  form.birthdate.data
        booking.martial =  form.martial.data 
        booking.nationality =   form.nationality.data
        booking.email =  form.email.data   
        booking.phone =  form.phone.data 
        booking.original_address = form.original_address.data 
        booking.original_city = form.original_city.data
        booking.original_state =form.original_state.data
        booking.original_zip =  form.original_zip.data
        booking.original_country =  form.original_country.data
        booking.indo_address = form.indo_address.data
        booking.indo_city =form.indo_city.data
        booking.indo_state =  form.indo_state.data
        booking.indo_zip =  form.indo_zip.data
        db.session.commit()
        return redirect(url_for("StepThree",url=url))
    return render_template("submission/steptwo.html",form=form)    


@app.route("/sub/step3/<url>",methods=["GET","POST"])
def StepThree(url):
    booking = Booking.query.filter_by(url=url).first()
    form = StepThreeForm()    
    if form.validate_on_submit():
        booking.emergency_name = form.emergency_name.data 
        booking.emergency_status =  form.emergency_status.data
        booking.emergency_address =  form.emergency_address.data
        booking.emergency_city = form.emergency_city.data
        booking.emergency_state = form.emergency_state.data
        booking.emergency_zip =  form.emergency_zip.data
        booking.emergency_country =  form.emergency_country.data
        booking.emergency_email = form.emergency_email.data
        booking.emergency_phone =  form.emergency_phone.data
        db.session.commit()
        return redirect(url_for("StepFour",url=url))
    return render_template("submission/stepthree.html",form=form)    


@app.route("/sub/step4/<url>",methods=["GET","POST"])
def StepFour(url):
    booking = Booking.query.filter_by(url=url).first()
    form = StepFourForm() 
    if form.validate_on_submit():
        travel = TravelDocument(tipe=form.tipe.data,document_number=form.document_number.data,
            place_issued=form.place_issued.data,date_issued=form.date_issued.data,date_expired=form.date_expired.data,
            traveldocumentowner_id=booking.id)
        db.session.add(travel)
        db.session.commit()

        booking.visit_purpose = form.visit_purpose.data
        booking.activities = form.activities.data
        booking.deported = form.deported.data
        booking.overstay = form.overstay.data
        db.session.commit()

        return redirect(url_for("StepFive",url=url))
    return render_template("submission/stepfour.html",form=form)  


@app.route("/sub/step5/<url>",methods=["GET","POST"])
def StepFive(url):
    booking = Booking.query.filter_by(url=url).first()
    all_document = Document.query.filter_by(documentowner_id=booking.id).all()       
    return render_template("submission/stepfive.html",all_document=all_document,booking=booking,Document=Document)  


@app.route("/sub/step5/<url>/upload/<tipe>",methods=["GET","POST"])
def UploadDocument(url,tipe):
    booking = Booking.query.filter_by(url=url).first()
    all_document = Document.query.filter_by(documentowner_id=booking.id).all()   
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data       
        if allowed_file(file.filename): 
            upload = Document(documentowner_id=booking.id,tipe=tipe)              
            
            db.session.add(upload)
            db.session.commit()

            filename = str(upload.id) + secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))

            upload.filename = filename
            db.session.commit()
            return redirect(url_for("StepFive",url=url))
    return render_template("submission/upload.html",booking=booking,form=form,all_document=all_document,Document=Document)        


@app.route("/sub/step5/<url>/delete/<tipe>/<filename>",methods=["GET","POST"])
def DeleteDocument(url,tipe,filename):
    file = Document.query.filter_by(tipe=tipe,filename=filename).first_or_404()
    os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'], file.filename))    
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for("StepFive",url=url))




@app.route("/sub/step6/<url>/finished",methods=["GET","POST"])
def CheckFinishedData(url):
    booking = Booking.query.filter_by(url=url).first()
    all_document = Document.query.filter_by(documentowner_id=booking.id).all()  
    if len(all_document) == 5 :
        booking.status = "complete order"
        db.session.commit()
        return redirect(url_for("InvoiceId",url=url))
    else:
        flash("Please complete your data","danger")
        return redirect(url_for("StepFive",url=url))    





@app.route("/sub/invoice/<url>",methods=["GET","POST"])
def InvoiceId(url):
    booking = Booking.query.filter_by(url=url).first()
    pricing = int(booking.pricing)
    return render_template("submission/invoice.html",booking=booking,pricing=pricing)




















































if __name__ == "__main__":
	#manager.run()
	app.jinja_env.cache = {}
	app.run(host='0.0.0.0',threaded=True)	






