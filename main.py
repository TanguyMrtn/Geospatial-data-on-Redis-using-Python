"""
@author: TanguyMrtn
"""

import overpy
import redis

r = redis.Redis(port=6379) # Redis connexion

api = overpy.Overpass() # Overpass API
    
# Query to get geospatial data from OpenStreetMap
request = api.query("""
area["ISO3166-2"="FR-74"][admin_level=6];
(
  node[place~"^(city|town|village)$"](area);
);
out center;
""")

# We only take city name, longitude and latitude
cities  = []
cities += [(node.tags["name"],float(node.lon), float(node.lat)) for node in request.nodes]

# Add cities in Redis
for city in cities :
    r.geoadd("cities",city[2],city[1],city[0])

# Get cities in a 6km radius around Annecy
request = r.georadiusbymember("cities","Annecy", 6, unit="km")

print(request)