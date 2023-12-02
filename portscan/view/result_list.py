from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Port Scan Result")
        self.setFixedSize(800, 600)
        # load ui file
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_directory, "result_list.ui")
        self.ui = QUiLoader().load(ui_file_path)
        self.setCentralWidget(self.ui)

        # connect
        self.ui.action_close.triggered.connect(self.close)

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