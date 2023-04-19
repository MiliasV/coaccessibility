//AMSTERDAM
/////////////////////////////////////////////////////////////////
//functions for presses that toggle the different layers // 
/////////////////////////////////////////////////////////////////

// INFO BUTTON
//// when button is pressed show the "info-window" and hide the legend-window if shownn

function toggleInfo() {
  var x = document.getElementById("info");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
    document.getElementById("legend-window").style.display = "none";
  }
}


function ageLayer(event){
  var buttonId = event.target.id;
  var button = document.getElementById(buttonId);

  if (buttonId=='children'){
      map.setPaintProperty('poi', 'circle-color', childCircleColor);
      button.style.color='#FFAF33';
      var eldbutton = document.getElementById("elderly");
      var agedivbutton = document.getElementById("agediv");
      eldbutton.style.color='white';
      agedivbutton.style.color='white';

  }
   else if (buttonId=='elderly'){
      map.setPaintProperty('poi', 'circle-color', elderlyCircleColor);
      button.style.color='#FFAF33';
      var childbutton = document.getElementById("children");
      var agedivbutton = document.getElementById("agediv");
      childbutton.style.color='white'
      agedivbutton.style.color='white'

  }
  else{
    map.setPaintProperty('poi', 'circle-color', circleColor)
    button.style.color='#FFAF33'
    var childbutton = document.getElementById("children");
    var eldbutton = document.getElementById("elderly");
    childbutton.style.color='white'
    eldbutton.style.color='white'


  }

}

function minutesLayer(event) {
  // Get the ID of the button that was clicked
  var buttonId = event.target.id;
  var button = document.getElementById(buttonId);
  var poi_visibility = map.getLayoutProperty('poi', 'visibility');
  var poi_labels_visibility = map.getLayoutProperty('poi-labels', 'visibility');
  var pop_opacity = map.getPaintProperty('population', 'fill-opacity');
  var pop_color = map.getPaintProperty('population', 'fill-color');


  // Perform different actions based on the button ID
  if (buttonId == "5min") {
    var otherbutton = document.getElementById("15min");

    if (button.style.color=='white'){
      button.style.color='#FFAF33'
      otherbutton.style.color='white'
      }
    map.removeLayer('population')
     map.addLayer({
        'id': 'population',
        'type': 'fill',
        'source': 'population',
        'source-layer': POP_LAYER,
       'paint': {
        'fill-opacity' : pop_opacity ,
        'fill-color': '#0B0B0B',
       }
      },
      
      );
    map.setPaintProperty('population', 'fill-color', pop_color)
    // remove existing and add the 5-minute isochrones layer
    map.removeLayer('iso_viz')
    map.addLayer({  
        'id': 'iso_viz',
        'type': 'fill',
        'source': 'iso_viz',
        'source-layer': ACCESS_AREA_LAYER,
        'paint': {
          'fill-opacity' : 0,
          'fill-color' : 'gray',
        }
     },
    );
  // remove existing and add 5-minute poi layer
  map.removeLayer('poi')
  map.removeLayer('poi-labels')

   map.addLayer({
    'id': 'poi',
    'type': 'circle',
    'source': 'poi',
    'source-layer': POI_LAYER,
        paint: {
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        1,
        5],
      'circle-opacity': 1,
      'circle-color': circleColor,
      //  'circle-stroke-width': 0.2,

      // 'circle-stroke-color': 'black'

    }
  },
  
  );

 map.addLayer({
  'id': 'poi-labels',
  'type': 'symbol',
  'source': 'poi',
  'source-layer': POI_LAYER,
  layout: {
    'text-field': ['get', 'subcategory'], // set the label text to the 'name' property of your data
    'text-size': 14,
    'text-offset': [0, 1], // adjust the offset of the label from the circle
    'text-allow-overlap': false // allow labels to overlap with each other
  },
  paint: {
    "text-color": "#A67F0E",
    "text-halo-color": "#fff",
    "text-halo-width": 100
  }

});

  } 

  else if (buttonId == "15min") {
    var otherbutton = document.getElementById("5min");
    if (button.style.color=='white'){
      button.style.color='#FFAF33'
      otherbutton.style.color='white'
    }

     map.removeLayer('population')
     map.addLayer({
        'id': 'population',
        'type': 'fill',
        'source': 'population_15',
        'source-layer': POP_LAYER_15,
       'paint': {
        'fill-opacity' : pop_opacity  ,
        'fill-color': pop_color,
        // 'fill-outline-color' : 'populationColor'
       }
      },
      
      );
    // Do something for 15 minutes button
    map.removeLayer('iso_viz')
    map.addLayer({
      'id': 'iso_viz',
      'type': 'fill',
      'source': 'iso_viz_15',
      'source-layer': ACCESS_AREA_LAYER_15,
      'paint': {
      'fill-opacity' : 0,
      'fill-color' : 'gray',
     }
  },
  );

  map.removeLayer('poi')
  map.addLayer({
    'id': 'poi',
    'type': 'circle',
    'source': 'poi_15',
    'source-layer': POI_LAYER_15,
        paint: {
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        1,
        5],
      'circle-opacity': 1,
      'circle-color': circleColor,
      //  'circle-stroke-width': 0.2,

      // 'circle-stroke-color': 'black'

    }
  },
  );
  map.removeLayer('poi-labels')

 map.addLayer({
  'id': 'poi-labels',
  'type': 'symbol',
  'source': 'poi_15',
  'source-layer': POI_LAYER_15,
  layout: {
    'text-field': ['get', 'subcategory'], // set the label text to the 'name' property of your data
    'text-size': 14,
    'text-offset': [0, 1], // adjust the offset of the label from the circle
    'text-allow-overlap': false // allow labels to overlap with each other
  },
  paint: {
    "text-color": "#A67F0E",
    "text-halo-color": "#fff",
     "text-halo-width": 100
  }

});

  }

  color = map.getPaintProperty('street','line-color')
   map.removeLayer('street')
   map.addLayer({
    'id': 'street',
    'type': 'line',
    'source': 'street',
    'source-layer': STREETS_LAYER,
     'paint': {
      'line-color': color,
      // 'line-color': '#DFDFDF',
      'line-width': 0.8
       },
  },
  );

  //keep the poi layer visible or invisble
  // if (poi_visibility!='visible'){
  //   map.setLayoutProperty('poi', 'visibility', 'none');
  // }
  // else{
  //     map.setLayoutProperty('poi', 'visibility', 'visible');

  // }
  map.setLayoutProperty('poi', 'visibility', poi_visibility);
  map.setLayoutProperty('poi-labels', 'visibility', poi_labels_visibility);


  // if (pop_visibility!='visible'){
  //   map.setLayoutProperty('population', 'visibility', 'none');
  // }
  // else{
  //     map.setLayoutProperty('population', 'visibility', 'visible');

  // }
}

