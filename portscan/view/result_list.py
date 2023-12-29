from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidget
from PySide6.QtUiTools import QUiLoader
import os
from data.target_scan import TargetScan, ExecList

from .input import InputWindow
from .option import OptionWindow
from .exec import ExecWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Scan Result")
        self.setFixedSize(800, 600)
        # ui file読み込み
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_directory, "result_list.ui")
        self.ui = QUiLoader().load(ui_file_path)
        self.setCentralWidget(self.ui)

        # テーブル初期設定
        self.table:QTableWidget = self.ui.main_table
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["IP Address", "Nmap"])

        self.exec_list = ExecList()
        # サブウィンドウ初期設定
        self.input_window = InputWindow(self.exec_list) # IP又はFQDNを入力するウィンドウ
        self.option_window = OptionWindow(self.exec_list) # オプション設定ウィンドウ
        self.exec_window = ExecWindow(self.exec_list) # 実行中のウィンドウ


        # connect
        self.ui.action_close.triggered.connect(self.close)
        self.ui.action_scan.triggered.connect(self.scan)

        # input_windowのconnect
        self.input_window.ui.next_button.clicked.connect(self.option_window.show)
        self.input_window.ui.next_button.clicked.connect(self.input_window.hide)

        # option_windowのconnect
        self.option_window.ui.backButton.clicked.connect(self.input_window.show)
        self.option_window.ui.backButton.clicked.connect(self.option_window.hide)
        self.option_window.ui.nextButton.clicked.connect(self.exec_window.show)
        self.option_window.ui.nextButton.clicked.connect(self.option_window.hide)

        # exec_windowのconnect
        self.exec_window.ui.closeButton.clicked.connect(self.exec_window.hide)
        self.exec_window.ui.backButton.clicked.connect(self.option_window.show)
        self.exec_window.ui.backButton.clicked.connect(self.exec_window.hide)

    def reload_table(self):
        for row, target_scan in enumerate(self.exec_list.exec_list):
            self.table.setItem(row, 0, target_scan.ip_fqdn)

    def closeEvent(self, event) -> None:
        # 未保存状態の場合は保存するか確認する TODO
        msg_box = QMessageBox.question(
            self,
            "確認",
            "未保存状態です。保存してから終了しますか？",
            buttons=QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if  msg_box == QMessageBox.Yes:
            # 保存して終了

            event.accept()
        # 保存せずに終了
        elif msg_box == QMessageBox.No:
            event.accept()
        # 終了しない
        else:
            event.ignore()

    def scan(self):
        self.input_window.show()