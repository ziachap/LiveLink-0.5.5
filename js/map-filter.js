/**
 * Created by Zia on 21/05/2016.
 * Functions for filtering the events
 */

// TODO
function updateListing (){
  for (var i = 0; i < $('#listingoverlay > div').length; i++){

  }
  for (var i = 0; i < markerData.length; i++){

  }
}

function updateMarkers () {
    var oldInfoWindow = null;
    if (infoWindow != null) {
        oldInfoWindow = infoWindow;
    }

    // Filter event markers
    var typeFiltered = filterTypes(masterData);
    var distanceFiltered = filterDistance(typeFiltered);
    markerData = distanceFiltered.slice();

    // Refresh
    clearAllMarkers();
    addAllMarkers();

    // Restore old info window
    if (infoWindow.anchor != null) {
        if (inBounds(oldInfoWindow.anchor.position.lng(), oldInfoWindow.anchor.position.lat())){
            infoWindow.open(map, oldInfoWindow.anchor);
        }
    }
}
function clearAllMarkers() {
    allMarkers = oms.getMarkers();
    for (var i = 0; i < allMarkers.length; i ++) {
        allMarkers[i].setMap(null);;
    }
}
function addAllMarkers() {
  // Loop through array of markers & place each one on the map
    for (var i = 0; i < window.markerData.length; i ++) {
        var position = new google.maps.LatLng(markerData[i][1], markerData[i][2]);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            icon: markerData[i][7],
            //icon: marker_path,
            title: markerData[i][0],
            index: i,
            style: "img-circle",
            options: {
                zIndex: i
            },
            id: markerData[i][3]
        });
        oms.addMarker(marker);
    }
}
function filterTypes(data){
    var tempData = [];
    for (var i = 0; i < data.length; i++){
        if ((masterData[i][5] == 'Club Night') && clubNight) {
            tempData.push(data[i]);
        }
        else if ((masterData[i][5] == 'Festival') && festival) {
            tempData.push(data[i]);
        }
        else if ((masterData[i][5] == 'Live Music') && liveMusic) {
            tempData.push(data[i]);
        }
    }
    return tempData.slice();
}
function filterDistance(data){
    var tempData = [];
    var zoomCorrection = Math.pow(map.getZoom(),10)
    for (var i = 0; i < data.length; i++){
        if (inBounds(data[i][2],data[i][1])) {
            tempData.push(data[i]);
        }
    }
    return tempData.slice();
}

// Not needed
function findDistance(long1, lat1, long2, lat2){
    var longd = long2 - long1;
    var latd = lat2 - lat1;
    var longd2 = Math.pow(longd,2);
    var latd2 = Math.pow(latd,2);
    var distance = Math.sqrt(longd2 + latd2);
    return distance;
}

// Finds whether the given coordinates are in the map's bounds
function inBounds(lng, lat){
    //var bounds = new google.maps.LatLngBounds();
    var bounds = map.getBounds();
    var southWest = bounds.getSouthWest();
    var northEast = bounds.getNorthEast();
    var lng1 = southWest.lng();
    var lng2 = northEast.lng();
    var lat2 = northEast.lat();
    var lat1 = southWest.lat();
    if (lng > lng1 && lng < lng2){
        if (lat > lat1 && lat < lat2){
            return true;
        }
    }
    return false;
}