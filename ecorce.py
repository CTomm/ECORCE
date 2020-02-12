from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Welcome to ECORCE</h1>"

@app.route("/test")
def user():
	conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
	cursor = conn.cursor()
	cursor.execute("""
            select json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(user84.*)::json)
            ) as geojson
            from user84
            """)
	return cursor.fetchone()[0]
