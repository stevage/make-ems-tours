/* jshint esnext: true */
var jsonfile = require('jsonfile');
var glob = require('glob-fs')();

var out = {
    type: 'FeatureCollection',
    features: []
};

glob.readdirSync('tmp/*.json', {}).forEach(filename => {
    try {
        var obj = jsonfile.readFileSync(filename);
        //console.log (`${filename} -> ${obj.features.length}`);
        obj.features.forEach(feature => {
            feature.properties = obj.features[0].properties; // all features have some props
            // this type coersion should be done in geojson-props.py
            feature.properties.Year = Number(feature.properties.Year);
            feature.properties.Participants = Number(feature.properties.Participants);
            //var p = obj.features[0].properties;
            /*feature.properties = {
                name: p.name,
                year: Number(p.year),
                desc: p.desc,
                ppl: Number(p.ppl)
            };*/
            console.log(obj.features[0].properties.Participants);
        });
        out.features.push(...obj.features);
    } catch (err) {
        console.error(err);
    }
});

jsonfile.writeFileSync('out/cycletours.geojson', out);
