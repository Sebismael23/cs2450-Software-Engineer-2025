import os
from PyQt5.QtWidgets import QFileDialog

def load_instruction_file(gui_instance):
    """Load instructions from a text file into memory."""
    file_path, _ = QFileDialog.getOpenFileName(
        gui_instance,
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
                        if -999999 <= instruction <= 999999:
                            instructions.append(instruction)
                        else:
                            raise ValueError(f"Instruction {instruction} out of valid range (-999999 to 999999)")
                    except ValueError as e:
                        gui_instance.console_output.append(f"Error parsing instruction: {line}")
                        return
            
            # Clear existing memory
            for label in gui_instance.memory_labels:
                label.setText("000000")
            
            # Load the new instructions
            for i, instruction in enumerate(instructions):
                if i < 250:  # Ensure we don't exceed memory size
                    gui_instance.memory_labels[i].setText(f"{instruction:+07d}")
                else:
                    gui_instance.console_output.append("Warning: Program exceeds memory size. Some instructions were not loaded.")
                    break
            
            gui_instance.console_output.append(f"Successfully loaded {min(len(instructions), 250)} instructions from {os.path.basename(file_path)}")
            
    except Exception as e:
        gui_instance.console_output.append(f"Error loading file: {str(e)}")

def save_instruction_file(gui_instance):
    """Save the current memory contents to a text file."""
    file_path, _ = QFileDialog.getSaveFileName(
        gui_instance,
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
            for i, label in enumerate(gui_instance.memory_labels):
                try:
                    value = int(label.text())
                    if value != 0:  # Only write non-zero values
                        file.write(f"{value:+07d}\n")
                        instructions_written += 1
                except ValueError:
                    gui_instance.console_output.append(f"Warning: Invalid value in memory location {i}, skipping...")
                    continue
            
            gui_instance.console_output.append(f"Successfully saved {instructions_written} instructions to {os.path.basename(file_path)}")
            
    except Exception as e:
        gui_instance.console_output.append(f"Error saving file: {str(e)}")
