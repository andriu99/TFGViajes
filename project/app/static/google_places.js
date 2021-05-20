let autocomplete
function initAutocomplete() {
    autocomplete_id("origin_address")
    autocomplete_id("destination_address")
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

