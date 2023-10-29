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
                geometry_data = feature["geometry"]
                feature_id = feature["id"]

                try:
                    # Attempt to create a GEOSGeometry object
                    geometry = GEOSGeometry(json.dumps(geometry_data))
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Skipping feature with feature_id {feature_id} due to invalid geometry: {str(e)}"
                        )
                    )
                    continue

                # Check if a feature with the same id already exists
                existing_feature = GeoJSONFeature.objects.filter(feature_id=feature_id).first()

                if existing_feature:
                    # If the feature with the same id exists, update its data
                    # Extract properties
                    properties = feature["properties"]
                    iso = properties.get("iso")
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

                    # Update the existing feature with the new data
                    existing_feature.geometry = geometry
                    existing_feature.iso = iso
                    existing_feature.name_0 = name_0
                    existing_feature.id_1 = id_1
                    existing_feature.name_1 = name_1
                    existing_feature.hasc_1 = hasc_1
                    existing_feature.ccn_1 = ccn_1
                    existing_feature.cca_1 = cca_1
                    existing_feature.type_1 = type_1
                    existing_feature.engtype_1 = engtype_1
                    existing_feature.nl_name_1 = nl_name_1
                    existing_feature.varname_1 = varname_1

                    existing_feature.save()
                else:
                    # If the feature doesn't exist, create a new feature
                    # Extract properties
                    properties = feature["properties"]
                    iso = properties.get("iso")
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

                    # Create a new feature with the parsed data
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
