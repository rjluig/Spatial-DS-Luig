#Program 5
Query1.py Query2.py and Query3.py use a mongodb call world data and they and uses the 
collections 'airports', 'earthquakes', 'meteorites'  and 'volcanos'.

in the world_data folder theres a batch.sh file used to load all the json files into the data base.
from from a terminal inside the world_data folder run './batch.sh' to load the files.

##Examples
#Query1
python3 query1.py [airport_code] [airport_code2] [distance]
python3 query1.py DAL LVN 500
python3 query1.py DAL TBG 500

#Query2
python3 query2.py [collection] [field] [value] [min/max] [max_results] [radius] [[lat,lon]]
python3 query2.py earthquakes mag 5 min 100 500 [-122,37]
python3 query2.py volcanos Altitude 0 min 100 500 [-155,19]
python3 query2.py earthquakes mag 5 min 100 500 [139,35]

#Query3
python3 query3.py [field] [min_pts] [eps]
python3 query3.py volcanos 15 10

earthquakes and meteorites take a long time


