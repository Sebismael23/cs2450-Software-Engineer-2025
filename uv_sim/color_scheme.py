import json
import os
from PyQt5.QtWidgets import QInputDialog

class ColorScheme:
    CONFIG_FILE = "color_config.json"

    def __init__(self):
        self.color_config = self.load_color_config()

    def load_color_config(self):
        # Default UVU colors: primary is dark green, off-color is white.
        default_config = {
            "primary_color": "#4C721D",
            "off_color": "#FFFFFF"
        }
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    # Basic validation: Check that both keys exist and are strings.
                    if ("primary_color" in config and "off_color" in config and
                        isinstance(config["primary_color"], str) and isinstance(config["off_color"], str)):
                        return config
            except Exception as e:
                print("Error loading color configuration:", e)
        return default_config

    def save_color_config(self):
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(self.color_config, f, indent=4)
        except Exception as e:
            print("Error saving color configuration:", e)

    def apply_color_scheme(self, widget):
        primary = self.color_config["primary_color"]
        off = self.color_config["off_color"]
        style = f"""
        QWidget {{
            background-color: {off};
            color: #333333;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12pt;
        }}
        QLineEdit {{
            background-color: #F0F0F0;
            border: 1px solid {primary};
            padding: 4px;
            color: #333333;
        }}
        QPushButton {{
            background-color: {primary};
            border: none;
            padding: 6px 12px;
            color: {off};
        }}
        QPushButton:hover {{
            background-color: #666666;
        }}
        QTextEdit {{
            background-color: #F0F0F0;
            border: 1px solid {primary};
            color: #333333;
        }}
        QLabel {{
            font-weight: bold;
        }}
        QScrollArea {{
            border: none;
        }}
        /* Style the vertical scrollbar */
        QScrollBar:vertical {{
            background: {off};
            width: 15px;
            margin: 15px 3px 15px 3px;
        }}
        QScrollBar::handle:vertical {{
            background: {primary};
            min-height: 20px;
            border-radius: 7px;
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background: none;
        }}
        """
        widget.setStyleSheet(style)

    def configure_color_scheme(self, widget, console_output):
        # Allow user to enter a new primary color.
        primary, ok1 = QInputDialog.getText(
            widget, "Set Primary Color", 
            "Enter primary color (hex, e.g., #4C721D):", text=self.color_config["primary_color"]
        )
        if not ok1 or not primary.strip():
            return
        
        off, ok2 = QInputDialog.getText(
            widget, "Set Off-Color", 
            "Enter off-color (hex, e.g., #FFFFFF):", text=self.color_config["off_color"]
        )
        if not ok2 or not off.strip():
            return

        # Basic validation: ensure they start with '#' and have 7 characters.
        if not (primary.startswith("#") and len(primary) == 7 and off.startswith("#") and len(off) == 7):
            console_output.append("Error: Colors must be in hex format (e.g., #RRGGBB).")
            return
        
        self.color_config["primary_color"] = primary
        self.color_config["off_color"] = off
        self.save_color_config()
        self.apply_color_scheme(widget)
        console_output.append("Color scheme updated.")