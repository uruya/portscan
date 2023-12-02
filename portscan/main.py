from PySide6 import QtWidgets
import sys
from view.result_list import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())