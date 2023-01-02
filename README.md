# Civ Prodject

## Overview
This repo creates a interactive web app to play an online version of the Civilization Board game. 

The app is hosted through [Heroku](https://www.heroku.com) using a [flask](https://www.fullstackpython.com/flask.html) framework.

The game logic is written in Python and states are stored in an SQL server hosted through Heroku.

The game board/map is drawn using [Leaflet](https://leafletjs.com/), open source mapping library for javascript.

The territories' styling layers are drawn by hand and converted to geojson using [geojson.io](https://geojson.io/#map=2/0/20).