// LEGEND BUTTON
// when button is pressed show the "legend-window" by changing its style from 'none' to 'block' and hide the info-window
function toggleLegend() {
  var x = document.getElementById("legend-window");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
    document.getElementById("info").style.display = "none";
  }
}


// WALKABLE STREET LAYER BUTTON
function toggleStreetLayer() {
	// var visibility = map.getLayoutProperty('street', 'visibility');
  var color = map.getPaintProperty('street', 'line-color');

	// toggle layer visibility by changing the layout object's visibility property
	// if (visibility === 'visible') {
  if (color === '#A67F0E') {

		// map.setLayoutProperty('street', 'visibility', 'none');
    map.setPaintProperty('street', 'line-color', 'white');

		document.getElementById('layer-button-img').src = '../assets/street_off.png'
		//this.className = '';
	} 
  else {
		//this.className = 'active';
		document.getElementById('layer-button-img').src = '../assets/street_on.png'
    map.removeLayer('street')
   map.addLayer({
    'id': 'street',
    'type': 'line',
    'source': 'street',
    'source-layer': STREETS_LAYER,
     'paint': {
     'line-color': '#A67F0E',
    'line-width': 0.8
       },
  },
  );
    // map.setPaintProperty('street', 'line-color', '#9B7944');
	}
}


// HOUSING BLOCK LAYER
function toggleHouseLayer() {
	var visibility = map.getLayoutProperty('population', 'visibility');
  var color = map.getPaintProperty('population', 'fill-color');
  var opacity = map.getPaintProperty('population', 'fill-opacity');

  console.log(color)
 
	// toggle layer visibility by changing the layout object's visibility property
	if (opacity === 0) {
    map.setPaintProperty('population', 'fill-color', populationColor); // change fill color to blue
    map.setPaintProperty('population', 'fill-opacity', 0.6); // change fill color to blue

		document.getElementById('layer-button2-img').src = '../assets/house_on.png'
		//this.className = '';
	} else {
		//this.className = 'active';
    // map.setPaintProperty('population', 'fill-color', '#0B0B0B'); // change fill color to blue
    map.setPaintProperty('population', 'fill-opacity', 0); // change fill color to blue


		document.getElementById('layer-button2-img').src = '../assets/house_off.png'
	}
}


