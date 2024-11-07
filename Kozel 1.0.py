from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class KozelBrowser(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.setWindowTitle("Козел")
        self.setGeometry(100, 100, 1200, 800)

        # Создание виджета для вкладок
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.open_new_tab)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        # Панель инструментов
        self.nav_bar = QtWidgets.QToolBar("Навигация")
        self.addToolBar(self.nav_bar)

        # Кнопка "Назад"
        back_button = QtWidgets.QAction("Назад", self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.nav_bar.addAction(back_button)

        # Кнопка "Вперед"
        forward_button = QtWidgets.QAction("Вперед", self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.nav_bar.addAction(forward_button)

        # Кнопка "Обновить"
        reload_button = QtWidgets.QAction("Обновить", self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.nav_bar.addAction(reload_button)

        # Поле ввода URL
        self.url_bar = QtWidgets.QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        # Открытие домашней страницы в новой вкладке
        self.add_new_tab(QtCore.QUrl("https://www.google.com"), "Новая вкладка")

        # Создание меню
        self.create_menu()

        # Режим компактности
        self.is_compact_mode = False
        self.set_shortcut_keys()

    def set_shortcut_keys(self):
        # Настройка горячей клавиши F3 для переключения компактного режима
        self.shortcut_f3 = QtWidgets.QShortcut(QtCore.Qt.Key_F3, self)
        self.shortcut_f3.activated.connect(self.toggle_compact_mode)

    def toggle_compact_mode(self):
        self.is_compact_mode = not self.is_compact_mode
        if self.is_compact_mode:
            # Включаем компактный режим
            self.setWindowTitle("Козел - Компактный режим")
            self.url_bar.hide()
            self.nav_bar.hide()
            self.resize(800, 600)  # Уменьшаем размер окна
        else:
            # Отключаем компактный режим
            self.setWindowTitle("Козел")
            self.url_bar.show()
            self.nav_bar.show()
            self.resize(1200, 800)  # Восстанавливаем размер окна

    def create_menu(self):
        # Создаем меню-бар
        menu_bar = self.menuBar()

        # Добавляем меню "Настройки"
        settings_menu = menu_bar.addMenu("Настройки")

        # Пункт для переключения темы
        self.theme_action = QtWidgets.QAction("Переключить тему", self, checkable=True)
        self.theme_action.setChecked(False)  # по умолчанию светлая тема
        self.theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(self.theme_action)

        # Пункт для режима инкогнито
        self.incognito_action = QtWidgets.QAction("Инкогнито", self, checkable=True)
        self.incognito_action.triggered.connect(self.toggle_incognito_mode)
        settings_menu.addAction(self.incognito_action)

        # Пункт для режима только чтения
        self.readonly_action = QtWidgets.QAction("Только чтение", self, checkable=True)
        self.readonly_action.triggered.connect(self.toggle_readonly_mode)
        settings_menu.addAction(self.readonly_action)

        # Пункт для простого интерфейса
        self.simple_ui_action = QtWidgets.QAction("Простой интерфейс", self, checkable=True)
        self.simple_ui_action.triggered.connect(self.toggle_simple_ui_mode)
        settings_menu.addAction(self.simple_ui_action)

        # Пункт для режима WinXP
        self.winxp_action = QtWidgets.QAction("WinXP стиль", self, checkable=True)
        self.winxp_action.triggered.connect(self.toggle_winxp_mode)
        settings_menu.addAction(self.winxp_action)

        # Пункт для режима Internet Explorer 11
        self.ie11_action = QtWidgets.QAction("Internet Explorer 11", self, checkable=True)
        self.ie11_action.triggered.connect(self.toggle_ie11_mode)
        settings_menu.addAction(self.ie11_action)

    def toggle_theme(self):
        if self.theme_action.isChecked():
            self.setStyleSheet("""
                QMainWindow { background-color: #2E2E2E; }
                QToolBar { background-color: #444444; }
                QTabWidget::pane { border: 1px solid #555555; background: #444444; }
                QLineEdit { background: #666666; border: 1px solid #555555; color: white; }
                QPushButton, QToolButton { background-color: #444444; border: 1px outset #555555; color: white; }
                QPushButton:hover, QToolButton:hover { background-color: #333333; }
                QMenuBar { background-color: #444444; color: white; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #FFFFFF; }
                QToolBar { background-color: #F1F1F1; }
                QTabWidget::pane { border: 1px solid #CCCCCC; background: #F1F1F1; }
                QLineEdit { background: white; border: 1px solid #CCCCCC; color: black; }
                QPushButton, QToolButton { background-color: #F1F1F1; border: 1px outset #CCCCCC; color: black; }
                QPushButton:hover, QToolButton:hover { background-color: #E0E0E0; }
                QMenuBar { background-color: #F1F1F1; color: black; }
            """)

    def toggle_incognito_mode(self):
        if self.incognito_action.isChecked():
            self.setWindowTitle("Козел - Режим инкогнито")
        else:
            self.setWindowTitle("Козел")

    def toggle_readonly_mode(self):
        if self.readonly_action.isChecked():
            self.url_bar.setDisabled(True)
            self.tabs.currentWidget().setDisabled(True)
        else:
            self.url_bar.setDisabled(False)
            self.tabs.currentWidget().setDisabled(False)

    def toggle_simple_ui_mode(self):
        if self.simple_ui_action.isChecked():
            self.nav_bar.hide()
        else:
            self.nav_bar.show()

    def toggle_winxp_mode(self):
        if self.winxp_action.isChecked():
            self.setWindowTitle("Козел - WinXP стиль")
            self.setStyleSheet("""
                QMainWindow { background-color: #E1E1E1; }
                QToolBar { background-color: #D4D0C8; border: 1px solid #808080; }
                QTabWidget::pane { border: 1px solid #808080; background: #D4D0C8; }
                QLineEdit { background: white; border: 1px solid #808080; padding: 3px; }
                QPushButton, QToolButton { background-color: #D4D0C8; border: 1px outset #808080; }
                QPushButton:hover, QToolButton:hover { background-color: #B0B0B0; }
            """)
        else:
            self.setWindowTitle("Козел")
            self.setStyleSheet("")

    def toggle_ie11_mode(self):
        if self.ie11_action.isChecked():
            self.setWindowTitle("Козел - Internet Explorer 11")
            self.setStyleSheet("""
                QMainWindow { background-color: #F1F1F1; }
                QToolBar { background-color: #E0E0E0; border: 1px solid #B0B0B0; }
                QTabWidget::pane { border: 1px solid #B0B0B0; background: #E0E0E0; }
                QLineEdit { background: white; border: 1px solid #B0B0B0; padding: 4px; font-family: 'Segoe UI', Tahoma, sans-serif; }
                QPushButton, QToolButton { background-color: #E0E0E0; border: 1px solid #B0B0B0; font-family: 'Segoe UI', Tahoma, sans-serif; }
                QPushButton:hover, QToolButton:hover { background-color: #C0C0C0; }
            """)
        else:
            self.setWindowTitle("Козел")
            self.setStyleSheet("")

    def add_new_tab(self, url=QtCore.QUrl("https://www.google.com"), label="Новая вкладка"):
        browser = QWebEngineView()
        browser.setUrl(url)
        self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

    def update_url_bar(self, qurl, browser=None):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http") and not url.startswith("Kozelsite://"):
            url = "Kozelsite://" + url
        self.tabs.currentWidget().setUrl(QtCore.QUrl(url))

    def open_new_tab(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

# Запуск приложения
app = QtWidgets.QApplication(sys.argv)
window = KozelBrowser()
window.show()
sys.exit(app.exec_())
