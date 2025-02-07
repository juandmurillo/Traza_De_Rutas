import json
from collections import defaultdict
import os

# Mapeo de códigos de países a continentes
country_to_continent = {
    "CO": "South America",  # Colombia
    "US": "North America",  # United States
    "BR": "South America",  # Brazil
    "AR": "South America",  # Argentina
    "NL": "Europe",         # Netherlands
    "DE": "Europe",         # Germany
    "AU": "Oceania",        # Australia
    "SG": "Asia",           # Singapore
    "ZA": "Africa",         # South Africa
    "TG": "Africa",         # Togo
    "GB": "Europe",         # United Kingdom
    "FR": "Europe",         # France
    "CA": "North America",  # Canada
    "ES": "Europe",         # Spain
    "PT": "Europe",         # Portugal
    "SE": "Europe",         # Sweden
    "NZ": "Oceania",        # New Zealand
    "HK": "Asia",           # Hong Kong
    "UG": "Africa",         # Uganda
    "IL": "Asia",           # Israel
    "PA": "North America",  # Panama
    "IT": "Europe",         # Italy
    "CH": "Europe",         # Switzerland
    "BE": "Europe",         # Belgium
    "DK": "Europe",         # Denmark
    "NO": "Europe",         # Norway
    "FI": "Europe",         # Finland
    "AT": "Europe",         # Austria
    "PL": "Europe",         # Poland
    "CZ": "Europe",         # Czech Republic
    "HU": "Europe",         # Hungary
    "RO": "Europe",         # Romania
    "GR": "Europe",         # Greece
    "TR": "Asia",           # Turkey
    "AE": "Asia",           # United Arab Emirates
    "SA": "Asia",           # Saudi Arabia
    "IN": "Asia",           # India
    "CN": "Asia",           # China
    "JP": "Asia",           # Japan
    "KR": "Asia",           # South Korea
    "TH": "Asia",           # Thailand
    "ID": "Asia",           # Indonesia
    "MY": "Asia",           # Malaysia
    "PH": "Asia",           # Philippines
    "VN": "Asia",           # Vietnam
    "MX": "North America",  # Mexico
    "CL": "South America",  # Chile
    "PE": "South America",  # Peru
    "EC": "South America",  # Ecuador
    "VE": "South America",  # Venezuela
    "PY": "South America",  # Paraguay
    "UY": "South America",  # Uruguay
    "BO": "South America",  # Bolivia
    "CR": "North America",  # Costa Rica
    "GT": "North America",  # Guatemala
    "HN": "North America",  # Honduras
    "NI": "North America",  # Nicaragua
    "SV": "North America",  # El Salvador
    "DO": "North America",  # Dominican Republic
    "PR": "North America",  # Puerto Rico
    "JM": "North America",  # Jamaica
    "TT": "North America",  # Trinidad and Tobago
    "BS": "North America",  # Bahamas
    "BB": "North America",  # Barbados
    "GD": "North America",  # Grenada
    "LC": "North America",  # Saint Lucia
    "VC": "North America",  # Saint Vincent and the Grenadines
    "AG": "North America",  # Antigua and Barbuda
    "DM": "North America",  # Dominica
    "KN": "North America",  # Saint Kitts and Nevis
    "BZ": "North America",  # Belize
    "SR": "South America",  # Suriname
    "GY": "South America",  # Guyana
    "GF": "South America",  # French Guiana
    "FK": "South America",  # Falkland Islands
    "GS": "South America",  # South Georgia and the South Sandwich Islands
    "TF": "Antarctica",     # French Southern Territories
    "AQ": "Antarctica",     # Antarctica
    "BV": "Antarctica",     # Bouvet Island
    "HM": "Antarctica",     # Heard Island and McDonald Islands
    "UM": "Oceania",        # United States Minor Outlying Islands
    "AS": "Oceania",        # American Samoa
    "CK": "Oceania",        # Cook Islands
    "FJ": "Oceania",        # Fiji
    "PF": "Oceania",        # French Polynesia
    "GU": "Oceania",        # Guam
    "KI": "Oceania",        # Kiribati
    "MH": "Oceania",        # Marshall Islands
    "FM": "Oceania",        # Micronesia
    "NR": "Oceania",        # Nauru
    "NC": "Oceania",        # New Caledonia
    "NU": "Oceania",        # Niue
    "NF": "Oceania",        # Norfolk Island
    "MP": "Oceania",        # Northern Mariana Islands
    "PW": "Oceania",        # Palau
    "PG": "Oceania",        # Papua New Guinea
    "PN": "Oceania",        # Pitcairn
    "WS": "Oceania",        # Samoa
    "SB": "Oceania",        # Solomon Islands
    "TK": "Oceania",        # Tokelau
    "TO": "Oceania",        # Tonga
    "TV": "Oceania",        # Tuvalu
    "VU": "Oceania",        # Vanuatu
    "WF": "Oceania",        # Wallis and Futuna
    "EH": "Africa",         # Western Sahara
    "CF": "Africa",         # Central African Republic
    "CG": "Africa",         # Congo
    "CD": "Africa",         # Democratic Republic of the Congo
    "DJ": "Africa",         # Djibouti
    "GQ": "Africa",         # Equatorial Guinea
    "ER": "Africa",         # Eritrea
    "ET": "Africa",         # Ethiopia
    "GA": "Africa",         # Gabon
    "GM": "Africa",         # Gambia
    "GH": "Africa",         # Ghana
    "GN": "Africa",         # Guinea
    "GW": "Africa",         # Guinea-Bissau
    "CI": "Africa",         # Ivory Coast
    "KE": "Africa",         # Kenya
    "LS": "Africa",         # Lesotho
    "LR": "Africa",         # Liberia
    "LY": "Africa",         # Libya
    "MG": "Africa",         # Madagascar
    "MW": "Africa",         # Malawi
    "ML": "Africa",         # Mali
    "MR": "Africa",         # Mauritania
    "MU": "Africa",         # Mauritius
    "YT": "Africa",         # Mayotte
    "MA": "Africa",         # Morocco
    "MZ": "Africa",         # Mozambique
    "NA": "Africa",         # Namibia
    "NE": "Africa",         # Niger
    "NG": "Africa",         # Nigeria
    "RE": "Africa",         # Réunion
    "RW": "Africa",         # Rwanda
    "SH": "Africa",         # Saint Helena
    "ST": "Africa",         # Sao Tome and Principe
    "SN": "Africa",         # Senegal
    "SC": "Africa",         # Seychelles
    "SL": "Africa",         # Sierra Leone
    "SO": "Africa",         # Somalia
    "SS": "Africa",         # South Sudan
    "SD": "Africa",         # Sudan
    "SZ": "Africa",         # Swaziland
    "TZ": "Africa",         # Tanzania
    "TD": "Africa",         # Chad
    "TN": "Africa",         # Tunisia
    "UG": "Africa",         # Uganda
    "ZM": "Africa",         # Zambia
    "ZW": "Africa",         # Zimbabwe
}

