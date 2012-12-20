PiTunes
=======

A Headless social music player for the Raspberry Pi based on the mpd music player daemon, written in Python (2.7).

Since it uses mpd as the backend, it supports some more advanced and less common features, including: broad format support, gapless playback, replaygain support, and more!

Requirements
------------

PiTunes has a number of dependancies that need to be installed and set up before it'll work. For details on installation and setup, see the [github project wiki][project wiki]

1.	mpd
	*	The [Music Player Daemon][mpd website] is in charge of actually playing the music. PiTunes basically just controls this...
2.	Tornado
	*	[Tornado][tornado website] is a web server for Python. This is what serves up PiTune's pages and the web-based api.
3. Python libraries:
	*	[python-mpd2][pympd github]
		*	This provides a simple client interface for mpd, so we can easily control it from python.
	*	urllib
		*	This is used to deal with decoding url encoded strings for things like search terms. It is usually installed with your python distribution.

Setup
-----

For full setup instructions, read the [guide][project wiki] in the wiki.

[project wiki]: https://github.com/rbrunt/PiTunes/wiki
[mpd website]: http://mpd.wikia.com/wiki/Music_Player_Daemon_Wiki
[tornado website]: http://www.tornadoweb.org/
[tornado github]: https://github.com/facebook/tornado
[pympd github]: https://github.com/Mic92/python-mpd2