// POI Layer
function togglePOILayer() {
	var visibility = map.getLayoutProperty('poi', 'visibility');
 
	// toggle layer visibility by changing the layout object's visibility property
	if (visibility === 'visible') {
		map.setLayoutProperty('poi', 'visibility', 'none');
    map.setLayoutProperty('poi-labels', 'visibility', 'none');
    document.getElementById('layer-button4-img').src = '../assets/poi_off.png'

  }
	 else {
		//this.className = 'active';
		map.setLayoutProperty('poi', 'visibility', 'visible');
    map.setLayoutProperty('poi-labels', 'visibility', 'none');
		document.getElementById('layer-button4-img').src = '../assets/poi_on.png'
	};
};

// initialize map 
mapboxgl.accessToken = MAPBOX_TOKEN;
var map = new mapboxgl.Map({
  container: 'map',
  style: MAPBOX_STYLE,
  center: CENTER,
  zoom: 1,
  maxZoom: 18,
  minZoom: 1,
  maxBounds:MAXBOUNDS,
  hash: true
});

map.addControl(
    new MapboxGeocoder({
      accessToken: MAPBOX_TOKEN,
      mapboxgl: mapboxgl,
      countries: 'nl',
      bbox: [4.72, 52.25,5.11, 52.44],
    })
    );

map.addControl(new mapboxgl.NavigationControl());

