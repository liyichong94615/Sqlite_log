import sqlite3
from sqlite3 import Error
import sys
import os
import numpy as np
import cv2
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *

form_db = uic.loadUiType("cnDlg.ui")[0]
form_main = uic.loadUiType("Main.ui")[0]
form_tbl = uic.loadUiType("tblDlg.ui")[0]
dbNames = []


class MainWindow(QMainWindow, form_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.process()
        self.newDbBtn.clicked.connect(self.showNewDb)
        self.newTblBtn.clicked.connect(self.showNewTbl)


    def process(self):
        for dbName in dbNames:
            en = dbName.find('.db')
            st = en
            while st:
                if dbName[st] is '/':
                    break
                st -= 1

            dbNm = []
            dbNm.append(dbName[st+1:en])
            tree_widget_item = QTreeWidgetItem(dbNm)
            self.dbTree.addTopLevelItem(tree_widget_item)

    def showNewDb(self):

        createDb = CreateDb()
        createDb.exec_()
        if createDb.conn:
            dbNm = []
            dbNm.append(createDb.db_name)
            tree_widget_item = QTreeWidgetItem(dbNm)
            self.dbTree.addTopLevelItem(tree_widget_item)

    def showNewTbl(self):

        createTbl = CreateTbl()
        createTbl.exec_()


class CreateTbl(QDialog, form_tbl):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okBtn.clicked.connect(self.create_table)
        self.clBtn.clicked.connect(self.closeWindow)

    def closeWindow(self):
        self.close()

    def create_table(self):
        print("Create Table")
        self.close()




class CreateDb(QDialog, form_db):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_file = ""
        self.db_path = ""
        self.db_name = ""
        self.pathBtn.clicked.connect(self.dbLocation)
        self.okBtn.clicked.connect(self.create_connection)
        self.clBtn.clicked.connect(self.closeWindow)
        self.conn = None

    def create_connection(self):
        """ create a database connection to a SQLite database """
        self.db_name = self.dbNameEdit.text()
        self.db_path = self.dbPathEdit.text()

        if self.db_name == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Alert")
            msg.setText("Please add Database Name")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.dbNameEdit.setFocus()
            return
        if self.db_path == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Alert")
            msg.setText("Please add Database Path")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.dbPathEdit.setFocus()
            return
        self.db_file = self.db_path + "/" + self.db_name + ".db"

        try:
            self.conn = sqlite3.connect(self.db_file)

        except Error as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Alert")
            msg.setText("Unable to access folder")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.dbPathEdit.setFocus()

        file = open("db.txt", "w")
        dbNames.append(self.db_file + "\n")

        for file_data in dbNames:
            file.write(file_data)

        file.close()
        self.close()

    def dbLocation(self):

        self.db_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.db_path:
            self.dbPathEdit.setText(self.db_path)

    def closeWindow(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if os.path.isfile("db.txt"):
        f = open("db.txt", "r")
        dbNames = f.readlines()
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
