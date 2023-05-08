import fiona
import geojson

# Define the input and output file paths
input_file = 'current_all/current_all.shp'
output_file = 'current_all.geojson.ld'

# Open the input shapefile and get the first layer
with fiona.open(input_file) as src:

    # Define the output schema as GeoJSON-LD
    output_schema = {
        'geometry': src.schema['geometry'],
        'properties': src.schema['properties'],
        'id': 'str',
        'type': 'str',
        '@context': {
            'id': '@id',
            'type': '@type',
            'geojson': 'http://ld.geojson.org/vocab#',
            'Feature': 'geojson:Feature',
            'Point': 'geojson:Point',
            'MultiPoint': 'geojson:MultiPoint',
            'LineString': 'geojson:LineString',
            'MultiLineString': 'geojson:MultiLineString',
            'Polygon': 'geojson:Polygon',
            'MultiPolygon': 'geojson:MultiPolygon',
            'coordinates': 'geojson:coordinates'
        }
    }

    # Open the output file and write the features as GeoJSON-LD
    with open(output_file, 'w') as dst:
        for feature in src:
            feature['type'] = 'Feature'
            feature['id'] = feature['id'] or feature['properties'].get('id')
            feature['@context'] = output_schema['@context']
            geojson.dump(feature, dst, indent=None, sort_keys=True)
            dst.write('\n')
