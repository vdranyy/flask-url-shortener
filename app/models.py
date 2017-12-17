import string
from math import floor
from urllib.parse import urlparse
from urllib.request import urlopen
from app import db


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.Text)
    short_url = db.Column(db.String(64))
    element_text = db.Column(db.Text)
    clicks = db.Column(db.Integer)
    created = db.Column(db.DateTime)

    def __str__(self):
        return "URL %s" % self.full_url

    def to_base_62(self, num, b=62):
        if b <= 0 or b > 62:
            return 0
        base = string.digits + string.ascii_lowercase + string.ascii_uppercase
        r = num % b
        res = base[r]
        q = floor(num / b)
        while q:
            r = q % b
            q = floor(q / b)
            res = base[int(r)] + res
        return res

    @staticmethod
    def to_base_10(num, b=62):
        base = string.digits + string.ascii_lowercase + string.ascii_uppercase
        limit = len(num)
        res = 0
        for i in range(limit):
            res = b * res + base.find(num[i])
        return res

    def check_url(self):
        try:
            response = urlopen(self.full_url)
            return response.status
        except ValueError:
            return

    def store_short_url(self, url=""):
        if url:
            self.short_url = url
        else:
            self.short_url = self.to_base_62(self.id)

    def build_short_url(self):
        return "http://localhost:5000/" + self.short_url

    @staticmethod
    def short_url_exists(url):
        short_url = Url.query.filter_by(short_url=url).first()
        return bool(short_url)

    def count_clicks(self):
        self.clicks += 1
