var watchPos = null;
var position = true;
var userName = null;
var socifymehidden = false;

document.addEventListener("visibilitychange", onVisibilityChange, false);

function onVisibilityChange(){
	if (socifymehidden == false) {
		socifymehidden = true;
	} else {
		document.getElementById('welcomepage').style.display = 'none';
		document.getElementById('socifymepage').style.display = 'none';
	}
	steroids.view.removeLoading();
}

$(document).ready(function() {
	steroids.view.removeLoading();
});

/*$(document).ready(function() {
	if (socifymehidden == false) {
		document.getElementById('welcomepage').style.display = 'inline-block';
		document.getElementById('socifymepage').style.display = 'none';
		document.getElementById('peoplepage').style.display = 'none';
	}
});*/


function gototwitter(linkhref) {
	var webView = new steroids.views.WebView(linkhref);
  	steroids.layers.push(webView);
  	return false;
}


function showPosition(position, data) {
	$('.btn-warning').addClass('btn-success').removeClass('btn-warning');
	document.getElementById('socifymepage').style.display = 'inline-block';
	document.getElementById('welcomepage').style.display = 'none';
	
	document.getElementById('hellouser').innerHTML = 'Hello <i>' + userName +'</i>. </br>';
	document.getElementById('notimportant').innerHTML = 'you are located at: <i>1555 West Pender St, Vancouver, BC</i></br>';
	//document.getElementById('latitude').innerHTML = 'Latitude: ' + position.coords.latitude;
	//document.getElementById('longitude').innerHTML = 'Longitude: ' + position.coords.longitude;
//		'Latitude: '          + position.coords.latitude          + '</br>' +
//		'Longitude: '         + position.coords.longitude         + '</br>' +
//		'Altitude: '          + position.coords.altitude          + '</br>' ;
//		'Accuracy: '          + position.coords.accuracy          + '</br>' +
//		'Altitude Accuracy: ' + position.coords.altitudeAccuracy  + '</br>' +
//		'Heading: '           + position.coords.heading           + '</br>' +
//		'Speed: '             + position.coords.speed             + '</br>' ;
//		'Timestamp: '         + position.timestamp                + '</br>';
}

function login() {
	//document.getElementById('login').innerHTML = 'Loading ...';
	if ($('#username').val() != '') {
		navigator.geolocation.getCurrentPosition(gps_onSuccess, gps_onError, {timeout:10000});
	}
}

function sendLogin(position) {
	$.ajax({
		type : 'GET',
		url : 'http://54.225.80.114:5000/1.0/tweets',
		data : {
  			hashtag: "fbvanatahack",
  			tw_handle: userName,
		},
        //crossDomain: true,
        //contentType: 'application/json',
        //dataType: 'json',
		beforeSend : function() {
			//document.getElementById('login').style.display = 'none';
			//$('#ajax-panel').html('<div class="loading"><img src="/icons/loading.png" alt="Loading..." height="55" width="75"/></div>');
			$('.btn-success').addClass('btn-warning').removeClass('btn-success');
		},
		success : function(data) {
			$('#ajax-panel').empty();
			//document.getElementById('login').style.display = 'initial';
			/*$(data).find('item').each(function(i) {
				$('#ajax-panel').append('<h4>' + $(this).find('tweets_no').text() + '</h4><p>' + $(this).find('link').text() + '</p>');
			});*/
			if (data.people_no >= 0) {
				showPosition(position, data);
			} else {
				alert('Oops, Invalid Twitter Account!');
				document.getElementById("username").value = "";
				//document.getElementById('login').innerHTML = "Where Am I?";
			}
		},
		error : function() {
			//document.getElementById('login').style.display = 'initial';
			//alert('error' + data);
			$('#ajax-panel').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments.</p>');
		}
	}); 
}

function gps_onSuccess(position) {
	steroids.view.removeLoading();
	position = position;
	userName = document.getElementById('username').value;
	sendLogin(position);
//	var options = { enableHighAccuracy: true };
//	watchPos = navigator.geolocation.watchPosition(watchPos_onSuccess, watchPos_onError, options);
}

function gps_onError(error) {
	alert('code: '    + error.code    + '\n' +
		'message: ' + error.message + '\n');
}

function showPeople() {
	document.getElementById('socifymepage').style.display = 'none';
	document.getElementById('welcomepage').style.display = 'none';
	document.getElementById('peoplepage').style.display = 'inline-block';
}


function socifyme() {
	$.ajax({
		type : 'GET',
		url : 'http://54.225.80.114:5000/1.0/people',
		data : {
  			tw_handle: userName,
		},
        //crossDomain: true,
        //contentType: 'application/json',
        //dataType: 'json',
		beforeSend : function() {
			//$('#ajax-panel').html('<div class="loading"><img src="/icons/loading.png" alt="Loading..." /></div>');
		},
		success : function(data) {
			//console.log(data);
			showPeople();

			//$('#peoplepage').append('<table>');
			//$('#peoplepage').append('<div style="width:90px">');
			for (var i=0; i<data.length; i++)
			{
				$('#peoplepage').append('<div style="float:left"> <img src=' + data[i].avatar_image_url + ' /></div>');
				$('#peoplepage').append('<div style="float:left; padding-left:10px"><a class="twitterlinks" href="http://twitter.com/'
									+data[i].screen+'">'+ data[i].name +'</a></br>'+ data[i].location +'</div>');
				$('#peoplepage').append('<div style="display: block; clear: both;"></div>');
				$('#peoplepage').append('</br>');
			}
			
			$( ".twitterlinks" ).click(function( event ) {
            	event.preventDefault();
            	var addressValue = $(this).attr('href');
            	gototwitter(addressValue);
        	});

			/*$(data).find('item').each(function(i) {
				$('#ajax-panel').append('<h4>' + $(this).find('location').text() + '</h4><p>' + $(this).find('url').text() + '</p>');
			});*/
		},
		error : function() {
			alert('error' + data);
			$('#ajax-panel').html('<p class="error"><strong>Oops!</strong> Try that again in a few moments.</p>');
		}
	}); 
}

/*function watchPos_onSuccess(position) {
	document.getElementById('gpsTable').innerHTML = 
		'Latitude: '          + position.coords.latitude          + '</br>' +
		'Longitude: '         + position.coords.longitude         + '</br>' +
		'Altitude: '          + position.coords.altitude          + '</br>' ;
}

function watchPos_onError(error) {
	alert('code: '    + error.code    + '\n' +
		'message: ' + error.message + '\n');
}

function gpsLocStop() {
	if (watchPos != null) {
		navigator.geolocation.clearWatch(watchPos);
		watchPos = null;
	}
}*/