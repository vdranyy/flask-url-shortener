from datetime import datetime
from flask import render_template, request, flash, \
    redirect, url_for, Markup
from app import db
from app.main import main
from app.main.forms import URLForm, EditURLForm
from app.models import Url


@main.route("/", methods=["GET", "POST"])
def index():
    urls = Url.query.all()
    form = URLForm()
    if form.validate_on_submit():
        full_url = form.full_url.data
        short_url = form.short_url.data
        if Url.short_url_exists(short_url):
            flash("Short url is already exist. Try another one.")
            return redirect(url_for("main.index"))
        new_url = Url(full_url=full_url, clicks=0, created=datetime.today())
        element_text = new_url.check_url()
        if not element_text:
            flash("Check url!!! Failed request %s" % new_url.full_url)
            return redirect(url_for("main.index"))
        new_url.element_text = element_text
        db.session.add(new_url)
        db.session.commit()
        new_url.store_short_url(short_url)
        flash("Your url has been created successfully.")
        return redirect(url_for("main.index"))

    return render_template("index.html", urls=urls, form=form)


@main.route("/detail/<short_url>", methods=["GET", "POST"])
def detail_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    form = EditURLForm(obj=url)
    if form.validate_on_submit():
        new_short_url = form.short_url.data
        if Url.short_url_exists(new_short_url) and short_url != new_short_url:
            flash("Short url is already in use.")
            return redirect(url_for("main.detail_url", short_url=url.short_url))
        url.short_url = new_short_url
        url.element_text = form.element_text.data
        return redirect(url_for("main.detail_url", short_url=url.short_url))
    return render_template("detail_url.html", url=url, form=form)


@main.route("/<short_url>")
def short_url_redirect(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    url.count_clicks()
    return redirect(url.full_url)
