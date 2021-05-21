let autocomplete

function init_autocomplete_map() {
    autocomplete_id("origin_address");
    autocomplete_id("destination_address");

    initMap();


    
}

function save_lat_lon(id_address,id_latitude,id_longitude){
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById(id_address).value

    geocoder.geocode( { 'address': address}, function(results, status) {

        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            document.getElementById(id_latitude).value = latitude;
            document.getElementById(id_longitude).value=longitude;
        } 
    }); 
}

function initMap(){
    // print(document.getElementById("latO").textContent)
    // document.write(parseFloat(document.getElementById("latO").textContent));

    // const cairo={}
    // try {
    //     const cairo = { lat:parseFloat(document.getElementById("latO").textContent), lng:parseFloat(document.getElementById("latO").textContent) };

    //   } catch (error) {
    //     const cairo = { lat:39, lng:24 };
    //   }
    list_address=['origin_address','destination_address']
  
    save_lat_lon(list_address[0],'lat_Origin','lon_Origin')
    save_lat_lon(list_address[1],'lat_Dest','lon_Dest')

    
    latO=document.getElementById("lat_Origin").value
    lonO=document.getElementById("lon_Origin").value
    latD=document.getElementById("lat_Dest").value
    lonD=document.getElementById("lon_Dest").value

    let list_location=[]
    let point={}
    if (latO === 181){
        point={lat:40.4165, lng:-3.70256}

    }else{
        point={lat:latO,lng:lonO}
    }
    document.write(point.lat)
    var map = new google.maps.Map(document.getElementById("google_map"), {
        scaleControl: true,
        center: point,
        zoom: 10,
    });
   
    try{
        list_location.push({lat:latO,lng:lonO});
        list_location.push({lat:latD,lng:lonD});

        list_location.forEach((element,index)=>{
             const infowindow = new google.maps.InfoWindow();
            infowindow.setContent( document.getElementById(list_address[index]).value);
            const marker = new google.maps.Marker({ map, position: element });

               marker.addListener("click", () => {
                infowindow.open(map, marker);
                });
    
        })
    
        // list_location.forEach((element, index) => {
            
    
        // const infowindow = new google.maps.InfoWindow();
        // infowindow.setContent( document.getElementById(list_address[index]).value);
        

        // const marker = new google.maps.Marker({ map, position: element });

        // marker.addListener("click", () => {
        //         infowindow.open(map, marker);
        // });
    


    }catch(error){
        document.write('ejeio')
        
    }
    // list_location.push({lat:latO,lng:lonO})
    // list_location.push({lat:latD,lng:lonD})

    // list_location.forEach((element, index) => {
        

    // const infowindow = new google.maps.InfoWindow();
    // infowindow.setContent( document.getElementById(list_address[index]).value);
    // const marker = new google.maps.Marker({ map, position: element });
    //     marker.addListener("click", () => {
    //         infowindow.open(map, marker);
    // });

    // if (latO===-181 || lonO===-181 || latD===-181 || lonD === -181){
    //     document.write('nada')
        

    // }else{
    //     list_location.push({lat:latO,lng:lonO})
    //     list_location.push({lat:latD,lng:lonD})

    //     list_location.forEach((element, index) => {
            

    //     const infowindow = new google.maps.InfoWindow();
    //     infowindow.setContent( document.getElementById(list_address[index]).value);
    //     const marker = new google.maps.Marker({ map, position: element });
    //         marker.addListener("click", () => {
    //             infowindow.open(map, marker);
    //     });
            
            
    //     });
    // }

   

    

    
    

    
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


