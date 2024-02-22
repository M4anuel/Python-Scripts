import json
import requests
import tokens

# csgoskins.gg api token: 8HYFXQTStviT2nMUmE6A9RGgmF5yOvJ1hZaX8nAj https://csgoskins.gg/api/v1/prices

api_key = tokens.CSGOGG_KEY
r = requests.get("https://csgoskins.gg/api/v1/prices",
                 headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'}).json()
parsed = json.loads(r)
print(json.dumps(parsed, indent=4, sort_keys=True))

print(r)
