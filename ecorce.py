from flask import Flask, request, render_template, jsonify, session, redirect
import psycopg2

app = Flask(__name__,  template_folder='static')
app.secret_key = "ecorce2020"


@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Welcome to ECORCE</h1>"

@app.route("/sendresultat", methods=['GET'])
def sendresultat():
    position = session.get('position', 'not set')
    emission = session.get('emissions', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
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

@app.route("/sendmoyenne", methods=['GET'])
def sendmoyenne():
    position = session.get('position', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with emissions as (select emission as e from commune where st_intersects(commune.geom, st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154))),
        parc as (select st_transform(geom, 4326) from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), (select e from emissions)))
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(parc.*)::json)
        ) as geojson
        from parc;
        """)
    moyenne = cursor.fetchone()[0]
    conn.close()
    return jsonify(moyenne)


@app.route('/sendposition', methods=['POST'])
def sendposition():
    position_api = request.form['position']
    session['position'] = position_api
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
            create materialized view parctri as select * from get_parctri(st_transform(st_geomfromtext('POINT("""+position_api+""")', 4326), 2154));
            """)
    conn.commit()
    conn.close()
    return render_template("questionchoix.html")


@app.route('/choice', methods=['POST'])
def choice():
    if request.form['Q0'] == 'V':
        return render_template("questionv.html")
    elif request.form['Q0'] == 'Veg':
        return render_template("questionvege.html")
    elif request.form['Q0'] == 'A':
        return render_template("question.html")


@app.route('/omni', methods=['POST'])
def omni():

    #ALIMENTATION

    #FIXE
    alimfixe = 282.72608

    poulet = 28.34551491*float(request.form['Q3_poulet'])
    porc = 34.90253149*float(request.form['Q3_porc'])
    agneau = 334.2929584*float(request.form['Q3_agneau'])
    boeuf = 235.1966514*float(request.form['Q3_boeuf'])
    poisson = 22.78607013*float(request.form['Q4'])
    session['viande']=float(request.form['Q3_poulet'])+float(request.form['Q3_porc'])+float(request.form['Q3_agneau'])+float(request.form['Q3_boeuf'])+float(request.form['Q4'])
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*int(request.form['Q7'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 44.82296
        session['legume']=leg
    else:
        leg = 267.98408
        session['legume']=leg

    #ENERGIE
    session['energie']=0
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
            session['energie']+=int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
            session['energie']+=int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
            session['energie']+=int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
            session['energie']+=int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    session['voiture']=voit_s
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    session['avion']=avion

    emissions = alimfixe+poulet+porc+agneau+boeuf+poisson+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+ tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emissions

    return redirect("http://localhost:8080/HTML_FP.html")

@app.route('/vege', methods=['POST'])
def vege():

    #Alimentation
    alimfixe = 282.72608
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
            elect = 0.696*int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])

    emissions = alimfixe+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emissions
    return redirect("http://localhost:8080/index.html")

@app.route('/vegan', methods=['POST'])
def vegan():

    #Alimentation
    legumineuse = 0.24024*int(request.form['Q1b'])
    cere = 0.58058*int(request.form['Q1c'])


    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 0.17108*int(request.form['Q1a'])
    else:
        leg = 1.02284*int(request.form['Q1a'])

    #ENERGIE
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])

    emissions = leg+legumineuse+cere+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emissions
    return redirect("http://localhost:8080/index.html")
    #return render_template("index.html")
# #A enlever quand on va sur la VM
# #app.run(host='0.0.0.0', port='5000')

@app.route('/change', methods=['POST'])
def change():
    energie= session.get('energie', 'not set')
    new_energie = energie*float(request.form['Q19'])

    legume=session.get('legume', 'not set')
    new_legume=float(request.form['Q7b'])

    viande = session.get('viande', 'not set')
    if request.form['Q0']== 'Veg' :
        new_viande=0
    else:
        new_viande=viande

    voiture= session.get('voiture', 'not set')
    if request.form['Q18']== 'A' :
        voiture= voiture*0.1846
    else:
        new_voiture=voiture

    avion=session.get('avion', 'not set')
    new_avion = request.form['Q17']

    emission=session.get('emissions', 'not set')-energie+new_energie-legume+new_legume-viande+new_viande-voiture+voiture-avion+avion
    emission=float(emission)

    position = session.get('position', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
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

@app.route('/energie', methods=['GET'])
def energie():
    return str(session.get('energie', 'not set'))

@app.route('/legume', methods=['GET'])
def legume():
    return str(session.get('legume', 'not set'))

@app.route('/viande', methods=['GET'])
def viande():
    return str(session.get('viande', 'not set'))

@app.route('/voiture', methods=['GET'])
def voiture():
    return str(session.get('voiture', 'not set'))

@app.route('/avion', methods=['GET'])
def avion():
    return str(session.get('avion', 'not set'))

@app.route('/emission', methods=['GET'])
def emission():
    return str(session.get('emissions', 'not set'))
