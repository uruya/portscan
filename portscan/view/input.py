import PySide6.QtGui
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QPlainTextEdit
import os
from PySide6.QtUiTools import QUiLoader
from data.target_scan import TargetScan, ExecList

class InputWindow(QMainWindow):
    def __init__(self, exec_list:ExecList):
        super().__init__()
        self.setWindowTitle("IP又はFQDNを入力してください(複数入力可)")
        self.setFixedSize(800, 600)
        # ui file読み込み
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_directory, "input.ui")
        self.ui = QUiLoader().load(ui_file_path)
        self.setCentralWidget(self.ui)

        self.input_text:QPlainTextEdit = self.ui.input_text
        self.exec_list = exec_list

        self.ui.next_button.setEnabled(False)
        # connect
        self.ui.next_button.clicked.connect(self.next)
        self.input_text.textChanged.connect(self.button_enable)

    def showEvent(self, event):
        for target_scan in self.exec_list.exec_list:
            self.input_text.appendPlainText(target_scan.ip_fqdn)

    def button_enable(self):
        if self.input_text.toPlainText() == '':
            self.ui.next_button.setEnabled(False)
        else:
            self.ui.next_button.setEnabled(True)

    def input_confirm(self):
        text_list = self.input_text.toPlainText().split('\n')
        for text in text_list:
            if text == '':
                continue
            target_scan = TargetScan()
            target_scan.ip_fqdn = text
            self.exec_list.exec_list.append(target_scan)

    def next(self):
        self.input_confirm()
        pass