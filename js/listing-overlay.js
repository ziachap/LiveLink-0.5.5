/**
 * Created by Zia on 04/04/2016.
 */
var panel = 'listing';

function toggle_listing_panel(){
    if (panel == 'listing'){
        close_panel();
        panel = 'none';
    }
    else {
        open_listing_panel();
        panel = 'listing';
    }
}

function toggle_filter_panel(){
    if (panel == 'filter'){
        close_panel();
        panel = 'none';
    }
    else {
        open_filter_panel();
        panel = 'filter';
    }
}

function open_listing_panel() {
    $("#listing-overlay").animate({
        left: '20px',
        opacity: '1'
    });
    $("#filter-overlay").animate({
        left: '-500px',
        opacity: '0'
    });

    document.getElementById("listing-overlay-open").style["opacity"] = "1";
    document.getElementById("filter-overlay-open").style["opacity"] = "0.6";

}

function open_filter_panel() {
    $("#listing-overlay").animate({
        left: '-500px',
        opacity: '0'
    });
    $("#filter-overlay").animate({
        left: '20px',
        opacity: '1'
    });
    document.getElementById("listing-overlay-open").style["opacity"] = "0.6";
    document.getElementById("filter-overlay-open").style["opacity"] = "1";
}

function close_panel() {
    $("#listing-overlay").animate({
        left: '-500px',
        opacity: '0'
    });
    $("#filter-overlay").animate({
        left: '-500px',
        opacity: '0'
    });
    document.getElementById("listing-overlay-open").style["opacity"] = "1";
    document.getElementById("filter-overlay-open").style["opacity"] = "1";

}