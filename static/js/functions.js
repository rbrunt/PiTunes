/*
	Copyright 2013, Richard Brunt

	This file is part of PiTunes.
	
	PiTunes is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	PiTunes is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with PiTunes.  If not, see <http://www.gnu.org/licenses/>.
*/

$(document).ready(function(){
	getstatus();
	//$('#shufflebtn').tooltip({placement:"bottom"})
	//$('#repeatbtn').tooltip({placement:"bottom"})
	$('#uploadbtn').tooltip({title: "Upload songs to your RaspberryPi and add them to the library", placement:"bottom"})
})

function ajaxRequest(url, callbackfunction, param1){ //param1 is optional, callbackfunction is not though an empty function is an ok parameter
	
	if (window.XMLHttpRequest){// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}else{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function(){
		
		if (xmlhttp.readyState==4 && xmlhttp.status==200){
			callbackfunction(param1);
			}
		}

		xmlhttp.open("GET",url,true); 
		xmlhttp.send();
	}

function add_li(list, text) {
	var list = document.getElementById(list);
	var li = document.createElement("li");
	li.innerHTML = text;
	list.appendChild(li);
}

function load_list(list, list_array) {
	for (var i = 0; i < list_array.length; i++) {
		add_li (list, list_array[i]);
	}
} 

function getSearchResults(){
	var searchterm = encodeURIComponent(document.getElementById('target').value);
	if (searchterm == "") {
		document.getElementById("resultlist").innerHTML="Type a search term";
	} else {
		var url='/api/search/'+searchterm;
		function callbackfunction(){
			document.getElementById("resultlist").innerHTML="";
			obj = JSON.parse(xmlhttp.responseText);
			load_list("resultlist",obj.albums);
			if (document.getElementById("resultlist").innerHTML=="") {
				document.getElementById("resultlist").innerHTML="No Results!";
			}
		}
		ajaxRequest(url, callbackfunction);
	}
}

function playPause(){
	ajaxRequest("api/playpause",getstatus);
}

function doupdate(status){
	if (status.state=="play"){
		$("#playpausebtn i").attr("class","icon-pause");
	} else {
		$("#playpausebtn i").attr("class","icon-play");
	}
}

function getstatus(){

	function callbackfunction(){
		responseobject = JSON.parse(xmlhttp.responseText);
		console.log("Status:",responseobject);
		doupdate(responseobject);
		getNowPlaying();
	}
	ajaxRequest("api/status",callbackfunction);
}

function updatenowplaying(songobj){
	nowplaying = songobj.song.artist + " - " + songobj.song.title;
	$("#nowplaying").html(nowplaying);
}

function getNowPlaying(){

	function callbackfunction(){
		responseobject = JSON.parse(xmlhttp.responseText);
		console.log(responseobject);
		updatenowplaying(responseobject);
	}
	ajaxRequest("api/now_playing",callbackfunction);

}

function nextsong() {
	ajaxRequest("api/next",getstatus);
}
function prevsong() {
	ajaxRequest("api/previous",getstatus);
}

var Player = {
	currstatus: {
		state: "play",
		volume: "0",
		random: "0",
		repeat: "0",
		position: "0"
	} ,
	nowplaying: {
		title: "",
		artist: "",
		album:"",
		length:0,
		id:0
	},

	updateAll: function(){
		this.updateStatus();
		//this.updateNowPlaying(); // Bug: only updates one: change API to return all data at once (will also reduce number of requests necassary).
	},
	
	doUpdateStatus: function(status){
		this.currstatus.state=status.state;
		this.currstatus.volume=status.volume;
		this.currstatus.random=status.random;
		this.currstatus.repeat=status.repeat;
		this.nowplaying.id=status.songid;
	},

	updateStatus: function(){
		function callbackfunction(){
			responseobject = JSON.parse(xmlhttp.responseText);
			Player.doUpdateStatus(responseobject);
		}
		ajaxRequest("api/status",callbackfunction);
	},

	doUpdateNowPlaying: function(songobj){
		this.nowplaying.title=songobj.song.title;
		this.nowplaying.artist=songobj.song.artist;
		this.nowplaying.album=songobj.song.album;
	},

	updateNowPlaying: function(){
		function callbackfunction(){
			responseobject = JSON.parse(xmlhttp.responseText);
			Player.doUpdateNowPlaying(responseobject);
		}
		ajaxRequest("api/now_playing",callbackfunction);
	}
}