import pymysql.cursors
import geojson
from jellyfish import soundex

connection = pymysql.connect(host='35.187.55.190',
                             user='candidate',
                             password='Fbps9Y7MhKQa4XPxjYo8',
                             db='test',
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `data` INNER JOIN `data_at_coordinate` ON `data`.id = `data_at_coordinate`.id_data " \
              "INNER JOIN `coordinates` ON `coordinates`.id = `data_at_coordinate`.id_coordinate " \
              "WHERE `score` >= 0.5 AND (`pokemon` SOUNDS LIKE 'Bulbasaur' " \
              "OR `pokemon` SOUNDS LIKE 'Charmander' OR `pokemon` SOUNDS LIKE 'Squirtle')"
        cursor.execute(sql)
        result = cursor.fetchall()

        features = []
        for row in result:
            point = geojson.Point((row['longitude'], row['latitude']))

            if soundex(row['pokemon']) == soundex("Bulbasaur"):
                row['pokemon'] = "Bulbasaur"
            elif soundex(row['pokemon']) == soundex("Charmander"):
                row['pokemon'] = "Charmander"
            elif soundex(row['pokemon']) == soundex("Squirtle"):
                row['pokemon'] = "Squirtle"
            features.append(geojson.Feature(geometry=point, properties={"Pokemon": row['pokemon'].upper(),
                                                                        "Score": row['score']}))

        feature_collection = geojson.FeatureCollection(features)
        with open('points.geojson', 'w') as f:
            geojson.dump(feature_collection, f)

finally:
    connection.close()