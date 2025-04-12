import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QFileDialog
)
from color_scheme import ColorScheme
from UVSimTab import UVSimTab
import os

class UVSimGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.color_scheme = ColorScheme()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("UVSim - Virtual Machine")
        self.setGeometry(100, 100, 1600, 1200)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tabs)

        # Control buttons
        controls_layout = QHBoxLayout()
        new_tab_button = QPushButton("New Tab")
        load_file_button = QPushButton("Open File")
        config_color_button = QPushButton("Color Config")
        controls_layout.addWidget(new_tab_button)
        controls_layout.addWidget(load_file_button)
        controls_layout.addWidget(config_color_button)
        main_layout.addLayout(controls_layout)

        # Connect buttons
        new_tab_button.clicked.connect(self.add_new_tab)
        load_file_button.clicked.connect(self.load_file_to_new_tab)
        config_color_button.clicked.connect(self.configure_color_scheme)

        # Add initial tab
        self.add_new_tab()

    def add_new_tab(self):
        tab = UVSimTab(self.color_scheme)
        tab_count = self.tabs.count() + 1
        self.tabs.addTab(tab, f"Program {tab_count}")
        self.tabs.setCurrentWidget(tab)
        self.color_scheme.apply_color_scheme(tab)
        return tab

    def load_file_to_new_tab(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Instructions File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            tab = self.add_new_tab()
            tab.file_path = file_path
            tab.load_file()
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(file_path))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.statusBar().showMessage("Cannot close the last tab.")

    def configure_color_scheme(self):
        if self.tabs.count() > 0:
            current_tab = self.tabs.currentWidget()
            self.color_scheme.configure_color_scheme(self, current_tab.console_output)
            for i in range(self.tabs.count()):
                tab = self.tabs.widget(i)
                self.color_scheme.apply_color_scheme(tab)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVSimGUI()
    window.show()
    sys.exit(app.exec_())
