from dotenv import load_dotenv
import requests
import tarfile
import time
import os


load_dotenv()


token = os.getenv('MAPBOX_ACCESS_TOKEN')
url = os.getenv('ALERT_SHAPEFILE_URL')
local_filename = 'current_all.tar.gz'
start = time.perf_counter()

with requests.get(url, stream=True) as r:     # NOTE the stream=True parameter
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        print('Downloading')
        for chunk in r.iter_content(chunk_size=8192):
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            #if chunk:
            f.write(chunk)
print(f'Downloaded {time.perf_counter() - start}')

with tarfile.open(local_filename, "r:gz") as tar:
    tar.extractall(path='current_all')
print(f'Extracted {time.perf_counter() - start}')

if os.path.exists(local_filename):
    os.remove(local_filename)

print(os.listdir())

# import convert
# os.system('pip install fiona')
os.system('fio cat current_all/current_all.shp > current_all.geojson.ld')
print(f'Converted {time.perf_counter() - start}')

os.system(f'tilesets upload-source joshphillips43 current_all current_all.geojson.ld --replace --token {token}')
os.system(f'tilesets publish joshphillips43.current_all --token {token}')
print(f'{time.perf_counter() - start}')
