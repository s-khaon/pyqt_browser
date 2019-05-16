# import sys
#
# from PyQt5.QtCore import QUrl, pyqtSlot, QFileInfo
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineDownloadItem
# from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QFileDialog
#
# from settings import HOME_HOST
#
# # 每次OPEN都新开一个页面
# # class WebEngineView(QWebEngineView):
# #     windowList = []
# #
# #     # 重写createwindow()
# #     def createWindow(self, QWebEnginePage_WebWindowType):
# #         new_webview = WebEngineView()
# #         new_window = MainWindow()
# #         new_window.setCentralWidget(new_webview)
# #         #new_window.show()
# #         self.windowList.append(new_window)  #注：没有这句会崩溃！！！
# #         return new_webview
#
# class WebEnginePage(QWebEnginePage):
#     def __init__(self, *args, **kwargs):
#         super(WebEnginePage, self).__init__()
#         self.profile().downloadRequested.connect(self.on_downloadRequested)
#
#     @pyqtSlot(QWebEngineDownloadItem)
#     def on_downloadRequested(self, download):
#         old_path = download.path()
#         suffix = QFileInfo(old_path).suffix()
#         path, _ = QFileDialog.getSaveFileName(self.view(), "Save File", old_path, "*."+suffix)
#         print(path)
#         if path:
#             download.setPath(path)
#             download.accept()
#
#
# # @pyqtSlot(QWebEngineDownloadItem)
# # def _downloadRequested(item, download): # QWebEngineDownloadItem
# #     print('downloading to', item.path())
# #     old_path = download.path()
# #     suffix = QFileInfo(old_path).suffix()
# #     path, _ = QFileDialog.getSaveFileName(self.view(), "Save File", old_path, "*."+suffix)
# #     if path:
# #         download.setPath(path)
# #         download.accept()
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle("森果批发收银台")
#         self.setWindowIcon(QIcon("./alipay.png"))
#         self.showMaximized()
#         self.browser = QWebEngineView()
#
#     def after(self):
#         page = WebEnginePage(self.browser)
#         self.browser.setPage(page)
#         self.browser.page().profile().downloadRequested.connect(page.on_downloadRequested)
#         self.browser.load(QUrl(HOME_HOST))
#         self.setCentralWidget(self.browser)
#
#     #     self.setContextMenuPolicy(ContextMenuPolicy)
#     #     # 添加标签栏
#     #     self.tabs = QTabWidget()
#     #     self.tabs.setDocumentMode(True)
#     #     # self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
#     #     # self.tabs.currentChanged.connect(self.current_tab_changed)
#     #     # 允许关闭标签
#     #     self.tabs.setTabsClosable(True)
#     #
#     #     self.add_new_tab(QUrl(url), 'Homepage')
#     #     self.add_new_tab(QUrl("http://www.baidu.com"), 'Homepage')
#     #
#     # def add_new_tab(self, qurl=QUrl(''), label='Blank'):
#     #     # 为标签创建新网页
#     #     browser = QWebEngineView()
#     #     browser.setUrl(qurl)
#     #
#     #     # 为标签页添加索引方便管理
#     #     i = self.tabs.addTab(browser, label)
#     #     self.tabs.setCurrentIndex(i)
#
#         # # 加载完成之后将标签标题修改为网页相关的标题
#         # browser.loadFinished.connect(lambda _, i=i, browser=browser:
#         #                              self.tabs.setTabText(i, browser.page().mainFrame().title()))
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#     win.after()
#     sys.exit(app.exec_())
from time import time

from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from settings import HOME_HOST


class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    customSignal = pyqtSignal(str)

    def __init__(self,*args, **kwargs):
        super(WebEngineView, self).__init__(*args, **kwargs)
        self.channel = QWebChannel(self)
        # 把自身对象传递进去
        self.channel.registerObject('Bridge', self)
        # 设置交互接口
        self.page().setWebChannel(self.channel)
        # self.page().loadStarted.connect(self.onLoadStart)
        # self._script = open('./qwebchannel.js', 'rb').read().decode()

    # def onLoadStart(self):
    #     print("here")
    #     self.page().runJavaScript(self._script)

    # 注意pyqtSlot用于把该函数暴露给js可以调用
    @pyqtSlot(str)
    def callFromJs(self, text):
        print(text)
        QMessageBox.information(self, "提示", "来自js调用：{}".format(text))

    def sendCustomSignal(self):
        # 发送自定义信号
        self.customSignal.emit('当前时间: ' + str(time()))

    @pyqtSlot(str)
    @pyqtSlot(QUrl)
    def load(self, url):
        '''
        eg: load("https://pyqt5.com")
        :param url: 网址
        '''
        return super(WebEngineView, self).load(QUrl(url))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("森果批发收银台")
        self.setWindowIcon(QIcon("./alipay.png"))
        self.showMaximized()
        self.browser = WebEngineView()
        self.browser.showMaximized()
        self.browser.setWindowTitle("森果批发收银台")
        self.browser.setWindowIcon(QIcon("./alipay.png"))
        page = WebEnginePage(self.browser)
        self.browser.setPage(page)
        self.browser.load(QUrl(HOME_HOST))
        self.setCentralWidget(self.browser)


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QtWebEngineWidgets.QWebEnginePage.__init__(self, *args, **kwargs)
        self.profile().downloadRequested.connect(self.on_downloadRequested)

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def on_downloadRequested(self, download):
        old_path = download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.view(), "Save File", old_path, "*."+suffix)
        if path:
            download.setPath(path)
            download.accept()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())