import os
import logging
from datetime import datetime
from datetime import timedelta
import data_models
from data_models import Rental, Renter, Page, Settings

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from datetime import date
import webapp2
from webapp2_extras import sessions

from utilities import Utilities


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


class EditRentalHandler(BaseHandler):
    def get(self):
        u = Utilities()

        action = self.request.get('a')
        if action == "d":
            self.response.out.write("Deleting...<br>")
            startDate = self.request.get('sd')
            house = self.request.get('h')
            renterEmail = self.request.get('re')

            rental = u.getRentalRecord(renterEmail, house, startDate)
            self.response.out.write(startDate)

            if rental:

                rental.delete()

                self.response.out.write("Record Deleted<br>")
            else:
                self.response.out.write("Record does not exist<br>")

        rentals = u.getAllRentalsForCurrentYear()

        rentals_table = "<table border=1><tr><td>Renter</td><td>House</td><td>Start Date</td><td>End Date</td><td>&nbsp;</td><td>&nbsp;</td></tr>"

        for rental in rentals:
            rentals_table = rentals_table + "<tr><td>" + rental.renterName + "</td><td>" + rental.houseName + "</td><td>" + rental.startDate.strftime("%m/%d/%Y") + "</td><td>" + rental.endDate.strftime(
                "%m/%d/%Y") + "</td><td>-</td><td><a href='/admin/editRentals/?a=d&re=" + rental.renterEmail + "&sd=" + rental.startDate.strftime("%m/%d/%Y") + "&h=" + rental.houseName + "'>delete</a></td></tr>"

        rentals_table = rentals_table + "</table>"

        context = {'admin_body': rentals_table}

        u.render("admin_base.html", context, self, True, "rental/schedule/")


class EditPageHandler(BaseHandler):
    def showPages(self):
        u = Utilities()
        addeditstyle = "display:inline"
        page = Page.all()  # .filter('id = ', 1)
        pageList = ""
        for p in page:
            pageList = pageList + "<tr><td>" + \
                str(p.id) + "</td><td>" + p.title + "</td></tr>"

        context = {'page': page, 'addeditstyle': addeditstyle,
                   'pageList': pageList}

        u.render("adminPage.html", context, self, True, "")

    def get(self):

        self.showPages()

    def post(self):
        u = Utilities()
        page = Page()

        page.id = self.request.get('id')
        page.title = self.request.get('title')
        page.body = self.request.get('body')

        page.put()

        self.showPages()


class EditSettingsHandler(BaseHandler):

    def showSettings(self):

        u = Utilities()
        y = u.getYear()
        startdate = u.getStartDate(y)
        enddate = u.getEndDate(y)
        rates = u.getRates()

        context = {'year': y, 'startdate': startdate,
                   'enddate': enddate, 'rates': rates}

        u.render("adminSettings.html", context, self, True, "")

    def get(self):

        self.showSettings()

    def post(self):
        #u = Utilities()
        self.response.out.write(self.request.get('year'))
        # db.delete(Settings.all())
        # self.response.out.write("deleted")
        settings = Settings()
        settings.year = int(self.request.get('year'))
        settings.startdate = datetime.strptime(
            self.request.get('startdate'), "%m/%d/%Y")
        self.response.out.write(self.request.get('startdate'))
        self.response.out.write(settings.startdate)
        settings.enddate = datetime.strptime(
            self.request.get('enddate'), "%m/%d/%Y")
        settings.put()
        self.response.out.write("saved")
        self.showSettings()


class AdminIndexHandler(BaseHandler):
    def get(self):

        u = Utilities()

        context = {
            'admin_body': "Welcome to the Lac Des Iles Administration Page"}

        u.render("admin_base.html", context, self, True, "rental/schedule/")

        #self.response.out.write("Edit Rentals<br>")
#		self.response.out.write("<br><br><a href='/admin/addRentals/'>Add Rentals</a><br><br>")
#		self.response.out.write("<a href='/admin/editRentals/'>Edit/Delete Rentals</a><br><br>")
#		self.response.out.write("<a href='/admin/addRenters/'>Add Renters</a><br>")
#		self.response.out.write("<br><br><br><hr><br><br><br>")
#		self.response.out.write("<a href='/admin/clearRentals/'>Clear ALL Rentals</a><br>")
#		self.response.out.write("<a href='/admin/resetUsers/'>Reset Renters</a><br>")


class EditRenterHandler(BaseHandler):
    def get(self):
        # self.redirect("../addRenters/")
        u = Utilities()

    def post(self):
        self.redirect("../addRenters/")


