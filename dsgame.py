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
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class DSGame(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('dsgame/DSGame.html')
		#This code used to verify the serer got stuff pre-actual-DB
		#gameName = self.request.get('gameName')
		#self.response.write(template.render(gameName = gameName))
		currentDateTime = utc_to_local(datetime.datetime.now())
		currentDateString = currentDateTime.strftime('%Y-%m-%d')
		self.response.write(template.render(currentDate = currentDateString))
		
		#TODO: Create a game when requested, return all current games
		#TODO: Full 'edit' and 'historical' workflows
		#self.response.write(template.render())

def utc_to_local(utc_dt):
	local_tz = pytz.timezone('US/Central')
	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
	return local_tz.normalize(local_dt)