let autocomplete

function initAutocomplete_map() {
    autocomplete_id("origin_address")
    autocomplete_id("destination_address")

    initMap()


    
}

function initMap(){
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

function autocomplete_id(idname){
    autocomplete= new google.maps.places.Autocomplete(
        document.getElementById(idname),
    {
        types: ['address'],
        componentRestrictions: {'country': ['es']},
    });
    autocomplete.addListener('place_changed',onPlaceChanged);

}

 

function onPlaceChanged(){
    var place=autocomplete.getPlace();
    if (!place.geometry){
        document.getElementById('origin_address').placeholder='Enter a place';

    }else{
        document.getElementById('origin_address').innerHTML=place.name;
    }
}

// function initMap(){
//     const cairo = { lat:40, lng:3 };
//     const map = new google.maps.Map(document.getElementById("map-route"), {
//     scaleControl: true,
//     center: cairo,
//     zoom: 10,
//     });

//     const infowindow = new google.maps.InfoWindow();
//     infowindow.setContent("Destino");

//     const marker = new google.maps.Marker({ map, position: cairo });
//     marker.addListener("click", () => {
//     infowindow.open(map, marker);
//     });
// }


