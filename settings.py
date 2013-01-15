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

"""Settings for PiTunes. Put here to be easily acessable"""

################
# MPD Settings #
################

HOSTNAME = "localhost"
MPD_PORT = 6600

#######################
# Web Server Settings #
#######################

PORT = 8080 # The port for the web server to listen on
DEBUG = True # Print debug messages to terminal?

####################
# Misc Preferences #
####################
#ALLOWED_EXTENSIONS  = ["mp3","ogg","m4a","flac"] # What extensions are people allowed to upload?
UPLOAD_PATH = "uploadedfiles/"
#UPlOAD_PATH = "/var/lib/mpd/music/"
FADE_ON_PLAY_PAUSE = False # Do you want to fade the music when pausing / resuming? Works better on computers than the RPi...
ALLOW_UPLOADS = True
