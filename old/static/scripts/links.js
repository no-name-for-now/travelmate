// links.js

function searchGoogle(term) {
    var searchUrl = "https://www.google.com/search?q=" + encodeURIComponent(term);
    window.open(searchUrl, "_blank");
}

function searchBooking(term) {
    var searchUrl = "https://www.booking.com/searchresults.html?ss=" + encodeURIComponent(term);
    window.open(searchUrl, "_blank");
}
