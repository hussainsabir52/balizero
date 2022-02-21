from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField, SelectField, SubmitField,FloatField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Email, Length
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.file import FileField, FileAllowed, FileRequired

images = UploadSet("images",IMAGES)



################################# Auth ####################################################
class UserRegisterForm(FlaskForm):
	username = StringField("name",validators=[InputRequired(),Length(max=100)])	
	email = StringField("email",validators=[InputRequired(),Email(),Length(max=200)])	
	password = PasswordField("password",validators=[InputRequired(),Length(min=6,max=100)])
	
class AddUserForm(FlaskForm):
	username = StringField("name",validators=[InputRequired(),Length(max=100)])	
	email = StringField("email",validators=[InputRequired(),Email(),Length(max=200)])	
	password = PasswordField("password",validators=[InputRequired(),Length(min=6,max=100)])
	role = SelectField("role",choices=[("manager","manager"),("director","director"),("admin","admin"),("project admin","project admin"),("production","production"),("design","design")])




class FormOne(FlaskForm):
	name = StringField("Your Name",validators=[InputRequired(),Length(max=100)])		
	email  = StringField("Email",validators=[InputRequired(),Length(max=100)])	
	time =  SelectField("Stay Duration",choices=[("Less than 30 days","Less than 30 days")
		,("More than 1 month and less than 6 month","More than 1 month and less than 6 month"),
		("Long term more than 6 month","Long term more than 6 month")])
	purpose = SelectField("My Travel Purpose",choices=[("Tourism","Tourism"),("Business/Other","Business/Other"),
		("Staycation/Business/Work Remotely","Staycation/Business/Work Remotely"),("Work","Work"),
		("Investment","Investment"),("I'm Retired","I'm Retired"),("I'm Married With Indonesian Citizen","I'm Married With Indonesian Citizen")])


class FormTwo(FlaskForm):
	name = StringField("Your Name",validators=[InputRequired(),Length(max=100)])		
	email  = StringField("Email",validators=[InputRequired(),Length(max=100)])	
	holder =  SelectField("Travel Document Holder of ",choices=[("Afghanistan","Afghanistan"),("Albania","Albania"),
		("Brazil","Brazil"),("Japan","Japan"),("Usa","Usa")])
	current = SelectField("Permanent Residency / Current Location",choices=[("Afghanistan","Afghanistan"),("Albania","Albania"),
		("Brazil","Brazil"),("Japan","Japan"),("Usa","Usa")])



class StepOneBusinessForm(FlaskForm):
	services = SelectField("Services",choices=[("E-Visa Regular Proccess Service","E-Visa Regular Proccess Service - IDR2.999.000"),
		("E-Visa Express Proccess Service","E-Visa Express Proccess Service - IDR3.800.000"),
		("E-Visa Regular Proccess Service + Visa Extention","E-Visa Regular Proccess Service + Visa Extention - IDR7.000.000")])
	payment = SelectField("Payment",choices=[("Credit Card","Credit Card"),("Paypal","Paypal")])

class StepOneSocialForm(FlaskForm):
	services = SelectField("Services",choices=[("E-Visa Service","E-Visa Service - IDR3.300.000"),
		("E-Visa Service + Visa Extention","E-Visa Service + Visa Extention - IDR6.500.000")])
	payment = SelectField("Payment",choices=[("Credit Card","Credit Card"),("Paypal","Paypal")])


class StepTwoForm(FlaskForm):
	fullname =  StringField("Full Name",validators=[InputRequired(),Length(max=100)])
	gender =  SelectField("Gender",choices=[("Male","Male"),("Female","Female")])  
	birthplace =  StringField("Birth Place",validators=[InputRequired(),Length(max=100)])
	birthdate = DateField("Birth Date",format="%m/%d/%Y")
	martial =  SelectField("Martial Status",choices=[("Single","Single"),("married","married")])  
	nationality = SelectField("Nationality",choices=[("Afghanistan","Afghanistan"),("Albania","Albania"),
		("Brazil","Brazil"),("Japan","Japan"),("Usa","Usa")])  
	email =   StringField("email",validators=[InputRequired(),Length(max=100)])
	phone =   StringField("phone",validators=[InputRequired(),Length(max=100)])
	original_address =   StringField("address",validators=[InputRequired(),Length(max=100)])
	original_city =  StringField("city",validators=[InputRequired(),Length(max=100)])
	original_state =   StringField("state/province/region",validators=[InputRequired(),Length(max=100)])
	original_zip =   StringField("zip",validators=[InputRequired(),Length(max=100)])
	original_country = SelectField("country",choices=[("Afghanistan","Afghanistan"),("Albania","Albania"),
		("Brazil","Brazil"),("Japan","Japan"),("Usa","Usa")])
	indo_address =   StringField("address",validators=[InputRequired(),Length(max=100)])
	indo_city =  StringField("city",validators=[InputRequired(),Length(max=100)])
	indo_state =  StringField("state/province/region",validators=[InputRequired(),Length(max=100)])
	indo_zip =   StringField("zip",validators=[InputRequired(),Length(max=100)])

class StepThreeForm(FlaskForm):
	emergency_name =  StringField("full name",validators=[InputRequired(),Length(max=100)])
	emergency_status =  SelectField("relationship",choices=[("Parents","Parents"),("Grand Parents","Grand Parents"),
		("Brother/Sister","Brother/Sister"),("Other Familly","Other Familly")])  
	emergency_address =  StringField("address",validators=[InputRequired(),Length(max=100)])
	emergency_city =StringField("city",validators=[InputRequired(),Length(max=100)])
	emergency_state =  StringField("state/region/province",validators=[InputRequired(),Length(max=100)])
	emergency_zip =  StringField("zip",validators=[InputRequired(),Length(max=100)])
	emergency_country =  SelectField("country",choices=[("Afghanistan","Afghanistan"),("Albania","Albania"),("Brazil","Brazil"),("Japan","Japan"),("Usa","Usa")])
	emergency_email =  StringField("email",validators=[InputRequired(),Length(max=100)])
	emergency_phone =  	StringField("phone",validators=[InputRequired(),Length(max=100)])

class StepFourForm(FlaskForm):
	tipe = SelectField("Type of Travel Document ",choices=[("Passport","Passport"),("Other Travel Document","Other Travel Document")])  
	document_number = StringField("Document Number",validators=[InputRequired(),Length(max=100)])
	place_issued = StringField("Place issued",validators=[InputRequired(),Length(max=100)])
	date_issued = DateField("Date issued",format="%m/%d/%Y")
	date_expired = DateField("Date expired",format="%m/%d/%Y")
	visit_purpose = SelectField("Visit Purpose",choices=[("Business Visit","Business Visit"),("Investment Visit","Investment Visit"),("Business Meeting","Business Meeting"),("Tourist Visit Purpose","Tourist Visit Purpose")])  
	activities = TextAreaField("Description of Your Activities")
	deported = SelectField("Do you has ever been deported from Indonesia? ",choices=[("No","No"),("Yes","Yes")])  
	overstay = SelectField("Do you has ever overstay in Indonesia?",choices=[("No","No"),("Yes","Yes")])  


class UploadForm(FlaskForm):	
	file = FileField("",validators=[FileRequired()])	
