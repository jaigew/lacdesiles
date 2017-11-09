import logging
from datetime import datetime
from datetime import timedelta
import data_models

from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
import webapp2
from data_models import House
from data_models import Rental, Renter, Page
from google.appengine.api import mail
from webapp2_extras import sessions

try:
	from utilities import Utilities # Assumed to be in the same directory.
except ImportError:
	logging.log(logging.ERROR, "Error loading utilities")




class BaseHandler(webapp2.RequestHandler):
        def dispatch(self):
                # Get a session store for this request.
                self.session_store = sessions.get_store(request=self.request)
 
                try:
                        # Dispatch the request.
                        webapp2.RequestHandler.dispatch(self)
                finally:
                        # Save all sessions.
                        self.session_store.save_sessions(self.response)
 
        @webapp2.cached_property
        def session(self):
                # Returns a session using the default cookie key.
                return self.session_store.get_session()

class LoginHandler(BaseHandler):
	def get(self):
		u = Utilities()
		u.logout(self)
		logging.log(logging.INFO, "get request to login")
		path = self.request.get("p")
		u.render('login.html', {}, self, False, path)
	
	def post(self):
		u = Utilities()
		logging.log(logging.INFO, "POST to loginhandler")
		path = self.request.get("p")
	
		if not u.checkLogin(self):
			logging.log(logging.INFO, "Not logged in-login")
			u.render("login.html", {}, self, login_required=False)
		else:
			logging.log(logging.INFO, "Logged in-login")
			
			self.redirect("/" + path)
		
		
class MainHandler(BaseHandler):
	
	def get(self):
		u = Utilities()
		p = Page.all().filter("id = ", 1)
		body = ""
		title = ""
		if p.count() > 0:
			for page in p:
				body = page.body
				title = page.title
		  
		context = {'content' : str(body), 'title' : title}
		u.render('base.html', context, self, login_required=False)
	
	def post(self):
		u = Utilities()
		logging.log(logging.INFO, "POST to login - mainhandler")
	
		if not u.checkLogin(self):
			logging.log(logging.INFO, "Not logged in-main")
			u.render("login.html", {}, self, login_required=False)
		else:
			logging.log(logging.INFO, "Logged in-main")
			u.render("base.html", {}, self, login_required=False)
		
class FamilyHandler(BaseHandler):
	
	def get(self):
		u = Utilities()
		logging.log(logging.DEBUG, 'Family Request')
		
		gallery = ""
		i = 1
		 
		while i <= 20:
			gallery = gallery + "<a href='/images/family/old_pics_" + str(i) + ".jpg' rel='lightbox[oldpics]' title=''><img src='/images/family/old_pics_" + str(i) + ".jpg' height='75' alt='' rel='lightbox' border=0/></a>&nbsp;&nbsp;"
			
			i = i + 1
			
		context = {'gallery':gallery}
		
		if u.isLoggedInFamily(u.getLoggedInEmail(self)):
			u.render('family.html', context, self, True, "family/")
		else:
			u.render('non_family.html', context, self, True, "family/")
	
	def post(self):
		u = Utilities()
		u.render('family.html', {}, self, login_required=True)
		
class LocalHandler(BaseHandler):
	
	def get(self):
		u = Utilities()
		logging.log(logging.DEBUG, 'GET Request - local')
		u.render('local.html', {}, self, login_required=False)
	
	def post(self):
		u = Utilities()
		u.render('local.html', {}, self, login_required=False)

class RentalHandler(BaseHandler):
	
	def get(self):
		logging.debug('GET Request - rental')
		u = Utilities()
		u.render('rental.html', {}, self, True, "rental/")
	
	def post(self):
		u = Utilities()
		u.render('rental.html', {}, self, login_required=True)
  
class RecreationHandler(BaseHandler):
	
	def get(self):
		logging.debug('GET Request')
		u = Utilities()
		u.render('recreation.html', {}, self, login_required=False)
	
	def post(self):
		u = Utilities()
		u.render('recreation', {}, self, login_required=False)
		
class ClearDataHandler(webapp2.RequestHandler):
	
	def get(self):
		logging.info("Clearing Data")
		handler.redirect("/login/?p=" + path)
	
	def post(self):
		logging.info("Clearing Data")
		handler.redirect("/login/?p=" + path)
		
