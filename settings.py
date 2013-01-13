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