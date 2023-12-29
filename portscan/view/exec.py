from typing import Optional
from PySide6.QtCore import QThreadPool, QRunnable, Signal, Slot, QObject
from PySide6.QtGui import QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
import os
from data.target_scan import TargetScan, ExecList, Status

class ExecWindow(QMainWindow):
    def __init__(self, exec_list):
        super().__init__()
        self.exec_list = exec_list
        self.setWindowTitle("実行中")
        self.setFixedSize(800, 600)
        # ui file読み込み
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ui_file_path = os.path.join(script_directory, "exec.ui")
        self.ui = QUiLoader().load(ui_file_path)
        self.setCentralWidget(self.ui)
        # テーブル初期設定
        self.table:QTableWidget = self.ui.exec_table
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["IP Address", "Nmap", "Status"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.stretchLastSection)
        # self.table.verticalHeader().setSectionResizeMode(QHeaderView.stretchLastSection)

        # 実行スレッドの設定(QThreadPoolを使う)
        self.thread = QThreadPool()
        self.thread.setMaxThreadCount(4)

        self.table:QTableWidget = self.ui.exec_table

        # connect
        self.ui.execButton.clicked.connect(self.exec)
        
        self.result = len(self.exec_list.exec_list)

    def showEvent(self, event):
        self.table.setRowCount(len(self.exec_list.exec_list))
        for i, target_scan in enumerate(self.exec_list.exec_list):
            tmp = QTableWidgetItem(target_scan.ip_fqdn)
            tmp.setData(1, target_scan.uuid)
            self.table.setItem(i, 0, tmp)
            # nmapステータスの設定
            if target_scan.service['Nmap']:
                self.table.setItem(i, 1, QTableWidgetItem('実行対象'))
            else:
                self.table.setItem(i, 1, QTableWidgetItem('未実行対象'))
            # ステータスの設定
            tmp = QTableWidgetItem(target_scan.status.value)
            tmp.setData(1, target_scan.uuid)
            self.table.setItem(i, 2, tmp)

        return super().show()
    
    def exec(self):
        # QMessageを表示する
        msg_box = QMessageBox()
        msg_box.setText('スキャンを開始しますがよろしいですか？')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if msg_box.exec() == QMessageBox.No:
            return
        # 実行ボタンを無効化する
        self.ui.execButton.setEnabled(False)
        self.result = len(self.exec_list.exec_list)
        # 別スレッドで実行する
        for i, target_scan in enumerate(self.exec_list.exec_list):
            if target_scan.service['Nmap']:
                tmp = ExecThread(target_scan)
                # スレッドの終了を検知する
                tmp.finished_signals.connect(self.show_message)
                tmp.table_signals.connect(self.update_table)

                self.thread.start(tmp)
                target_scan.status = Status.RUNNING
                self.table.setItem(i, 2, QTableWidgetItem(target_scan.status.value))

    def update_table(self):
        for i, target_scan in enumerate(self.exec_list.exec_list):
            self.table.setItem(i, 2, QTableWidgetItem(target_scan.status.value))

    def show_message(self):
        self.result -= 1
        if self.result == 0:
            msg_box = QMessageBox()
            msg_box.setText('実行が完了しました。')
            msg_box.exec()
            self.ui.execButton.setEnabled(True)
    
class ExecThread(QRunnable):
    table_signals  = Signal()
    finished_signals = Signal()

    def __init__(self, target_scan:TargetScan):
        self.target_scan = target_scan

    def run(self):
        # TODO nmapを実行する

        # 実行結果を設定
        self.target_scan.status = Status.DONE
        # テーブルを更新
        self.table_signals.emit()
        self.finished_signals.emit()