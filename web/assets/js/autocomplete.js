function initService() {
    const displaySuggestions = function (predictions, status) {
      if (status != google.maps.places.PlacesServiceStatus.OK || !predictions) {
        alert(status);
        return;
      }
      predictions.forEach((prediction) => {
          console.log(prediction.description)
        const li = document.createElement("li");
        li.appendChild(document.createTextNode(prediction.description));
        document.getElementById("results").appendChild(li);
      });
    };
    const service = new google.maps.places.AutocompleteService();
    // const getElementById("origin-place").text();
    service.getQueryPredictions(document.getElementById("results"), displaySuggestions);
  }