def obtener_continente(codigo_pais):
    return country_to_continent.get(codigo_pais, "Desconocido")

def procesar_estadisticas(datos):
    cache_file = "estadisticas.json"
    # Verificar si el archivo de caché ya existe
    if os.path.exists(cache_file):
        print("Cargando estadisticas desde el archivo de caché...")
        with open(cache_file, "r") as file:
            return json.load(file)
    else:
        print("Procesando datos y guardando en caché...")
        estadisticas = {
            "saltos_por_continente": defaultdict(int),
            "tiempo_respuesta_por_continente": defaultdict(list),
            "puntos_muertos_por_continente": defaultdict(int),
            "max_saltos": {"saltos": 0, "registro": None},
            "min_saltos": {"saltos": float('inf'), "registro": None},
            "max_tiempo_respuesta": {"tiempo": 0, "registro": None},
            "min_tiempo_respuesta": {"tiempo": float('inf'), "registro": None},
            "puntos_muertos": []
        }

        for key, data in datos.items():
            total_hops = data["stats"]["total_hops"]
            avg_response_time = data["stats"]["avg_response_time"]

            # Iterar sobre cada hop en route_data
            for hop in data["route_data"]:
                hop_number = hop["hop"]
                hop_ip = hop["ip"]
                hop_avg_time = hop["avg_time"]
                hop_ip_info = hop["ip_info"]

                # Obtener el continente basado en el código del país del hop
                if hop_ip_info and hop_ip_info.get("countryCode"):
                    continente = obtener_continente(hop_ip_info["countryCode"])
                else:
                    # Si no hay información de IP, usar el continente del último hop conocido
                    if data["stats"]["last_hop"]["location"] and data["stats"]["last_hop"]["location"].get("countryCode"):
                        continente = obtener_continente(data["stats"]["last_hop"]["location"]["countryCode"])
                    else:
                        continente = "Desconocido"

                # 1. Número de saltos por continente
                estadisticas["saltos_por_continente"][continente] += 1

                # 2. Tiempo de respuesta por continente (se almacena para calcular el promedio después)
                estadisticas["tiempo_respuesta_por_continente"][continente].append(hop_avg_time)

                # 3. Registros de puntos muertos de conexión por continente
                if hop_ip_info is None:
                    estadisticas["puntos_muertos_por_continente"][continente] += 1

                # 4. Registros con mayor y menor número de saltos
                if hop_number > estadisticas["max_saltos"]["saltos"]:
                    estadisticas["max_saltos"]["saltos"] = hop_number
                    estadisticas["max_saltos"]["registro"] = key
                if hop_number < estadisticas["min_saltos"]["saltos"]:
                    estadisticas["min_saltos"]["saltos"] = hop_number
                    estadisticas["min_saltos"]["registro"] = key

                # 5. Registros con mayor y menor número de tiempo de respuesta
                if hop_avg_time > estadisticas["max_tiempo_respuesta"]["tiempo"]:
                    estadisticas["max_tiempo_respuesta"]["tiempo"] = hop_avg_time
                    estadisticas["max_tiempo_respuesta"]["registro"] = key
                if hop_avg_time < estadisticas["min_tiempo_respuesta"]["tiempo"]:
                    estadisticas["min_tiempo_respuesta"]["tiempo"] = hop_avg_time
                    estadisticas["min_tiempo_respuesta"]["registro"] = key

                # 6. Registros de puntos muertos de conexión
                if hop_ip_info is None:
                    estadisticas["puntos_muertos"].append({
                        "registro": key,
                        "hop": hop_number,
                        "ip": hop_ip
                    })

        # Calcular el promedio de tiempo de respuesta por continente
        for continente, tiempos in estadisticas["tiempo_respuesta_por_continente"].items():
            if tiempos:  # Evitar división por cero
                estadisticas["tiempo_respuesta_por_continente"][continente] = sum(tiempos) / len(tiempos)
            else:
                estadisticas["tiempo_respuesta_por_continente"][continente] = 0

        # Guardar las estadísticas en el archivo de caché
        with open(cache_file, 'w') as f:
            json.dump(estadisticas, f, indent=4)

        return estadisticas