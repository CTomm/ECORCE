from flask import Flask, request, render_template, jsonify, session
#import Session
import psycopg2

app = Flask(__name__)
Session(app)
app.secret_key = "ecorce2020"

@app.route('/<path:path>')
def send_file(path):
    return app.send_static_file(path)

@app.route("/")
def hello2():
    return "<h1 style='color:blue'>Welcome to ECORCE</h1>"

@app.route("/test")
def user():
    conn = psycopg2.connect(host="localhost",database="ecorce", user="postgres", password="postgres")
    cursor = conn.cursor()
    cursor.execute("""
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
    
    tc_s = 184.6*int(request.form['Q12'])
    voit_s = 9560.2*int(request.form['Q13']) #Multiplier passager
    train = 7*int(request.form['Q14'])
    voit_annee = 85.5*int(request.form['Q15']) #Multiplier passager
    car = 58.5*int(request.form['Q16'])
    avion = 144.6*int(request.form['Q17'])

    emissions = alimfixe+poulet+porc+agneau+boeuf+poisson+oeufs+fromage+lait+leg+elect+fioul+bois+gaz+ tc_s+voit_s+train+voit_annee+car+avion
    session['emissions'] = emissions
    return render_template("wait.html")



#A enlever quand on va sur la VM
app.run(host='0.0.0.0', port='5000')