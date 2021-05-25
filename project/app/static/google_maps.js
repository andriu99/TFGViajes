
function init_autocomplete_map() {
  autocomplete_id("origin_address");
  autocomplete_id("destination_address");

  initMap();

}


function save_lat_lon(id_address, id_latitude, id_longitude, geocoder) {

  var address = document.getElementById(id_address).value;
  if (id_address != 'origin_address' || address != document.getElementById('current_address').value) {

    geocoder.geocode({ 'address': address }, function (results, status) {
      if (status === google.maps.GeocoderStatus.OK) {



        save_locationData_inHTML(id_latitude, id_longitude, results[0].geometry.location.lat(), results[0].geometry.location.lng());


      } else {
        window.alert("Geocode was not successful for the following reason: " + status);
      }

    });
  }

}

function save_locationData_inHTML(id_latitude, id_longitude, latitude, longitude) {

  document.getElementById(id_latitude).value = latitude;
  document.getElementById(id_longitude).value = longitude;
  window.alert(latitude + '       ' + longitude);
  window.alert(id_latitude + '    ' + id_longitude)

}

function initMap() {

  let list_address = ['origin_address', 'destination_address']

  // var geocoder = new google.maps.Geocoder();


  // save_lat_lon(list_address[0], 'lat_Origin', 'lon_Origin', geocoder);
  // save_lat_lon(list_address[1], 'lat_Dest', 'lon_Dest', geocoder);




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
          // document.getElementById('lat_currentLocat').value = current_lat
          // document.getElementById('lon_currentLocat').value = current_lng

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


        // document.getElementById('current_address').value = results[0].formatted_address;
        document.getElementById('origin_address').value = results[0].formatted_address;

        // document.getElementById('lat_Origin').value = lat;
        // document.getElementById('lon_Origin').value = lng;

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


function autocomplete_id(idname) {

  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById(idname),
    {
      types: ['address'],
      componentRestrictions: { 'country': ['es'] },
    });

  autocomplete.addListener('place_changed', function () {
    onPlaceChanged('origin_address','lat_Origin','lon_Origin')
  });

  autocomplete.addListener('place_changed', function () {
    onPlaceChanged('destination_address','lat_Dest','lon_Dest')
  });


}



function onPlaceChanged(address_id,lat_id,long_id) {

  var geocoder = new google.maps.Geocoder()
  var address = document.getElementById(address_id).value

  geocoder.geocode({ 'address': address }, function (results, status) {

    if (status == google.maps.GeocoderStatus.OK) {
      var latitude = results[0].geometry.location.lat();
      var longitude = results[0].geometry.location.lng();
      document.getElementById(lat_id).value=latitude;
      document.getElementById(long_id).value=longitude;
    
    }
  });

}

