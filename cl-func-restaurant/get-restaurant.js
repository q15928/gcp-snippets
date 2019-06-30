// GCP cloud function to interact with dialogflow and return the restaurant info
// Source from qwiklabs

'use strict';

const {
  dialogflow,
  Image,
  Suggestions
} = require('actions-on-google');

const functions = require('firebase-functions');
const app = dialogflow({debug: true});

function getMeters(i) {
     return i*1609.344;
}

app.intent('get_restaurant', (conv, {location, proximity, cuisine}) => {
      const axios = require('axios');
      var api_key = "<YOUR_API_KEY_HERE>";
      var user_location = JSON.stringify(location["street-address"]);
      var user_proximity;
      if (proximity.unit == "mi") {
        user_proximity = JSON.stringify(getMeters(proximity.amount));
      } else {
        user_proximity = JSON.stringify(proximity.amount * 1000);
      }
      var loc = JSON.stringify(location);
      var geo_code = "https://maps.googleapis.com/maps/api/geocode/json?address=" + encodeURIComponent(user_location) + "&region=<YOUR_REGION>&key=" + api_key;
      return axios.get(geo_code)
        .then(response => {
          var places_information = response.data.results[0].geometry.location;
          var place_latitude = JSON.stringify(places_information.lat);
          var place_longitude = JSON.stringify(places_information.lng);
          var coordinates = [place_latitude, place_longitude];
          return coordinates;
      }).then(coordinates => {
        var lat = coordinates[0];
        var long = coordinates[1];
        var place_search = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=" + encodeURIComponent(cuisine) +"&inputtype=textquery&fields=photos,formatted_address,name,opening_hours,rating&locationbias=circle:" + user_proximity + "@" + lat + "," + long + "&key=" + api_key;
        return axios.get(place_search)
        .then(response => {
            var photo_reference = response.data.candidates[0].photos[0].photo_reference;
            var address = JSON.stringify(response.data.candidates[0].formatted_address);
            var name = JSON.stringify(response.data.candidates[0].name);
            var photo_request = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=' + photo_reference + '&key=' + api_key;
            conv.ask(`Fetching your request...`);
            conv.ask(new Image({
                url: photo_request,
                alt: 'Restaurant photo',
              }))
            conv.close(`Okay, the restaurant name is ` + name + ` and the address is ` + address + `. The following photo uploaded from a Google Places user might whet your appetite!`);
        })
    })
});

exports.get_restaurant = functions.https.onRequest(app);