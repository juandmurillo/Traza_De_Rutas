from flask import Flask, render_template, jsonify
from Data import getFullData
from ProcessStats import procesar_estadisticas

app = Flask(__name__)

#procesar datos al iniciar el servidor 
datos_procesados = getFullData()
estadisticas = procesar_estadisticas(datos_procesados)

#rutas
@app.route('/')
def index():
    return render_template('routes.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

#Rutas - datos


@app.route('/api/stats')
def stats1():    
    return jsonify(estadisticas)

@app.route('/api/Local_Amz')
def data1():    
    return jsonify(datos_procesados["Local_Amz"])

@app.route('/api/Local_Ig')
def data2():    
    return jsonify(datos_procesados["Local_Ig"])

@app.route('/api/Local_Pin')
def data3():    
    return jsonify(datos_procesados["Local_Pin"])

@app.route('/api/NA_Seattle_Amz')
def data4():    
    return jsonify(datos_procesados["NA_Seattle_Amz"])

@app.route('/api/NA_Seattle_Ig')
def data5():    
    return jsonify(datos_procesados["NA_Seattle_Ig"])

@app.route('/api/NA_Seattle_Pin')
def data6():    
    return jsonify(datos_procesados["NA_Seattle_Pin"])

@app.route('/api/NA_NewYork_Amz')
def data7():    
    return jsonify(datos_procesados["NA_NewYork_Amz"])

@app.route('/api/NA_NewYork_Ig')
def data8():    
    return jsonify(datos_procesados["NA_NewYork_Ig"])

@app.route('/api/NA_NewYork_Pin')
def data9():    
    return jsonify(datos_procesados["NA_NewYork_Pin"])

@app.route('/api/SA_SaoPaulo_Amz')
def data10():    
    return jsonify(datos_procesados["SA_SaoPaulo_Amz"])

@app.route('/api/SA_SaoPaulo_Ig')
def data11():    
    return jsonify(datos_procesados["SA_SaoPaulo_Ig"])

@app.route('/api/SA_SaoPaulo_Pin')
def data12():    
    return jsonify(datos_procesados["SA_SaoPaulo_Pin"])

@app.route('/api/SA_BuenosAires_Amz')
def data13():    
    return jsonify(datos_procesados["SA_BuenosAires_Amz"])

@app.route('/api/SA_BuenosAires_Ig')
def data14():    
    return jsonify(datos_procesados["SA_BuenosAires_Ig"])

@app.route('/api/SA_BuenosAires_Pin')
def data15():    
    return jsonify(datos_procesados["SA_BuenosAires_Pin"])

@app.route('/api/EU_Amsterdam_Amz')
def data16():    
    return jsonify(datos_procesados["EU_Amsterdam_Amz"])

@app.route('/api/EU_Amsterdam_Ig')
def data17():    
    return jsonify(datos_procesados["EU_Amsterdam_Ig"])

@app.route('/api/EU_Amsterdam_Pin')
def data18():    
    return jsonify(datos_procesados["EU_Amsterdam_Pin"])

@app.route('/api/EU_Hamburgo_Amz')
def data19():    
    return jsonify(datos_procesados["EU_Hamburgo_Amz"])

@app.route('/api/EU_Hamburgo_Ig')
def data20():    
    return jsonify(datos_procesados["EU_Hamburgo_Ig"])

@app.route('/api/EU_Hamburgo_Pin')
def data21():    
    return jsonify(datos_procesados["EU_Hamburgo_Pin"])

@app.route('/api/OC_Sidney_Amz')
def data22():    
    return jsonify(datos_procesados["OC_Sidney_Amz"])

@app.route('/api/OC_Sidney_Ig')
def data23():    
    return jsonify(datos_procesados["OC_Sidney_Ig"])

@app.route('/api/OC_Sidney_Pin')
def data24():    
    return jsonify(datos_procesados["OC_Sidney_Pin"])

@app.route('/api/OC_Singapur_Amz')
def data25():    
    return jsonify(datos_procesados["OC_Singapur_Amz"])

@app.route('/api/OC_Singapur_Ig')
def data26():    
    return jsonify(datos_procesados["OC_Singapur_Ig"])

@app.route('/api/OC_Singapur_Pin')
def data27():    
    return jsonify(datos_procesados["OC_Singapur_Pin"])

@app.route('/api/AF_Togo_Amz')
def data28():    
    return jsonify(datos_procesados["AF_Togo_Amz"])

@app.route('/api/AF_Togo_Ig')
def data29():    
    return jsonify(datos_procesados["AF_Togo_Ig"])

@app.route('/api/AF_Togo_Pin')
def data30():    
    return jsonify(datos_procesados["AF_Togo_Pin"])

@app.route('/api/AF_SudAfrica_Amz')
def data31():    
    return jsonify(datos_procesados["AF_SudAfrica_Amz"])

@app.route('/api/AF_SudAfrica_Ig')
def data32():    
    return jsonify(datos_procesados["AF_SudAfrica_Ig"])

@app.route('/api/AF_SudAfrica_Pin')
def data33():    
    return jsonify(datos_procesados["AF_SudAfrica_Pin"])




if __name__ == '__main__':
    app.run(port = 3000, debug = True)
