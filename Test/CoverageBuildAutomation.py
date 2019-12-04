import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

import log
import file_temp

form_class = uic.loadUiType("main.ui")[0]


class MainApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Coverage build Automation Program')
        self.setWindowIcon(QIcon('QA_IMAGE.png'))
        self.pushButton_find1.clicked.connect(self.plugin_clicked_find)
        self.pushButton_find2.clicked.connect(self.target_clicked_find)
        self.pushButton_check.clicked.connect(self.check_clicked)

    def plugin_clicked_find(self):
        logger.info('plugin_clicked!')
        working_path = QFileDialog.getExistingDirectory(self,"select Directory")
        self.textBrowser_path1.setText(working_path)

    def target_clicked_find(self):
        logger.info('target_clicked!')
        working_path = QFileDialog.getExistingDirectory(self,"select Directory")
        self.textBrowser_path2.setText(working_path)

    def check_clicked(self):
        logger.info('checked!!')
        #plug = r'C:\Program Files\CodeScroll Controller Tester 3.1\plugins'
        #target = r'C:\Users\fdongfdong\Desktop\TestFolder\target'
        #file_temp.main(self.textBrowser_path1.toPlainText(), self.textBrowser_path2.toPlainText())
        file_temp.main(self.textBrowser_path1.toPlainText(), self.textBrowser_path2.toPlainText())
        self.close()
        #if file_temp.main(plug,target) == True:
        #    self.close()


if __name__ == '__main__':
    logger = log.CreateLogger('my')

    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())




