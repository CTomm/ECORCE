from flask import Flask, request, render_template, jsonify, session, redirect
import psycopg2

app = Flask(__name__,  template_folder='static')
app.secret_key = "ecorce2020"

position = '0'
emission = 0
viande = 0
avion = 0
legume = 0
voiture = 0
energie = 0

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

#Nettoyer la session et la base de données quand l'utilisateur quitte l'application
@app.route('/leaving')
def clear():
    #session.clear()
    print(session)
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
            drop materialized view parctri;
            """)
    conn.commit()
    conn.close()
    return 'App closed.'

#Page d'accueil
@app.route("/")
def welcome():
    #session.clear()
    return redirect("http://localhost:8080/cover.html")

#Envoyer les résultats finaux dans la requête Postgres (dans HTML_FP.html)
@app.route("/sendresultat", methods=['GET'])
def sendresultat():
    global position
    #print('on send resultat : '+ str(session))
    # position = session.get('position', 'not set')
    # emission = session.get('emissions', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with parc as (select st_transform(st_union(geom), 4326) from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), """+str(emission)+"""))
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
@app.route("/sendmoyenne", methods=['GET'])
def sendmoyenne():
    global position
    #position = session.get('position', 'not set')
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute(""" 
        with parc as (select st_transform(st_union(geom), 4326) from get_parcproche(st_transform(st_geomfromtext('POINT("""+str(position)+""")', 4326), 2154), 3104.67))
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
    global position
    #position_api = request.form['position']
    position = request.form['position']
    #session['position'] = position_api
    #print('on send position : '+ str(session))
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="geonum2020")
    cursor = conn.cursor()
    cursor.execute("""
            create materialized view parctri as select * from get_parctri(st_transform(st_geomfromtext('POINT("""+position+""")', 4326), 2154));
            """)
    conn.commit()
    conn.close()
    return 'ok'


#Choisir son type d'alimentation (bouton "Suite du questionnaire" de questionchoix.html)
@app.route('/choice', methods=['POST'])
def choice():
    #print('on choice : '+ str(session))
    if request.form['Q0'] == 'V':
        #session["regime"] = "V"
        return render_template("questionv.html")
    elif request.form['Q0'] == 'Veg':
        return render_template("questionvege.html")
    elif request.form['Q0'] == 'A':
        return render_template("question.html")


