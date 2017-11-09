import os
import logging
from datetime import datetime
from data_models import House, Renter, Rental, Settings

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from datetime import date
from utilities import Utilities


try:
    import utilities # Assumed to be in the same directory.
except ImportError:
    logging.error("Error loading utilities")

class ClearRentalHandler(webapp.RequestHandler):
	def get(self):
		rentals = Rental.all()
		db.delete(rentals)
		self.response.out.write("All Rental Records Deleted")
		
class CreateSettingsHandler(webapp.RequestHandler):
	def get(self):
		s = Settings()
		s.year = 2012
		s.startdate = datetime.strptime("6/4/12", "%m/%d/%y")
		s.enddate = datetime.strptime("9/4/12", "%m/%d/%y")
		s.put()

class ResetUserDataHandler(webapp.RequestHandler):

	def showRenters(self):
		u = Utilities()
		
		renterList = ""
		
		renters = Renter.all()
		
		for renter in renters:
			renterList = renterList + "<span style='background-color:#" + renter.color + ";height=20px;width=100px;'>" + renter.name + "</span> - " + renter.email + " - " + renter.color + "<br>"	
			
		
		context = {'renterList':renterList}
		
		u.render('adminRenter.html', context, self, False, "admin/")
		
	def createUser(self, id, name, email, password, color, pos, family=0):
		r = Renter()
		r.id = id
		r.name = name
		r.email = email
		r.password = password
		r.color = color
		r.update_date = date.today()
		r.rotation_pos = pos
		r.family = family
		r.put()
		id = id + 1
		return id
		
	def get(self):
		logging.log(logging.DEBUG, "Resetting Users")
		self.response.out.write("Resetting Renters<br>")
		renters = Renter.all()        
		db.delete(renters)
		
		#for renter in renters:
		#    renter.delete()

		self.response.out.write("Saving Renters<br>")
		id = 1
		#id = self.createUser(id, "Greg", "gewing@gewing.com", "flavia", "#0033FF")	
		#id = self.createUser(id, "Bill", "bmott@theoceanproject.org", "flavia", "#6600FF")
		#id = self.createUser(id, "Fred", "fred@duncannondesign.com", "flavia", "#FF33FF")
		
		id = self.createUser(id, 'David', 'david.m.mott@gmail.com', 'flavia', 'FFFF66', 1, 1)
		id = self.createUser(id, 'Miven', 'miventrageser@gmail.com', 'flavia', '99FF66', 2, 1)
		id = self.createUser(id, 'Rooney', '2008roxanna@gmail.com', 'flavia', 'ff6666', 3, 1)
		id = self.createUser(id, 'John', 'cmarciano@rcn.com', 'flavia', '33ffff', 4, 1)
		id = self.createUser(id, 'Chris', 'ChristopherMott@hotmail.com', 'flavia', 'ff0000', 5, 1)
		id = self.createUser(id, 'Jay', 'jm52716@aol.com', 'flavia', '33ff33', 6, 1)
		id = self.createUser(id, 'Emily', 'emily@emilymott.com', 'flavia', '3399ff', 7, 1)
		id = self.createUser(id, 'Fred', 'fred@duncannondesign.com', 'flavia', '99ccff', -1, 1)
		id = self.createUser(id, 'Annemarie', 'annemarie.mott.ewing@gmail.com', 'flavia', '3366ff', 8, 1)
		id = self.createUser(id, 'Greg', 'gewing@gewing.com', 'flavia', 'ff3300', -1, 1)
		id = self.createUser(id, 'Jim', 'jhmott@juno.com', 'flavia', '9999ff', 9, 1)
		id = self.createUser(id, 'Bill', 'bmott@theoceanproject.org', 'flavia', 'cc66ff', 10, 1)
		id = self.createUser(id, 'Julie', 'jmott.munger@gmail.com', 'flavia', '9966ff', 11, 1)
		id = self.createUser(id, 'Alison', 'alison', 'flavia', 'cc99cc', 12, 1)
		id = self.createUser(id, 'Charlie', 'emottfamily@aol.com', 'flavia', '00ccff', 13, 1)
		id = self.createUser(id, 'Andy & Gail', 'agmott6810@hotmail.com', 'flavia', 'ff9900', -1, 1)
		id = self.createUser(id, 'Tony & Joan', 'atmott@yahoo.com', 'flavia', 'ffcc00', -1, 1)
		id = self.createUser(id, 'Peter & Gail', 'interconnect_mott@frontiernet.net', 'flavia', '33ff66', -1, 1)
		id = self.createUser(id, 'Jay & Leslie', 'JGMott@aol.com', 'flavia', 'ccff66', -1, 1)
		id = self.createUser(id, 'Anne and John', 'booth', 'flavia', '33cc33', -1, 1)
		id = self.createUser(id, 'Goodith', 'cybergoodie@cogeco.ca', 'flavia', '66ffcc', -1, 0)
        
        
