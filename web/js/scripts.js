$(document).ready(function() { /* google maps ----*/

    // Set global Variables
    var map, markers = [];

    var data, beatDisplay = $(".beat-name"),
        displayTarget = $(".display-table");
    var murderRow = $(".murder-cases");
    var assaultRow = $(".assault-cases");
    var rapeRow = $(".rape-cases");

    $.getJSON("js/future.json", function(d) {
        data = d;
    })

    var caseInt2Text = function(cases) {
        if (cases < 1)
            return "0"
        else if (cases = 1)
            return "1 Case"
        else
            return cases.toString + " Cases"
    }

    var displayBeatData = function(event) {
        var beatName = event.feature.A.name.toUpperCase()
        beatDisplay.html(beatName)
        if (data != null) {
            if (beatName in data) {
                var i, arr = data[beatName];
                for (i = 0; i < 7; ++i) {
                    var day = ".day-" + i.toString()
                    murderRow.children(day).html(caseInt2Text(arr[i]["murder"]))
                    assaultRow.children(day).html(caseInt2Text(arr[i]["assault"]))
                    rapeRow.children(day).html(caseInt2Text(arr[i]["rape"]))
                }
            } else {
                for (i = 0; i < 7; ++i) {
                    var day = ".day-" + i.toString()
                    murderRow.children(day).html("")
                    assaultRow.children(day).html("")
                    rapeRow.children(day).html("")
                }
            }
        }
    }

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
                fillColor: '#FF0000',
                strokeColor: stroke
            };
        });
        map.data.addListener('click', displayBeatData);



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


    /**
     * Show button
     */

    $('#faBtn').click(function() {
        console.log('moreclicked');
        if ($('#faBtn').hasClass('fa-plus')) {
            $('#faBtn').html('<i class="fa fa-times"></i>');
        } else {
            $('#faBtn').html('<i class="fa fa-plus"></i>');
        }
    });
}); /* end google maps -----------------------*/
