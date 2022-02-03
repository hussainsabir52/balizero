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
	time =  SelectField("How Long You Plan To Stay",choices=[("Less than 30 days","Less than 30 days")
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

