from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTextEdit, QLabel, QPushButton, QApplication, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests


import sys
import os


class Browser(QWebEngineView):

    def __init__(self):
        super().__init__()
        response = requests.get('http://google.com')
        html = str(response.text)

        # With QWebEnginePage.setHtml, the html is loaded immediately.
        # baseUrl is used to resolve relative URLs in the document.
        # For whatever reason, it seems like the baseUrl resolves to
        # the parent of the path, not the baseUrl itself.  As a
        # workaround, either append a dummy directory to the base url
        # or start all relative paths in the html with the current
        # directory.
        # https://doc-snapshots.qt.io/qtforpython-5.15/PySide2/QtWebEngineWidgets/QWebEnginePage.html#PySide2.QtWebEngineWidgets.PySide2.QtWebEngineWidgets.QWebEnginePage.setHtml
        here = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        base_path = os.path.join(os.path.dirname(
            here), 'dummy').replace('\\', '/')
        self.url = QUrl('file:///' + base_path)
        self.page().setHtml(html, baseUrl=self.url)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_widgets()
        self.init_layout()

    def init_widgets(self):
        self.browser = Browser()

    def init_layout(self):
        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()

        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)

        self.key_label = QLabel('Key')
        self.key_label.setMaximumHeight(30)
        self.key_label.setMaximumWidth(50)
        self.value_label = QLabel('Value')
        self.value_label.setMaximumHeight(30)
        self.value_label.setMaximumWidth(50)
        self.key_bar = QTextEdit()
        self.key_bar.setMaximumHeight(30)
        self.value_bar = QTextEdit()
        self.value_bar.setMaximumHeight(30)
        self.auth_bnt = QPushButton('Add auth')
        self.auth_bnt.setMinimumHeight(30)

        self.get_btn = QPushButton('GET')
        self.get_btn.setMinimumHeight(30)
        self.get_btn.clicked.connect(
            lambda: self.get_request(self.url_bar.toPlainText()))

        self.post_btn = QPushButton('POST')
        self.post_btn.setMinimumHeight(30)
        self.post_btn.clicked.connect(
            lambda: self.post_request(self.url_bar.toPlainText()))

        self.head_btn = QPushButton('HEAD')
        self.head_btn.setMinimumHeight(30)

        self.delete_btn = QPushButton('DELETE')
        self.delete_btn.setMinimumHeight(30)

        self.horizontal1.addWidget(self.head_btn)
        self.horizontal1.addWidget(self.get_btn)
        self.horizontal1.addWidget(self.url_bar)
        self.horizontal1.addWidget(self.post_btn)
        self.horizontal1.addWidget(self.delete_btn)

        self.horizontal2.addWidget(self.key_label)
        self.horizontal2.addWidget(self.key_bar)
        self.horizontal2.addWidget(self.value_label)
        self.horizontal2.addWidget(self.value_bar)
        self.horizontal2.addWidget(self.auth_bnt)

        layout = QVBoxLayout()
        layout.addLayout(self.horizontal1)
        layout.addLayout(self.horizontal2)
        layout.addWidget(self.browser)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    # def load_finished(self, status):
    #     self.msg = QMessageBox()
    #     self.msg.setIcon(QMessageBox.Information)
    #     self.msg.setWindowTitle('Load Status')
    #     self.msg.setText(f"It is {str(status)} that the page loaded.")
    #     self.msg.show()

    def get_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        response = requests.get(url)
        html = str(response.text)
        self.browser.setHtml(html)

    def post_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        response = requests.post(url)
        html = str(response.text)
        self.browser.setHtml(html)

    def head_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        response = requests.head(url)
        html = str(response.text)
        self.browser.setHtml(html)

    def delete_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        response = requests.delete(url)
        html = str(response.text)
        self.browser.setHtml(html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
