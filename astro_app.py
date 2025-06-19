# astro_app.py
# Main application UI for the astrological chart generator

import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QDateEdit, QComboBox, QFormLayout, QGroupBox
)
from PyQt5.QtCore import QDate

from astro_constants import AstroConstants
from astro_utils import AstroUtils
from astro_calculator import AstroCalculator
from chart_renderer import ChartRenderer

class AstroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = AstroCalculator()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Mapa Astral")
        self.setMinimumSize(480, 480)
        
        main_layout = QVBoxLayout()
        
        # Person info group
        person_group = QGroupBox("Dados Pessoais")
        person_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        person_layout.addRow("Nome:", self.name_input)
        
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        person_layout.addRow("Data de Nascimento:", self.date_input)
        
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("HH:MM")
        self.time_input.textChanged.connect(self.format_time)
        person_layout.addRow("Hora de Nascimento:", self.time_input)
        
        person_group.setLayout(person_layout)
        main_layout.addWidget(person_group)
        
        # Location group
        location_group = QGroupBox("Localização")
        location_layout = QFormLayout()
        
        self.city_input = QLineEdit()
        location_layout.addRow("Cidade:", self.city_input)
        
        self.hemisphere_combo = QComboBox()
        self.hemisphere_combo.addItems(["Hemisfério Norte", "Hemisfério Sul"])
        self.hemisphere_combo.setCurrentIndex(1)  # Default to Southern (Brazil)
        location_layout.addRow("Hemisfério:", self.hemisphere_combo)
        
        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems(AstroConstants.TIMEZONE_MAP.keys())
        self.timezone_combo.setCurrentIndex(0)  # Default to Brasil
        location_layout.addRow("Região:", self.timezone_combo)
        
        self.house_system_combo = QComboBox()
        self.house_system_combo.addItems(AstroConstants.HOUSE_SYSTEMS.keys())
        location_layout.addRow("Sistema de Casas:", self.house_system_combo)
        
        location_group.setLayout(location_layout)
        main_layout.addWidget(location_group)
        
        # Generate button
        self.generate_btn = QPushButton("Gerar Mapa Astral")
        self.generate_btn.clicked.connect(self.generate_chart)
        main_layout.addWidget(self.generate_btn)
        
        # Status label
        self.status = QLabel("")
        main_layout.addWidget(self.status)
        
        self.setLayout(main_layout)
    
    def format_time(self):
        """Format time input as HH:MM."""
        text = self.time_input.text().replace(":", "")
        if len(text) == 4 and ":" not in self.time_input.text():
            self.time_input.setText(f"{text[:2]}:{text[2:]}")
    
    def generate_chart(self):
        """Generate the astrological chart."""
        try:
            # Get input values
            name = self.name_input.text()
            date = self.date_input.date()
            date_str = date.toString("dd/MM/yyyy")
            time_str = self.time_input.text()
            city = self.city_input.text()
            
            # Validate inputs
            if not name:
                self.status.setText("Por favor, insira um nome.")
                return
            
            if not time_str:
                self.status.setText("Por favor, insira a hora de nascimento.")
                return
            
            if not city:
                self.status.setText("Por favor, insira a cidade de nascimento.")
                return
            
            # Parse date and time
            try:
                dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
            except ValueError:
                self.status.setText("Formato de hora inválido. Use HH:MM.")
                return
            
            # Get location
            lat, lon = AstroUtils.find_location_offline(city)
            if lat is None:
                self.status.setText("Cidade não encontrada.")
                return
            
            # Apply hemisphere correction if needed
            if self.hemisphere_combo.currentText() == "Hemisfério Sul" and lat > 0:
                lat = -lat
            elif self.hemisphere_combo.currentText() == "Hemisfério Norte" and lat < 0:
                lat = abs(lat)
            
            # Get timezone
            region = self.timezone_combo.currentText()
            timezone = AstroConstants.TIMEZONE_MAP[region]
            
            # Get house system
            house_system_name = self.house_system_combo.currentText()
            house_system = AstroConstants.HOUSE_SYSTEMS[house_system_name]
            
            # Calculate chart data
            self.status.setText("Calculando dados do mapa...")
            chart_data = self.calculator.calculate_chart_data(
                dt, lat, lon, timezone, house_system
            )
            
            # Create chart visualization
            self.status.setText("Gerando visualização...")
            output_file = f"mapa_astral_{name.replace(' ', '_')}.pdf"
            ChartRenderer.create_chart(chart_data, name, date_str, output_file)
            
            self.status.setText(f"Mapa gerado com sucesso! Arquivo salvo como {output_file}")
        
        except Exception as e:
            self.status.setText(f"Erro: {str(e)}")
            import traceback
            traceback.print_exc()


# Only run this module directly for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    astro_app = AstroApp()
    astro_app.show()
    sys.exit(app.exec_())