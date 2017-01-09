This repo contains scripts for generating the map data for https://stevage.github.io/ems-tours. Scripts in, for no good reason, Bash, NodeJS *and* Python.

1. convert-tracks-and-routes.sh: convert all GPX files in a directory into GeoJSON files.
2. geojson-props.py: mash those GeoJSON files up with a Google Sheet, adding properties to the files.
3. combine.js: merge all the GeoJSON files.

There's currently an unautomated step 4: upload out/cycletours.geojson to Mapbox.

### Prerequsites
Python: Install whatever it says at the top of the Python script.
NodeJS: npm install

