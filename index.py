import os
import urllib
import jinja2
import webapp2
import json
from pytz.gae import pytz
from itertools import *
import operator
from google.appengine.ext import ndb
import ingress
import dsgame

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/ingress/intel', ingress.IngressIntel),
	('/ingress/uploadFarmData', ingress.IngressUploadFarmData),
	('/dsgame', dsgame.DSGame)
], debug=True)