const socket = io();

const getMail = document.getElementById("getMail");
getMail.addEventListener('click', (e) => {
data = 5;
                      socket.emit('getMails', data);
                
})

socket.on("done",(data) => {
console.log(data["nesto"]);
//console.log(data[0]);
document.getElementById("resenje").innerHTML = "<p>" + data["nesto"] + "</p>";

})
function initMap() {
  
  // Instantiate a directions service.
  
  // Create a map and center it on Manhattan.
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 13,
    center: { lat: 40.771, lng: -73.974 },
  });
  
  const ps = new ParserSender(map);
  ps.sendPathToServer();
}



class ParserSender {
  constructor(map) {
    this.directionsService = new google.maps.DirectionsService();
    this.map = map;
    this.markerArray = [];
    this.cities = new Set()
    this.directionsRenderer = new google.maps.DirectionsRenderer({ map: map });    
    this.stepDisplay = new google.maps.InfoWindow();
    this.geocoder = new google.maps.Geocoder();
    this.infoWindow = new google.maps.InfoWindow();
    this.xhttp = new XMLHttpRequest();
  }  

  calculateAndDisplayRoute(
    directionsRenderer,
    directionsService,
    markerArray,
    stepDisplay,
    map
  ) {
    // First, remove any existing markers from the map.
    for (let i = 0; i < markerArray.length; i++) {
      markerArray[i].setMap(null);
    }
    // Retrieve the start and end locations and create a DirectionsRequest using
    // WALKING directions.
    directionsService.route(
      {
        origin: document.getElementById("start").value,
        destination: document.getElementById("end").value,
        travelMode: google.maps.TravelMode.WALKING,
      },
      (result, status) => {
        // Route the directions and pass the response to a function to create
        // markers for each step.
        if (status === "OK" && result) {
          document.getElementById("warnings-panel").innerHTML =
            "<b>" + result.routes[0].warnings + "</b>";
          directionsRenderer.setDirections(result);
          this.showSteps(result, markerArray, stepDisplay, map);
        } else {
          window.alert("Directions request failed due to " + status);
        }
      }
    );
  }


  geocodeLatLng(geocoder, map, infowindow, latlng) {  
    geocoder.geocode({ location: latlng }, (results, status) => {
      if (status === "OK") {
        if (results[0]) {
          map.setZoom(11);
          const marker = new google.maps.Marker({
            position: latlng,
            map: map,
          });
          const city = results[0].formatted_address.split(",", 3)[1];
          infowindow.setContent(city);
          infowindow.open(map, marker);
          console.log(city);
          this.cities.add(city);
          // console.log(results[0].formatted_address);
          // console.log(results[0].formatted_address.split(",", 3));
        } else {
          window.alert("No results found");
        }
      } else {
        window.alert("Geocoder failed due to: " + status);
      }
    });
  }


  showSteps(directionResult, markerArray, infoWindow, map) {
    // For each step, place a marker, and add the text to the marker's infowindow.
    // Also attach the marker to an array so we can keep track of it and remove it
    // when calculating new routes.
    const myRoute = directionResult.routes[0].legs[0];

    for (let i = 0; i < myRoute.steps.length; i++) {
      const marker = (markerArray[i] =
        markerArray[i] || new google.maps.Marker());
      marker.setMap(map);

      const start_pos = myRoute.steps[i].start_location;        
      marker.setPosition(start_pos);

      
      // stepDisplay.open(map, marker);    
      this.wrap(marker, infoWindow, map, start_pos);

    }

  }

  wrap(marker, stepDisplay, map, start_pos) {        
    
    // geocodeLatLng(geocoder, map, stepDisplay, start_pos);
    
    google.maps.event.addListener(marker, "click", () => {
      this.geocodeLatLng(this.geocoder, map, stepDisplay, start_pos);
      // Open an info window when the marker is clicked on, containing the text
      // of the step.    
      // this.geocodeLatLng(geocoder, map, stepDisplay, start_pos);
        // stepDisplay.setContent(marker.formatted_address);
        // stepDisplay.open(map, marker);
    });    
  }

  sendPathToServer() {
    document.getElementById("submit").addEventListener("click", () => {
      this.calculateAndDisplayRoute(
        this.directionsRenderer,
        this.directionsService,
        this.markerArray,
        this.stepDisplay,
        this.map
      );
    });
  }

  /*
  sendPathToServer() {

    // Display the route between the initial start and end selections.
    
    this.calculateAndDisplayRoute(
      this.directionsRenderer,
      this.directionsService,
      this.markerArray,
      this.stepDisplay,
      this.map
    );
      
    // Listen to change events from the start and end lists.
    
    this.onChangeHandler = function () {
      calculateAndDisplayRoute(
        this.directionsRenderer,
        this.directionsService,
        this.markerArray,
        this.stepDisplay,
        this.map
      );
    };
    
    // document.getElementById("start").addEventListener("change", onChangeHandler);
    // document.getElementById("end").addEventListener("change", onChangeHandler);
    
    
    document.getElementById("submit").addEventListener("click", () => {
        geocodeLatLng(geocode, map, infoWindow);
    });
    
    
    document.getElementById("submit").addEventListener("click", this.onChangeHandler);
  }
*/
}