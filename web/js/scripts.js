$(document).ready(function() { /* google maps ----*/

    // Set global Variables
    var map, markers = [];
    var initialize = function() {

        var houstonLocation = new google.maps.LatLng(29.757150, -95.363903);


        /* Setup initial configuration */
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 11,
            center: houstonLocation
        });

        /* Setup InputField*/
        var input = document.getElementById('pac-input');

        // Set InputField inside of Map
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
        var searchBox = new google.maps.places.SearchBox(input);

        // Put Set Map Listener on InputField
        google.maps.event.addListener(searchBox, 'places_changed', function() {

            // Get Coordinates
            var places = searchBox.getPlaces();

            if (places.length == 0) return;

            // Clear out markers Array
            markers = [];

            var bounds = new google.maps.LatLngBounds();
            for (var i = 0, place; place = places[i]; i++) {

                // Set image if important
                var image = {
                    url: place.icon,
                    size: new google.maps.Size(71, 71),
                    origin: new google.maps.Point(0, 0),
                    anchor: new google.maps.Point(17, 34),
                    scaledSize: new google.maps.Size(25, 25)
                };

                // Set Marker
                var marker = new google.maps.Marker({
                    map: map,
                    icon: image,
                    animation: google.maps.Animation.DROP,
                    title: place.name || input.value,
                    position: place.geometry.location
                });

                // Add marker to markers Array
                markers.push(marker);

                // Change bounds of Map to marker
                bounds.extend(place.geometry.location);

                // Add Listener to marker
                google.maps.event.addListener(marker, 'click', function() {
                    infoWindow = InfoWindow(marker.title);
                    infoWindow.open(map, marker);

                    // Close Marker after 3 seconds
                    setTimeout(function() {
                        infoWindow.close();
                    }, 3000);
                });
            }

            // Update map's bounds
            map.fitBounds(bounds);
        });





        map.data.loadGeoJson('js/beats.geojson');
        map.data.setStyle(function(feature) {
            var fill = feature.getProperty('fill');
            var stroke = feature.getProperty('stroke');
            return {
                fillColor: fill,
                strokeColor: stroke
            };
        });
        map.data.addListener('click', function(event) {
            console.log(event);
        });



        map.data.addListener('mouseover', function(event) {
            map.data.overrideStyle(event.feature, {
                strokeWeight: 2.0,
                fillColor: 'green'
            });
        });

        map.data.addListener('mouseout', function(event) {
            map.data.overrideStyle(event.feature, {
                fillColor: '#FF0000'
            });
        });



    };

    ///* Setup InfoWindow */
    var InfoWindow = function(content) {
        //Create InfoWindow
        var iWindow = new google.maps.InfoWindow({
            content: setDummyText(content),
            maxWidth: 100
        });

        return iWindow;
    };

    ///* Setup Dummy Text for infoWindow */
    var setDummyText = function(title) {
        var str = 'The title of this marker is ' + title + 'a maxWidth of 100 and it closes in 3 seconds';
        return str;
    };

    /* Wait till initialize() finishes */
    google.maps.event.addDomListener(window, 'load', initialize);

}); /* end google maps -----------------------*/
