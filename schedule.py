from google.appengine.ext import db
from datetime import date

class schedule:
    rentalSchedule = []
    
    def initiateRentalSchedule(self, year):
        date = datetime.date(year, 1, 1)
        #while date.year == year:
            
        
