import os
import logging
from datetime import datetime
from datetime import date
from datetime import timedelta
from google.appengine.ext import db
import data_models
from Cookies import Cookies
import Cookie
#from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
#import cookielib

import re
import base64

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp

from data_models import Renter, Rental, House, Settings


class Utilities:

    def getYear(self):
        query = db.GqlQuery("SELECT year FROM Settings")
        s = query.get()
        if s:
            return s.year
        else:
            return 2014
    # def getSettingsID(self):
    #     query = db.GqlQuery("SELECT rates FROM Settings")
    #     s = query.get()
    #     if s:
    #         return s.rates
    #     else:
    #         return "Error loading rates."

    def getRates(self):
        query = db.GqlQuery("SELECT * FROM Settings")
        s = query.get()
        if s:
            return s.rates
        else:
            return "Error loading rates."

    def getStartDate(self, year):

        query = db.GqlQuery("SELECT startDate FROM Settings")
        s = query.get()
        return s.startDate
        '''
        if year == "":
            query = db.GqlQuery("SELECT startDate FROM Settings")
            s = query.get()
            return s.startDate
        else:
            span = timedelta(days=1)
            sDate = datetime(int(year), 6, 1)
            # logging.info(date.weekday(sDate))
            while date.weekday(sDate) <= 4:
                # logging.info(date.weekday(sDate))
                sDate = sDate + span

            return sDate
        '''

    def getEndDate(self, year):
        query = db.GqlQuery("SELECT endDate FROM Settings")
        s = query.get()
        return s.endDate
        '''
        if year == "":
            query = db.GqlQuery("SELECT endDate FROM Settings")
            s = query.get()
            return s.endDate
        else:
            return datetime(int(year), 9, 10)
        '''

    def getSessionValue(self, request, key):
        logging.info("getting session value for " + key)
        return request.session.get(key)

    def getCookieValue(self, request, key):
        cookie = Cookies(request)
        try:
            # Read a cookie from request or pending request
            result = cookie[key]
        except KeyError:
            return ""

        logging.info('Cookie value = ' + result)
        return result

