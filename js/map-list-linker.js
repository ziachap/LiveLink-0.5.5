/**
 * Created by Zia on 20/05/2016.
 * Functions for interlinking the map and list selections for more responsiveness
 */

var selectedListingId;

// Clicking on a listing that is already selected should redirect to its URL
function checkSelected(id){
    if (selectedListingId==id) {
        console.log("double click");
        window.location.replace("/event/"+id);
    }
    else {
        selectedListingId = id;
    }
}

// Given an event id, open it's info window on the map
function openInfoWindow(id) {
    checkSelected(id)
    if (oms.getMarkers() != []) {
        // Close other info window and make a new one
        if (infoWindow) {
            infoWindow.close();
        }
        infoWindow = new google.maps.InfoWindow();

        // Find the correct window content
        for (var i = 0; i < masterData.length; i++){
            if (masterData[i][3] == id) {
                // Move the map
                map.panTo(new google.maps.LatLng(masterData[i][1],masterData[i][2]));
                map.setZoom(15);
                infoWindow.setContent(masterData[i][4]);
                // Find the correct marker and show infoWindow
                for (var i = 0; i < oms.getMarkers().length; i++) {
                    if (oms.getMarkers()[i].id == id) {
                        // Show the info window
                        infoWindow.open(map, oms.getMarkers()[i]);
                        return;
                    }
                }
            }
        }
    }
}

// Given an event id, highlight and scroll to its listing
function highlightListing(id){
    $('#listing-overlay > div').css('-webkit-filter', 'brightness(95%)');
    $('#listing-overlay > div').css("background-color", "rgba(245,245,245,0.7)");
    $('#listing-'+id).css('-webkit-filter', 'brightness(105%)');
    $('#listing-'+id).css("background-color", "rgba(245,245,245,0.8)");
    //$('#listing-overlay').effect( "bounce", {times:2}, 300 );
    $('#listing-overlay').animate({
        scrollTop: $('#listing-overlay').scrollTop()+$("#listing-"+id).position().top-$('#listing-overlay').height()/2+$("#listing-"+id).height()/2-20
    }, 600);
}

// Given an event id, highlight and scroll to its listing
function dehighlightListing(){
    $('#listing-overlay > div').css('-webkit-filter', 'brightness(100%)');
    $('#listing-overlay > div').css("background-color", "rgba(245,245,245,0.7)");
}
