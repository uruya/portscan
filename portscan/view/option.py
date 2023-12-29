import PySide6.QtGui
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore, QtGui, QtWidgets
import os


class OptionWindow(QMainWindow):
    def __init__(self, exec_list):
        super().__init__()
        self.setWindowTitle("オプション設定")
        self.setFixedSize(800, 600)
        self.exec_list = exec_list
        # ui file読み込み
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_directory, "option.ui")
        self.ui = QUiLoader().load(ui_file_path)
        self.setCentralWidget(self.ui)

        # テーブル初期設定
        self.table:QTableWidget = self.ui.option_table
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["IP Address", "Nmap"])

    def showEvent(self, event):
        self.table.setRowCount(len(self.exec_list.exec_list))
        for i, target_scan in enumerate(self.exec_list.exec_list):
            self.table.setItem(i, 0, QTableWidgetItem(target_scan.ip_fqdn))
            # チェックボックスの設定
            # target_scan.service['Nmap']がTrueならチェックを入れる
            tmp = QtWidgets.QCheckBox()
            if target_scan.service['Nmap']:
                # セルの真ん中にチェックボックスを配置
                self.table.setCellWidget(i, 1, tmp)
                tmp.setChecked(True)
            else:  # Falseならチェックを外す
                self.table.setCellWidget(i, 1, tmp)
                tmp.setChecked(False)
            tmp.stateChanged.connect(self.change_check)
        return super().show()
    def change_check(self, state):
        # チェックボックスの状態を取得
        checkbox = self.sender()
        # チェックボックスの行番号を取得
        row = self.table.indexAt(checkbox.pos()).row()
        # チェックボックスの状態を取得
        if state == 2:
            self.exec_list.exec_list[row].service['Nmap'] = True
        else:
            self.exec_list.exec_list[row].service['Nmap'] = False