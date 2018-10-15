/*
    interactivity.js
    Authors: Aman Panda, Abha Laddha, Noah Brackenbury
    2/16/17
 */

// Global Variables
var selectedYear = "1990";
var curRadio = "total";
var mapInfo;

// Function that deals with user changing the slider value.
// Triggers a mapUpdate()
function sliderUpdate() {
  selectedYear = document.getElementById("yearSlider").value;
	document.getElementById("outputSlider").value = selectedYear;
  mapUpdate();
}

// Function that deals with user changing the selected radio button
// Triggers a mapUpdate()
function radioUpdate(id) {
  if(curRadio != id) {
    curRadio = id;
    mapUpdate()
  }
}

// Function that deals with a page redirect to country.html, with a 
// user inputted countryName
function searchRedirect(element) {
  if(event.keyCode == 13) {
    var countryName = element.value;
    var country_url = country_url_temp.replace('NOTACOUNTRY', countryName);
    window.location = country_url;
  }
}

// Redirect to frontpage.html
function homeRedirect() {
  window.location = '/'
}

// Function that rerenders geochart map based on selected year and radio button
// by user.
function mapUpdate() {
  var url = '/y' + selectedYear + '/' + curRadio;
  xmlHttpRequest = new XMLHttpRequest();
  xmlHttpRequest.open('get', url);

  xmlHttpRequest.onreadystatechange = function() {
    if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
      mapUpdateCallback(JSON.parse(xmlHttpRequest.response));
    }
  }

  xmlHttpRequest.send(null);
}

// Callback function for mapUpdate()
function mapUpdateCallback(jsonResponse) {
  mapInfo = jsonResponse['rows'];
  mapInfo.unshift(["Country", "Value"]);
  drawRegionsMap();
  //console.log(mapInfo);
}

// Function that gets data for an inputted country from database.
// Calls helper function capitalizeString() to make sure string is
// of appropriate case, and has a callback function.
function searchCountry(countryString) {
  modifiedCountry = capitalizeString(countryString)
  var url = '/' + modifiedCountry;
  xmlHttpRequest = new XMLHttpRequest();
  xmlHttpRequest.open('get', url);

  xmlHttpRequest.onreadystatechange = function() {
    if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
      searchCountryCallback(JSON.parse(xmlHttpRequest.response));
    }
  }

  xmlHttpRequest.send(null) 
}

// Callback function for searchCountry()
function searchCountryCallback(jsonResponse) {
  var countryInfo = jsonResponse['rows'];
  if(countryInfo.length != 0) {
    // console.log("here");
    var countryStr = '';
    countryStr += '<table><tr><th>Emissions Data Type</th>';
    for(var i = 1990; i <= 2008; i++) {
      countryStr += '<th>' + i.toString() + '</th>';
    }
    countryStr += '</tr>';
    for(i = 0; i < 3; i++) {
      countryStr += '<tr><td>';
      if (i == 0) {
        countryStr += 'Total (Kt of CO<sub>2</sub>)';
      } else if (i == 1) {
        countryStr += 'Per Capita (Metric Tons)';
      } else {
        countryStr += 'Per Unit of GDP (kg/$1,000)';
      }
      countryStr += '</td>';
      for(var j = 3; j < countryInfo[0].length; j++) {
        countryStr += '<td>' + countryInfo[i][j].toString() + '</td>';
      }
      countryStr += '</tr>';
    }
    countryStr += '</table>';
  } else {
    countryStr = "Sorry! We couldn't find any data for this country. Please try again."
  }
  // console.log(countryStr);
  document.getElementById("tableDiv").innerHTML = countryStr;
}

// Function to take a string a capitalize the first letter of each
// word in the string.
function capitalizeString(str) {
  var lowerCase = str.toLowerCase();
  return lowerCase.replace(/(^| )(\w)/g, function(modified) {
    return modified.toUpperCase();
  });
}




