import sys
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
    QInputDialog,
    QFileDialog
)
from UVSim import UVSim
from color_scheme import ColorScheme

class UVSimGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.uvsim = UVSim()
        self.color_scheme = ColorScheme() 
        self.initUI()
        self.color_scheme.apply_color_scheme(self)
    
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
        
        for i in range(250):
            # Create a horizontal layout for each memory location
            mem_row_layout = QHBoxLayout()
            
            # Add address label
            addr_label = QLabel(f"{i:03d}:")
            addr_label.setFixedWidth(40)
            mem_row_layout.addWidget(addr_label)
            
            # Add memory value QLineEdit
            mem_label = QLineEdit("+000000")
            mem_label.setFixedWidth(80)
            mem_row_layout.addWidget(mem_label)
            
            # Add the row layout to the memory container
            memory_layout.addLayout(mem_row_layout)
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
        
        # File operation buttons
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
        
        # Console Output (Below Buttons)
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        right_layout.addWidget(QLabel("Console Output:"))
        right_layout.addWidget(self.console_output)
        
        # Accumulator & Program Counter (Bottom Right)
        self.accumulator_label = QLabel("Accumulator: 0000")
        self.program_counter_label = QLabel("Program Counter: 000")
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
        self.load_file_button.clicked.connect(self.load_instruction_file)
        self.save_file_button.clicked.connect(self.save_instruction_file)
    
    def configure_color_scheme(self):
        self.color_scheme.configure_color_scheme(self, self.console_output)

    def update_memory_display(self):
        for i in range(250):
            self.memory_labels[i].setText(f"{self.uvsim.memory.get_value(i):+07}")
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
    
    def read_user_input(self):
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
        self.uvsim.load_program(program)
        self.console_output.append("Program loaded. Running program...")
        
        execution_limit = 1000
        step_count = 0
        continue_exec = True

        while continue_exec and step_count < execution_limit:
            # Get the current instruction for debugging purposes
            instruction = self.uvsim.memory.get_value(self.uvsim.program_counter)
            opcode = instruction // 100
            operand = instruction % 100
            self.console_output.append(f"Step {step_count + 1}: PC = {self.uvsim.program_counter:02d}, Opcode = {opcode}, Operand = {operand}")

            # Handle READ instruction separately (requires user input)
            if opcode == 10:
                value = self.read_user_input()
                if value is None:
                    self.console_output.append("Error: No input provided for READ instruction.")
                    break
            else:
                value = None

            # Execute the instruction using the run() method
            try:
                message, continue_exec = self.uvsim.run(value)
                self.console_output.append(message)
            except Exception as e:
                self.console_output.append(f"Error executing instruction: {str(e)}")
                break

            # Update the GUI display
            self.update_memory_display()

            # Increment step count
            step_count += 1

        if step_count >= execution_limit:
            self.console_output.append("Execution halted due to reaching execution limit.")

    def step_execution(self):
        #Still broken. Work on more later
        self.console_output.append("Executing one step...")
        if self.uvsim.program_counter >= 100:
            self.console_output.append("Program counter out of range. Cannot step further.")
            return
        
        try:
            message, continue_exec = self.uvsim.run()
            self.console_output.append(message)
            self.update_memory_display()
        except Exception as e:
            self.console_output.append(f"Error executing instruction: {str(e)}")

    def reset_simulator(self):
        self.console_output.clear()
        self.console_output.append("Simulator reset.")
        self.uvsim = UVSim()
        self.update_memory_display()
    
    def halt_execution(self):
        self.console_output.append("Program halted by user.")
        self.uvsim.program_counter = 100
        self.uvsim.control.halt()
        self.update_memory_display()

    def load_instruction_file(self):
        """Load instructions from a text file into memory."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Instructions File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as file:
                instructions = []
                for line in file:
                    # Remove any whitespace and comments
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            # Convert the instruction to an integer
                            instruction = int(line)
                            if -9999 <= instruction <= 9999:
                                instructions.append(instruction)
                            else:
                                raise ValueError(f"Instruction {instruction} out of valid range (-9999 to 9999)")
                        except ValueError as e:
                            self.console_output.append(f"Error parsing instruction: {line}")
                            return
                
                # Clear existing memory
                for label in self.memory_labels:
                    label.setText("0000")
                
                # Load the new instructions
                for i, instruction in enumerate(instructions):
                    if i < 100:  # Ensure we don't exceed memory size
                        self.memory_labels[i].setText(f"{instruction:+05d}")
                    else:
                        self.console_output.append("Warning: Program exceeds memory size. Some instructions were not loaded.")
                        break
                
                self.console_output.append(f"Successfully loaded {min(len(instructions), 100)} instructions from {os.path.basename(file_path)}")
                
        except Exception as e:
            self.console_output.append(f"Error loading file: {str(e)}")

    def save_instruction_file(self):
        """Save the current memory contents to a text file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Instructions File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as file:
                # Write a header comment
                file.write("# UVSim Instructions File\n")
                file.write("# Generated from memory contents\n\n")
                
                # Write all non-zero memory contents
                instructions_written = 0
                for i, label in enumerate(self.memory_labels):
                    try:
                        value = int(label.text())
                        if value != 0:  # Only write non-zero values
                            file.write(f"{value:+05d}\n")
                            instructions_written += 1
                    except ValueError:
                        self.console_output.append(f"Warning: Invalid value in memory location {i}, skipping...")
                        continue
                
                self.console_output.append(f"Successfully saved {instructions_written} instructions to {os.path.basename(file_path)}")
                
        except Exception as e:
            self.console_output.append(f"Error saving file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVSimGUI()
    window.show()
    sys.exit(app.exec_())
