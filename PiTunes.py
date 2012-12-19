from __future__ import division
import mpd
import time
import tornado.ioloop
import tornado.web
import json
import urllib
import os
import tornado.template
#from mutagen import File

client = mpd.MPDClient()
client.timeout = 10
client.ideltimeout = None
client.connect("localhost",6600)

def fadeout(timer=0.3):
	if timer != 0 or timer != 0.0:
		startvol = int(client.status()['volume'])
		for i in xrange(startvol-1):
			client.setvol(startvol-i)
			time.sleep(timer/startvol)
		client.pause()
		client.setvol(startvol)
	else:
		client.pause()
def fadein(timer=0.4):
	if timer != 0 or timer != 0.0:
		endvol = int(client.status()['volume'])
		client.play()
		for i in xrange(endvol):
			client.setvol(i)
			time.sleep(timer/endvol)
	else:
		client.play()

def search(term,tag="any"):
	searchterm = urllib.unquote(term)
	results = client.search(tag,searchterm)
	print term
	print searchterm
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

class MainHandler(tornado.web.RequestHandler):

	def initialize(self):
		self.loader = tornado.template.Loader(os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates"))

	def get(self):
		self.write(self.loader.load("index.html").generate())

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
	(r"/(.*)", MainHandler)
#	(r"/api/seek/([0-9]{1,3})",seekhandler)
])







if __name__=="__main__":
	application.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
	while True:
		print "Now Playing: \"%s\" from the album \"%s\" by \"%s\"." % (client.currentsong()['title'], client.currentsong()['album'], client.currentsong()['artist'])

		input = raw_input("command: ")
		if input == "pause":
			print "pausing..."
			fadeout(0.3)
		elif input == "play":
			print "playing..."
			fadein(0.3)
		elif input == "next":
			print "next track..."
			client.next()
		elif input == "art":
			getalbumart()
		elif input=="q":
			client.disconnect()
			exit(0)

