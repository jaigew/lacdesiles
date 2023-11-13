from google.appengine.ext import db
#from google.cloud.db import db

#client = db.Client()


class House(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()
    bedrooms = db.IntegerProperty()
    bathrooms = db.IntegerProperty()
    us_rental = db.FloatProperty()
    can_rental = db.FloatProperty()
    desc = db.StringProperty()
    picture_link = db.StringProperty()
    gallery_link = db.StringProperty()
    update_date = db.DateProperty()


class Renter(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()
    email = db.StringProperty()
    password = db.StringProperty()
    color = db.StringProperty()
    update_date = db.DateProperty()
    rotation_pos = db.IntegerProperty()
    family = db.IntegerProperty()


class Rental(db.Model):
    houseName = db.StringProperty()
    startDate = db.DateTimeProperty()
    endDate = db.DateTimeProperty()
    renterName = db.StringProperty()
    renterEmail = db.StringProperty()
    renterId = db.IntegerProperty()
    updateDate = db.DateTimeProperty(auto_now_add=True)


class Page(db.Model):
    id = db.IntegerProperty()
    title = db.StringProperty()
    body = db.TextProperty()


class Settings(db.Model):
    year = db.IntegerProperty()
    startDate = db.DateTimeProperty()
    endDate = db.DateTimeProperty()
    rates = db.TextProperty()
    keyName = db.StringProperty()
