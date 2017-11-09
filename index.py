import os
import cgi

from handlers import MainHandler, CottagesHandler, FamilyHandler, LocalHandler, RentalHandler, ContactHandler, MapHandler, LoginHandler, ScheduleHandler, EmailNextHandler, RecreationHandler
from data_loader import DataHandler, ResetUserDataHandler, ClearRentalHandler, CreateSettingsHandler
from adminHandler import AddRentalHandler, EditRentalHandler, AdminIndexHandler, AddRenterHandler, EditRenterHandler, EditPageHandler, EditSettingsHandler
from page_reset import ResetPageDataHandler
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '123456',
}

application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/cottages/', CottagesHandler),
    ('/local/', LocalHandler),
    ('/family/', FamilyHandler),
    ('/rental/', RentalHandler),
    ('/rental/schedule/', ScheduleHandler),
    ('/rental/emailnext/', EmailNextHandler),
    ('/contact/', ContactHandler),
    ('/map/', MapHandler),
    ('/recreation/', RecreationHandler),
    ('/cottages/([-\w]+)/', CottagesHandler),
    ('/data/', DataHandler),
    ('/admin/resetUsers/', ResetUserDataHandler),
    ('/admin/clearRentals/', ClearRentalHandler),
    ('/admin/editRentals/', EditRentalHandler),
    ('/admin/addRentals/', AddRentalHandler),
    ('/admin/addRenters/', AddRenterHandler),
    ('/admin/editRenter/', EditRenterHandler),
    ('/admin/editPage/', EditPageHandler),
    ('/admin/editSettings/', EditSettingsHandler),
    ('/admin/resetPages/', ResetPageDataHandler),
    ('/admin/createSettings/', CreateSettingsHandler),
    ('/admin/', AdminIndexHandler),
    ('/login/', LoginHandler)
    
    ],config=config, debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
  
  
  

