/* Preparation and displaying the map */

$(document).ready(function () {
    resize_map();
    resize_listing_panel();
    //initMap();
});

window.onresize = function(event) {
    //initialize();
    resize_map();
    resize_listing_panel();
};

function resize_map() {
    var new_height = $(window).height()-60;
    document.getElementById("map-canvas-full").style["min-height"] = new_height+"px";
}

function resize_listing_panel() {
    var new_height = $(window).height()-140;
    document.getElementById("listing-overlay").style["height"] = new_height+"px";       // Resizing the panel
    //document.getElementById("filter-overlay").style["height"] = new_height-100+"px";       // Resizing the panel
    //var new_offset = document.getElementById("listing-overlay").offsetWidth+25;
    //document.getElementById("listing-overlay-").style["left"] = new_offset+"px";   // Moving the close button
}


var updateTimer;
var map;
var oms;
var markers = [];
var infoWindow = new google.maps.InfoWindow();

var clubNight = true;
var festival = true;
var liveMusic = true;

function setMapAll(map) {   // depreciated
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function initialize() {


    // Using a nice map color scheme from https://snazzymaps.com/
    myStyle = [{"featureType":"landscape.man_made","elementType":"geometry.fill","stylers":[{"lightness":"-5"}]},{"featureType":"landscape.man_made","elementType":"labels.text.fill","stylers":[{"saturation":"21"}]},{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"saturation":"1"},{"color":"#eae2d3"},{"lightness":"20"}]},{"featureType":"road.highway","elementType":"labels.icon","stylers":[{"saturation":"39"},{"lightness":"7"},{"gamma":"1.06"},{"visibility":"on"},{"hue":"#00b8ff"},{"weight":"1.44"}]},{"featureType":"road.arterial","elementType":"geometry.stroke","stylers":[{"visibility":"on"},{"lightness":"100"},{"weight":"1.16"},{"color":"#e0e0e0"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"saturation":"-16"},{"lightness":"28"},{"gamma":"0.87"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"saturation":"-75"},{"lightness":"-15"},{"gamma":"1.35"},{"weight":"1.45"},{"hue":"#00dcff"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#626262"}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"saturation":"19"},{"weight":"1.84"}]}];
    lightDream = [{"featureType":"landscape","stylers":[{"hue":"#FFBB00"},{"saturation":43.400000000000006},{"lightness":37.599999999999994},{"gamma":1}]},{"featureType":"road.highway","stylers":[{"hue":"#FFC200"},{"saturation":-61.8},{"lightness":45.599999999999994},{"gamma":1}]},{"featureType":"road.arterial","stylers":[{"hue":"#FF0300"},{"saturation":-100},{"lightness":51.19999999999999},{"gamma":1}]},{"featureType":"road.local","stylers":[{"hue":"#FF0300"},{"saturation":-100},{"lightness":52},{"gamma":1}]},{"featureType":"water","stylers":[{"hue":"#0078FF"},{"saturation":-13.200000000000003},{"lightness":2.4000000000000057},{"gamma":1}]},{"featureType":"poi","stylers":[{"hue":"#00FF6A"},{"saturation":-1.0989010989011234},{"lightness":11.200000000000017},{"gamma":1}]}]
    customStyle = [{"featureType":"administrative","elementType":"all","stylers":[{"visibility":"on"},{"lightness":33}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2e5d4"}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#c5dac6"}]},{"featureType":"poi.park","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":20}]},{"featureType":"road","elementType":"all","stylers":[{"lightness":20}]},{"featureType":"road.highway","elementType":"geometry","stylers":[{"color":"#c5c6c6"}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#e4d7c6"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#fbfaf7"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"},{"color":"#acbcc9"}]}]


    // Setup map
    var mapOptions = {
      center: { lat: 51.45451, lng: -2.58791},
      zoom: 12,
      disableDefaultUI: true,
      streetViewControl: true,
      streetViewControlOptions: {
        position: google.maps.ControlPosition.BOTTOM_CENTER
      },
      zoomControl: true,
      zoomControlOptions: {
        position: google.maps.ControlPosition.RIGHT_CENTER
      },
      styles: myStyle
    };
    // map and OMS

    map = new google.maps.Map(document.getElementById('map-canvas-full'),
        mapOptions);
    oms = new OverlappingMarkerSpiderfier(map ,{
        legWeight: 2
    });



    // --- SEARCH BOX --- //
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {

          if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
          } else {
            bounds.extend(place.geometry.location);
          }
        });
      map.fitBounds(bounds);
    });


    // Add listeners
    oms.addListener('click', function(marker, event) {
      if (!infoWindow) infoWindow
      infoWindow.setContent(markerData[marker.index][4]);
      infoWindow.open(map, marker);
      // Highlight corresponding listing box
      highlightListing(marker.id);
    });
    oms.addListener('spiderfy', function(markers) {
        if (infoWindow) infoWindow.close();
        else infoWindow = new google.maps.InfoWindow();
        for(var i = 0; i < markers.length; i++) {
            markers[i].icon = markerData[markers[i].index][6];
        }
    });
    oms.addListener('unspiderfy', function(markers) {
        for(var i = 0; i < markers.length; i++) {
            markers[i].icon = markerData[markers[i].index][7];
            //markers[i].icon = marker_path;
        }
    });
    oms.addListener('mouseover', function(marker) {
        oms.createEvent('spiderfy');
    });
    google.maps.event.addListener(map, 'click', function() {
        if(infoWindow) infoWindow.close();
        closeClickHandler()
    });
    google.maps.event.addListener(map, 'bounds_changed', function() {
        clearTimeout(updateTimer);
        updateTimer = setTimeout(updateMarkers, 300);
        oms.unspiderfy();

    });
    // Might not need this
    google.maps.event.addListenerOnce(map,'idle', function(){
        //updateMarkers();
        closeClickHandler()
    });
    // Stop windows reappearing when they are closed and the viewpoint changes
    google.maps.event.addListener(infoWindow,'closeclick',function(){
       closeClickHandler()
    });
    function closeClickHandler() {
        dehighlightListing();
        infoWindow = new google.maps.InfoWindow();
        google.maps.event.addListener(infoWindow,'closeclick',function(){
           closeClickHandler()
        });
    }



  }
  google.maps.event.addDomListener(window, 'load', initialize);
