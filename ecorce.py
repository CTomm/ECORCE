from flask import Flask, request, render_template, jsonify, session, redirect
import psycopg2

app = Flask(__name__,  template_folder='static')
app.secret_key = "ecorce2020"

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

#Nettoyer la session et la base de données quand l'utilisateur quitte l'application
@app.route('/leaving')
def clear():
    try:
        conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
        cursor = conn.cursor()
        cursor.execute("""
                drop materialized view parctri;
                """)
        conn.commit()
        conn.close()
        return 'Materialized view dropped.'
    except:
        return 'No materialized view.'

#Page d'accueil
@app.route("/")
def welcome():
    return redirect("http://localhost:8080/cover2.html")

#Envoyer les résultats finaux dans la requête Postgres (dans HTML_FP.html)
@app.route("/sendresultat", methods=['POST'])
def sendresultat():
    emission = session.get('emissions', 'not set')
    position = request.form['position']
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    print (emission)
    #return str(emission)
    cursor.execute(""" 
        with results as (select * from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), """+str(emission)+""")),
        dist as (select max(distance) as maxdist, max(total) as total from results),
        uniongeom as (select st_union(geom) as newgeom from results),
        areageom as (select st_area(newgeom) as aire from uniongeom),
        parc as (select maxdist, total, aire, st_transform(newgeom, 4326) from uniongeom, dist, areageom)
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(parc.*)::json)
        ) as geojson
        from parc;
        """)
    resultat = cursor.fetchone()[0]
    conn.close()
    return jsonify(resultat)

#Requêter les moyennes (bouton "moyenne" de HTML_FP.html)
@app.route("/sendmoyenne", methods=['POST'])
def sendmoyenne():
    position = request.form['position']
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with results as (select * from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), 5711.633)),
        dist as (select  max(total) as total from results),
        uniongeom as (select st_union(geom) as newgeom from results),
        areageom as (select st_area(newgeom) as aire from uniongeom),
        parc as (select total, aire, st_transform(newgeom, 4326) from uniongeom, dist, areageom)
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(parc.*)::json)
        ) as geojson
        from parc;
        """)
    moyenne = cursor.fetchone()[0]
    conn.close()
    return jsonify(moyenne)

@app.route("/sendideal", methods=['POST'])
def sendideal():
    position = request.form['position']
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with results as (select * from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), 1500)),
        dist as (select max(total) as total from results),
        uniongeom as (select st_union(geom) as newgeom from results),
        areageom as (select st_area(newgeom) as aire from uniongeom),
        parc as (select total, aire, st_transform(newgeom, 4326) from uniongeom, dist, areageom)
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(parc.*)::json)
        ) as geojson
        from parc;
        """)
    moyenne = cursor.fetchone()[0]
    conn.close()
    return jsonify(moyenne)
    
