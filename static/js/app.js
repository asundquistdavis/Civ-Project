init();

d3.json('/static/assets/territories.geojson').then(territories => d3.json('/static/assets/board.geojson').then(boardCoords => map(territories, boardCoords)));

console.log('here');

let player = 'Andrew'

let board;

let geojson;

// run at start
// populates html for all cards
function init() {
    populateTerritoriesCard();
};

// populates the html for the territories card
async function populateTerritoriesCard(territory) {
    
    let div = d3.select('div#territoryInfo');

    let html = '';

    if (territory) {

        let territoryName = territory.properties.name;

        let players = await d3.json('/static/assets/playertestdata.json');
        players = players['players'].filter(player=>player['territories'].map(territory=>territory['name']).includes(territoryName));

        html += `<h3>${territoryName}</h3>`;

        switch (players.length) {
            case 1:
                let units = players[0]['territories'].filter(_territory=>_territory['name']==territoryName)[0]['units'];
                let city = players[0]['territories'].filter(_territory=>_territory['name']==territoryName)[0]['city'];
                html += `<p>Owner: ${players[0]['name']} with ${units? units: 0} units${city? ' and a city':''}. </p>`;
                break;
            case 0:
                html += '<p>Unoccupied</p>';
                break;
            default:
                html += `<p>Contested</p>`;
                for (i=0; i<players.length; i++) {
                    let units = players[i]['territories'].filter(_territory=>_territory['name']==territoryName)[0]['units'];
                    let city = players[i]['territories'].filter(_territory=>_territory['name']==territoryName)[0]['city'];
                    html += `<p>${players[i]['name']} with ${units? units: 0} units${city? ' and a city':''}. </p>`;
                };
                break;
        
        };

    // if a territory is not provided
    } else {

        html =+ '<h3>Select a Territory</h3>';
    };

    div.html(html);

};


// assigns color to territory based on support (type=land), or blues (type=water/ocean) and defaults to grey 
function featureColor(properties) {
    let type = properties.type;
    switch (type) {
        case 'land':
            let support = properties.support? properties.support: 0;
            return support == 0 ? 'white':
                   support == 1 ? 'orange':
                   support == 2 ? 'yellow':
                   support == 3 ? 'lightgreen':
                   support == 4 ? 'darkgreen':
                                  'grey';
        case 'water':
            return '#5050F5';
        case 'ocean':
            return '#1010FF';
        default:
            return 'gray';
    };
};

// set as default style for each feature
function style(feature) {
    return {
        fillColor: featureColor(feature.properties),
        fillOpacity: 0.2,
        weight: 3,
        opacity: 1,
        color: 'black'
    };
};

// called on mouse over event
function highlightFeature(event) {
    var layer = event.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    layer.bringToFront();
};

// called on mouse out event
function resetHighlightFeature(event) {
    geojson.resetStyle(event.target);
};

// called on click event
function showFeature(event) {
    board.fitBounds(event.target.getBounds());
    populateTerritoriesCard(event.target.feature)
};

// adds listener to each feature
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlightFeature,
        click: showFeature
    });
};

// draws map + tile layer w/ attribution + geojson layer with event listeners
function map(territories, boardCoords) {

    let mapBounds = boardCoords['geometry']['coordinates'][0].slice(0, 4).map(coor => [coor[1], coor[0]]);

    board = L.map('board', {maxBounds: mapBounds, maxBoundsViscosity: 1}).setView([38.52, 42.74], 6)
    // .fitBounds(mapBounds);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {maxZoom: 8, minZoom: 6, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>'}).addTo(board);

    geojson = L.geoJson(territories, {style: style, onEachFeature: onEachFeature}).addTo(board);

    // console.log(mapCoords);
};