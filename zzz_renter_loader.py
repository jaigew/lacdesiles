import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import renter

class RenterLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Renter',
                               [('id'), int,
                                ('name', str),
                                ('email', str),
                                ('password', str),
                                ('update_date', lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date())
                               ])

loaders = [RenterLoader]
