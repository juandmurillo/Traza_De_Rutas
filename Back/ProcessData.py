import pandas as pd
import numpy as np
import requests
import time

class IPInfoFetcher:
    def __init__(self):
        self.cache = {}
        self.last_request_time = 0
        self.rate_limit_delay = 1.1  # Delay en segundos para respetar el rate limit

    def get_ip_info(self, ip):
        """Obtiene información de una IP con control de rate limit y caché."""
        # No consultar IPs inválidas o privadas
        if ip == '*' or self._is_private_ip(ip):
            return None

        # Usar caché si está disponible
        if ip in self.cache:
            return self.cache[ip]

        # Controlar rate limit
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last_request)

        # Realizar la consulta
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        self.last_request_time = time.time()

        if response.status_code == 200:
            data = response.json()
            info = {
                "query": data.get("query"),
                "status": data.get("status"),
                "continent": data.get("continent"),
                "continentCode": data.get("continentCode"),
                "country": data.get("country"),
                "countryCode": data.get("countryCode"),
                "region": data.get("region"),
                "regionName": data.get("regionName"),
                "city": data.get("city"),
                "district": data.get("district", ""),
                "zip": data.get("zip"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "org": data.get("org")
            }
            self.cache[ip] = info
            return info
        return None

    def _is_private_ip(self, ip):
        """Verifica si una IP es privada."""
        if ip.startswith(('10.', '172.16.', '192.168.')):
            return True
        return False

class TracerouteData:
    def __init__(self, server_name, site_name, data_path):
        self.server_name = server_name
        self.site_name = site_name
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None
        self.stats = {}
        self.ip_fetcher = IPInfoFetcher()
        
    def read_data(self):
        """Lee el archivo CSV y procesa los datos iniciales."""
        # Leer el CSV saltando la primera fila (nombre del sitio)
        self.raw_data = pd.read_csv(self.data_path, sep=';', skiprows=1, header=0)
        # Renombrar columnas para mejor manejo
        self.raw_data.columns = ['hop', 'time1', 'time2', 'time3', 'ip']
        return self
        
    def clean_data(self):
        """Limpia y procesa los datos."""
        # Crear copia para procesar
        df = self.raw_data.copy()
        
        # Eliminar filas donde todos los tiempos son '*'
        mask = ~((df['time1'] == '*') & (df['time2'] == '*') & (df['time3'] == '*'))
        df = df[mask]
        
        # Convertir '*' a NaN en las columnas de tiempo
        time_columns = ['time1', 'time2', 'time3']
        df[time_columns] = df[time_columns].replace('*', np.nan)
        
        # Convertir columnas de tiempo a tipo numérico
        df[time_columns] = df[time_columns].astype(float)
        
        # Calcular tiempo promedio
        df['avg_time'] = df[time_columns].mean(axis=1)
        
        # Eliminar saltos repetidos (mantener primera ocurrencia)
        df = df.drop_duplicates(subset=['ip'], keep='first')
        
        # Reiniciar índices después de la limpieza
        df = df.reset_index(drop=True)
        
        # Añadir información geográfica para cada IP
        df['ip_info'] = df['ip'].apply(self.ip_fetcher.get_ip_info)
        
        self.processed_data = df
        return self
        
    def calculate_stats(self):
        """Calcula estadísticas de los datos procesados."""
        if self.processed_data is None:
            raise ValueError("Datos no procesados. Ejecutar clean_data primero.")
            
        self.stats = {
            'server_name': self.server_name,
            'site_name': self.site_name,
            'total_hops': len(self.processed_data),
            'avg_response_time': self.processed_data['avg_time'].mean(),
            'first_hop': {
                'ip': self.processed_data.iloc[0]['ip'],
                'time': self.processed_data.iloc[0]['avg_time'],
                'location': self.processed_data.iloc[0]['ip_info']
            },
            'last_hop': {
                'ip': self.processed_data.iloc[-1]['ip'],
                'time': self.processed_data.iloc[-1]['avg_time'],
                'location': self.processed_data.iloc[-1]['ip_info']
            }
        }   
        return self
    
    def get_route_info(self):
        """Retorna un diccionario con toda la información procesada."""
        return {
            'stats': self.stats,
            'route_data': self.processed_data.to_dict('records')
        }

# Ejemplo de uso
def process_traceroute(server_name, site_name, file_path):
    traceroute = TracerouteData(server_name, site_name, file_path)
    
    # Procesar datos
    traceroute.read_data() \
             .clean_data() \
             .calculate_stats()
    
    return traceroute.get_route_info()

