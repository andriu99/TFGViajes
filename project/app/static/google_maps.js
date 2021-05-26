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
    get_currentLocation(map);
    set_origin_throughtMap(map);
    autocomplete("origin_address", "destination_address", map);

}

function set_origin_throughtMap(map) {
    const set_originButton = document.createElement("button");
    set_originButton.id = 'button-id';


    set_originButton.textContent = "Origin Location";
    set_originButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(set_originButton);

    var click = false;
    var listener = null;
    set_originButton.addEventListener("click", () => {
        if (click) {
            background = "#fff";
            listener.remove();

        } else {
            background = "green";
            listener = map.addListener("click", (mapsMouseEvent) => {

                infoWindow = new google.maps.InfoWindow();
                get_address_withLocation(mapsMouseEvent.latLng.lat(), mapsMouseEvent.latLng.lng(), map)

            });

        }
        set_originButton.style.backgroundColor = background;

        click = !click;


    });
}


function get_currentLocation(map) {
    const locationButton = document.createElement("button");

    locationButton.id = 'button-id';

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

                    if (dict_markers.origin != null)
                        dict_markers.origin.setMap(null);

                    get_address_withLocation(current_lat, current_lng, map)
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

function get_address_withLocation(lat, lng, map) {
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


                document.getElementById('origin_address').value = results[0].formatted_address;

                document.getElementById('lat_Origin').value = lat;
                document.getElementById('lon_Origin').value = lng;
                dict_markers.origin = marker;


            } else {
                window.alert("No results found");
            }
        } else {
            window.alert("Geocoder failed due to: " + status);
        }
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

            if (address_id == 'origin_address') {
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
    });

}