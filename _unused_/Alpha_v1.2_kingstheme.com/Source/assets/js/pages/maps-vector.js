$( document ).ready(function() {
    $('#map-canvas').vectorMap({
        map: 'world_mill_en',
        series: {
            regions: [{
                values: gdpData,
                scale: ['#b0bec5'],
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function(e, el, code){
            el.html(el.html()+' (GDP - '+gdpData[code]+')');
        },
    markerStyle: {
      initial: {
        fill: '#ec407a',
        stroke: '#ec407a'
      }
    },
    markers: [
      {latLng: [42.5, 1.51], name: 'Andorra'},
      {latLng: [47.14, 9.52], name: 'Liechtenstein'},
      {latLng: [14.01, -60.98], name: 'Saint Lucia'},
      {latLng: [1.3, 103.8], name: 'Singapore'}
    ]
    });
    
    $('.jvectormap-zoomin').addClass('btn blue-grey');
    $('.jvectormap-zoomout').addClass('btn blue-grey');

});