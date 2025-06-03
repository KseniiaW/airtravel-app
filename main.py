import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTableWidget, QTableWidgetItem, QComboBox, 
                            QTabWidget, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt

class AirTravelApp(QMainWindow):
    """
    Главное окно приложения для работы с данными аэропортов и авиакомпаний
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Air Travel Database")
        self.setGeometry(100, 100, 900, 600)
        
        # Подключение к базе данных
        self.conn = sqlite3.connect('airtravel.db')
        
        # Создание интерфейса
        self.init_ui()
        
    def init_ui(self):

        # Создаем виджет с вкладками
        self.tabs = QTabWidget()
        
        # Вкладка поиска аэропортов
        self.tab_airports = QWidget()
        self.init_airports_tab()
        self.tabs.addTab(self.tab_airports, "Аэропорты")
        
        # Вкладка поиска рейсов
        self.tab_routes = QWidget()
        self.init_routes_tab()
        self.tabs.addTab(self.tab_routes, "Рейсы")
        
        # Устанавливаем центральный виджет
        self.setCentralWidget(self.tabs)
    
    def init_airports_tab(self):
        """Инициализация вкладки поиска аэропортов"""
        layout = QVBoxLayout()
        
        # Группа для поиска по координатам
        coord_group = QGroupBox("Поиск по координатам")
        coord_layout = QHBoxLayout()
        
        self.lat_min = QLineEdit()
        self.lat_min.setPlaceholderText("Минимальная широта")
        self.lat_max = QLineEdit()
        self.lat_max.setPlaceholderText("Максимальная широта")
        self.lon_min = QLineEdit()
        self.lon_min.setPlaceholderText("Минимальная долгота")
        self.lon_max = QLineEdit()
        self.lon_max.setPlaceholderText("Максимальная долгота")
        
        coord_btn = QPushButton("Найти")
        coord_btn.clicked.connect(self.search_by_coordinates)
        
        coord_layout.addWidget(QLabel("Широта:"))
        coord_layout.addWidget(self.lat_min)
        coord_layout.addWidget(self.lat_max)
        coord_layout.addWidget(QLabel("Долгота:"))
        coord_layout.addWidget(self.lon_min)
        coord_layout.addWidget(self.lon_max)
        coord_layout.addWidget(coord_btn)
        coord_group.setLayout(coord_layout)
        
        # Группа для поиска по городу и стране
        city_group = QGroupBox("Поиск по городу и стране")
        city_layout = QHBoxLayout()
        
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Город")
        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("Страна")
        
        city_btn = QPushButton("Найти")
        city_btn.clicked.connect(self.search_by_city_country)
        
        city_layout.addWidget(self.city_input)
        city_layout.addWidget(self.country_input)
        city_layout.addWidget(city_btn)
        city_group.setLayout(city_layout)
        
        # Таблица для отображения результатов
        self.airports_table = QTableWidget()
        self.airports_table.setColumnCount(6)
        self.airports_table.setHorizontalHeaderLabels(
            ["Название", "Город", "Страна", "IATA", "Широта", "Долгота"])
        self.airports_table.setSortingEnabled(True)
        
        # Добавляем все виджеты на вкладку
        layout.addWidget(coord_group)
        layout.addWidget(city_group)
        layout.addWidget(self.airports_table)
        
        self.tab_airports.setLayout(layout)
    
    def init_routes_tab(self):
        """Инициализация вкладки поиска рейсов"""
        layout = QVBoxLayout()
        
        # Группа для поиска рейсов из города
        from_group = QGroupBox("Рейсы из города")
        from_layout = QHBoxLayout()
        
        self.from_city = QLineEdit()
        self.from_city.setPlaceholderText("Город отправления")
        self.from_country = QLineEdit()
        self.from_country.setPlaceholderText("Страна отправления")
        
        from_btn = QPushButton("Найти рейсы")
        from_btn.clicked.connect(self.search_flights_from)
        
        from_layout.addWidget(self.from_city)
        from_layout.addWidget(self.from_country)
        from_layout.addWidget(from_btn)
        from_group.setLayout(from_layout)
        
        # Группа для поиска рейсов между городами
        between_group = QGroupBox("Рейсы между городами")
        between_layout = QVBoxLayout()
        
        # Город отправления
        from_layout2 = QHBoxLayout()
        from_layout2.addWidget(QLabel("Из:"))
        self.from_city2 = QLineEdit()
        self.from_city2.setPlaceholderText("Город")
        self.from_country2 = QLineEdit()
        self.from_country2.setPlaceholderText("Страна")
        from_layout2.addWidget(self.from_city2)
        from_layout2.addWidget(self.from_country2)
        
        # Город назначения
        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("В:"))
        self.to_city = QLineEdit()
        self.to_city.setPlaceholderText("Город")
        self.to_country = QLineEdit()
        self.to_country.setPlaceholderText("Страна")
        to_layout.addWidget(self.to_city)
        to_layout.addWidget(self.to_country)
        
        between_btn = QPushButton("Найти рейсы")
        between_btn.clicked.connect(self.search_flights_between)
        
        between_layout.addLayout(from_layout2)
        between_layout.addLayout(to_layout)
        between_layout.addWidget(between_btn)
        between_group.setLayout(between_layout)
        
        # Таблица для отображения результатов
        self.routes_table = QTableWidget()
        self.routes_table.setColumnCount(6)
        self.routes_table.setHorizontalHeaderLabels(
            ["Авиакомпания", "Из", "В", "Код", "Остановки", "Самолет"])
        self.routes_table.setSortingEnabled(True)
        
        # Добавляем все виджеты на вкладку
        layout.addWidget(from_group)
        layout.addWidget(between_group)
        layout.addWidget(self.routes_table)
        
        self.tab_routes.setLayout(layout)
    
    def search_by_coordinates(self):
        """Поиск аэропортов по диапазону координат"""
        try:
            lat_min = float(self.lat_min.text())
            lat_max = float(self.lat_max.text())
            lon_min = float(self.lon_min.text())
            lon_max = float(self.lon_max.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения координат")
            return
        
        query = """
        SELECT name, city, country, iata, latitude, longitude 
        FROM Airports 
        WHERE latitude BETWEEN ? AND ? 
        AND longitude BETWEEN ? AND ?
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (lat_min, lat_max, lon_min, lon_max))
        results = cursor.fetchall()
        
        self.display_airports(results)
    
    def search_by_city_country(self):
        """Поиск аэропортов по городу и стране"""
        city = self.city_input.text().strip()
        country = self.country_input.text().strip()
        
        if not city and not country:
            QMessageBox.warning(self, "Ошибка", "Введите город или страну для поиска")
            return
        
        query = """
        SELECT name, city, country, iata, latitude, longitude 
        FROM Airports 
        WHERE city LIKE ? AND country LIKE ?
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (f"%{city}%", f"%{country}%"))
        results = cursor.fetchall()
        
        self.display_airports(results)
    
    def search_flights_from(self):
        """Поиск всех рейсов из заданного города"""
        city = self.from_city.text().strip()
        country = self.from_country.text().strip()
        
        if not city and not country:
            QMessageBox.warning(self, "Ошибка", "Введите город или страну для поиска")
            return
        
        query = """
        SELECT 
            al.name, 
            ap1.city || ', ' || ap1.country as source, 
            ap2.city || ', ' || ap2.country as destination,
            r.codeshare,
            r.stops,
            GROUP_CONCAT(p.name, ', ') as planes
        FROM Routes r
        JOIN Airlines al ON r.airline_id = al.id
        JOIN Airports ap1 ON r.source_airport_id = ap1.id
        JOIN Airports ap2 ON r.dest_airport_id = ap2.id
        LEFT JOIN Planes p ON r.equipment LIKE '%' || p.iata || '%'
        WHERE ap1.city LIKE ? AND ap1.country LIKE ?
        GROUP BY r.id
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (f"%{city}%", f"%{country}%"))
        results = cursor.fetchall()
        
        self.display_routes(results)
    
    def search_flights_between(self):
        """Поиск рейсов между двумя городами"""
        from_city = self.from_city2.text().strip()
        from_country = self.from_country2.text().strip()
        to_city = self.to_city.text().strip()
        to_country = self.to_country.text().strip()
        
        if not from_city or not from_country or not to_city or not to_country:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля для поиска")
            return
        
        query = """
        SELECT 
            al.name, 
            ap1.city || ', ' || ap1.country as source, 
            ap2.city || ', ' || ap2.country as destination,
            r.codeshare,
            r.stops,
            GROUP_CONCAT(p.name, ', ') as planes
        FROM Routes r
        JOIN Airlines al ON r.airline_id = al.id
        JOIN Airports ap1 ON r.source_airport_id = ap1.id
        JOIN Airports ap2 ON r.dest_airport_id = ap2.id
        LEFT JOIN Planes p ON r.equipment LIKE '%' || p.iata || '%'
        WHERE ap1.city LIKE ? AND ap1.country LIKE ?
        AND ap2.city LIKE ? AND ap2.country LIKE ?
        GROUP BY r.id
        """
        
        cursor = self.conn.cursor()
        cursor.execute(query, (
            f"%{from_city}%", f"%{from_country}%",
            f"%{to_city}%", f"%{to_country}%"
        ))
        results = cursor.fetchall()
        
        self.display_routes(results)
    
    def display_airports(self, data):
        """Отображение результатов поиска аэропортов в таблице"""
        self.airports_table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.airports_table.setItem(row_idx, col_idx, item)
        
        self.airports_table.resizeColumnsToContents()
    
    def display_routes(self, data):
        """Отображение результатов поиска рейсов в таблице"""
        self.routes_table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.routes_table.setItem(row_idx, col_idx, item)
        
        self.routes_table.resizeColumnsToContents()
    
    def closeEvent(self, event):
        """Обработчик закрытия окна - закрываем соединение с БД"""
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AirTravelApp()
    window.show()
    sys.exit(app.exec_())