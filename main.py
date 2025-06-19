# main.py
# Entry point for the Astrological Chart Application

import sys
from PyQt5.QtWidgets import QApplication
from astro_app import AstroApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    astro_app = AstroApp()
    astro_app.show()
    sys.exit(app.exec_())