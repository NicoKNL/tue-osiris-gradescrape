import sys
import os
import json
from PyQt5.QtCore import QEventLoop, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup

class Render(QWebEngineView):
    def __init__(self, url, app, osiris_login):
        self.html = None
        self.app = app # QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        self.osiris_login = osiris_login
        # TODO: remove osiris_url dependency
        osiris_url = r"https://osiris.tue.nl/osiris_student_tueprd/ToonResultaten.do"

        while self.html is None or self.page().url().toString() != osiris_url or "<title>Working...</title>" in self.html:
            self.app.processEvents(
                QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)
        # self.app.quit()

    def _callable(self, data):
        self.html = data

    def _loadFinished(self, result):
        self.page().runJavaScript(f"document.getElementById(Login.userNameInput).value=\'{self.osiris_login['UserName']}\'")
        self.page().runJavaScript(f"document.getElementById(Login.passwordInput).value=\'{self.osiris_login['Password']}\'")
        self.page().runJavaScript(f"document.forms['loginForm'].submit()")
        self.page().toHtml(self._callable)