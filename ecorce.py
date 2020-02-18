from flask import Flask, request, render_template, jsonify, session
import psycopg2

app = Flask(__name__)
<<<<<<< HEAD
=======
Session(app)
>>>>>>> 26da9dd7952373932bb8c4ddb8db3d6a748f2b65
app.secret_key = "ecorce2020"

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Welcome to ECORCE</h1>"

@app.route("/sendresultat")
def sendresultat():
    position = session.get('position', 'not set')
    emission = session.get('emissions', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
<<<<<<< HEAD
        with parc as (select st_transform(geom, 4326) from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), """+str(emission)+"""))
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(parc.*)::json)
        ) as geojson
        from parc;
        """)
    resultat = cursor.fetchone()[0]
    conn.close()
    return jsonify(resultat)
    # cursor.execute("""
    # create view parcproche as select * from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), """+str(emission)+""")
    # """)
    # conn.commit()
    # conn.close()
    # return 'go to qgis'


@app.route('/sendposition', methods=['POST'])
def sendposition():
    position = request.form['position']
    session['position'] = position
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
            create materialized view parctri as select * from get_parctri(st_transform(st_geomfromtext('POINT("""+position+""")', 4326), 2154));
            """)
    conn.commit()
    conn.close()
    return render_template("wait.html")

=======
            select json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(ST_AsGeoJSON(utilisateur.*)::json)
            ) as geojson
            from utilisateur
            """)
    test = cursor.fetchone()[0]
    return jsonify(test)

@app.route('/myvalue')
def test():
    my_var = session.get('emissions', None)
    return str(my_var)
>>>>>>> 26da9dd7952373932bb8c4ddb8db3d6a748f2b65

@app.route('/handle_data', methods=['POST'])
def handle_data():
    #poulet = request.form['Q3_poulet']
    #Récupérer toutes les valeurs du questionnaire
    #Calculer les émissions totales
    #Envoyer le résultat à psql
    # conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="postgres")
    # cursor = conn.cursor()
    # cursor.execute("""
    #         update utilisateur set conso = 4000
    #         where id = 3"""
    #         )
    # conn.commit()
    # conn.close()
    #return render_template("wait.html")


    #ALIMENTATION

    #FIXE
    alimfixe = 282.72608

    #VARIABLE  
    poulet = 28.34551491*float(request.form['Q3_poulet'])
    porc = 34.90253149*float(request.form['Q3_porc'])
    agneau = 334.2929584*float(request.form['Q3_agneau'])
    boeuf = 235.1966514*float(request.form['Q3_boeuf'])
    poisson = 22.78607013*float(request.form['Q4'])
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*int(request.form['Q7'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 44.82296
    else:
        leg = 267.98408

    #ENERGIE
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 696*int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 230*int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 275*int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 13*int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13']) #Multiplier passager
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15']) #Multiplier passager
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])

    emissions = alimfixe+poulet+porc+agneau+boeuf+poisson+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+ tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emissions
    return render_template("wait.html")


#A enlever quand on va sur la VM
app.run(host='0.0.0.0', port='5000')