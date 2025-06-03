import sqlite3
import pandas as pd
from pathlib import Path

def import_data_to_db(db_path: str, data_dir: str = 'data'):
    """
    Импортирует данные из .dat файлов в SQLite базу данных
    
    :param db_path: Путь к файлу базы данных
    :param data_dir: Директория с исходными данными
    """
    conn = sqlite3.connect(db_path)
    
    # Функция для обработки NULL значений (\N)
    def parse_null(value):
        return None if value == '\\N' else value
    
    # Импорт авиакомпаний
    airlines = pd.read_csv(
        Path(data_dir) / 'airlines.dat',
        header=None,
        names=['id', 'name', 'alias', 'iata', 'icao', 'callsign', 'country', 'active'],
        na_values=['\\N'],
        quotechar='"'
    )
    airlines.to_sql('Airlines', conn, if_exists='replace', index=False)
    
    # Импорт аэропортов (используем extended версию)
    airports = pd.read_csv(
        Path(data_dir) / 'airports-extended.dat',
        header=None,
        names=['id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 
               'longitude', 'altitude', 'timezone', 'dst', 'tz', 'type', 'source'],
        na_values=['\\N'],
        quotechar='"'
    )
    airports.to_sql('Airports', conn, if_exists='replace', index=False)
    
    # Импорт самолетов
    planes = pd.read_csv(
        Path(data_dir) / 'planes.dat',
        header=None,
        names=['name', 'iata', 'icao'],
        na_values=['\\N'],
        quotechar='"'
    )
    planes['id'] = range(1, len(planes) + 1)  # Добавляем ID
    planes.to_sql('Planes', conn, if_exists='replace', index=False)
    
    # Импорт стран
    countries = pd.read_csv(
        Path(data_dir) / 'countries.dat',
        header=None,
        names=['name', 'code', 'dafif'],
        na_values=['\\N'],
        quotechar='"'
    )
    countries['id'] = range(1, len(countries) + 1)
    countries.to_sql('Countries', conn, if_exists='replace', index=False)
    
    # Импорт маршрутов
    routes = pd.read_csv(
        Path(data_dir) / 'routes.dat',
        header=None,
        names=['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 
               'codeshare', 'stops', 'equipment'],
        na_values=['\\N'],
        quotechar='"'
    )
    routes['id'] = range(1, len(routes) + 1)
    routes.to_sql('Routes', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Данные успешно импортированы в базу данных")

if __name__ == "__main__":
    import_data_to_db('airtravel.db')