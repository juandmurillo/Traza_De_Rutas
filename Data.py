from Back.ProcessData import *
import json
import os

_ruta = "C:/Users/jdieg/Desktop/Universidad/2. Redes II/Proyecto/Programa/Servidor/Back/Datos/"

def getFullData():
    # Ruta del archivo donde se guardarán los datos procesados
    cache_file = "datos_procesados.json"

    # Verificar si el archivo de caché ya existe
    if os.path.exists(cache_file):
        print("Cargando datos desde el archivo de caché...")
        with open(cache_file, "r") as file:
            return json.load(file)
    else:
        print("Procesando datos y guardando en caché...")
        # Diccionario para almacenar los resultados
        resultados = {}

        # Procesar cada archivo y almacenar el resultado en el diccionario
        resultados["Local_Amz"] = process_traceroute("Local", "Amazon", _ruta + "Local_Amz.csv")
        resultados["Local_Ig"] = process_traceroute("Local", "Instagra", _ruta + "Local_Ig.csv")
        resultados["Local_Pin"] = process_traceroute("Local", "Pinterest", _ruta + "Local_Pin.csv")

        resultados["NA_Seattle_Amz"] = process_traceroute("Seattle", "Amazon", _ruta + "NA_Seattle_Amz.csv")
        resultados["NA_Seattle_Ig"] = process_traceroute("Seattle", "Instagra", _ruta + "NA_Seattle_Ig.csv")
        resultados["NA_Seattle_Pin"] = process_traceroute("Seattle", "Pinterest", _ruta + "NA_Seattle_Pin.csv")

        resultados["NA_NewYork_Amz"] = process_traceroute("NewYork", "Amazon", _ruta + "NA_NewYork_Amz.csv")
        resultados["NA_NewYork_Ig"] = process_traceroute("NewYork", "Instagra", _ruta + "NA_NewYork_Ig.csv")
        resultados["NA_NewYork_Pin"] = process_traceroute("NewYork", "Pinterest", _ruta + "NA_NewYork_Pin.csv")

        resultados["SA_SaoPaulo_Amz"] = process_traceroute("SaoPaulo", "Amazon", _ruta + "SA_SaoPaulo_Amz.csv")
        resultados["SA_SaoPaulo_Ig"] = process_traceroute("SaoPaulo", "Instagra", _ruta + "SA_SaoPaulo_Ig.csv")
        resultados["SA_SaoPaulo_Pin"] = process_traceroute("SaoPaulo", "Pinterest", _ruta + "SA_SaoPaulo_Pin.csv")

        resultados["SA_BuenosAires_Amz"] = process_traceroute("BuenosAires", "Amazon", _ruta + "SA_BuenosAires_Amz.csv")
        resultados["SA_BuenosAires_Ig"] = process_traceroute("BuenosAires", "Instagra", _ruta + "SA_BuenosAires_Ig.csv")
        resultados["SA_BuenosAires_Pin"] = process_traceroute("BuenosAires", "Pinterest", _ruta + "SA_BuenosAires_Pin.csv")

        resultados["EU_Amsterdam_Amz"] = process_traceroute("Amsterdam", "Amazon", _ruta + "EU_Amsterdam_Amz.csv")
        resultados["EU_Amsterdam_Ig"] = process_traceroute("Amsterdam", "Instagra", _ruta + "EU_Amsterdam_Ig.csv")
        resultados["EU_Amsterdam_Pin"] = process_traceroute("Amsterdam", "Pinterest", _ruta + "EU_Amsterdam_Pin.csv")

        resultados["EU_Hamburgo_Amz"] = process_traceroute("Hamburgo", "Amazon", _ruta + "EU_Hamburgo_Amz.csv")
        resultados["EU_Hamburgo_Ig"] = process_traceroute("Hamburgo", "Instagra", _ruta + "EU_Hamburgo_Ig.csv")
        resultados["EU_Hamburgo_Pin"] = process_traceroute("Hamburgo", "Pinterest", _ruta + "EU_Hamburgo_Pin.csv")

        resultados["OC_Sidney_Amz"] = process_traceroute("Sidney", "Amazon", _ruta + "OC_Sidney_Amz.csv")
        resultados["OC_Sidney_Ig"] = process_traceroute("Sidney", "Instagra", _ruta + "OC_Sidney_Ig.csv")
        resultados["OC_Sidney_Pin"] = process_traceroute("Sidney", "Pinterest", _ruta + "OC_Sidney_Pin.csv")

        resultados["OC_Singapur_Amz"] = process_traceroute("Singapur", "Amazon", _ruta + "OC_Singapur_Amz.csv")
        resultados["OC_Singapur_Ig"] = process_traceroute("Singapur", "Instagra", _ruta + "OC_Singapur_Ig.csv")
        resultados["OC_Singapur_Pin"] = process_traceroute("Singapur", "Pinterest", _ruta + "OC_Singapur_Pin.csv")

        resultados["AF_Togo_Amz"] = process_traceroute("Local", "Togo", _ruta + "AF_Togo_Amz.csv")
        resultados["AF_Togo_Ig"] = process_traceroute("Local", "Togo", _ruta + "AF_Togo_Ig.csv")
        resultados["AF_Togo_Pin"] = process_traceroute("Local", "Togo", _ruta + "AF_Togo_Pin.csv")

        resultados["AF_SudAfrica_Amz"] = process_traceroute("SudAfrica", "Amazon", _ruta + "AF_SudAfrica_Amz.csv")
        resultados["AF_SudAfrica_Ig"] = process_traceroute("SudAfrica", "Instagra", _ruta + "AF_SudAfrica_Ig.csv")
        resultados["AF_SudAfrica_Pin"] = process_traceroute("SudAfrica", "Pinterest", _ruta + "AF_SudAfrica_Pin.csv")
        

        # Guardar los datos procesados en un archivo JSON
        with open(cache_file, "w") as file:
            json.dump(resultados, file, indent=4)

        return resultados



