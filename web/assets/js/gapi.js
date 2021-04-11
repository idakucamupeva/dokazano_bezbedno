const socket = io();
socket.on("done",(data) => {
  const lines = data["nesto"].split(')');
              
  document.getElementById("panel").innerHTML = "<ul style='padding-left:10px; font-size:15px;'>\n";
  for(var i = 0; i < lines.length; i++)
  {                
    document.getElementById("panel").innerHTML += ("<li>" + lines[i] + "</li>\n");
  }
  document.getElementById("panel").innerHTML += "</ul>";    
  })
function sendData(send_cities) {
  const socket = io();

  /*
  const getMail = document.getElementById("getMail");
  getMail.addEventListener('click', (e) => {
  data = 5;
                        socket.emit('getMails', data);
                  
  });
  */

  socket.emit('getCities', send_cities);
 
  socket.on("done",(send_data) => {
  console.log(send_data["nesto"]);
  });
  
}

function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    mapTypeControl: false,
    center: { lat: 45.0688, lng: 20.2195 },
    zoom: 9,
  });
  new AutocompleteDirectionsHandler(map);
}

function getCity(step) {
  for(var i = 0; i < data.length; i++) {            
    if(Math.abs( data[i].lat - step.start_point.lat()) < 0.08 
              && Math.abs( data[i].lng - step.start_point.lng()) < 0.08)
              {
                  // console.log(data[i].city);
                  return data[i].city.split(' ').join('_');
              }                      
  }
  return "";
}


class AutocompleteDirectionsHandler {
  constructor(map) {
    this.map = map;
    this.originPlaceId = "";
    this.destinationPlaceId = "";
    this.travelMode = google.maps.TravelMode.DRIVING;
    this.directionsService = new google.maps.DirectionsService();
    this.directionsRenderer = new google.maps.DirectionsRenderer();
    this.directionsRenderer.setMap(map);
    // this.cityData = JSON.parse(data);
    this.cities = []
    const originInput = document.getElementById("origin-input");
    const destinationInput = document.getElementById("destination-input");
    const modeSelector = document.getElementById("mode-selector");
    const originAutocomplete = new google.maps.places.Autocomplete(originInput);
    // Specify just the place data fields that you need.
    originAutocomplete.setFields(["place_id"]);
    const destinationAutocomplete = new google.maps.places.Autocomplete(
      destinationInput
    );
    // Specify just the place data fields that you need.
    destinationAutocomplete.setFields(["place_id"]);
    this.setupClickListener(
      "changemode-driving",
      google.maps.TravelMode.DRIVING
    );
    this.setupClickListener(
      "changemode-walking",
      google.maps.TravelMode.WALKING
    );
    this.setupClickListener(
      "changemode-transit",
      google.maps.TravelMode.TRANSIT
    );    
    this.setupPlaceChangedListener(originAutocomplete, "ORIG");
    this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
      destinationInput
    );
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
  }
  // Sets a listener on a radio button to change the filter type on Places
  // Autocomplete.
  setupClickListener(id, mode) {
    const radioButton = document.getElementById(id);
    radioButton.addEventListener("click", () => {
      this.travelMode = mode;
      this.route();
    });
  }
  setupPlaceChangedListener(autocomplete, mode) {
    autocomplete.bindTo("bounds", this.map);
    autocomplete.addListener("place_changed", () => {
      const place = autocomplete.getPlace();

      if (!place.place_id) {
        window.alert("Please select an option from the dropdown list.");
        return;
      }

      if (mode === "ORIG") {
        this.originPlaceId = place.place_id;
      } else {
        this.destinationPlaceId = place.place_id;
      }
      this.route();
    });
  }
  route() {
    if (!this.originPlaceId || !this.destinationPlaceId) {
      return;
    }
    const me = this;
    this.directionsService.route(
      {
        origin: { placeId: this.originPlaceId },
        destination: { placeId: this.destinationPlaceId },
        travelMode: this.travelMode,
      },
      (response, status) => {
        if (status === "OK") {
          const myRoute = response.routes[0].legs[0].steps;
          const res = response;
          
          // console.log(myRoute)
          // console.log(myRoute.start_location.lat());
          for(var i = 0; i < myRoute.length; i++) {
            var cityStep = getCity(myRoute[i]);
            if (cityStep.localeCompare("") != 0 && !this.cities.includes(cityStep)) {
              // console.log(cityStep);
              this.cities.push(cityStep);
            }
          }

          // console.log(res);
          console.log("CITIES: ");
          console.log(this.cities);
          
          me.directionsRenderer.setDirections(response);

          const cities_copy = this.cities;
          
          //const socket = io();
          // sendData(this.cities);
          socket.emit('getCities', cities_copy);
 
          socket.on("done",(send_data) => {
            const lines = send_data["nesto"].split('\n');
              
              document.getElementById("panel").innerHTML = '<ul id="ispis">\n';
              document.getElementById("ispis").fontSize = "200px";
              for(var i = 0; i < lines.length; i++)
              {                
                document.getElementById("panel").innerHTML += ("<li>" + lines[i] + "</li>\n");
              }
              document.getElementById("panel").innerHTML += "</ul>";         
          });
          this.cities = [];

        } else {
          window.alert("Directions request failed due to " + status);
        }
      }      
    );

        
  }
}