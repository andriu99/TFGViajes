
var map;

// Initialize and add the map
function initMap () {
    const cairo = { lat:40, lng:3 };
    map = new google.maps.Map(document.getElementById("google_map"), {
    scaleControl: true,
    center: cairo,
    zoom: 10,
    });

    const infowindow = new google.maps.InfoWindow();
    infowindow.setContent("Destino");

    const marker = new google.maps.Marker({ map, position: cairo });
    marker.addListener("click", () => {
    infowindow.open(map, marker);
    });
}

    // const cairo = { lat:40, lng:3 };
    // const map = new google.maps.Map(document.getElementById("map"), {
    // scaleControl: true,
    // center: cairo,
    // zoom: 10,
    // });

    // const infowindow = new google.maps.InfoWindow();
    // infowindow.setContent("Destino");

    // const marker = new google.maps.Marker({ map, position: cairo });
    // marker.addListener("click", () => {
    // infowindow.open(map, marker);
    // });
