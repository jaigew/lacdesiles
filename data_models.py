from google.appengine.ext import db

class House(db.Model):
    id = db.IntegerProperty()
    name = db.StringProperty()
    bedrooms = db.IntegerProperty()
    bathrooms = db.IntegerProperty()
    us_rental = db.FloatProperty()
    can_rental = db.FloatProperty()
    desc = db.StringProperty(multiline=True)
    picture_link = db.LinkProperty()
    gallery_link = db.LinkProperty()
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
    houseName = db.StringProperty(multiline=False)
    startDate = db.DateTimeProperty()
    endDate = db.DateTimeProperty()
    renterName = db.StringProperty(multiline=False)
    renterEmail = db.StringProperty(multiline=False)
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
	rates = db.StringProperty(multiline=True)