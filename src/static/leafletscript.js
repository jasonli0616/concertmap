// Initialize map
var map = L.map('map')
    .setView([43.65, -79.38], 12); // Coordinates: 43.65, -79.38 (Toronto); zoom: 12


// Add OpenStreetMap tile layer
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


/**
 * Add a concert marker to the map.
 * When clicked, it will display details and the link to the setlist.
 * 
 * @param {*} lat latitude
 * @param {*} lng longitude
 * @param {*} artistName artist name
 * @param {*} dateRaw date of concert in dd-MM-yyyy as specified in setlist.fm API
 * @param {*} venue venue name
 * @param {*} url setlist url
 */
function addConcertMarker(lat, lng, artistName, dateRaw, venue, url) {

    // Format date from dd-MM-yyyy
    let [day, month, year] = dateRaw.split("-");
    let date = new Date(year, month, day)

    // Create marker (pin)
    let marker = L.marker([lat, lng]).addTo(map);

    // Show details in tooltip on hover
    marker.bindTooltip(`${artistName}<br>${date.toLocaleDateString()}<br>${venue}`)

    // Open page on setlist.fm in new tab on click
    marker.on("click", () => window.open(url, "_blank"))
}

/**
 * Show user's current location, if available.
 */
function showCurrentLocation(event) {

    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((pos) => {

            let currentPosition = [pos.coords.latitude, pos.coords.longitude];

            // Move map to current location
            map.setView(currentPosition, 12);

            // Add pin to current location
            let marker = L.marker(currentPosition).addTo(map);

            // Marker tooltip on hover
            marker.bindTooltip("Current location")
        })
    } else {
        window.alert("Not available");
    }
}
