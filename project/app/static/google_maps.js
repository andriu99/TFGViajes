
function initMap(){
    const cairo = { lat:lat_d, lng:long_d };
    const map = new google.maps.Map(document.getElementById("map-route"), {
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