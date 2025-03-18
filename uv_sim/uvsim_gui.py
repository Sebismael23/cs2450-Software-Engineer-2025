import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QLineEdit,
    QScrollArea,
    QInputDialog
)
from memory_structure import UVSimMemory
from operations import UVSimOperations
from UVSim import UVSim

class UVSimGUI(QWidget):
    CONFIG_FILE = "color_config.json"

    def __init__(self):
        super().__init__()
        self.uvsim = UVSim()
        self.color_config = self.load_color_config()
        self.initUI()
        self.apply_color_scheme()
    
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

    def apply_color_scheme(self):
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
        self.setStyleSheet(style)


    def initUI(self):
        self.setWindowTitle("UVSim - Virtual Machine")
        self.setGeometry(100, 100, 1600, 1200)
        
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        # Memory Display (Left Panel as a Scrollable List)
        self.memory_labels = []
        memory_container = QWidget()
        memory_layout = QVBoxLayout(memory_container)
        
        for i in range(100):
            mem_label = QLineEdit("0000")
            mem_label.setFixedWidth(80)
            memory_layout.addWidget(mem_label)
            self.memory_labels.append(mem_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(memory_container)
        scroll_area.setFixedHeight(1100)
        left_layout.addWidget(scroll_area)
        
        # User Input Section (Top Right)
        self.user_input = QLineEdit()
        right_layout.addWidget(QLabel("User Input (for READ instructions):"))
        right_layout.addWidget(self.user_input)
        
        # Controls (Below User Input)
        self.run_button = QPushButton("Run")
        self.step_button = QPushButton("Step Execution")
        self.reset_button = QPushButton("Reset")
        self.halt_button = QPushButton("Halt")
        
        right_layout.addWidget(self.run_button)
        right_layout.addWidget(self.step_button)
        right_layout.addWidget(self.reset_button)
        right_layout.addWidget(self.halt_button)
        
        # Console Output (Below Buttons)
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        right_layout.addWidget(QLabel("Console Output:"))
        right_layout.addWidget(self.console_output)
        
        # Accumulator & Program Counter (Bottom Right)
        self.accumulator_label = QLabel("Accumulator: 0000")
        self.program_counter_label = QLabel("Program Counter: 00")
        right_layout.addWidget(self.accumulator_label)
        right_layout.addWidget(self.program_counter_label)
        
        # Add button to configure color scheme
        self.config_button = QPushButton("Configure Color Scheme")
        right_layout.addWidget(self.config_button)
        self.config_button.clicked.connect(self.configure_color_scheme)
        
        # Adding layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)
        
        # Connect buttons to functionality
        self.run_button.clicked.connect(self.run_program)
        self.step_button.clicked.connect(self.step_execution)
        self.reset_button.clicked.connect(self.reset_simulator)
        self.halt_button.clicked.connect(self.halt_execution)
    
    def configure_color_scheme(self):
        # Allow user to enter a new primary color.
        primary, ok1 = QInputDialog.getText(
            self, "Set Primary Color", 
            "Enter primary color (hex, e.g., #4C721D):", text=self.color_config["primary_color"]
        )
        if not ok1 or not primary.strip():
            return
        
        off, ok2 = QInputDialog.getText(
            self, "Set Off-Color", 
            "Enter off-color (hex, e.g., #FFFFFF):", text=self.color_config["off_color"]
        )
        if not ok2 or not off.strip():
            return

        # Basic validation: ensure they start with '#' and have 7 characters.
        if not (primary.startswith("#") and len(primary) == 7 and off.startswith("#") and len(off) == 7):
            self.console_output.append("Error: Colors must be in hex format (e.g., #RRGGBB).")
            return
        
        self.color_config["primary_color"] = primary
        self.color_config["off_color"] = off
        self.save_color_config()
        self.apply_color_scheme()
        self.console_output.append("Color scheme updated.")

    def update_memory_display(self):
        for i in range(100):
            self.memory_labels[i].setText(f"{self.uvsim.memory.get_value(i):+05d}")
        self.accumulator_label.setText(f"Accumulator: {self.uvsim.accumulator:+05d}")
        self.program_counter_label.setText(f"Program Counter: {self.uvsim.program_counter:02d}")
    
    def load_program_from_memory_labels(self):
        self.console_output.append("Loading program into memory...")
        program = []
        for i in range(100):
            try:
                instruction = int(self.memory_labels[i].text())
                if -9999 <= instruction <= 9999:
                    program.append(instruction)
                else:
                    self.console_output.append(f"Error: Invalid instruction at memory[{i}]: {instruction}")
                    return None
            except ValueError:
                self.console_output.append(f"Error: Non-numeric value in memory[{i}]")
                return None
        return program

    def execute_instruction(self):
        """Executes a single instruction and returns True if execution should continue."""
        if self.uvsim.program_counter < 0 or self.uvsim.program_counter >= 100:
            self.console_output.append("Program counter out of range. Halting execution.")
            return False
        
        instruction = self.uvsim.memory.get_value(self.uvsim.program_counter)
        opcode = instruction // 100
        operand = instruction % 100
        self.console_output.append(f"Executing instruction at {self.uvsim.program_counter:02d}: opcode {opcode}, operand {operand}")
        
        if opcode == 10:  # READ
            text_value = self.user_input.text().strip()
            if text_value == "":
                value, ok = QInputDialog.getInt(
                    self,
                    "Input Required",
                    "Enter an integer:",
                    0, -9999, 9999, 1
                )
                if not ok:
                    self.console_output.append("Error: Input cancelled.")
                    return False
            else:
                try:
                    value = int(text_value)
                except ValueError:
                    self.console_output.append("Error: Invalid integer input for READ.")
                    return False

            if -9999 <= value <= 9999:
                self.uvsim.memory.set_value(operand, value)
                self.console_output.append(f"READ: Stored {value:+05d} in memory[{operand}]")
                self.user_input.clear()
            else:
                self.console_output.append("Error: Value out of range for READ instruction.")
                return False
        elif opcode == 11:  # WRITE
            value = self.uvsim.memory.get_value(operand)
            self.console_output.append(f"WRITE: Memory[{operand}] = {value:+05d}")
        elif opcode == 20:  # LOAD
            self.uvsim.accumulator = self.uvsim.memory.get_value(operand)
            self.console_output.append(f"LOAD: Accumulator set to {self.uvsim.accumulator:+05d}")
        elif opcode == 21:  # STORE
            self.uvsim.memory.set_value(operand, self.uvsim.accumulator)
            self.console_output.append(f"STORE: Memory[{operand}] set to {self.uvsim.accumulator:+05d}")
        elif opcode == 30:  # ADD
            val = self.uvsim.memory.get_value(operand)
            self.uvsim.accumulator += val
            self.console_output.append(f"ADD: Accumulator updated to {self.uvsim.accumulator:+05d}")
        elif opcode == 31:  # SUBTRACT
            val = self.uvsim.memory.get_value(operand)
            self.uvsim.accumulator -= val
            self.console_output.append(f"SUBTRACT: Accumulator updated to {self.uvsim.accumulator:+05d}")
        elif opcode == 32:  # DIVIDE
            val = self.uvsim.memory.get_value(operand)
            if val == 0:
                self.console_output.append("Error: Division by zero. Halting execution.")
                return False
            self.uvsim.accumulator //= val
            self.console_output.append(f"DIVIDE: Accumulator updated to {self.uvsim.accumulator:+05d}")
        elif opcode == 33:  # MULTIPLY
            val = self.uvsim.memory.get_value(operand)
            self.uvsim.accumulator *= val
            self.console_output.append(f"MULTIPLY: Accumulator updated to {self.uvsim.accumulator:+05d}")
        elif opcode == 40:  # BRANCH
            self.console_output.append(f"BRANCH: Jumping to address {operand:02d}")
            self.uvsim.program_counter = operand
            self.update_memory_display()
            return True  # Skip the normal increment below
        elif opcode == 41:  # BRANCHNEG
            if self.uvsim.accumulator < 0:
                self.console_output.append(f"BRANCHNEG: Accumulator negative, jumping to address {operand:02d}")
                self.uvsim.program_counter = operand
                self.update_memory_display()
                return True
            else:
                self.console_output.append("BRANCHNEG: Accumulator not negative, no branch.")
        elif opcode == 42:  # BRANCHZERO
            if self.uvsim.accumulator == 0:
                self.console_output.append(f"BRANCHZERO: Accumulator zero, jumping to address {operand:02d}")
                self.uvsim.program_counter = operand
                self.update_memory_display()
                return True
            else:
                self.console_output.append("BRANCHZERO: Accumulator not zero, no branch.")
        elif opcode == 43:  # HALT
            self.console_output.append("HALT: Program execution halted.")
            self.uvsim.program_counter = 100  # force end
            self.update_memory_display()
            return False
        else:
            self.console_output.append(f"Error: Unknown opcode {opcode}. Halting execution.")
            return False
        
        self.uvsim.program_counter += 1
        self.update_memory_display()
        return True

    def run_program(self):
        program = self.load_program_from_memory_labels()
        if program is None:
            return
        self.uvsim.load_program(program)
        self.console_output.append("Program loaded. Running program...")
        
        execution_limit = 1000
        step_count = 0
        continue_exec = True
        while continue_exec and step_count < execution_limit:
            continue_exec = self.execute_instruction()
            step_count += 1
        if step_count >= execution_limit:
            self.console_output.append("Execution halted due to reaching execution limit.")
        self.update_memory_display()

    def step_execution(self):
        self.console_output.append("Executing one step...")
        if self.uvsim.program_counter >= 100:
            self.console_output.append("Program counter out of range. Cannot step further.")
            return
        self.execute_instruction()

    def reset_simulator(self):
        self.console_output.clear()
        self.console_output.append("Simulator reset.")
        self.uvsim = UVSim()
        self.update_memory_display()
    
    def halt_execution(self):
        self.console_output.append("Program halted by user.")
        self.uvsim.program_counter = 100
        self.uvsim.operations.halt()
        self.update_memory_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVSimGUI()
    window.show()
    sys.exit(app.exec_())
