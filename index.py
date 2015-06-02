import os
import urllib

import jinja2
import webapp2
import json

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class Portal(ndb.Model):
	Name=ndb.StringProperty();
	Level8ResonatorOwners=ndb.StringProperty(repeated=True)
	@classmethod
	def getPortals(cls):
		return cls.query();

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())

class IngressUploadFarmData(webapp2.RequestHandler):
	def post(self):
		self.response.headers.add_header('Access-Control-Allow-Origin', "https://www.ingress.com")
		self.response.headers['Content-Type'] = 'application/json'
		portals = Portal.getPortals().fetch()
		for portal in portals:
			portal.key.delete()
		newPortals = json.loads(self.request.body)
		for newPortal in newPortals:
			Portal(Name=newPortal[8], Level8ResonatorOwners=[resonator[0] for resonator in newPortal[14] if resonator[1] == 8]).put()

		#todo: parse portals and stick them in db
		#PortalList(List=self.request.body).put()

	def options(self):
		self.response.headers['Access-Control-Allow-Origin'] = 'https://www.ingress.com'
		self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST'

class IngressIntel(webapp2.RequestHandler):
	def get(self):
		portals = Portal.getPortals().fetch();
		for portal in portals:
			self.response.write("<div>" + portal.Name)
			self.response.write("<ul>")
			for owner in portal.Level8ResonatorOwners:
				self.response.write("<li>" + owner + "</li>")
			self.response.write("</ul></div>")

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/ingress/intel', IngressIntel),
	('/ingress/uploadFarmData', IngressUploadFarmData)
], debug=True)