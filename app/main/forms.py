from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class URLForm(FlaskForm):
    full_url = StringField("Your URL", validators=[Required()])
    short_url = StringField("Your short URL (optional)")
    submit = SubmitField("Create short URL")
