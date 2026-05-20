import sys
import os

# Добавляем путь к проекту в sys.path
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()