from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, DateTimeField
from wtforms.validators import Required


class URLForm(FlaskForm):
    full_url = StringField("Your URL", validators=[Required()])
    short_url = StringField("Your short URL (optional)")
    submit = SubmitField("Create short URL")


class EditURLForm(FlaskForm):
    short_url = StringField("Short URL", validators=[Required()])
    element_text = TextField("Message")
    created = DateTimeField("Created", render_kw={"readonly": True})
    clicks = StringField("Clicks", render_kw={"readonly": True})
    submit = SubmitField("Save")
