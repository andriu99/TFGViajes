function print_moovitmap(origin_address, dest_address, latO, lonO) {

    window.origin_ad = origin_address;
    window.dest_ad = dest_address;



    window.origin_coordinates = latO.toString() + '_' + lonO.toString();


    window.open('/new', '_blank', "rel=opener");



}

function set_moovitmap() {
    var m = document.getElementById('mapa_moovit');
    const origin = window.opener.origin_ad;
    const destination = window.opener.dest_ad;



    m.setAttribute("data-from", origin);
    m.setAttribute("data-to", destination);

    m.setAttribute("data-from-lat-long", window.opener.origin_coordinates);
    m.setAttribute("data-to-lat-long", window.opener.origin_coordinates);




}