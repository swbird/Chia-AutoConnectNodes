from node import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QTimer, QEvent, pyqtSignal, QStringListModel
import sys, time, os
from core import get_nodes, connect_nodes, async_run
import threading
from Utils import ReadConfig



class RenderWindow(QMainWindow, Ui_MainWindow):
    print_to_table_signal = pyqtSignal(str)
    print_to_status_signal = pyqtSignal(str)
    def __init__(self, parent=None):
        super(RenderWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.OpenDirectory)
        self.pushButton_2.clicked.connect(lambda: self.RunInWorkerThread(self.Main_Operation))
        self.filename = ''
        self.print_to_table_signal[str].connect(self.ShowList)
        self.print_to_status_signal[str].connect(self.ShowStatus)
        self.listWidget.setAutoScroll(True)
        if os.path.exists('node.ini'):
            config = ReadConfig('node.ini')
            print(config)
            self.filename = config['chia_path']
            self.print_to_table_signal.emit(f'已选择<{self.filename}>目录')
        self.print_to_table_signal.emit(f'如果软件对你有帮助,请我吃夜宵叭,TRC20地址↓↓')
        self.print_to_table_signal.emit('TMKkqTWkHUYs3ETT8s7XWP9VJYbEqdnaYz')

        self.print_to_status_signal.emit('当前状态->等待同步')



    def RunInWorkerThread(self, func):
        td = threading.Thread(target=func)
        td.setDaemon(True)
        td.start()

    def OpenDirectory(self):
        chia_path = QFileDialog().getExistingDirectory()
        print(chia_path)
        self.filename = chia_path+''
        print(self.filename)
        self.print_to_table_signal.emit(f'已选择<{chia_path}>目录')
        string = f'''[chia父目录]
chia_path={self.filename}'''
        with open('node.ini','w',encoding='utf-8') as f:
            f.write(string)

    def ShowStatus(self, string):
        self.statusbar.showMessage(string)

    def ShowList(self, string):

        self.listWidget.addItem(string)
        self.listWidget.scrollToBottom()

    def Main_Operation(self):
        if self.filename != '':
            if self.checkBox.isChecked():
                t = self.lineEdit.text()
                try:
                    self.print_to_status_signal.emit(f'当前状态->抓取可用的节点地址')
                    async_run(get_nodes)
                except Exception as e:
                    self.print_to_table_signal.emit(f'{e}')

                while True:
                    if t == '':
                        self.print_to_table_signal.emit('请填写间隔时间')
                        break
                    t = int(t) * 60
                    self.print_to_status_signal.emit(f'当前状态->正在同步')
                    connect_nodes(self.filename, self.print_to_table_signal.emit)
                    self.print_to_status_signal.emit(f'当前状态->任务结束,休眠{t/60}分钟')
                    time.sleep(t)
            else:
                try:
                    self.print_to_status_signal.emit(f'当前状态->抓取可用的节点地址')
                    async_run(get_nodes)
                except Exception as e:
                    self.print_to_table_signal.emit(f'{e}')
                self.print_to_status_signal.emit(f'当前状态->正在同步')
                connect_nodes(self.filename, self.print_to_table_signal.emit)
                self.print_to_status_signal.emit(f'当前状态->任务结束')
        else:
            print('失败')

    def ListViewTest(self):
        pass
        self.print_to_table_signal.emit("string")


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    win = RenderWindow()
    win.show()
    sys.exit(APP.exec_())