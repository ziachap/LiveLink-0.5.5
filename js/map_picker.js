/**
 * Created by Sir Zia on 30/07/2015.
 */

    <!-- Based on the reverse geocoding example for gmaps.js -->

    var geocoder = new google.maps.Geocoder();
    var map, marker;
    function geocodePosition(pos) {
      geocoder.geocode({
        latLng: pos
      }, function(responses) {
        if (responses && responses.length > 0) {
          updateMarkerAddress(responses[0].formatted_address);
        } else {
          updateMarkerAddress('?');
        }
      });
    }

    function updateMarkerStatus(str) {
      //document.getElementById('markerStatus').innerHTML = str;
    }

    function updateMarkerPosition(latLng) {
      document.getElementById("long_form").value = latLng.lng();
      document.getElementById("lat_form").value = latLng.lat();
    }

    function updateMarkerAddress(str) {
      document.getElementById('address').innerHTML = str;
      document.getElementById('address_form').value = str;
    }

    function initialize() {
      var latLng = new google.maps.LatLng(51.45451, -2.58791);
      map = new google.maps.Map(document.getElementById('mapCanvas'), {
        zoom: 14,
        center: latLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true
      });

      marker = new google.maps.Marker({
        position: latLng,
        title: 'Point A',
        map: map,
        draggable: true
      });

      // Update current position info.
      updateMarkerPosition(latLng);
      geocodePosition(latLng);

      // Add dragging event listeners.
      google.maps.event.addListener(marker, 'dragstart', function() {
        updateMarkerAddress('Dragging...');
      });

      google.maps.event.addListener(marker, 'drag', function() {
        updateMarkerStatus('Dragging...');
        updateMarkerPosition(marker.getPosition());
      });

      google.maps.event.addListener(marker, 'dragend', function() {
        updateMarkerStatus('Drag ended');
        geocodePosition(marker.getPosition());
      });


    }

    // Geolocate once loaded
    window.onload = postLoad;
    function postLoad() {
        prepareGeolocation();
        doGeolocation();
    };

    // Onload handler to fire off the app.
    google.maps.event.addDomListener(window, 'load', initialize);

    ///////////////// GEOLOCATION ///////////////////

      function doGeolocation() {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(positionSuccess, positionError);
        } else {
          positionError(-1);
        }
      }

      function positionError(err) {
        var msg;
        switch(err.code) {
          case err.UNKNOWN_ERROR:
            msg = "Unable to find your location";
            break;
          case err.PERMISSION_DENINED:
            msg = "Permission denied in finding your location";
            break;
          case err.POSITION_UNAVAILABLE:
            msg = "Your location is currently unknown";
            break;
          case err.BREAK:
            msg = "Attempt to find location took too long";
            break;
          default:
            msg = "Location detection not supported in browser";
        }
        document.getElementById('info').innerHTML = msg;
      }

      function positionSuccess(position) {
        // Centre the map on the new location
        var coords = position.coords || position.coordinate || position;
        var latLng = new google.maps.LatLng(coords.latitude, coords.longitude);
        map.setCenter(latLng);
        map.setZoom(15);
        marker.setPosition(latLng);
        updateMarkerPosition(latLng);
        geocodePosition(latLng);
        //document.getElementById('info').innerHTML = 'Looking for <b>' + coords.latitude + ', ' + coords.longitude + '</b>...';

        // And reverse geocode.
        (new google.maps.Geocoder()).geocode({latLng: latLng}, function(resp) {
              var place = "Dont know mate!";
              if (resp[0]) {
                  var bits = [];
                  for (var i = 0, I = resp[0].address_components.length; i < I; ++i) {
                      var component = resp[0].address_components[i];
                      if (contains(component.types, 'political')) {
                          bits.push('<b>' + component.long_name + '</b>');
                        }
                    }
                    if (bits.length) {
                        place = bits.join(' > ');
                    }
                    marker.setTitle(resp[0].formatted_address);
                }
                //document.getElementById('info').innerHTML = place;
          });
      }

      function contains(array, item) {
          for (var i = 0, I = array.length; i < I; ++i) {
              if (array[i] == item) return true;
            }
            return false;
      }