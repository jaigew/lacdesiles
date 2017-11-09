import os
import logging
from datetime import datetime
from data_models import House, Renter, Rental, Page

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
    
class ResetPageDataHandler(webapp.RequestHandler):
        
    def createPage(self, id, title, body):
        p = Page()
        p.id = id
        p.title = title
        p.body = str(body)
        p.put()
        id = id + 1
        return id
        
    def get(self):
        logging.log(logging.DEBUG, "Resetting Users")
        self.response.out.write("Resetting Pages<br>")
        pages = Page.all()        
        db.delete(pages)
        
        #for renter in renters:
        #    renter.delete()

        self.response.out.write("Saving Pages<br>")
        id = 1
        
        hometext = "Welcome! Bienvenue!<br><br>Lac des Iles is a special place to relax and recreate, especially in summer and fall. Summer brings plenty of sunshine, swimming, canoeing, and family feasts. Fall is very quiet, with magnificent foliage on the far hills across the lake. The New York Times describes Lac des Iles as the most beautiful lake in the Laurentian region. The lake itself is about five square miles, with approximately a dozen islands, nearly all of which are undeveloped and permanently protected as habitat for wildlife.<br><br>Motts have been coming to Lac des Iles for five generations. Times have changed over the years, with cottages springing up around the lake, but it's still a relatively natural and remote location. It's a perfect place to leave the city and work life behind.<br><br>This website provides details on each of the cottages, pictures, information on the local area and nearby activities, maps, an updated schedule, policies, rates, and other relevant information for anyone using the cottages.<br><br>For family, this site also contains information on the family council and policies, rotation, budget, and maintenance information. You can find a great family tree as well as a photo gallery. Please send in your family pictures to add to the site.<br><br>Let us know if you have any suggestions to improve this site, and enjoy the lake!"



        
        id = self.createPage(id, 'Lac Des Iles: Home', hometext)
        id = self.createPage(id, 'Lac Des Iles: Main House', '')
        id = self.createPage(id, 'Lac Des Iles: Bose House', '')
        id = self.createPage(id, 'Lac Des Iles: Mink Point', '')
        id = self.createPage(id, 'Lac Des Iles: The Island', '')
        id = self.createPage(id, 'Lac Des Iles: Contact', '')
        id = self.createPage(id, 'Lac Des Iles: Rental Schedule', '')


