import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit,
    QLineEdit, QScrollArea, QInputDialog
)
from UVSim import UVSim
from file_functions import load_instruction_file, save_instruction_file

class UVSimTab(QWidget):
    def __init__(self, color_scheme, parent=None):
        super().__init__(parent)
        self.uvsim = UVSim()
        self.color_scheme = color_scheme
        self.file_path = None  # Track associated file
        self.file_format = "6-digit"  # Default to new format
        self.initUI()
        self.color_scheme.apply_color_scheme(self)

    def initUI(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Memory Display
        self.memory_labels = []
        memory_container = QWidget()
        memory_layout = QVBoxLayout(memory_container)

        for i in range(250):
            mem_row_layout = QHBoxLayout()
            addr_label = QLabel(f"{i:03d}:")
            addr_label.setFixedWidth(40)
            mem_row_layout.addWidget(addr_label)
            mem_label = QLineEdit("+000000")
            mem_label.setFixedWidth(80)
            mem_row_layout.addWidget(mem_label)
            memory_layout.addLayout(mem_row_layout)
            self.memory_labels.append(mem_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(memory_container)
        left_layout.addWidget(scroll_area)

        # User Input
        self.user_input = QLineEdit()
        right_layout.addWidget(QLabel("User Input (for READ instructions):"))
        right_layout.addWidget(self.user_input)

        # Controls
        self.run_button = QPushButton("Run")
        self.step_button = QPushButton("Step Execution")
        self.reset_button = QPushButton("Reset")
        self.halt_button = QPushButton("Halt")
        file_buttons_layout = QHBoxLayout()
        self.load_file_button = QPushButton("Load Instructions File")
        self.save_file_button = QPushButton("Save Instructions")
        file_buttons_layout.addWidget(self.load_file_button)
        file_buttons_layout.addWidget(self.save_file_button)

        right_layout.addWidget(self.run_button)
        right_layout.addWidget(self.step_button)
        right_layout.addWidget(self.reset_button)
        right_layout.addWidget(self.halt_button)
        right_layout.addLayout(file_buttons_layout)

        # Console Output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        right_layout.addWidget(QLabel("Console Output:"))
        right_layout.addWidget(self.console_output)

        # Accumulator & Program Counter
        self.accumulator_label = QLabel("Accumulator: 0000")
        self.program_counter_label = QLabel("Program Counter: 000")
        right_layout.addWidget(self.accumulator_label)
        right_layout.addWidget(self.program_counter_label)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

        # Connect buttons
        self.run_button.clicked.connect(self.run_program)
        self.step_button.clicked.connect(self.step_execution)
        self.reset_button.clicked.connect(self.reset_simulator)
        self.halt_button.clicked.connect(self.halt_execution)
        self.load_file_button.clicked.connect(self.load_file)
        self.save_file_button.clicked.connect(self.save_file)

    def load_file(self):
        load_instruction_file(self)
        if self.file_path:
            self.console_output.append(f"Loaded file: {self.file_path}")

    def save_file(self):
        save_instruction_file(self)
        if self.file_path:
            self.console_output.append(f"Saved file: {self.file_path}")

    def update_memory_display(self):
        if not hasattr(self, 'file_format'):
            self.file_format = "6-digit"  # Default to new format
            
        for i in range(min(250, len(self.memory_labels))):  # Updated to support 250 memory locations
            value = self.uvsim.memory.get_value(i)
            if self.file_format == "4-digit":
                self.memory_labels[i].setText(f"{value:+05d}")
            else:  # 6-digit
                self.memory_labels[i].setText(f"{value:+07d}")
                
        self.accumulator_label.setText(f"Accumulator: {self.uvsim.accumulator:+05d}")
        self.program_counter_label.setText(f"Program Counter: {self.uvsim.program_counter:03d}")
        
    def load_program_from_memory_labels(self):
        self.console_output.append("Loading program into memory...")
        program = []
        
        # Check if format is alredy determind
        if not hasattr(self, 'file_format'):
            self.file_format = "6-digit"  # Default to new format
        
        for i in range(250):  # UVSim memory size
            try:
                instruction = int(self.memory_labels[i].text())
                if instruction == 0:
                    program.append(0)  # Add zero instructions
                    continue
                    
                # Validate against the current format
                if self.file_format == "4-digit":
                    if -9999 <= instruction <= 9999:
                        program.append(instruction)
                    else:
                        self.console_output.append(f"Error: Invalid 4-digit instruction at memory[{i}]: {instruction}")
                        return None
                else:  # 6-digit
                    if -999999 <= instruction <= 999999:
                        program.append(instruction)
                    else:
                        self.console_output.append(f"Error: Invalid 6-digit instruction at memory[{i}]: {instruction}")
                        return None
            except ValueError:
                self.console_output.append(f"Error: Non-numeric value in memory[{i}]")
                return None
        
        self.console_output.append(f"Program loaded in {self.file_format} format")
        return program


    def read_user_input(self):
        text_value = self.user_input.text().strip()
        if text_value == "":
            value, ok = QInputDialog.getInt(
                self, "Input Required", "Enter an integer:",
                0, -999999, 999999, 1
            )
            if not ok:
                self.console_output.append("Error: Input cancelled.")
                return None
        else:
            try:
                value = int(text_value)
            except ValueError:
                self.console_output.append("Error: Invalid integer input for READ.")
                return None
        return value

    def run_program(self):
        program = self.load_program_from_memory_labels()
        if program is None:
            return
            
        # Modify the instruction parsing based on format
        self.uvsim.load_program(program)
        self.console_output.append(f"Program loaded in {self.file_format} format. Running program...")

        execution_limit = 1000
        step_count = 0
        continue_exec = True

        while continue_exec and step_count < execution_limit:
            instruction = self.uvsim.memory.get_value(self.uvsim.program_counter)
            
            # Parse opcode and operand differently based on format
            if self.file_format == "4-digit":
                opcode = instruction // 100
                operand = instruction % 100
            else:  # 6-digit
                opcode = instruction // 1000
                operand = instruction % 1000
                
            self.console_output.append(f"Step {step_count + 1}: PC = {self.uvsim.program_counter:03d}, Opcode = {opcode}, Operand = {operand}")

            if opcode == 10:
                value = self.read_user_input()
                if value is None:
                    self.console_output.append("Error: No input provided for READ instruction.")
                    break
                self.uvsim.memory.set_value(operand, value)
            try:
                self.uvsim.instruction_register = instruction
                self.uvsim.opcode = opcode
                self.uvsim.operand = operand
                if opcode == 43:
                    self.console_output.append("HALT instruction encountered.")
                    continue_exec = False
                elif opcode in [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42]:
                    result, continue_exec = self.uvsim.run(value=None)
                    self.console_output.append(result)
                else:
                    self.console_output.append(f"Unknown opcode: {opcode}")
                    break
            except Exception as e:
                self.console_output.append(f"Error executing instruction: {str(e)}")
                break

            self.update_memory_display()
            step_count += 1

        if step_count >= execution_limit:
            self.console_output.append("Execution halted due to reaching execution limit.")


    def step_execution(self):
        self.console_output.append("Executing one step...")
        if self.uvsim.program_counter >= 250:
            self.console_output.append("Program counter out of range. Cannot step further.")
            return
        try:
            instruction = self.uvsim.memory.get_value(self.uvsim.program_counter)
            
            # Parse opcode and operand based on format
            if self.file_format == "4-digit":
                opcode = instruction // 100
                operand = instruction % 100
            else:  # 6-digit
                opcode = instruction // 1000
                operand = instruction % 1000
                
            self.console_output.append(f"Step: PC = {self.uvsim.program_counter:03d}, Opcode = {opcode}, Operand = {operand}")
            
            if opcode == 10:
                value = self.read_user_input()
                if value is None:
                    self.console_output.append("Error: No input provided for READ instruction.")
                    return
                self.uvsim.memory.set_value(operand, value)
            self.uvsim.instruction_register = instruction
            self.uvsim.opcode = opcode
            self.uvsim.operand = operand
            if opcode == 43:
                self.console_output.append("HALT instruction encountered.")
            elif opcode in [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42]:
                result, continue_exec = self.uvsim.run(value=None)
                self.console_output.append(result)
            else:
                self.console_output.append(f"Unknown opcode: {opcode}")
            self.update_memory_display()
        except Exception as e:
            self.console_output.append(f"Error executing instruction: {str(e)}")
        
    def reset_simulator(self):
        self.console_output.clear()
        self.console_output.append("Simulator reset.")
        self.uvsim = UVSim()
        for label in self.memory_labels:
            label.setText("+000000")
        self.update_memory_display()

    def halt_execution(self):
        self.console_output.append("Program halted by user.")
        self.uvsim.program_counter = 100
        self.update_memory_display()