# def setCookieValue(self, name, value, expires=None):
##                """Set a cookie"""
# if value is None:
##                        value = 'deleted'
##                        expires = datetime.timedelta(minutes=-50000)
##                jar = Cookie.SimpleCookie()
##                jar[name] = value
##                jar[name]['path'] = u'/'
# if expires:
# if isinstance(expires, datetime.timedelta):
##                                expires = datetime.datetime.now() + expires
# if isinstance(expires, datetime.datetime):
##                                expires = expires.strftime('%a, %d %b %Y %H:%M:%S')
##                jar[name]['expires'] = expires
##                self.response.headers.add_header(*jar.output().split(u': ', 1))

    def checkLogin(self, request):
        logging.info("Checking login")
        username = request.request.get('username')
        password = request.request.get('password')

        logging.info("user " + username)
        logging.info("password " + password)

        query = db.GqlQuery("SELECT * FROM Renter WHERE email = :email "
                            "AND password = :pwd ",
                            email=username, pwd=password)

        user = query.get()
        if user:

            logging.info("Setting loggedIn cookie for " + username)
            # Create a CookieJar object to hold the cookies
            #cj = cookielib.CookieJar()
            # Create an opener to open pages using the http protocol and to process cookies.
            #opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

            # Cookies(request) #Optional arguments: max_age, path, domain, secure, httponly, version, comment
            cookies = request.request.cookies
            #cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
            #cookies = Cookie.SimpleCookie()

            if cookies:
                logging.info("cookie loaded")
            else:
                logging.info("no cookie")
                cookies = Cookie.SimpleCookie()
            # Expires will be calculated based on max_age. If secure is not set, it will be set to current connection status
            #self.setCookieValue("email", user.email)
            cookies['email'] = user.email  # Write a cookie to response
            #self.setCookieValue("name", user.name)
            cookies['name'] = user.name  # Write a cookie to response
            #self.setCookieValue("color", user.color)
            cookies['color'] = user.color  # Write a cookie to response

            # for morsel in new_cookie.values():
            #        self.response.headers.add_header('Set-Cookie',morsel.OutputString(None))

            # del cookies['cookiename'] #Delete a cookie from pending request and client browser

            logging.info("setting session user values")
            request.session['email'] = user.email
            request.session['name'] = user.name
            request.session['color'] = user.color

            logging.info(request.response.headers)
            return 1  # 0 = false, 1 = true
        else:
            logging.info("Not logged in")

    def isLoggedIn(self, request):
        logging.info("Checking if logged in")
        # return "test"
        # return self.getCookieValue(request, 'name')
        return self.getSessionValue(request, 'name')

    def getLoggedInEmail(self, request):
        # return self.getCookieValue(request, 'email')
        return self.getSessionValue(request, 'email')

    def getLoggedInColor(self, request):
        # return self.getCookieValue(request, 'color')
        return self.getSessionValue(request, 'color')

    def getUserByEmail(self, email):
        query = db.GqlQuery("SELECT * FROM Renter WHERE email = :email ",
                            email=email)

        return query.get()

    def getRenterById(self, id):
        #logging.info("u. id = " + id)
        query = db.GqlQuery("SELECT * FROM Renter WHERE id = :id ",
                            id=int(id))

        return query.get()

    def getRenterColor(self, email):

        user = self.getUserByEmail(email)

        if user:
            return user.color
        else:
            return ""

    def isLoggedInFamily(self, email):
        logging.info("email = " + str(email))
        user = self.getUserByEmail(email)

        if user:
            logging.info("family = " + str(user.family))
            return user.family
        else:
            return 0

    def getRentalRecord(self, renterEmail, houseName, startDate):
        query = db.GqlQuery("SELECT * FROM Rental WHERE renterEmail = :email and houseName = :house",
                            email=renterEmail,
                            house=houseName)

        return query.get()

    def getNextRenterId(self):

        return Renter.all().order('-id').get().id + 1

    def getNextRenterByCurrentEmail(self, currentemail):
        query = db.GqlQuery("SELECT * FROM Renter WHERE email = :email ",
                            email=currentemail)

        currentuser = query.get()

        if currentuser:

            if currentuser.rotation_pos:
                query2 = db.GqlQuery("SELECT * FROM Renter WHERE rotation_pos = :next_pos ",
                                     next_pos=currentuser.rotation_pos + 1)
                nextuser = query2.get()

                return nextuser
            else:
                return
        else:
            return ""

    def getRenterSelect(self):

        renters = Renter.all()

        emailSelect = ""

        for renter in renters:
            emailSelect = emailSelect + "<option value='" + renter.email + "' label='" + \
                renter.name + "'>" + renter.name + \
                " (" + renter.email + ")</option>"

        return emailSelect

    def getAllRentalsForCurrentYear(self):

        return Rental.all().filter('startDate > ', datetime(self.getYear(), 1, 1)).filter('startDate <', datetime(self.getYear(), 12, 31))

    def getRenterScheduledByEmail(self, email):
        query = db.GqlQuery("SELECT * FROM Rental WHERE renterEmail = :email ",
                            email=email)
        user = query.get()

        return user

    def logout(self, request):
        logging.info("Logging out")
        cookie = Cookies(request)
        del cookie['email']
        del cookie['name']
        del cookie['color']

    def getSaturdaySelects(self, year):
        sDate = self.getStartDate(year)
        #datetime(year, 6, 4)
        span = timedelta(days=1)

        # logging.info(date.weekday(sDate))
        while date.weekday(sDate) < 5:
            # logging.info(date.weekday(sDate))
            sDate = sDate + span

        # logging.info("--------")
        span = timedelta(days=7)
        # logging.info(sDate)
        y = year
        saturdays = ""
        while y == year:
            saturdays += sDate.strftime(
                "<option value='%m/%d/%Y'>%m/%d/%Y</option>")
            sDate = sDate + span
            # logging.info(year)
            y = sDate.year
            # logging.info(year)

        return saturdays

    def createDateHeaderRow(self, startDate, endDate):

        row = "<tr>"
        date = startDate
        week = timedelta(days=7)

        while date <= endDate:
            row += date.strftime(
                "<td class='scheduleCell' align='center' width='120px'>%-m/%-d - <br>")
            # logging.info(date)
            date += week
            row += date.strftime("%-m/%-d</td>")

        row += "</tr>"

        return row

    def rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def createScheduleRow(self, rentals, houseFilter, startDate, endDate, houseName, request, public="n"):

        date = startDate
        week = timedelta(days=7)
        # the 17 needs to be calculated....
        row = "<tr><td colspan=17 bgcolor='#B8B8B8'>" + houseName + "</td></tr>"
        row += "<tr>"
        tempRow = ""
        prevRenterName = ""
        # logging.info(houseFilter)
        # logging.info(rentals.count())
        # logging.info(date)
        doubledCell = False
        #logging.info("resetting renterRepeatCount 1")
        renterRepeatCount = 0

        while date <= endDate:

            for rental in rentals:
                if rental.startDate.month == date.month and rental.startDate.day == date.day and rental.startDate.year == date.year:
                    # logging.info(rental.renterName)
                    # lookup renter color
                    color = self.getRenterColor(rental.renterEmail)
                    #logging.info("color = " + color + " for renterEmail = " + rental.renterEmail)

                    if prevRenterName == rental.renterName:

                        #rIndex = row.rfind("colspan", 0)
                        #logging.info("Adding extra week for " + rental.renterName)
                        #logging.info("prevRenterName = " + prevRenterName)
                        #logging.info("renterName = " + rental.renterName)
                        renterRepeatCount = renterRepeatCount + 1
                        #logging.info("renter repeat count = ")
                        # logging.info(renterRepeatCount)

                        if renterRepeatCount == 2:
                            row = self.rreplace(
                                row, "colspan=2", "colspan=3", 1)

                        if renterRepeatCount == 1:
                            row = self.rreplace(
                                row, "colspan=1", "colspan=2", 1)

                        doubledCell = True
                        prevRenterName = rental.renterName
                        #logging.info("tr = " + tempRow)
                        #tempRow = "<td bgcolor='" + color + "' width='120px'>&nbsp;</td>"
                        break
                    else:
                        logging.info("Adding cell to row for " +
                                     rental.renterName + " in " + houseFilter)
                        if public == "y":
                            tempRow = "<td class='scheduleCell' colspan=1 bgcolor='" + \
                                color + "' width='120px'>&nbsp;</td>"
                        else:
                            tempRow = "<td class='scheduleCell' colspan=1 bgcolor='" + \
                                color + "' width='120px'>" + rental.renterName + "</td>"
                        doubledCell = False
                        #logging.info("resetting renterRepeatCount 2")
                        renterRepeatCount = 0
                        prevRenterName = rental.renterName
                        break
                    color = ""
                else:
                    #logging.info(date.strftime("No renter the week of %m/%d/%y for ") + rental.houseName)
                    doubledCell = False
                    #logging.info("resetting renterRepeatCount 3")
                    #renterRepeatCount = 0
            if (tempRow == "" and doubledCell == False):
                #logging.info("Adding blank cell")
                row += "<td class='scheduleCell' >&nbsp;&nbsp;&nbsp;</td>"
            else:
                #logging.info("Adding tempRow to row")
                row += tempRow

            date += week
            tempRow = ""

        row += "</tr>"

        return row

    def render(self, template_file, context, handler, login_required=True, path="", public="n"):
        #user = users.get_current_user()
        # if user_required and not user:
        #	handler.redirect(users.create_login_url(handler.request.uri))
        #context.update({'user':user, 'urls':urls})
        u = Utilities()
        logging.info("render start - " + template_file)
        loggedInUser = u.isLoggedIn(handler)
        if public == "y":
            loggedInUser = "public"
        loggedInEmail = u.getLoggedInEmail(handler)
        if loggedInUser is not None:
            logging.info("username = " + str(loggedInUser) +
                         ", email = " + str(loggedInEmail))
        else:
            loggedInUser = ""

        if (loggedInUser == "" or loggedInUser is None) and login_required:
            #path = os.path.join(os.path.dirname(__file__), os.path.join('templates', "login.html"))
            handler.redirect("/login/?p=" + path)
            return
        else:
            path = os.path.join(os.path.dirname(__file__),
                                os.path.join('templates', template_file))
            if not context:
                context = {'loggedInUser': loggedInUser,
                           'loggedInEmail': loggedInEmail}
            else:
                context['loggedInUser'] = loggedInUser
                context['loggedInEmail'] = loggedInEmail

        #logging.info("render header = ")
        # logging.info(handler.response.headers)
        logging.info("render end")
        handler.response.out.write(template.render(path, context))


#	def setCookie(self, response, name, value):
#		c = Cookie.SimpleCookie()
#		c[name] = str(base64.b64encode(value))
#		c[name]["expires"] = -1
#		headerStr = c.output()
#		regExObj = re.compile('^Set-Cookie: ')
#		response.headers.cookies.add()
#		response.headers.add_header('Set-Cookie', str(regExObj.sub('', headerStr, count=1)))
#
#	def getCookie(self, request, cookieName):
#		try:
#			logging.info(request.request.cookies)
#			return str(base64.b64decode(request.request.cookies[cookieName]))
#		except KeyError:
#			#There wasn't a Cookie called that
#			logging.info("No cookie named " + cookieName)
#			return ''
