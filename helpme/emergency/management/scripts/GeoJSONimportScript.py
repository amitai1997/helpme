import json

from django.contrib.gis.geos import GEOSGeometry

from helpme.emergency.models import CustomMap

# Replace 'your_geojson_file.geojson' with the path to your GeoJSON file.
with open("/app/helpme/emergency/static/maps/stanford-ch107xc0728-geojson.json") as f:
    data = json.load(f)

for feature in data["features"]:
    geometry = GEOSGeometry(json.dumps(feature["geometry"]))
    properties = feature["properties"]
    CustomMap.objects.create(geom=geometry, **properties)
