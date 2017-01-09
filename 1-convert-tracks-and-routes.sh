#!/bin/bash
rm *.json
pushd ..
for file in *.gpx ; do 
    for layer in routes tracks ; do 
        echo $file $layer > /dev/stderr
        echo -n "$file $layer " &&
        ogr2ogr -f csv /dev/stdout "$file" -sql "select count(*) from $layer" |
        awk 'NR>1'
    done
done | awk '$3' > /tmp/layers.tmp
popd
while read f l j ; do
  echo "Loading $f $l" > /dev/stderr
  ogr2ogr -f GeoJSON tmp/"${f%.gpx}.json" "../${f}" $l 
done < /tmp/layers.tmp
