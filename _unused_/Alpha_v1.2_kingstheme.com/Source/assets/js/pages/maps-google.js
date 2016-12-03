$( document ).ready(function() {
    function initialize() {
        var mapOptions = {
            center: new google.maps.LatLng(59.8873193,10.6993369,12),
            zoom: 12
        };
        var map = new google.maps.Map(document.getElementById('map-canvas'),  mapOptions); 
    }
    google.maps.event.addDomListener(window, 'load', initialize);
    

});