import sys
import ctypes 
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit,
    QTabWidget, QStatusBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

try:
    myappid = 'kirko.browser.app.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

HOME_URL = "http://gemiled.unaux.com"
SEARCH_URL = "http://gemiled.unaux.com?q="

class KirkoBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kirko Web Browser")
        self.setWindowIcon(QIcon("logo.ico"))  
        self.resize(1280, 720)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        self.back_btn = QAction("← Back", self)
        self.back_btn.setStatusTip("Go back to the previous page")
        self.back_btn.triggered.connect(lambda: self.current_browser().back() if self.current_browser() else None)
        nav_bar.addAction(self.back_btn)

        self.forward_btn = QAction("Forward →", self)
        self.forward_btn.setStatusTip("Go forward to the next page")
        self.forward_btn.triggered.connect(lambda: self.current_browser().forward() if self.current_browser() else None)
        nav_bar.addAction(self.forward_btn)

        self.reload_btn = QAction("↻ Reload", self)
        self.reload_btn.setStatusTip("Reload current page")
        self.reload_btn.triggered.connect(lambda: self.current_browser().reload() if self.current_browser() else None)
        nav_bar.addAction(self.reload_btn)

        home_btn = QAction("⌂ Home", self)
        home_btn.setStatusTip("Go to home page")
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        nav_bar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search with Kirko or enter web address...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        new_tab_btn = QAction("+ New Tab", self)
        new_tab_btn.setStatusTip("Open a new tab")
        new_tab_btn.triggered.connect(lambda: self.add_new_tab(HOME_URL, "New Tab"))
        nav_bar.addAction(new_tab_btn)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.add_new_tab(HOME_URL, "Homepage")

    def add_new_tab(self, qurl_str=HOME_URL, label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(qurl_str))

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, b=browser: self.update_urlbar(qurl, b))
        browser.titleChanged.connect(lambda title, b=browser: self.update_tab_title(title, b))

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return  
        self.tabs.removeTab(i)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        if self.current_browser():
            self.current_browser().setUrl(QUrl(HOME_URL))

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        if "." in text and " " not in text:
            if not (text.startswith("http://") or text.startswith("https://")):
                url = "http://" + text
            else:
                url = text
        else:
            url = SEARCH_URL + text

        if self.current_browser():
            self.current_browser().setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(q.toString())

    def update_tab_title(self, title, browser=None):
        index = self.tabs.indexOf(browser)
        if index != -1:
            short_title = title[:15] + "..." if len(title) > 15 else title
            self.tabs.setTabText(index, short_title)

    def tab_changed(self, i):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Kirko Browser")
    
    window = KirkoBrowser()
    window.show()
    
    sys.exit(app.exec_())
