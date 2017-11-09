import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import data_models

class HouseLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'House',
                               [('id'), int,
                                ('name', str),
                                ('bedrooms'), int,
                                ('bathrooms'), int,
                                ('us_rental'), float,
                                ('can_rental'), float,
                                ('desc', str),
                                ('picture_link', str),
                                ('gallery_link', str),
                                ('update_date', lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date())
                               ])

loaders = [HouseLoader]
