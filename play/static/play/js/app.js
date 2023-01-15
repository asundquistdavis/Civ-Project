init();

let player = 'Andrew'

let board;

let territoriesLayer;

let fromTerritory;

let moveUnits;

let toTerritory;

let moveTerritoriesLayer;

let moves = [];

d3.json('/play/territories').then(territories => d3.json('/play/board').then(boardCoords => {
    map(territories, boardCoords)
}));

// run at start
// populates html for all cards
function init() {
    populateTerritoriesCard();
};

function moveTo(territory) {
    toTerritory = territory;
    moves.push({'from': fromTerritory, 'to': toTerritory, 'units': moveUnits});
    board.removeLayer(moveTerritoriesLayer);
    populateTerritoriesCard(fromTerritory);
};

function moveStyle(feature) {
    return {
        fillColor: featureColor(feature.properties),
        fillOpacity: 0.7,
        weight: 5,
        opacity: 1,
        color: 'black'
    };
};

function moveToListener(feature, layer) {
    layer.on({
        click: event => moveTo(event.target.feature.properties.name)
    })
};

async function moveFrom(_fromTerritory, _moveUnits) {
    fromTerritory = _fromTerritory;
    moveUnits = _moveUnits;
    let territories = await d3.json('/static/assets/territories.geojson');
    let adjacentTerritories = territories['features'].filter(territory=>territory['properties']['adjacent'].includes(fromTerritory));
    let movableTerritories = [];
    for (i=0; i<adjacentTerritories.length; i++) {
        if (adjacentTerritories[i].properties.type=='land') {
            movableTerritories.push(adjacentTerritories[i])
        };
    };

    moveTerritoriesLayer = L.geoJson(movableTerritories, {style: moveStyle, onEachFeature: moveToListener}).addTo(board) 
};

// populates the html for the territories card
async function populateTerritoriesCard(territory) {

    let div = d3.select('div#territoryInfo');

    let html = '';

    if (territory) {

        let players = await d3.json('/static/assets/playertestdata.json');
        players = players['players'].filter(player=>player['territories'].map(territory=>territory['name']).includes(territory));

        html += `<h3>${territory}</h3>`;

        switch (players.length) {
            case 1:
                let startingUnits = players[0]['territories'].filter(_territory=>_territory['name']==territory)[0]['units'];
                let city = players[0]['territories'].filter(_territory=>_territory['name']==territory)[0]['city'];
                let fromUnits = moves.filter(move=>move.from==territory).map(move=>move.units).reduce((a, b) => parseInt(a) + parseInt(b), 0);
                let toUnits = moves.filter(move=>move.to==territory).map(move=>move.units).reduce((a, b) => parseInt(a) + parseInt(b), 0);
                let units = startingUnits-fromUnits;
                console.log(fromUnits)
                html += `<p><b>Owner:</b> ${players[0]['name']} with ${units? units: 0} units avialable to move${fromUnits>0?' ('+String(fromUnits)+' leaving)':''}${(toUnits>0 && players[0]['name'] == player)? ' ('+String(toUnits)+' entering)':''}${city? ' and a city':''}. </p>`;
                if (players[0]['name']==player) {
                    html += `<button onclick="moveFrom('${territory}', d3.select('input#unitsToMove').node().value)">Move</button><input type="number" id="unitsToMove" min="1" max="${units? units: 0}" value="1"></input>`
                };
                break;
            case 0:
                html += '<p>Unoccupied</p>';
                break;
            default:
                html += `<p><b>Contested</b></p>`;
                for (i=0; i<players.length; i++) {
                    let units = players[i]['territories'].filter(_territory=>_territory['name']==territory)[0]['units'];
                    let city = players[i]['territories'].filter(_territory=>_territory['name']==territory)[0]['city'];
                    html += `<p>${players[i]['name']} with ${units? units: 0} units${city? ' and a city':''}. </p>`;
                };
                break;
        
        };

    // if a territory is not provided
    } else {
        html = '<h3>Select a Territory</h3>';
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
    territoriesLayer.resetStyle(event.target);
};

// called on click event
function showFeature(event) {
    board.fitBounds(event.target.getBounds());
    populateTerritoriesCard(event.target.feature.properties.name)
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

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {maxZoom: 8, minZoom: 6, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attribution">CARTO</a>'}).addTo(board);

    territoriesLayer = L.geoJson(territories, {style: style, onEachFeature: onEachFeature}).addTo(board);

};

// var socket = io();
// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });