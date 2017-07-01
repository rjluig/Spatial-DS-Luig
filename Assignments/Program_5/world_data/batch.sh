mongoimport --db world_data --collection airports --type json --file airports_geo_json.json --jsonArray
mongoimport --db world_data --collection cities --type json --file city_locations_geo_json.json --jsonArray
mongoimport --db world_data --collection countries --type json --file countries_geo_json.json --jsonArray
mongoimport --db world_data --collection earthquakes --type json --file earthquakes_geo_json.json --jsonArray
mongoimport --db world_data --collection states --type json --file states_geo_json.json --jsonArray
mongoimport --db world_data --collection volcanos --type json --file volcanos_geo_json.json --jsonArray