''' 
# Ejecutar el procesamiento
if __name__ == "__main__":
    resultado = process_traceroute("Local","Amazon", r"C:/Users/jdieg/Desktop/Universidad/2. Redes II/Proyecto/Programa/Back/Datos/Local_Amz.csv")
    
    # Imprimir resultados
    print(f"/nEstadísticas para {resultado['stats']['server_name']}:")
    print(f"/n/nSitio web {resultado['stats']['site_name']}:")
    print(f"Total de saltos: {resultado['stats']['total_hops']}")
    print(f"Tiempo promedio de respuesta: {resultado['stats']['avg_response_time']:.2f} ms")
    
    print("/nPrimer salto:")
    print(f"IP: {resultado['stats']['first_hop']['ip']}")
    print(f"Tiempo: {resultado['stats']['first_hop']['time']:.2f} ms")
    if resultado['stats']['first_hop']['location']:
        loc = resultado['stats']['first_hop']['location']
        print(f"Ubicación: {loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}")
    
    print("/nÚltimo salto:")
    print(f"IP: {resultado['stats']['last_hop']['ip']}")
    print(f"Tiempo: {resultado['stats']['last_hop']['time']:.2f} ms")
    if resultado['stats']['last_hop']['location']:
        loc = resultado['stats']['last_hop']['location']
        print(f"Ubicación: {loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}")
    
    print("/nRuta completa:")
    for hop in resultado['route_data']:
        print(f"/nSalto {hop['hop']}:")
        print(f"IP: {hop['ip']}")
        print(f"Tiempo promedio: {hop['avg_time']:.2f} ms")
        if hop['ip_info']:
            info = hop['ip_info']
            print(f"Ubicación: {info.get('city', 'N/A')}, {info.get('country', 'N/A')}")
            print(f"Coordenadas: {info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}")


'''