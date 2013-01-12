#!/usr/bin/env python
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
import settings
#from mutagen import File

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
		current = client.currentsong()
		response = json.dumps({"song":{"title":current['title'],"artist":current['artist'],"album":current['album']}})
		self.write(response)
		
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, World")

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

class uploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect("/")

	def push(self):
		files = self.request.files
		for aFile in files:
			output_file = open("uploadedfiles/" + aFile["filename"], 'w')
			output_file.write(aFile['body'])
    	response = "{success:\"true\"}"
        self.write(response)



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
	(r"/upload", uploadHandler),
	(r"/(.*)", MainHandler)
], **tornadosettings)

if __name__=="__main__":
	print "Connecting to MPD..."
	client = mpd.MPDClient()
	client.timeout = 10
	client.idletimeout = None
	client.connect(settings.HOSTNAME,settings.MPD_PORT)

	print "Starting web service on port %i..." % (settings.PORT)
	application.listen(settings.PORT)
	print "Server Started. Starting tornado ioloop..."
	tornado.ioloop.IOLoop.instance().start()
