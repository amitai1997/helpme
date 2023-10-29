import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from helpme.emergency.models import GeoJSONFeature


class Command(BaseCommand):
    help = "Import GeoJSON data into the database"

    def add_arguments(self, parser):
        parser.add_argument("geojson_file", type=str, help="Path to the GeoJSON file")

    def handle(self, *args, **kwargs):
        geojson_file = kwargs["geojson_file"]
        with open(geojson_file) as f:
            data = json.load(f)
            features = data["features"]

            for feature in features:
                geometry = GEOSGeometry(json.dumps(feature["geometry"]))
                feature_id = feature["id"]

                # Check if a feature with the same id already exists
                existing_feature, created = GeoJSONFeature.objects.get_or_create(feature_id=feature_id)

                # If the feature with the same id doesn't exist, create it
                if created:
                    # Extract properties
                    properties = feature["properties"]
                    iso = properties["iso"]
                    name_0 = properties.get("name_0")
                    id_1 = properties.get("id_1")
                    name_1 = properties.get("name_1")
                    hasc_1 = properties.get("hasc_1")
                    ccn_1 = properties.get("ccn_1")
                    cca_1 = properties.get("cca_1")
                    type_1 = properties.get("type_1")
                    engtype_1 = properties.get("engtype_1")
                    nl_name_1 = properties.get("nl_name_1")
                    varname_1 = properties.get("varname_1")

                    # Create a GeoJSONFeature object with the parsed data
                    geojson_feature = GeoJSONFeature(
                        geometry=geometry,
                        feature_id=feature_id,
                        iso=iso,
                        name_0=name_0,
                        id_1=id_1,
                        name_1=name_1,
                        hasc_1=hasc_1,
                        ccn_1=ccn_1,
                        cca_1=cca_1,
                        type_1=type_1,
                        engtype_1=engtype_1,
                        nl_name_1=nl_name_1,
                        varname_1=varname_1,
                    )
                    geojson_feature.save()

        self.stdout.write(self.style.SUCCESS("GeoJSON data imported successfully"))
