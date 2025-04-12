import os
from PyQt5.QtWidgets import QFileDialog

def load_instruction_file(tab):
    """Load instructions from a text file into memory."""
    file_path, _ = QFileDialog.getOpenFileName(
        tab, "Select Instructions File", "",
        "Text Files (*.txt);;All Files (*)"
    )
    if not file_path:
        return
    tab.file_path = file_path
    try:
        with open(file_path, 'r') as file:
            instructions = []
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        instruction = int(line)
                        if -999999 <= instruction <= 999999:
                            instructions.append(instruction)
                        else:
                            raise ValueError(f"Instruction {instruction} out of valid range (-999999 to 999999)")
                    except ValueError as e:
                        tab.console_output.append(f"Error parsing instruction: {line}")
                        return
            for label in tab.memory_labels:
                label.setText("+000000")
            for i, instruction in enumerate(instructions):
                if i < 250:
                    tab.memory_labels[i].setText(f"{instruction:+07d}")
                else:
                    tab.console_output.append("Warning: Program exceeds memory size. Some instructions were not loaded.")
                    break
            tab.console_output.append(f"Successfully loaded {min(len(instructions), 250)} instructions from {os.path.basename(file_path)}")
    except Exception as e:
        tab.console_output.append(f"Error loading file: {str(e)}")

def save_instruction_file(tab):
    """Save the current memory contents to a text file."""
    if not tab.file_path:
        file_path, _ = QFileDialog.getSaveFileName(
            tab, "Save Instructions File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            tab.file_path = file_path
    else:
        file_path = tab.file_path
    if not file_path:
        return
    try:
        with open(file_path, 'w') as file:
            file.write("# UVSim Instructions File\n")
            file.write("# Generated from memory contents\n\n")
            instructions_written = 0
            for i, label in enumerate(tab.memory_labels):
                try:
                    value = int(label.text())
                    if value != 0:
                        file.write(f"{value:+07d}\n")
                        instructions_written += 1
                except ValueError:
                    tab.console_output.append(f"Warning: Invalid value in memory location {i}, skipping...")
                    continue
            tab.console_output.append(f"Successfully saved {instructions_written} instructions to {os.path.basename(file_path)}")
    except Exception as e:
        tab.console_output.append(f"Error saving file: {str(e)}")
