#!/usr/bin/python
# -*- coding: utf-8 -*-

# gridlayout2.py

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from smtp import SendEmail
from compress import Zip


def TEXT(s):
    return s.decode('utf-8')

def QTEXT(s):
    return TEXT(str(s.toUtf8()))

def echo(str, title='Message', self=None):
    QtGui.QMessageBox.question(self, 'Message', str)

class Login(QtGui.QDialog):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)
        self.initUI()
        self.center()

    def initUI(self):
        self.resize(250, 180)
        self.setWindowTitle(TEXT('信息输入'))
        self.setWindowIcon(QtGui.QIcon('pic/info.ico'))

        user = QtGui.QLabel(TEXT('Email'), self)
        pwd = QtGui.QLabel(TEXT('密码'), self)
        login = QtGui.QPushButton(TEXT('确定'), self)
        self.userEdit = QtGui.QLineEdit(self)
        self.pwdEdit = QtGui.QLineEdit(self)
        self.pwdEdit.setEchoMode(QtGui.QLineEdit.Password)
        
        # read from config file
        self.userEdit.setText("282018901@qq.com")
        self.pwdEdit.setText("include<stdio.h>")

        user.move(30, 50)
        pwd.move(30, 80)
        self.userEdit.move(80, 50)
        self.pwdEdit.move(80, 80)
        login.move(90, 110)
        self.connect(login, QtCore.SIGNAL('clicked()'), self.login)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

    def login(self):
        self.accept()
        return (self.userEdit.text(), self.pwdEdit.text())

    @staticmethod
    def getDate(user= None, parent = None):
        # todo:: fill user name
        dialog = Login(parent)
        result = dialog.exec_()
        user, pwd = dialog.login()
        return (str(user), str(pwd), result == QtGui.QDialog.Accepted)

class Addtion(QtGui.QWidget):
    def __init__(self, window):
        super(Addtion, self).__init__()
        self.window = window
        self.resize(80, 100)
        addBtn = QtGui.QPushButton(TEXT('添加附件'))
        self.connect(addBtn, QtCore.SIGNAL('clicked()'), self.window.newAditionDialog)
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.setDirection( QtGui.QBoxLayout.RightToLeft )
        self.hbox.addStretch(1)
        self.hbox.addWidget(addBtn)
        self.setLayout(self.hbox)

    def push(self, path):
        self.hbox.addWidget(QtGui.QLabel(path))


class EmailEditor(QtGui.QWidget):
    def __init__(self, window):
        super(EmailEditor, self).__init__()
        self.window = window
        self.initUI()

    def initUI(self):
        self.resize(350, 300)
        recv = QtGui.QLabel(TEXT('收件人'))
        title = QtGui.QLabel(TEXT('标题'))
        content = QtGui.QLabel(TEXT('内容'))
        addtion = QtGui.QLabel(TEXT('附件'))
        login = QtGui.QPushButton(TEXT('发送'))
        self.recvEdit = QtGui.QLineEdit()
        self.titleEdit = QtGui.QLineEdit()
        self.contentEdit = QtGui.QTextEdit()

        # todo:: read config 
        self.recvEdit.setText('lellansin@gmail.com')
        self.titleEdit = QtGui.QLineEdit(TEXT('你好~'))
        self.contentEdit = QtGui.QTextEdit(TEXT('中文测试， hello email content'))

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(recv, 1, 0)
        grid.addWidget(self.recvEdit, 1, 1)
        grid.addWidget(title, 2, 0)
        grid.addWidget(self.titleEdit, 2, 1)
        grid.addWidget(addtion, 3, 0)
        grid.addWidget(self.window.addAdition, 3, 1)
        grid.addWidget(content, 4, 0)
        grid.addWidget(self.contentEdit, 4, 1, 5, 1)
        grid.addWidget(login, 8, 1)

        self.connect(login, QtCore.SIGNAL('clicked()'), self.send)
        self.setLayout(grid)

    def getContent(self):
        return (
            QTEXT(self.recvEdit.text()),
            QTEXT(self.titleEdit.text()),
            QTEXT(self.contentEdit.toPlainText()).encode('utf-8', 'replace')
        )

    def send(self):
        user, pwd, ok = Login.getDate()
        to, title, content = self.getContent()
        if ok:
            if (user != '') and (pwd != ''):
                try:
                    # todo:: save user, pwd to config file
                    err = SendEmail(user, pwd, to, title, content, self.window.attachment_list)
                    QtGui.QMessageBox.question(self, 'Message', TEXT('发送成功!'))
                    self.window.attachment_list = []
                except Exception, e:
                    QtGui.QMessageBox.question(self, 'Message', str(e) + TEXT('\t如需帮助，请联系作者邮箱： Lellansin@gmail.com'))
            else:
                QtGui.QMessageBox.question(self, 'Message', TEXT('请输入您的邮件账户和密码'))
           


class MainWindow(QtGui.QMainWindow):
    attachment_list = []
    Attachment = None
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(500, 400)
        self.setWindowTitle(TEXT('Auto Email - 自动邮件助手'))
        self.addAdition = Addtion(self)
        textEdit = EmailEditor(self)
        self.setCentralWidget(textEdit)
        self.setMenu()

    def setMenu(self):
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip(TEXT('添加附件'))
        self.connect(openFile, QtCore.SIGNAL('triggered()'), self.newAditionDialog)

        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip(TEXT('退出程序'))
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        # todo:: add email server menu

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exit)

    def newAditionDialog(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', '/home')
        if filenames:
            for path in filenames:
                self.attachment_list.append(str(path))
                self.addAdition.push('['+str(path)+']')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Auto Email')
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())