class EmailNextHandler(BaseHandler):
	def get(self):
		renter_finished_name = self.request.get('rfn')
		renter_finished_email = self.request.get('rfe')
		renter_next_name = self.request.get('rnn')
		renter_next_email = self.request.get('rne')
		
		#renter_next_email = "gewing@gewing.com"
		renter_finished_email = renter_finished_email + ",gewing@gmail.com,bmott.top@gmail.com"
		
		mail.send_mail(sender="Lac Des Iles Web <gewing@gmail.com>",
			to=renter_next_email,
			cc=renter_finished_email,
			subject="Lac Des Iles Rental - You're Next!",
			body="""You're next!  """ + renter_finished_name + """ just finished selecting their times so you are next.  Please
visit the site at http://lac-des-iles.appspot.com/ and sign in with your email address (""" + renter_next_email + """) and the password 
you received earlier (the Island's proper name).  Please make your choice as soon as possible to keep the rotation running smoothly.

Email Greg at gewing@gewing.com if you have any trouble with the site.
Email Bill at bmott.top@gmail.com if you have any questions about selection.""")
		
		self.response.out.write("Email sent to " + renter_next_email + ".<br><br>")
		self.response.out.write("<a href='/'>Return to the Lac Des Iles website</a>")

class ScheduleHandler(BaseHandler):
		
	def renderSchedule(self, errorMsg="", rfn=""):
		logging.log(logging.INFO, '********GET Request in Schedule Handler')
		public = self.request.get("p")
		yearString = self.request.get("y")
		logging.log(logging.INFO, '*** public = ' + public)
			
		u = Utilities()
		today = datetime.today()
		logging.info(today.year)
		year=0
		if yearString == "":
			year = u.getYear()
		else:
			year = int(yearString)

	
		startDates = u.getSaturdaySelects(year)
		endDates = u.getSaturdaySelects(year)
		
		startDate = u.getStartDate(year) 
		#datetime(u.getYear(), 6, 2) 
		logging.info(startDate)
		endDate = u.getEndDate(year)
		#datetime(u.getYear(), 9, 24)
		
		#rentals = Rental.all()
		#for r in rentals:
		#	logging.info("delete " + r.houseName)
		#	r.delete()
		
		if public == "y":
			rfe = ""
		else:
			rfe = u.getLoggedInEmail(self)
			logging.log(logging.INFO, '* rfe = ' + rfe)
			
		nextrenter = u.getNextRenterByCurrentEmail(rfe)
		
		if nextrenter:
			rne = nextrenter.email 
			rnn = nextrenter.name
		else:
			rne = ""
			rnn = ""
		
		#query = db.GqlQuery("SELECT * FROM Rental WHERE renterEmail = :email",
		#		email=u.getLoggedInEmail(self)).filter('startDate > ', datetime(u.getYear(), 1, 1))
		
		rental = Rental.all().filter('renterEmail = ', u.getLoggedInEmail(self)).filter('startDate > ', datetime(year, 1, 1))
		#rental = query.get()
		
		#rental = u.getRenterScheduledByEmail(rfe)
		logging.log(logging.INFO, '** count = ' + str(rental.count()))
		if rental.count() > 0:
			rentalSaved = True
			logging.info("rentalSaved = True")
		else:
			rentalSaved = False
			logging.info("rentalSaved = False")
		
		rotationList = ""
		if u.isLoggedInFamily(u.getLoggedInEmail(self)):
			rotation = Renter.all().order('rotation_pos')
			rotationList = "Rotation for " + str(year) + ":<br>"
			for rot in rotation:
				if rot.rotation_pos > 0:
					rotationList = rotationList + str(rot.rotation_pos) + ". " + rot.name + "<br>"	
		
		logging.info(rotationList) 
			
		dateHeaderRow = u.createDateHeaderRow(startDate, endDate)
		boseRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'bose').order('-startDate'), startDate, endDate, "Bose House", self, public)
		minkRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'mink').order('-startDate'), startDate, endDate, "Mink Point", self, public)
		mainRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'main').order('-startDate'), startDate, endDate, "Main House", self, public)
		islandRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'island').order('-startDate'), startDate, endDate, "Island", self, public)
		#logging.info("boseRentalRow = " + boseRentalRow)
		
		context = {'userTurnToSchedule' : 'true', 'startDatesSelect' : startDates, 
			'endDatesSelect' : endDates, 'boseRentals': boseRentalRow, 'mainRentals':mainRentalRow, 
			'islandRentals':islandRentalRow, 'minkRentals':minkRentalRow, 'dateHeaderRow':dateHeaderRow ,
			'errorMsg':errorMsg, 'rnn':rnn, 'rne':rne, 'rfn':rfn, 'rfe':rfe, 'rentalSaved':rentalSaved, 
			'rotationList':rotationList, 'public':public}

		u.render('schedule.html', context, self, False, "rental/schedule/", public)
		
	def get(self):
		self.renderSchedule()
		
	def post(self):
		logging.info("POST to Schedule" + self.request.get('startDateSelect'))
		
		rentalExists = False
		
		errorMsg = ""
		sDate = datetime.strptime(self.request.get('startDateSelect'), "%m/%d/%Y")
		eDate = datetime.strptime(self.request.get('endDateSelect'), "%m/%d/%Y")
		houseName = self.request.get('houseName')
		span = timedelta(days=7)
		rentalSaved = False
		
		#check if rental exists, if it does exit
		while sDate < eDate:
			query = db.GqlQuery("SELECT * FROM Rental WHERE houseName = :house AND startDate = :start AND endDate = :end",
				house=houseName, start=sDate, end=eDate)
			rental = query.get()
			logging.info("Checking if rental exists for " + houseName + " starting on " + self.request.get('startDateSelect'))
			if rental:
				rentalExists = True
				errorMsg = "This house is already rented for at least part of that time by " + rental.renterName
				logging.info("RENTAL EXISTS : " + errorMsg)
				break
			sDate = sDate + span
			
		if not rentalExists:
			#rental doesn't exist so reset sDate and save rental
			sDate = datetime.strptime(self.request.get('startDateSelect'), "%m/%d/%Y")
			while sDate < eDate:
				r = Rental()
				r.houseName = houseName
				r.renterEmail = self.request.get('renterEmail')
				r.renterName = self.request.get('renterName')
				r.startDate = sDate
				r.endDate = eDate
				r.put()
				rentalSaved = True
				logging.info("Saved for record for " + r.houseName)
				sDate = sDate + span
		
		mail.send_mail(sender="Lac Des Iles Web <gewing@gmail.com>",
			to="gewing@gmail.com",
			cc="bmott.top@gmail.com",
			subject="Lac Des Iles Rental Saved",
			body="""Choise Saved for """ + self.request.get('renterName') + """ in """ + houseName + """ from """ + 
				self.request.get('startDateSelect') + """ to """ + self.request.get('endDateSelect') + """.""")
				
		self.renderSchedule(errorMsg, self.request.get('renterName'))
	

