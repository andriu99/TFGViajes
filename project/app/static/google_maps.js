var dict_markers = {
    origin: null,
    destination: null
}

function init_autocomplete_map() {

    var map = new google.maps.Map(document.getElementById("google_map"), {
        scaleControl: true,
        center: { //Madrid Coordinates
            lat: 40.4165,
            lng: -3.70256
        },
        zoom: 6,
    });

    init_marker('origin_address', 'lat_Origin', 'lon_Origin', map);
    init_marker('destination_address', 'lat_Dest', 'lon_Dest', map);

    get_currentLocation(map);
    set_origin_dest_throughtMap(map);
    autocomplete("origin_address", "destination_address", map);

}

function init_marker(address_id, lat_id, long_id, map) {
    if (document.getElementById(address_id).value != '') {
        onPlaceChanged(address_id, lat_id, long_id, map)

    }

}



function get_currentLocation(map) {
    const locationButton = document.createElement("button");
    locationButton.setAttribute("type", "button");
    locationButton.class = 'buttons_current_origin_dest';

    locationButton.textContent = "Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);

    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    current_lat = position.coords.latitude;
                    current_lng = position.coords.longitude;

                    const pos = {
                        lat: current_lat,
                        lng: current_lng,
                    };

                    get_address_withLocation(current_lat, current_lng, map, true);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });
}

function get_address_withLocation(lat, lng, map, is_origin) {
    infoWindow = new google.maps.InfoWindow();
    const geocoder = new google.maps.Geocoder();
    const latlng = {
        lat: lat,
        lng: lng,
    };
    geocoder.geocode({ location: latlng }, (results, status) => {
        if (status === "OK") {
            if (results[0]) {
                map.setZoom(7);
                const marker = new google.maps.Marker({
                    position: latlng,
                    map: map,
                });
                contentString =
                    '<div id="content-map">' +
                    '<p>' + results[0].formatted_address + '</p>' +
                    "</div>";
                infoWindow.setContent(contentString);
                infoWindow.open(map, marker);


                if (is_origin) {
                    document.getElementById('origin_address').value = results[0].formatted_address;
                    document.getElementById("lat_Origin").value = lat;
                    document.getElementById("lon_Origin").value = lng;

                    remove_mapMarkers('origin_address', marker)


                } else {
                    document.getElementById('destination_address').value = results[0].formatted_address;
                    document.getElementById("lat_Dest").value = lat;
                    document.getElementById("lon_Dest").value = lng;
                    remove_mapMarkers('destination_address', marker);


                }



            } else {
                window.alert("No results found");
            }

        } else {
            window.alert("Geocoder failed due to: " + status);
        }
    });



}




function set_origin_dest_throughtMap(map) {
    const div_button_origin_dest = document.createElement("div");
    div_button_origin_dest.className = 'buttons_current_origin_dest';

    const set_originButton = document.createElement("button");
    set_originButton.setAttribute("type", "button");
    const set_destinationButton = document.createElement("button");
    set_destinationButton.setAttribute("type", "button");


    div_button_origin_dest.appendChild(set_destinationButton);
    div_button_origin_dest.appendChild(set_originButton);

    const list_buttons = [set_originButton, set_destinationButton];
    const list_names_buttons = ['Origin Location', 'Destination Location']
    var list_is_origin = [true, false];
    var list_is_activated = [false, false];



    list_buttons.forEach((button, index) => {
        button.textContent = list_names_buttons[index];
        button.classList.add("custom-map-control-button");
        map.controls[google.maps.ControlPosition.TOP_CENTER].push(button);

        var listener = null;
        button.addEventListener("click", () => {
            previus_index = index - 1;
            if (previus_index == -1) previus_index = list_buttons.length - 1;



            if (list_is_activated[previus_index] == false) {
                if (list_is_activated[index]) {
                    list_is_activated[index] = false;
                    var background = "#fff";
                    listener.remove();

                } else {

                    list_is_activated[index] = true;
                    var background = "darkgreen";
                    listener = map.addListener("click", (mapsMouseEvent) => {
                        get_address_withLocation(mapsMouseEvent.latLng.lat(), mapsMouseEvent.latLng.lng(), map, list_is_origin[index]);
                    });
                }

            }


            button.style.backgroundColor = background;
        });
    });

}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation ?
        "Error: The Geolocation service failed." :
        "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}

function autocomplete(id_name_origin, id_name_destination, map) {
    var autocomplete_origin = create_autocomplete(id_name_origin);
    var autocomplete_dest = create_autocomplete(id_name_destination);

    autocomplete_origin.addListener('place_changed', function() {
        onPlaceChanged('origin_address', 'lat_Origin', 'lon_Origin', map)
    });

    autocomplete_dest.addListener('place_changed', function() {
        onPlaceChanged('destination_address', 'lat_Dest', 'lon_Dest', map)
    });

}

function create_autocomplete(id) {
    var autocomplete = new google.maps.places.Autocomplete(
        document.getElementById(id), {
            types: ['address'],
            componentRestrictions: { 'country': ['es'] },
        });
    return autocomplete;
}



function onPlaceChanged(address_id, lat_id, long_id, map) {

    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById(address_id).value;

    geocoder.geocode({ 'address': address }, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {

            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();


            document.getElementById(lat_id).value = latitude;
            document.getElementById(long_id).value = longitude;

            const infowindow = new google.maps.InfoWindow();
            contentString =
                '<div id="content-map">' +
                '<p>' + address + '</p>' +
                "</div>";

            infowindow.setContent(contentString);
            const marker = new google.maps.Marker({ map, position: { lat: latitude, lng: longitude } });

            marker.addListener("click", () => {
                infowindow.open(map, marker);
            });
            remove_mapMarkers(address_id, marker);


        } else {
            window.alert('Bad ' + status);
        }
    });

}

function remove_mapMarkers(id, marker) {
    if (id == 'origin_address') {

        var marker_remove = dict_markers.origin;
        dict_markers.origin = marker;

    } else {

        var marker_remove = dict_markers.destination;
        dict_markers.destination = marker;

    }

    if (marker_remove != null) {
        marker_remove.setMap(null);

    }

}