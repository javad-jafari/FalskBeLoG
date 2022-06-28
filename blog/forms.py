from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User
from flask_login import current_user


class RegisterForm(FlaskForm):

    username = StringField("username", validators=[DataRequired(),Length(min=4, max=30)])

    email = StringField("email", validators=[DataRequired() ])

    password = PasswordField("password", validators=[DataRequired(), Length(min=4, max=30)])

    confirm_password = PasswordField("confirm_password",validators=[DataRequired(), EqualTo("password")])
    


    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This user, is already exist !")

    def validate_email(self,email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email, is already exist !")








class LoginForm(FlaskForm):
    
    username = StringField("username", validators=[DataRequired()])

    password = PasswordField("password", validators=[
    DataRequired(), Length(min=4, max=30)])

    rememberme = BooleanField("remember me")



class UpdateProfileForm(FlaskForm):

    username = StringField("username", validators=[DataRequired(),Length(min=4, max=30)])

    email = StringField("email", validators=[ DataRequired()])

    def validate_username(self,username):
        if current_user.username != username.data :
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This user, is already exist !")

    def validate_email(self,email):

        if current_user.email != email.data :
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email, is already exist !")



class CreatePostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(),Length(min=4, max=30)])

    content = StringField("content", validators=[ DataRequired()])
