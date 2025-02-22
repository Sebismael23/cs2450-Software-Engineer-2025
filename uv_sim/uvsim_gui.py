import sys
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
    QInputDialog  # Added for modal input
)
from memory_structure import UVSimMemory
from operations import UVSimOperations
from UVSim import UVSim

class UVSimGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.uvsim = UVSim()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("UVSim - Virtual Machine")
        self.setGeometry(100, 100, 1600, 1200)
        
        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
            }
            QLineEdit {
                background-color: #3c3f41;
                border: 1px solid #555;
                padding: 4px;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #555;
                border: none;
                padding: 6px 12px;
                color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QTextEdit {
                background-color: #3c3f41;
                border: 1px solid #555;
                color: #f0f0f0;
            }
            QLabel {
                font-weight: bold;
            }
            QScrollArea {
                border: none;
            }
        """)

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
        
        # Adding layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)
        
        # Connect buttons to functionality
        self.run_button.clicked.connect(self.run_program)
        self.step_button.clicked.connect(self.step_execution)
        self.reset_button.clicked.connect(self.reset_simulator)
        self.halt_button.clicked.connect(self.halt_execution)
    
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
                # Blocking modal dialog to wait for input
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
        # Halt
        self.uvsim.program_counter = 100
        self.uvsim.operations.halt()
        self.update_memory_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVSimGUI()
    window.show()
    sys.exit(app.exec_())