#Envoyer la position pour trier les parcs (api_adresse.html)
@app.route('/sendposition', methods=['POST'])
def sendposition():
    position = request.form['position']
    print(position)
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
            create materialized view parctri as select * from get_parctri(st_transform(st_geomfromtext('POINT("""+position+""")', 4326), 2154));
            """)
    conn.commit()
    conn.close()
    return position


#Choisir son type d'alimentation (bouton "Suite du questionnaire" de questionchoix.html)
@app.route('/choice', methods=['POST'])
def choice():
    if request.form['Q0'] == 'V':
        return render_template("questionv.html")
        session['regime'] = 'Vegan'
    elif request.form['Q0'] == 'Veg':
        return render_template("questionvege.html")
        session['regime'] = 'Vege'
    elif request.form['Q0'] == 'A':
        return render_template("question.html")
        session['regime'] = 'Omni'


#Récupérer réponse questionnaire et envoyer la requête (dans question.html)
@app.route('/omni', methods=['POST'])
def omni():

    #ALIMENTATION

    #FIXE
    alimfixe = 282.72608

    poulet = 214.4*float(request.form['Q3_poulet'])
    porc = 304.2*float(request.form['Q3_porc'])
    agneau = 1451.32*float(request.form['Q3_agneau'])
    boeuf = 1493.96*float(request.form['Q3_boeuf'])
    poisson = 22.78607013*float(request.form['Q4'])
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*int(request.form['Q7'])

    # #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 1.834*0.17108
    else:
        leg = 1.834*1.02284
    alimentation = alimfixe + poulet + porc + agneau + boeuf + poisson + oeufs + fromage + lait + leg
    # #ENERGIE
    if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
    if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
    if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
    if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
    energie = elect + bois + fioul + gaz
    session['energie'] = energie

    # #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])

    transport = tc_s + voit_s + train +train + voit_annee + car + avion

    emission = alimfixe+poulet+porc+agneau+boeuf+poisson+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+ tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emission

    return render_template("HTML_FP.html", alimentation = str(alimentation), energie = str(energie), transport = str(transport))

#Récupérer réponse questionnaire et envoyer la requête (dans questionvege.html)
@app.route('/vege', methods=['POST'])
def vege():

    #Alimentation
    alimfixe = 282.72608
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*float(request.form['Q7'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 1.834*0.17108
    else:
        leg = 1.834*1.02284
    alimentation = alimfixe + oeufs + fromage + lait + leg



    # #ENERGIE
    if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
    if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
    if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
    if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
    energie = elect + bois + fioul + gaz
    session['energie'] = energie

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    print(voit_s)
    voiture = int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    transport = tc_s + voit_s + train +train + voit_annee + car + avion

    emission = alimfixe+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emission
    return render_template("HTML_FP.html", alimentation = str(alimentation), energie = str(energie), transport = str(transport))

#Récupérer réponse questionnaire et envoyer la requête (dans questionv.html)
@app.route('/vegan', methods=['POST'])
def vegan():
    #Alimentation
    legumineuse = 0.24024*float(request.form['Q1b'])
    cere = 0.58058*float(request.form['Q1c'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 0.17108*float(request.form['Q1a'])
    else:
        leg = 1.02284*float(request.form['Q1a'])
    alimentation = legumineuse + cere + leg


    # #ENERGIE
    if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
    if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
    if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
    if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
    energie = elect + bois + fioul + gaz

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    voiture = int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    transport = tc_s + voit_s + train +train + voit_annee + car + avion


    emission = leg+legumineuse+cere+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emission
    return render_template("HTML_FP.html", alimentation = str(alimentation), energie = str(energie), transport = str(transport))


#Changer ses résultats (bouton "nouvelles valeurs" de HTML_FP.html)
@app.route('/change', methods=['POST'])
def change():
    energie = float(request.form['energie'])
    new_energie = energie*float(request.form['new_energie'])

    legume = float(request.form['legume'])
    new_legume=legume*float(request.form['new_legume'])

    new_avion = int(request.form['new_avion'])
    avion = int(request.form['avion'])

    # print(request.form['viande'])
    viande = float(request.form['viande'])
    if request.form['regime']== 'Veg' :
        new_viande=0
    elif request.form['regime']== 'V' :
        new_viande=0        
    elif request.form['regime']== 'A' :
        if viande == 0:
            new_viande = 964.393612 #poisson y compris
        else:
            new_viande=viande

    voiture= int(request.form['voiture'])*9.5602
    if request.form['new_voiture']== 'A' :
        new_voiture= int(request.form['voiture'])*0.1846
    else:
        new_voiture=int(request.form['voiture'])*9.5602

    emission = session.get('emissions', 'not set')

    alimentation = float(request.form['alim'])-legume+new_legume-viande+new_viande
    energie = session.get('energie')+new_energie
    transport = float(request.form['transport'])-voiture+new_voiture-avion+new_avion

    emission=emission-session.get('energie')+new_energie-legume+new_legume-viande+new_viande-voiture+new_voiture-avion+new_avion

    if session.get('regime') == 'Vegan':
        emission +=343.155904
        #print('add laitage')
        
    #print(emission)
    emission=float(emission)
    mydict = {'alim' :alimentation, 'transport' :transport, 'energie' :energie, 'emission': emission}
    return jsonify(mydict)

@app.route('/getchangeresults', methods=['POST'])
def getchangeresults():
    position = request.form['position']
    emission = request.form['emission']
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with new_parc as (select st_transform(st_union(geom), 4326) from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), """+str(emission)+"""))
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(new_parc.*)::json)
        ) as geojson
        from new_parc;
        """)
    resultat = cursor.fetchone()[0]
    conn.close()
    return jsonify(resultat)

@app.route('/getemissionmoy', methods=['POST'])
def getemissionmoy():
    position = request.form['position']
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with commune_indiv as (select hab, emission, nom, st_transform(geom, 4326) from commune where st_intersects(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), geom))
        select json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(ST_AsGeoJSON(commune_indiv.*)::json)
        ) as geojson
        from commune_indiv;
        """)
    moyenne = cursor.fetchone()[0]
    conn.close()
    return jsonify(moyenne)



#app.run(host='0.0.0.0', port=8080, debug=True)