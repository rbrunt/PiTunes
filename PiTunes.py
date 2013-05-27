#!/usr/bin/env python
#########################################################################
#	This file is part of PiTunes.
#	
#	PiTunes is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	PiTunes is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with PiTunes.  If not, see <http://www.gnu.org/licenses/>.
#########################################################################
"""
PiTunes
=======

A headless social media player for the RaspberryPi. It provides a web control interface and web-based api for mpd (the backend that plays the music).
"""

from __future__ import division
import mpd
import time
import tornado.ioloop
import tornado.web
import json
import urllib2 as urllib
import os
import tornado.template
import uuid
import settings # Local settings file

def connectToClient(host=settings.HOSTNAME,port=settings.MPD_PORT):
	client.connect(host,port)

def fadeout(timeout=0.3):
	"""Fades out the music, then pauses it. Much nicer sounding than an abrupt stop...

	Parameters
	----------
	timeout: digit
		Length (in seconds) of fadeout. Defaults to 0.3. If this is set too long, you may be able to hear the individual changes in volume."""
	if (timeout != 0 or timeout != 0.0) and settings.FADE_ON_PLAY_PAUSE:
		startvol = int(client.status()['volume'])
		for i in xrange(startvol+1):
			client.setvol(startvol-i)
			if settings.DEBUG: print "setting volume to", startvol-i
			time.sleep(timeout/startvol)
		client.pause()
		client.setvol(startvol)
	else:
		client.pause()
	if settings.DEBUG: print "paused"

def fadein(timeout=0.4):
	"""Fades in the music, restoring it to volume that it was at when it was paused.

	Parameters
	----------
	timeout: digit
		Length (in seconds) of fadeout. Defaults to 0.3. If this is set too long, you may be able to hear the individual changes in volume."""
	if (timeout != 0 or timeout != 0.0) and settings.FADE_ON_PLAY_PAUSE:
		endvol = int(client.status()['volume'])
		client.play()
		for i in xrange(endvol+1):
			client.setvol(i)
			if settings.DEBUG: print "setting volume to", i
			time.sleep(timeout/endvol)
	else:
		client.play()
	if settings.DEBUG: print "playing"

def search(term,tag="any"):
	"""Performs a serch of the database of the given search term for the given tag

	Parameters
	----------
	term: string
		The search term (url encoded) to search the database for

	tag: string
		The tag to search. Valid tags: any, artist, album, title, track, name, genre, date, performer, disc"""
	searchterm = urllib.unquote(term)
	results = client.search(tag,searchterm)
	print "Searching", tag, "for:", searchterm
	#print "term: ", term, "tag: ", tag,"\n"
	response = {
		"songs":[],
		"albums":[],
		"artists":[]
	}
	if tag=="album":
		for song in results:
	#		print song	
			if song["album"] not in response["albums"]:
				response["albums"].append(song["album"])
	
	return response

def getalbumart():
#	file = File("/media/Win7/Users/Richard/Music/%s" % client.currentsong()['file'])
#	print file
#	artwork = file.tags['APIC:'].data
#	with open('artwork.jpg','wb') as img:
#		img.write(artwork)
	return

class now_playing(tornado.web.RequestHandler):
	def get(self):
		try:
			current = client.currentsong()
		except:
			if settings.DEBUG: print "Connection to MPD lost, trying to reconnect..."
			connectToClient()
			current = client.currentsong()
		response = json.dumps({"song":{"title":current['title'],"artist":current['artist'],"album":current['album'],"length":current["time"]}})
		self.write(response)
		
class get_volume(tornado.web.RequestHandler):
	def get(self):
		response = json.dumps({"player":{"volume":client.status()['volume']}})
		self.write(response)

class player_status(tornado.web.RequestHandler):
	def get(self):
		response = json.JSONEncoder().encode(client.status())
		self.write(response)

class set_volume(tornado.web.RequestHandler):
	def get(self,value):
		client.setvol(value)

class nexthandler(tornado.web.RequestHandler):
	def get(self):
		client.next()

class prevhandler(tornado.web.RequestHandler):
	def get(self):
		client.previous()

class seekhandler(tornado.web.RequestHandler):
	def get(self,position):
		pass

class searchhandler(tornado.web.RequestHandler):
	def get(self,term,tag):
		self.write(json.JSONEncoder().encode(search(term,"album")))

class playpause(tornado.web.RequestHandler):
	def get(self):
		status = client.status()['state']
		if status == "pause":
			fadein()
		elif status == "stop":
			fadein()
		elif status == "play":
			fadeout()

class UploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect("/")
	def post(self):
		if settings.ALLOW_UPLOADS:
				response = {"success":False} # initalise the response dict (turned into JSON later)

				if settings.DEBUG: print "Receiving Upload..."
				data = self.request.body
				if not data:
					self.write("Payload expected.")
					self.set_status(500)
					return
				try:
					output_file = open(settings.UPLOAD_PATH + urllib.unquote(self.request.headers.get("X-File-Name")), 'w')
					output_file.write(data)
					output_file.close()
					if settings.DEBUG: print "%s successfully uploaded" % (urllib.unquote(self.request.headers.get("X-File-Name")))
				except:
					if settings.DEBUG: print "there was a problem saving the file"
					response["error"] = "There was an error saving the file to disk"

				if "error" in response:
					response["success"] = False
				else:
					response["success"] = True
				self.write(json.JSONEncoder().encode(response))
		else:
			self.write("Uploads have been disabled. Click <a href=\"/\">here</a> to go back home");

class MainHandler(tornado.web.RequestHandler):

	def initialize(self):
		self.loader = tornado.template.Loader(os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates"))

	def get(self):
		self.write(self.loader.load("index.html").generate())


tornadosettings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

# Setting up what requests go to which handlers...
application = tornado.web.Application(
[
	(r"/api/now_playing",now_playing),
	(r"/api/get_volume",get_volume),
	(r"/api/set_volume/([0-9]{1,3})",set_volume),
	(r"/", MainHandler),
	(r"/api/status", player_status),
	(r"/api/playpause",playpause),
	(r"/api/next", nexthandler),
	(r"/api/previous", prevhandler),
	(r"/api/search/(.*)(/[a-z]{1,6})?", searchhandler),
#	(r"/api/seek/([0-9]{1,3})",seekhandler),
	(r"/upload", UploadHandler),
	(r"/(.*)", MainHandler)
], **tornadosettings)

if __name__=="__main__":
	print "Connecting to MPD..."
	client = mpd.MPDClient()
	client.timeout = 10
	client.idletimeout = None
	connectToClient()

	print "Starting web service on port %i..." % (settings.PORT)
	application.listen(settings.PORT)
	print "Server Started. Starting tornado ioloop..."
	tornado.ioloop.IOLoop.instance().start()