#Récupérer réponse questionnaire et envoyer la requête (dans question.html)
@app.route('/omni', methods=['POST'])
def omni():
    global viande, avion, emission, energie, voiture, legume
    emission = 0
    viande = 0
    avion = 0
    legume = 0
    voiture = 0
    energie = 0

    #ALIMENTATION

    #FIXE
    alimfixe = 282.72608

    poulet = 28.34551491*float(request.form['Q3_poulet'])
    porc = 34.90253149*float(request.form['Q3_porc'])
    agneau = 334.2929584*float(request.form['Q3_agneau'])
    boeuf = 235.1966514*float(request.form['Q3_boeuf'])
    poisson = 22.78607013*float(request.form['Q4'])
    viande = 52*(float(request.form['Q3_poulet'])+float(request.form['Q3_porc'])+float(request.form['Q3_agneau'])+float(request.form['Q3_boeuf'])+float(request.form['Q4']))
    #session['qteviande']=52*(float(request.form['Q3_poulet'])+float(request.form['Q3_porc'])+float(request.form['Q3_agneau'])+float(request.form['Q3_boeuf'])+float(request.form['Q4']))
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*int(request.form['Q7'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 1.834*0.17108
        legume = 1.834
        #session['legume']=1.834
    else:
        leg = 1.834*1.02284
        legume = 1.834
        #session['legume']=1.834

    #ENERGIE
    #session['energie']=0
    energie = 0
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
            #session['energie']+=int(request.form['Q9_electrique'])
            energie +=int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
            #session['energie']+=int(request.form['Q9_gaz'])
            energie +=int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
            #session['energie']+=int(request.form['Q9_fioul'])
            energie +=int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
            #session['energie']+=int(request.form['Q9_bois'])
            energie +=int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    voiture = int(request.form['Q13'])
    #session['voiture']=int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    #session['avion']=avion

    emission = alimfixe+poulet+porc+agneau+boeuf+poisson+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+ tc_s+voit_s+train+voit_annee+car+avion
    #session['emissions'] = emissions
    print('on questionnaire : ' + str(session))

    return render_template("HTML_FP.html")

#Récupérer réponse questionnaire et envoyer la requête (dans questionvege.html)
@app.route('/vege', methods=['POST'])
def vege():
    global avion, emission, energie, voiture, legume, viande
    emission = 0
    viande = 0
    avion = 0
    legume = 0
    voiture = 0
    energie = 0

    print('on vege : ' + str(session))
    #Alimentation
    alimfixe = 282.72608
    oeufs = 11.10564*int(request.form['Q5'])
    fromage = 356.72*float(request.form['Q6'])
    lait = 52.53948708*int(request.form['Q7'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 1.834*0.17108
        legume = 1.834
        #session['legume']=1.834
    else:
        leg = 1.834*1.02284
        legume = 1.834
        #session['legume']=1.834

    #session['viande'] = 0
    #Energie

    #ENERGIE
    #session['energie']=0
    energie = 0
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
            #session['energie']+=int(request.form['Q9_electrique'])
            energie +=int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
            #session['energie']+=int(request.form['Q9_gaz'])
            energie +=int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
            #session['energie']+=int(request.form['Q9_fioul'])
            energie +=int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
            #session['energie']+=int(request.form['Q9_bois'])
            energie +=int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    voiture = int(request.form['Q13'])
    #session['voiture']=int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    #session['avion']=avion

    emission = alimfixe+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    #session['emissions'] = emissions
    return render_template("HTML_FP.html")

#Récupérer réponse questionnaire et envoyer la requête (dans questionv.html)
@app.route('/vegan', methods=['POST'])
def vegan():
    global avion, emission, energie, voiture, legume, viande
    emission = 0
    viande = 0
    avion = 0
    legume = 0
    voiture = 0
    energie = 0
    #print("on vegan : " + str(session))
    #Alimentation
    legumineuse = 0.24024*int(request.form['Q1b'])
    cere = 0.58058*int(request.form['Q1c'])

    #Légumes de saison ou pas
    if request.form['Q7b'] == 'A':
        leg = 0.17108*int(request.form['Q1a'])
        legume = int(request.form['Q1a'])
        #session['legume']=int(request.form['Q1a'])
    else:
        leg = 1.02284*int(request.form['Q1a'])
        legume = int(request.form['Q1a'])
        #session['legume']=int(request.form['Q1a'])

    #session['viande'] = 0
    #Energie
    #session['energie']=0
    energie = 0
    if request.form['Q8'] == "A":
        if request.form['Q9_electrique'] != None:
            elect = 0.696*int(request.form['Q9_electrique'])
            #session['energie']+=int(request.form['Q9_electrique'])
            energie +=int(request.form['Q9_electrique'])
        if request.form['Q9_gaz'] != None:
            gaz = 0.230*int(request.form['Q9_gaz'])
            #session['energie']+=int(request.form['Q9_gaz'])
            energie +=int(request.form['Q9_gaz'])
        if request.form['Q9_fioul'] != None:
            fioul = 0.275*int(request.form['Q9_fioul'])
            #session['energie']+=int(request.form['Q9_fioul'])
            energie +=int(request.form['Q9_fioul'])
        if request.form['Q9_bois'] != None:
            bois = 0.013*int(request.form['Q9_bois'])
            #session['energie']+=int(request.form['Q9_bois'])
            energie +=int(request.form['Q9_bois'])
    else:
        elect = 0
        gaz = 0
        fioul = 0
        bois = 0

    #TRANSPORTS
    
    tc_s = 0.1846*int(request.form['Q12'])
    voit_s = 9.5602*int(request.form['Q13'])
    voiture = int(request.form['Q13'])
    #session['voiture']=int(request.form['Q13'])
    train = 0.007*int(request.form['Q14'])
    voit_annee = 0.0855*int(request.form['Q15'])
    car = 0.0585*int(request.form['Q16'])
    avion = 0.1446*int(request.form['Q17'])
    #session['avion']=avion

    emission = leg+legumineuse+cere+elect+fioul+bois+gaz+tc_s+voit_s+train+voit_annee+car+avion
    #session['emissions'] = emissions
    return render_template("HTML_FP.html")


#Changer ses résultats (bouton "nouvelles valeurs" de HTML_FP.html)
@app.route('/change', methods=['POST'])
def change():
    global avion, viande, energie, voiture, legume, emission
    #print('on change : ' + str(session))
    #energie= session.get('energie', 'not set')
    new_energie = energie*float(request.form['energie'])

    #legume=session.get('legume', 'not set')
    #print("legume" + str(legume))
    new_legume=legume*float(request.form['legume'])

    #avion=session.get('avion', 'not set')
    #print("avion" + str(avion))
    new_avion = int(request.form['avion'])

    #viande = session.get('qteviande', 'not set')
    #print(viande)
    if request.form['regime']== 'Veg' :
        new_viande=0
    elif request.form['regime']== 'V' :
        new_viande=0        
    elif request.form['regime']== 'A' :
        if viande == 0:
            new_viande = 877.710652
        else:
            new_viande=viande
    print(viande, new_viande)
    #print(new_viande)

    #voiture= session.get('voiture', 'not set')
    if request.form['voiture']== 'A' :
        new_voiture= voiture*0.1846
    else:
        new_voiture=voiture*9.5602


    # if viande == 'not set':
    #     emission=session.get('emissions', 'not set')-energie+new_energie-legume+new_legume+new_viande-voiture+new_voiture-avion+new_avion
    #     print ('hello')
    # else:
    #     print('hi')
    emission=emission-energie+new_energie-legume+new_legume-viande+new_viande-voiture+new_voiture-avion+new_avion

    emission=float(emission)

    #position = session.get('position', 'not set')
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

app.run(host='0.0.0.0', port='8080', debug=True)