import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def detect_file_format(instructions):
    """
    Detect if a file contains 4-digit or 6-digit instructions.
    
    Args:
        instructions: List of parsed integer instructions
    
    Returns:
        str: "4-digit" or "6-digit" or None if empty list
    """
    if not instructions:
        return None
        
    # Check the range of each instruction
    four_digit_count = 0
    six_digit_count = 0
    
    for instruction in instructions:
        if -9999 <= instruction <= 9999:
            four_digit_count += 1
        if -999999 <= instruction <= 999999:
            six_digit_count += 1
    
    # If all instructions fit in 4-digit range
    if four_digit_count == len(instructions):
        # Check if any instruction has 5 or 6 digits
        for instruction in instructions:
            if abs(instruction) >= 10000:
                return "6-digit"
        return "4-digit"
    else:
        return "6-digit"

def convert_4digit_to_6digit(instruction):
    """
    Convert a 4-digit instruction to 6-digit format.
    
    Args:
        instruction: 4-digit instruction integer
    
    Returns:
        int: 6-digit equivalent instruction
    """
    # Get opcode and operand from 4-digit instruction
    opcode = instruction // 100
    operand = instruction % 100
    
    # Convert to 6-digit format (opcode * 1000 + operand)
    return opcode * 1000 + operand

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
            
            # Detect file format
            format_type = detect_file_format(instructions)
            if not format_type:
                tab.console_output.append("Empty file loaded.")
                return
                
            tab.file_format = format_type  # Store the detected format
            tab.console_output.append(f"Detected {format_type} instruction format")
            
            # If 4-digit format is detected, ask if user wants to convert to 6-digit
            if format_type == "4-digit":
                msg_box = QMessageBox()
                msg_box.setWindowTitle("File Format Detected")
                msg_box.setText(f"This appears to be a 4-digit format file. How would you like to proceed?")
                msg_box.addButton("Keep as 4-digit", QMessageBox.AcceptRole)
                convert_button = msg_box.addButton("Convert to 6-digit", QMessageBox.ActionRole)
                msg_box.setDefaultButton(convert_button)
                msg_box.exec_()
                
                if msg_box.clickedButton() == convert_button:
                    # Convert to 6-digit format
                    instructions = [convert_4digit_to_6digit(instr) for instr in instructions]
                    tab.console_output.append("Converted instructions to 6-digit format")
                    tab.file_format = "6-digit"  # Update format after conversion
            
            # Clear memory display
            for label in tab.memory_labels:
                label.setText("+000000")
                
            # Load instructions into memory display with appropriate formatting
            for i, instruction in enumerate(instructions):
                if i < 250:
                    if tab.file_format == "4-digit":
                        tab.memory_labels[i].setText(f"{instruction:+05d}")
                    else:  # 6-digit
                        tab.memory_labels[i].setText(f"{instruction:+07d}")
                else:
                    tab.console_output.append("Warning: Program exceeds memory size. Some instructions were not loaded.")
                    break
                    
            tab.console_output.append(f"Successfully loaded {min(len(instructions), 250)} instructions from {os.path.basename(file_path)}")
    except Exception as e:
        tab.console_output.append(f"Error loading file: {str(e)}")

def save_instruction_file(tab):
    """Save the current memory contents to a text file."""
    # Determine current format
    if not hasattr(tab, 'file_format'):
        # If format not yet determined, try to detect from memory contents
        instructions = []
        for label in tab.memory_labels:
            try:
                value = int(label.text())
                if value != 0:
                    instructions.append(value)
            except ValueError:
                continue
        
        tab.file_format = detect_file_format(instructions) or "6-digit"  # Default to 6-digit if detection fails
    
    # Ask user if they want to save in a different format
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Save Format")
    msg_box.setText(f"Current format is {tab.file_format}. How would you like to save?")
    
    # Add format options
    keep_button = msg_box.addButton(f"Keep as {tab.file_format}", QMessageBox.AcceptRole)
    
    if tab.file_format == "6-digit":
        # No option to convert to 4-digit as per requirements
        pass
    else:  # 4-digit
        convert_button = msg_box.addButton("Convert to 6-digit", QMessageBox.ActionRole)
    
    msg_box.setDefaultButton(keep_button)
    msg_box.exec_()
    
    save_format = tab.file_format
    if tab.file_format == "4-digit" and msg_box.clickedButton() != keep_button:
        # User wants to convert from 4 to 6
        save_format = "6-digit"
    
    # Ask for file path if needed
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
            file.write(f"# Format: {save_format}\n\n")
            instructions_written = 0
            
            for i, label in enumerate(tab.memory_labels):
                try:
                    value = int(label.text())
                    if value != 0:
                        # If converting from 4 to 6 digit
                        if tab.file_format == "4-digit" and save_format == "6-digit":
                            value = convert_4digit_to_6digit(value)
                            
                        # Format based on save format
                        if save_format == "4-digit":
                            file.write(f"{value:+05d}\n")
                        else:  # 6-digit
                            file.write(f"{value:+07d}\n")
                            
                        instructions_written += 1
                except ValueError:
                    tab.console_output.append(f"Warning: Invalid value in memory location {i}, skipping...")
                    continue
                    
            # Update tab's format if converting
            if tab.file_format != save_format:
                tab.file_format = save_format
                
            tab.console_output.append(f"Successfully saved {instructions_written} instructions to {os.path.basename(file_path)} in {save_format} format")
    except Exception as e:
        tab.console_output.append(f"Error saving file: {str(e)}")

def validate_instruction_format(tab):
    """
    Validate that instructions in memory are consistent with the current format.
    Returns True if valid, False otherwise.
    """
    if not hasattr(tab, 'file_format'):
        return True  # No format specified yet
        
    instructions = []
    for label in tab.memory_labels:
        try:
            value = int(label.text())
            if value != 0:
                instructions.append(value)
        except ValueError:
            continue
            
    if not instructions:
        return True  # No instructions to validate
        
    # Check if all instructions match the format
    for instruction in instructions:
        if tab.file_format == "4-digit":
            if not (-9999 <= instruction <= 9999):
                return False
        else:  # 6-digit
            if not (-999999 <= instruction <= 999999):
                return False
                
    return True