#id = self.createUser(id, 'Miven', 'miventrageser@gmail.com - 99FF66
#id = self.createUser(id, 'John', 'cmarciano@rcn.com - 33ffff
#id = self.createUser(id, 'Jay', 'jm52716@aol.com - 33ff33
#id = self.createUser(id, 'Fred', 'fred@duncannondesign.com - 99ccff
#id = self.createUser(id, 'Annemarie', 'annemarie.mott.ewing@gmail.com - 3366ff
#id = self.createUser(id, 'Jim', 'jhmott@juno.com - 9999ff
#id = self.createUser(id, 'Julie', 'jmott.munger@gmail.com - 9966ff
#id = self.createUser(id, 'Charlie', 'emottfamily@aol.com - 00ccff
#id = self.createUser(id, 'Jay & Leslie', 'JGMott@aol.com - ccff66
#id = self.createUser(id, 'Goodith', 'cybergoodie@cogeco.ca - 66ffcc
#id = self.createUser(id, 'David', 'david.m.mott@gmail.com - FFFF66
#id = self.createUser(id, 'Rooney', '2008roxanna@gmail.com - ff6666
#id = self.createUser(id, 'Chris', 'ChristopherMott@hotmail.com - ff0000
#id = self.createUser(id, 'Emily', 'emily@emilymott.com - 3399ff
#id = self.createUser(id, 'Greg', 'gewing@gewing.com - ff3300
#id = self.createUser(id, 'Bill', 'bmott@theoceanproject.org - cc66ff
#id = self.createUser(id, 'Alison', 'alison - cc99cc
#id = self.createUser(id, 'Andy & Gail', 'agmott6810@hotmail.com - ff9900
#id = self.createUser(id, 'Tony & Joan', 'atmott@yahoo.com - ffcc00
#id = self.createUser(id, 'Peter & Gail', 'interconnect_mott@frontiernet.net - 33ff66
#id = self.createUser(id, 'Anne and John', 'booth - 33cc33
#id = self.createUser(id, 'Patrick Mott - pmott10@gmail.com - 
#id = self.createUser(id, 'Kath Kasirer - k.kasirer@nfb.ca - FFeeCC
#id = self.createUser(id, 'Bruce McKay - bmckay@seaweb.org - 99ffff
#id = self.createUser(id, 'M. & B. Morison - morisonbu@proctornet.com - 33ff99
#id = self.createUser(id, 'N. & J. Wootton - nicholaswootton@hotmail.com - 66cc99
#id = self.createUser(id, 'Tim Heeney - theeney@goodmans.ca - FF9966
#id = self.createUser(id, 'Matthew Heeney - matthew_heeney@hotmail.com - FF3399
#id = self.createUser(id, 'A. Kasirer & P. Kettner - AnnaPaul@total.net - CC9999
#id = self.createUser(id, 'P. Schiot & G. Ladd - gmladd@gmail.com - CCFF00
#id = self.createUser(id, 'Kate Haik - threemaples@mac.com - 33cccc
#id = self.createUser(id, 'T. & J. Dawe - janettom1235@aol.com - 00ffff
#id = self.createUser(id, 'D. Smock & L. Stovall - lhgsds@comcast.net - 00ff00
#id = self.createUser(id, 'Steve & Karen - saedson@sympatico.ca - FFFF00
		
		
		 
		self.response.out.write("Renters Saved<br><hr>")
			
		self.showRenters()		
        
class DataHandler(webapp.RequestHandler):        
    def get(self):
        house = House()
        house.id = 1
        house.name = "Bose House"
        house.bedrooms = 3
        house.bathrooms = 1
        house.us_rental = 550.5
        house.can_rental = 450.5
        house.desc = "The Bose House"
        house.picture_link = "http://lac-des-iles.appspot.com/"
        house.gallery_link = "http://lac-des-iles.appspot.com/"
        house.put()
        self.response.out.write("Saved House: " + house.name)
        
