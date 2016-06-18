/**
 * Created by Zia on 21/05/2016.
 * Functions for the filtering interface elements
 */

function readTypeFilters(){
    clubNight = $('#clubNight:checked').val();
    liveMusic = $('#liveMusic:checked').val();
    festival = $('#festival:checked').val();

    updateMarkers();
}