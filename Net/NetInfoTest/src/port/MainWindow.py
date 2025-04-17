import sys;
from typing import Any, List;
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QComboBox,QTableView,QVBoxLayout,QHBoxLayout,QHeaderView,QAbstractItemView
from PySide6.QtGui import QStandardItemModel,QStandardItem
from PySide6.QtCore import Qt,Slot

from port.PortScanner import *;

class MainWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initializePage()
        self.initializeData()
        self.initializeConnections()

    def initializePage(self):
        
        self.rootLayout = QVBoxLayout(self)
        
        self.searchLayout = QHBoxLayout(self)
        self.searchCombo = QComboBox(self)
        self.searchLineEdit = QLineEdit(self)
        self.searchButton = QPushButton(self)
        
        self.searchLayout.addWidget(self.searchCombo,1)
        self.searchLayout.addWidget(self.searchLineEdit,5)
        self.searchLayout.addWidget(self.searchButton,1)
        self.rootLayout.addLayout(self.searchLayout)

        self.tableView = QTableView(self)
        self.rootLayout.addWidget(self.tableView)

        self.bottomLayout = QHBoxLayout(self)
        self.bottomStartSearchButton = QPushButton(self)
        self.bottomStopSearchButton = QPushButton(self)
        self.bottomLayout.addWidget(self.bottomStartSearchButton)
        self.bottomLayout.addWidget(self.bottomStopSearchButton)
        self.rootLayout.addLayout(self.bottomLayout)

    def initializeData(self):
        self.setWindowTitle("Port Scanner")
        self.setFixedSize(800,600)


        self.searchCombo.setFixedHeight(30)
        self.searchCombo.addItem("process_name")
        self.searchCombo.addItem("local_port")
        self.searchCombo.addItem("local_ip")
        self.searchCombo.addItem("pid")
        self.searchLineEdit.setFixedHeight(30)

        self.searchButton.setText("搜索")
        self.searchButton.setFixedHeight(30)

        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSortingEnabled(True)
        self.tableView.horizontalHeader().setSectionsClickable(True)
        self.model.setHorizontalHeaderLabels(["name","pid","local_port","local_ip","protocol","remote_ip","remote_port","state"])
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.bottomStartSearchButton.setText("开始检索")
        self.bottomStartSearchButton.setFixedHeight(30)
        self.bottomStopSearchButton.setText("停止检索")
        self.bottomStopSearchButton.setFixedHeight(30)
        self.bottomStopSearchButton.setEnabled(False)

    def initializeConnections(self):
        self.bottomStartSearchButton.clicked.connect(lambda: self.handleData())
        self.searchButton.clicked.connect(lambda: self.searchData())
        
    def appendRow(self,rowData:dict[str,Any]):
        row = [
            QStandardItem(str(rowData["process_name"])),
            QStandardItem(str(rowData["pid"])),
            QStandardItem(str(rowData["local_port"])),
            QStandardItem(rowData["local_ip"]),
            QStandardItem(rowData["protocol"]),
            QStandardItem(str(rowData["remote_ip"])),
            QStandardItem(str(rowData["remote_port"])),
            QStandardItem(rowData["state"])
        ]

        self.model.appendRow(row)

    @Slot()
    def handleData(self):
        print("-- START FLUSH PORT DATA --")
        self.bottomStartSearchButton.setText("刷新")
        self.model.removeRows(0,self.model.rowCount())
        data = PortScanner.get_all_ports()
        for d in data[:]:
            self.appendRow(d)
        
    @Slot()
    def searchData(self):
        comboText = self.searchCombo.currentText()
        searchText = self.searchLineEdit.text()
        search_and_scroll(self.tableView,comboText,searchText)


def find_column_index(model, column_name: str) -> int:
    """根据列名获取列索引"""
    for col in range(model.columnCount()):
        if model.headerData(col, Qt.Horizontal, Qt.DisplayRole) == column_name:
            return col
    return -1  # 未找到列名

def search_and_scroll(table_view, column_name: str, target_value: str):
    """根据列名和值搜索并跳转"""
    model = table_view.model()
    col = find_column_index(model, column_name)
    
    if col == -1:
        return False  # 列名不存在
    
    for row in range(model.rowCount()):
        index = model.index(row, col)
        if model.data(index, Qt.DisplayRole) == target_value:
            # 跳转并选中整行
            table_view.scrollTo(index, QTableView.PositionAtCenter)
            table_view.selectRow(row)
            return True
    return False