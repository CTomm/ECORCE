from flask import Flask, request, render_template
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


@app.route('/handle_data', methods=['POST'])
def handle_data():
    poulet = request.form['Q3_poulet']
    #Récupérer toutes les valeurs du questionnaire
    #Calculer les émissions totales
    #Envoyer le résultat à psql
    # conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    # cursor = conn.cursor()
    # cursor.execute("""
    #         update utilisateur set conso = 4000
    #         where id = """ + poulet
    #         )
    # conn.commit()
    #conn.close()
    #return render_template("wait.html")


    #ALIMENTATION

    #FIXE
    alimfixe = 282.72608
    if request.form['Q2'] == 'A'
        leg = 44.82296
    leg = 267.98408

    #VARIABLE
    lait = 52.53948708*int(request.form['Q7'])

    oeufs = 11.10564 #VAR
    poisson = 22.78607013 #VAR
    poulet = 28.34551491 #VAR
    porc = 34.90253149 #VAR
    agneau = 334.2929584 #VAR
    boeuf = 235.1966514 #VAR
    fromage = 356.72 #VAR

    #ENERGIE
    elect = 696 #VAR
    fioul = 275 #VAR
    bois = 13 #VAR
    gaz = 230  #VAR

    #TRANSPORTS

    voit_s = 9560.2
    return str(lait)




app.run(host='0.0.0.0', port='5000')