map.on('load', function() {
  // Insert the layer beneath any symbol layer.
  var layers = map.getStyle().layers;

  var labelLayerId;
  for (var i = 0; i < layers.length; i++) {
    if (layers[i].type === 'symbol') {
      labelLayerId = layers[i].id;
      break;
    }
  }

  // add layer sources to the map
  map.addSource('population', {
     type: 'vector',
     url: POP_TILESET
  });

    map.addSource('population_15', {
     type: 'vector',
     url: POP_TILESET_15
  });

  map.addSource('iso_viz', {
     type: 'vector',
     url: ACCESS_AREA_TILESET
  });

    map.addSource('iso_viz_15', {
     type: 'vector',
     url: ACCESS_AREA_TILESET_15
  });
	
  map.addSource('poi', {
     type: 'vector',
     url: POI_TILESET,

  });

  map.addSource('poi_15', {
     type: 'vector',
     url: POI_TILESET_15,
       cluster: true,
  clusterMaxZoom: 12, // set maximum zoom level for clustering
  clusterRadius: 50 // set cluster radius
  });
      map.addSource('street', {
     type: 'vector',
     url: STREETS_TILESET
  });


  // add the layer to the map
  
 map.addLayer({
    'id': 'population',
    'type': 'fill',
    'source': 'population',
    'source-layer': POP_LAYER,
   'paint': {
    'fill-opacity' : 0 ,
    'fill-color': populationColor,
    // 'fill-outline-color' : 'populationColor'
   }
  },
  labelLayerId
  );

	
  map.addLayer({
    'id': 'iso_viz',
    'type': 'fill',
    'source': 'iso_viz',
    'source-layer': ACCESS_AREA_LAYER,
    'paint': {
    'fill-opacity' : 0,
    'fill-color' : 'gray',
   }
  },
  labelLayerId
  );
	

  
 map.addLayer({
    'id': 'poi',
    'type': 'circle',
    'source': 'poi',
    'source-layer': POI_LAYER,
    paint: {
      'circle-radius': [
        'interpolate',
        ['linear'],
        ['zoom'],
        1,
        5],
      'circle-opacity': 1,
      'circle-color': circleColor,
      //  'circle-stroke-width': 0.2,
      // 'circle-stroke-color': 'black'

    },

}, labelLayerId
);

 map.addLayer({
  'id': 'poi-labels',
  'type': 'symbol',
  'source': 'poi',
  'source-layer': POI_LAYER,
  layout: {
    'text-field': ['get', 'subcategory'], // set the label text to the 'name' property of your data
    'text-size': 14,
    'text-offset': [0, 1], // adjust the offset of the label from the circle
    'text-allow-overlap': false // allow labels to overlap with each other
  },
  paint: {
    "text-color": "#A67F0E",
    "text-halo-color": "#fff",
    "text-halo-width": 100
  }

});

   map.addLayer({
    'id': 'street',
    'type': 'line',
    'source': 'street',
    'source-layer': STREETS_LAYER,
     'paint': {
     'line-color': 'white',
    'line-width': 0.8
       },
  },
  labelLayerId
  );
 
// set visibility of the layers
map.setLayoutProperty('poi-labels', 'visibility', 'none');
map.setLayoutProperty('street', 'visibility', 'visible');
map.setLayoutProperty('population', 'visibility', 'visible');
map.setLayoutProperty('poi', 'visibility', 'visible');
map.setLayoutProperty('iso_viz', 'visibility', 'visible');

// var filters = [];


// add a legend item
//The function takes two parameters: "item" and "index". 
//"item" is an object that contains information about a group, including its rating, value, and color. 
//"index" is the index of the group in an array of groups called "GROUPS".

//The function first checks if the previous group (i.e., the group with an index one less than the current group's index) exists. 
//For instance, if it does not exist (i.e., the current group is the first group), then the low value of the group's range is set to the group's value, 
//and the high value is set to infinity. The string variable is set to the low value.

//The function then adds a filter object to an array called "filters". 
// The filter object represents the range of values for the group, and it is used to filter the data that is displayed in the visualization. 
// The filter object contains a "condition" property that is an array of two conditions: 
//one that checks if a data point's "width" property is greater than the low value of the group's range, 
//and another that checks if the "width" property is less than or equal to the high value of the group's range. 
//The "active" property of the filter object is initially set to false.

  function addLegendItem(item, index) {

      if (item.group==0){
        group = GROUPS_HOMES
      }
      else{
        group = GROUPS_POIS
        if (index == 0) {  
          var legend_title = '</br><h3><img style="width: 36px; height: 36px; vertical-align:middle " src="../assets/poi_on.png"> ' +
          ' <span style="">Age diversity of the people who have access to each place within an X-minute walk </span> </h3>'
          var newElement = document.createElement('div');
          newElement.innerHTML = legend_title;

      var textNode = document.createTextNode(legend_title);
document.getElementById("legend-main").appendChild(newElement);

        }
      }

      if (group[index - 1] == null) {
        var low = item.value
        var high = Infinity
        var string = low + item.unit + ' (+)'

      }

      else {
        if (item.value==0)
          var low = 0
        else
          var low =item.value

        var high = group[index - 1].value
        var string = low + ' - ' + high + item.unit
      }

      // filters.push({'condition': ['all',['>', 'width', low],['<=', 'width', high]], 'active': false})

      var row = document.createElement("LI");
      var rowContent = document.createElement("DIV");
      var rowLeft = document.createElement("DIV");
      var color = document.createElement("DIV");
      var rowRight = document.createElement("DIV");

      // rowLeft.innerHTML = "<p>" + item.rating + "</p>"
      rowLeft.classList.add("row-left");
      color.classList.add("color");
      color.setAttribute("style", "background:" + item.color + ";");
      rowLeft.appendChild(color)
      row.appendChild(rowLeft)
      rowRight.classList.add("row-right");
      rowRight.innerHTML = "<p>" + string + "</p>";
      row.appendChild(rowRight);
      document.getElementById("legend-main").appendChild(row);
    }
  


  GROUPS_HOMES.reverse().forEach(addLegendItem);

  GROUPS_POIS.reverse().forEach(addLegendItem);

  // GROUPS_HOMES.reverse()

  var popup = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: true
  });

  function addPopup(e) {

    map.getCanvas().style.cursor = 'pointer';

    var coordinates = e.lngLat;
    // coordinates = [coordinates.lng, coordinates.lat + 0.003];  
    var walk = '5'
    var button = document.getElementById("5min");
    console.log(button.style.color)
    if (button.style.color==='white'){
      walk = '15'
    }
    else {
      walk='5'
    }
  	var description = ''

  	 if(e.features[0].source === "poi" || e.features[0].source === "poi_15"){
       var lineColor = e.features[0].layer.paint['circle-color'];

  		 var children = e.features[0].properties['Number of children']
       var adults = e.features[0].properties['Number of adults']
       var elderly = e.features[0].properties['Number of elderly']

       var name = e.features[0].properties['name']
       var category = e.features[0].properties['category']
       var subcategory = e.features[0].properties['subcategory']

       var age_diversity = e.features[0].properties['Age diversity(%)']

  		 description =
   
        '<div style="color:' + lineColor + '" class="message"> Place Info </div> ' + 
        '<ul>' + 
        '<li><div style="color:' + lineColor + '" class="message"> Name of Place: ' + name  + '</div>' +
        '<li><div style="color:' + lineColor + '" class="message"> Category: ' + category  + '</div>' +
        '<li><div style="color:' + lineColor + '" class="message"> Subcategory: ' + subcategory  + '</div>' +
        '</ul>' + 
        
        '<div style="color:' + lineColor + '" class="name"> ------------------------------------------------------------------------------ </div>' +
        '<div class="message">Who can access this place within a ' + walk + ' minute walk? </div>' +


         '<ul>' + 
        '<li><div style="color:' + lineColor + '" class="message"> Number of Children: ' + children  + '</div>' +
        '<li><div style="color:' + lineColor + '" class="message"> Number of Adults: ' + adults  + '</div>' +
        '<li><div style="color:' + lineColor + '" class="message"> Number of Elderly: ' + elderly  + '</div>' +
        '</ul>' + 
          '<div style="color:' + lineColor + '" class="message"> Age Diversity: ' + age_diversity  + ' % </div>' 
  	 }

      else  if(e.features[0].source === "population" || e.features[0].source === "population_15"){
        var lineColor = e.features[0].layer.paint['fill-color'];
        // var lineColor = '#0B0B0B';

        var places = e.features[0].properties['All Places']
        var public = e.features[0].properties['Public Places']
        var shop = e.features[0].properties['shop_count']
        var culture = e.features[0].properties['Culture Places']
        var food_drink = e.features[0].properties['Food/Drink Places']

        var walk_area = Math.round(e.features[0].properties['Walking Area (m2)'])

        walk_area = walk_area.toLocaleString('en', {useGrouping:true})
        description = 
          '<div class="message"> Accessible within a ' + walk + '  minute walk </div> ' +
            '<ul>' + 

          '<li> <div style="color:' + lineColor + '" class="message"> Public places: ' + public  + '</div></li>' +
          '<li> <div style="color:' + lineColor + '" class="message"> Culture places: ' + culture  + '</div></li>' +
          '<li> <div style="color:' + lineColor + '" class="message"> Food/drink places: ' + food_drink  + '</div></li>' +
          '<li> <div style="color:' + lineColor + '" class="message"> Shops: ' + shop  + '</div></li></br>' +
          '<li> <div style="color:' + lineColor + '" class="message"> Walking Area (m2): ' + walk_area  + '</div></li>' + 
          '</ul>' +
         '<div style="color:' + lineColor + '" class="name"> -------------------------------- ' + '</div>' +
         '<div style="color:' + lineColor + '" class="message"> Total number of places: ' + places  + '</div>'
     }
     // console.log(description)

    popup.setLngLat(coordinates)
    popup.setHTML(description)
    popup.addTo(map)

    popup._content.style.color = lineColor
    popup._content.style.borderColor = lineColor
    popup._content.style.minWidth = "450px";


    if (popup._tip.offsetParent.className.includes('mapboxgl-popup-anchor-bottom')) {
      popup._tip.style.borderTopColor = lineColor
    }
    if (popup._tip.offsetParent.className.includes('mapboxgl-popup-anchor-top')) {
      popup._tip.style.borderBottomColor = lineColor
    }
    if (popup._tip.offsetParent.className.includes('mapboxgl-popup-anchor-right')) {
      popup._tip.style.borderLeftColor = lineColor
    }
    if (popup._tip.offsetParent.className.includes('mapboxgl-popup-anchor-left')) {
      popup._tip.style.borderRightColor = lineColor
    }

    popup.addTo(map)
  }

  map.on('touchstart', function(e) {
    console.log(e)
  })


  map.on('click', 'population', function(e) {
    addPopup(e);
    
  });

  map.on('click', 'poi', function(e) {
    addPopup(e);
    var properties = e.features[0].properties;
        console.log(properties['Number of children']/properties['Number of people']);


});

map.on('mousemove', function (e) {
    var features = map.queryRenderedFeatures(e.point, {
          layers: ['population'],
          filter: ['==', '$type', 'Polygon']
      });
      if (features.length > 0) {
        var id = features[0].properties.c28992r100;
        var filter = ['==', 'c28992r100', id];
        map.setPaintProperty('iso_viz', 'fill-color', '#3182bd');
        map.setPaintProperty('iso_viz', 'fill-opacity', 0.4);
        map.setFilter('iso_viz', filter);

        }  
});

map.on('zoom', function() {
  var zoom = map.getZoom();
  // console.log(zoom)
  if (zoom <= 14) { // change 10 to the desired zoom level
    map.setLayoutProperty('poi-labels', 'visibility', 'none');
  } else if (map.getLayoutProperty('poi', 'visibility') === 'visible')
{
       map.setLayoutProperty('poi-labels', 'visibility', 'visible');

  }
});

});