class AddRenterHandler(BaseHandler):

    def showRenters(self):
        u = Utilities()

        id = self.request.get('id')
        #logging.info("id = " + id)
        addeditstyle = "display:inline"
        if id == "None":
            r = Renter()
            id = -1
            email = self.request.get('email')
            r = u.getUserByEmail(email)
            r.name = " "
            r.email = " "
            r.color = " "
            r.password = "flavia"

        else:
            if id == "":
                r = Renter()
                addeditstyle = "display:none"
                r.id = -1
                r.name = ""
                r.email = ""
                r.color = ""
                r.password = "flavia"
                r.rotation_pos = -1
            else:
                r = u.getRenterById(id)
            #logging.info("id = " + id)

        renterList = ""

        renters = Renter.all()

        for renter in renters:
            if id == str(renter.id):
                logging.info("Renter = " + r.name)
            renterList = renterList + "<a href='../addRenters/?id=" + str(renter.id) + "&email=" + renter.email + "'>Edit</a>&nbsp;-&nbsp;<span style='background-color:#" + \
                renter.color + ";height=20px;width=100px;'>" + renter.name + \
                "</span> - " + renter.email + " - " + renter.color + "<br>"

        context = {'renterList': renterList,
                   'r': r, 'addeditstyle': addeditstyle}

        u.render('adminRenter.html', context, self, False, "admin/")

    def get(self):

        # self.response.out.write("AddRenterHandler<br>")
        self.showRenters()

    def post(self):
        u = Utilities()

        id = self.request.get('renterId')
        # renter without an ID
        logging.info("id = " + id)
        if id == "None":
            r = Renter()
            id = -1
            email = self.request.get('email')
            r = u.getUserByEmail(email)

        elif self.request.get('renterId') == "-1":
            # new renter or no renter
            #	r.id = int(self.request.get('renterId'))
            # else:
            r = Renter()
            r.id = u.getNextRenterId()
            logging.info("***id = " + str(r.id))

        else:
            # renter with an ID
            r = u.getRenterById(id)

        r.email = self.request.get('renterEmail')
        r.name = self.request.get('renterName')
        r.color = self.request.get('renterColor')
        r.family = int(self.request.get('renterFamily'))
        if self.request.get('renterPosition') == "-1":
            r.rotation_pos = -1
        else:
            r.rotation_pos = int(self.request.get('renterPosition'))

        r.password = self.request.get('renterPassword')

        r.put()
        self.redirect("../addRenters/")
        # self.showRenters()


class AddRentalHandler(BaseHandler):

    def renderSchedule(self):
        u = Utilities()
        year = u.getYear()
        startDate = u.getStartDate(year)
        #datetime(u.getYear(), 6, 4)
        logging.info(startDate)
        endDate = u.getEndDate(year)
        #datetime(u.getYear(), 9, 24)
        startDates = u.getSaturdaySelects(u.getYear())
        endDates = u.getSaturdaySelects(u.getYear())

        renterEmailSelect = u.getRenterSelect()
        logging.info(renterEmailSelect)

        dateHeaderRow = u.createDateHeaderRow(startDate, endDate)
        boseRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'bose').order(
            '-startDate'), 'bose', startDate, endDate, "Bose House", self)
        minkRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'mink').order(
            '-startDate'), 'mink', startDate, endDate, "Mink Point", self)
        mainRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'main').order(
            '-startDate'), 'main', startDate, endDate, "Main House", self)
        islandRentalRow = u.createScheduleRow(Rental.all().filter('houseName = ', 'island').order(
            '-startDate'), 'island', startDate, endDate, "Island", self)

        context = {'userTurnToSchedule': 'true', 'startDatesSelect': startDates, 'endDatesSelect': endDates,
                   'boseRentals': boseRentalRow, 'mainRentals': mainRentalRow, 'islandRentals': islandRentalRow,
                   'minkRentals': minkRentalRow, 'dateHeaderRow': dateHeaderRow, 'renterEmailSelect': renterEmailSelect}

        u.render('adminSchedule.html', context,
                 self, False, "rental/schedule/")

    def get(self):
        # self.response.out.write("AddRentalHandler<br>")

        self.renderSchedule()

    def post(self):
        logging.info("POST to Admin Schedule Add" +
                     self.request.get('startDateSelect'))

        sDate = datetime.strptime(
            self.request.get('startDateSelect'), "%m/%d/%Y")
        eDate = datetime.strptime(
            self.request.get('endDateSelect'), "%m/%d/%Y")
        span = timedelta(days=7)

        while sDate < eDate:
            r = Rental()
            r.houseName = self.request.get('houseName')
            r.renterEmail = self.request.get('renterEmail')
            r.renterName = self.request.get('renterName')
            r.startDate = sDate
            r.endDate = eDate
            r.put()
            logging.info("Saved for record for " + r.houseName)
            sDate = sDate + span

        self.renderSchedule()