class CottagesHandler(BaseHandler):
	
	def get(self, return_key=None):
		key = return_key
		if key:
			logging.info('Return Key = ' + return_key)
		else:
			logging.info('No return_key')
			key = "cottages"
		
		
#		query = House.gql("WHERE id = :id",
#				  id=key )
#		houses = query.fetch(1)
#		for house in houses:
#			logging.info("Retrieved = " + house.name)
#		
		u = Utilities()   
		u.render(key + '.html', {}, self, login_required=False)
	
	def post(self):
		u = Utilities()
		u.render('cottages.html', {}, self, login_required=False)
		

class ContactHandler(BaseHandler):
	
	def get(self):
		logging.log(logging.DEBUG, 'GET Request')
		u = Utilities()
		u.render('contact.html', {}, self, login_required=False)
	
	def post(self):
		logging.log(logging.DEBUG, dir(request))
		u = Utilities()
		u.render('contact.html', {}, self, login_required=False)

class MapHandler(BaseHandler):
	
	def get(self):
		logging.log(logging.DEBUG, 'GET Request')
		u = Utilities()
		u.render('map.html', {}, self, login_required=False)
	
	def post(self):
		logging.log(logging.DEBUG, dir(request))
		u = Utilities()
		u.render('map.html', {}, self, login_required=False)
