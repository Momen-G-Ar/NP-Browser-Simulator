from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTextEdit, QLabel, QPushButton, QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

import requests
from requests.auth import HTTPBasicAuth
import strings

import sys
import os


class Browser(QWebEngineView):

    def __init__(self):
        super().__init__()
        html = strings.basic_html

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
        self.auth = HTTPBasicAuth('momin', '12345')
        self.item = {}
        self.resize(1200, 800)
        self.init_widgets()
        self.init_layout()
        self.setWindowTitle('Momin Browser')

        self.invalid_method_html = strings.invalid_method_html

    def init_widgets(self):
        self.browser = Browser()

    def init_layout(self):
        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        self.horizontal4 = QHBoxLayout()
        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)

        self.username_label = QLabel('username')
        self.username_label.setMaximumHeight(30)
        self.username_label.setMaximumWidth(50)
        self.password_label = QLabel('password')
        self.password_label.setMaximumHeight(30)
        self.password_label.setMaximumWidth(50)
        self.username_bar = QTextEdit()
        self.username_bar.setMaximumHeight(30)
        self.password_bar = QTextEdit()
        self.password_bar.setMaximumHeight(30)
        self.auth_bnt = QPushButton('Save Auth')
        self.auth_bnt.setMinimumHeight(30)
        self.auth_bnt.clicked.connect(lambda: self.save_auth())

        self.item_label = QLabel('Item info')
        self.item_label.setMaximumHeight(30)
        self.name_bar = QLabel('Name')
        self.name_bar.setMaximumHeight(30)
        self.name_value_bar = QTextEdit()
        self.name_value_bar.setMaximumHeight(30)
        self.price_bar = QLabel('Price')
        self.price_bar.setMaximumHeight(30)
        self.price_value_bar = QTextEdit()
        self.price_value_bar.setMaximumHeight(30)
        self.body_btn = QPushButton('Save item info')
        self.body_btn.setMinimumWidth(30)
        self.body_btn.setMinimumHeight(30)
        self.body_btn.clicked.connect(lambda: self.save_item())

        self.get_btn = QPushButton('GET')
        self.get_btn.setMinimumHeight(30)
        self.get_btn.clicked.connect(
            lambda: self.get_request(self.url_bar.toPlainText()))

        self.post_btn = QPushButton('POST')
        self.post_btn.setMinimumHeight(30)
        self.post_btn.clicked.connect(
            lambda: self.post_request(self.url_bar.toPlainText()))

        self.delete_btn = QPushButton('DELETE')
        self.delete_btn.setMinimumHeight(30)
        self.delete_btn.clicked.connect(
            lambda: self.delete_request(self.url_bar.toPlainText()))

        self.horizontal1.addWidget(self.get_btn)
        self.horizontal1.addWidget(self.url_bar)
        self.horizontal1.addWidget(self.post_btn)
        self.horizontal1.addWidget(self.delete_btn)

        self.horizontal2.addWidget(self.username_label)
        self.horizontal2.addWidget(self.username_bar)
        self.horizontal2.addWidget(self.password_label)
        self.horizontal2.addWidget(self.password_bar)
        self.horizontal2.addWidget(self.auth_bnt)

        self.horizontal3.addWidget(self.item_label)

        self.horizontal4.addWidget(self.name_bar)
        self.horizontal4.addWidget(self.name_value_bar)
        self.horizontal4.addWidget(self.price_bar)
        self.horizontal4.addWidget(self.price_value_bar)
        self.horizontal4.addWidget(self.body_btn)

        layout = QVBoxLayout()
        layout.addLayout(self.horizontal1)
        layout.addLayout(self.horizontal2)
        layout.addLayout(self.horizontal3)
        layout.addLayout(self.horizontal4)
        layout.addWidget(self.browser)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def get_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        if (url != 'http://'):
            response = requests.get(
                url, auth=self.auth)
            if (response.status_code == 200):
                self.browser.setHtml(response.text)
            else:
                self.browser.setHtml(self.invalid_method_html)
        else:
            self.browser.setHtml(self.invalid_method_html)

    def post_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        if (url != 'http://'):
            response = requests.post(
                url, auth=self.auth, json=self.item)
            if (response.status_code == 201):
                self.browser.setHtml(response.text)
            else:
                self.browser.setHtml(self.invalid_method_html)
        else:
            self.browser.setHtml(self.invalid_method_html)

    def delete_request(self, url: str):
        if (not url.startswith('http://')):
            url = 'http://' + url
            self.url_bar.setText(url)
        if (url != 'http://'):
            response = requests.delete(url, auth=self.auth, json=self.item)
            if (response.status_code == 204):
                self.browser.setHtml(
                    strings.start_html + strings.item_deleted_successfully+strings.end_html)
            else:
                self.browser.setHtml(self.invalid_method_html)
        else:
            self.browser.setHtml(self.invalid_method_html)

    def save_item(self):
        name = self.name_value_bar.toPlainText()
        if (name == ''):
            name = 'None',
        try:
            price = float(self.price_value_bar.toPlainText())
        except:
            price = 0
        self.item = {'name': name, 'price': price}

    def save_auth(self):
        name = self.username_bar.toPlainText()
        password = self.password_bar.toPlainText()
        self.auth = HTTPBasicAuth(name, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
