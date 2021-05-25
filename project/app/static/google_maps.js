
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

  autocomplete("origin_address","destination_address",map);


  

}



function initMap() {

  let list_address = ['origin_address', 'destination_address']


  let latO = parseFloat(document.getElementById("lat_Origin").value);
  let lonO = parseFloat(document.getElementById("lon_Origin").value);

  let latD = parseFloat(document.getElementById('lat_Dest').value);
  let lonD = parseFloat(document.getElementById('lon_Dest').value);

  document.write(latO + ' ' + lonO + '\n');
  document.write(latD + ' ' + lonD + '\n');

  let list_location = [];
  let point_origin = { lat: latO, lng: lonO };

  let origin_exists = !(latO == 181 || lonO == 181 || latD == 181 || lonO == 181)

  var map = new google.maps.Map(document.getElementById("google_map"), {
    scaleControl: true,
    center: point_origin,
    zoom: 6,
  });
  get_currentLocation(map);



  if (origin_exists) {

    point_origin = { lat: latO, lng: lonO }
    list_location.push(point_origin);
    list_location.push({ lat: latD, lng: lonD });

    list_location.forEach((element, index) => {
      const infowindow = new google.maps.InfoWindow();
      contentString =
        '<div id="content-map">' +
        '<p>' + document.getElementById(list_address[index]).value + '</p>' +
        "</div>";

      infowindow.setContent(contentString);
      const marker = new google.maps.Marker({ map, position: element });

      marker.addListener("click", () => {
        infowindow.open(map, marker);
      });

    });

  } else {
    map.setCenter({ //Madrid Coordinates
      lat: 40.4165,
      lng: -3.70256
    });
  }




}

function get_currentLocation(map) {
  infoWindow = new google.maps.InfoWindow();
  const locationButton = document.createElement("button");
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

          get_address_withLocation(current_lat, current_lng, infoWindow, map)

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

function get_address_withLocation(lat, lng, infoWindow, map) {
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
        document.getElementById('lat_Origin').value=lat;
        document.getElementById('lon_Origin').value=lng;

    
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
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

function autocomplete(id_name_origin, id_name_destination,map) {
  var autocomplete_origin = create_autocomplete(id_name_origin);
  var autocomplete_dest = create_autocomplete(id_name_destination);

  autocomplete_origin.addListener('place_changed', function () {
    onPlaceChanged('origin_address', 'lat_Origin', 'lon_Origin',map)
  });

  autocomplete_dest.addListener('place_changed', function () {
    onPlaceChanged('destination_address', 'lat_Dest', 'lon_Dest',map)
  });

}

function create_autocomplete(id) {
  var autocomplete = new google.maps.places.Autocomplete(
    document.getElementById(id),
    {
      types: ['address'],
      componentRestrictions: { 'country': ['es'] },
    });
  return autocomplete;
}




function onPlaceChanged(address_id,lat_id,long_id,map) {

  var geocoder = new google.maps.Geocoder()
  var address = document.getElementById(address_id).value

  geocoder.geocode({ 'address': address }, function (results, status) {

    if (status == google.maps.GeocoderStatus.OK) {

      var latitude = results[0].geometry.location.lat();
      var longitude = results[0].geometry.location.lng();
      document.getElementById(lat_id).value=latitude;
      document.getElementById(long_id).value=longitude;

      const infowindow = new google.maps.InfoWindow();
      contentString =
        '<div id="content-map">' +
        '<p>' + address + '</p>' +
        "</div>";

      infowindow.setContent(contentString);
      const marker = new google.maps.Marker({ map, position: {lat:latitude,lng:longitude} });

      marker.addListener("click", () => {
        infowindow.open(map, marker);
      });

    }
  });

}

