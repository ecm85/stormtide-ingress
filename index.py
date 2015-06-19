import os
import urllib
import jinja2
import webapp2
import json
from pytz.gae import pytz
from itertools import *
import operator
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class Portal(ndb.Model):
	Name=ndb.StringProperty()
	Level8ResonatorOwners=ndb.StringProperty(repeated=True)
	Faction=ndb.StringProperty()
	MissingResonatorCount=ndb.IntegerProperty()
	PercentEnergy=ndb.IntegerProperty()

class PortalList(ndb.Model):
	Portals=ndb.LocalStructuredProperty(Portal, repeated=True)
	UploadedDate=ndb.DateTimeProperty(auto_now_add=True)

class EnlightenedPortalCount(object):
	def __init__(self):
		self.resonatorCount = self.count = None

class PortalCounts(object):
	def __init__(self):
		self.neutralPortals = self.resistancePortals = self.enlightendPortals = None
		self.enlightenedPortalCounts = None

class Deployer(object):
	def __init__(self):
		self.Name = self.DeployedCount = None

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())

class IngressUploadFarmData(webapp2.RequestHandler):
	def post(self):
		self.response.headers.add_header('Access-Control-Allow-Origin', "https://www.ingress.com")
		self.response.headers['Content-Type'] = 'application/json'
		
		portalList = PortalList.query().get()
		if portalList is not None:
			portalList.key.delete()
		
		newPortals = json.loads(self.request.body)
		portalList = PortalList()
		portalList.portals = []
		for newPortal in newPortals:
			level8ResonatorOwners = [resonator[0] for resonator in newPortal[15] if resonator[1] == 8]
			portalList.Portals.append(Portal(
				Name=newPortal[8],
				Level8ResonatorOwners=level8ResonatorOwners,
				Faction=newPortal[1],
				MissingResonatorCount=8-len(level8ResonatorOwners),
				PercentEnergy=newPortal[5]
			))
		portalList.put()

	def options(self):
		self.response.headers['Access-Control-Allow-Origin'] = 'https://www.ingress.com'
		self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
		self.response.headers['Access-Control-Allow-Methods'] = 'POST'

def utc_to_local(utc_dt):
    local_tz = pytz.timezone('US/Central')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

class IngressIntel(webapp2.RequestHandler):
	def get(self):
		portalList = PortalList.query().get()
		portals = portalList.Portals
		portalCounts = PortalCounts()

		neutralPortals = [portal for portal in portals if portal.Faction == 'N']
		resistancePortals = [portal for portal in portals if portal.Faction == 'R']
		enlightenedPortals = [portal for portal in portals if portal.Faction == 'E']

		portalCounts.neutralPortals = len(neutralPortals)
		portalCounts.resistancePortals = len(resistancePortals)
		portalCounts.enlightenedPortals = len(enlightenedPortals)

		resonatorCount = lambda portal: len(portal.Level8ResonatorOwners)
		sortedEnglightenedPortals = sorted(enlightenedPortals, key=resonatorCount)
		enlightenedPortalCounts = []
		for key, group in groupby(sortedEnglightenedPortals, key=resonatorCount):
			enlightenedPortalCount = EnlightenedPortalCount()
			enlightenedPortalCount.resonatorCount = key
			enlightenedPortalCount.count = len(list(group))
			enlightenedPortalCounts.append(enlightenedPortalCount)
		portalCounts.enlightenedPortalCounts = enlightenedPortalCounts

		IGN = self.request.get('IGN')

		template = JINJA_ENVIRONMENT.get_template('ingress/ingressReport.html')
		portalsForIGN = sorted([portal for portal in enlightenedPortals if IGN not in portal.Level8ResonatorOwners and portal.MissingResonatorCount > 0], key=lambda portal: portal.MissingResonatorCount)
		neutralPortalsForIGN = sorted(neutralPortals, key=lambda portal: portal.Name)
		resistancePortalsForIGN = sorted(resistancePortals, key=lambda portal: portal.Name)
		deployedPortalCountForIGN = len([portal for portal in enlightenedPortals if IGN in portal.Level8ResonatorOwners])

		portalsSortedByEnergy = sorted(portals, key=lambda portal: portal.PercentEnergy)
		farmEnergies = [portal.PercentEnergy for portal in portals]
		farmEnergy = round(float(sum(farmEnergies))/len(farmEnergies), 2)

		currentDeployerNames = (list(set([deployer for portal in enlightenedPortals for deployer in portal.Level8ResonatorOwners])))
		currentDeployers = []
		for currentDeployerName in currentDeployerNames:
			deployer = Deployer()
			deployer.Name = currentDeployerName
			deployer.DeployedCount = len([portal for portal in enlightenedPortals if currentDeployerName in portal.Level8ResonatorOwners])
			currentDeployers.append(deployer)

		self.response.write(template.render(
			farmEnergy = farmEnergy,
			portalCounts = portalCounts,
			portalsSortedByEnergy = portalsSortedByEnergy,
			dateUpdated = utc_to_local(portalList.UploadedDate).strftime('%a %b %d, %Y %I:%M %p'),
			IGN = IGN,
			portalsForIGN = portalsForIGN,
			neutralPortalsForIGN = neutralPortalsForIGN,
			resistancePortalsForIGN = resistancePortalsForIGN,
			deployedPortalCountForIGN = deployedPortalCountForIGN,
			currentDeployers = sorted(currentDeployers, key=lambda currentDeployer: -currentDeployer.DeployedCount)
		))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/ingress/intel', IngressIntel),
	('/ingress/uploadFarmData', IngressUploadFarmData)
], debug=True)