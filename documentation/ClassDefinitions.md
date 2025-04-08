# **Class Design Document**

This document outlines the classes in the UVSim project, their purposes, and their functions. The design ensures modularity, loose coupling, and proper separation of concerns.

## 1. **UVSimMemory Class**

### **Purpose**

The `UVSimMemory` class represents the memory structure of the UVSim virtual machine. It provides methods to load programs into memory, retrieve and set values at specific memory addresses, and display memory contents.

### **Fields**

- `memory`: A list of 250 integers representing the memory locations.

### **Functions**

#### `load_program(program)`

- **Purpose**: Loads a list of machine instructions (BasicML) into memory.
- **Input Parameters**:

  - `program`: A list of integers representing the program instructions.

- **Return Value**: None.
- **Pre-condition**: The program size must not exceed 250 instructions.
- **Post-condition**: Memory is populated with the program instructions.

#### `get_value(address)`

- **Purpose**: Retrieves the value stored at a given memory address.
- **Input Parameters**:

  - `address`: An integer representing the memory address (0-249).

- **Return Value**: The value stored at the specified address.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: None.

#### `set_value(address, value)`

- **Purpose**: Stores a value in a specific memory address.
- **Input Parameters**:

  - `address`: An integer representing the memory address (0-249).
  - `value`: An integer to store in memory (must be between -999999 and +999999).

- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range, and the value must be a signed six-digit number.
- **Post-condition**: The specified memory location is updated with the new value.

#### `display_memory(start, end)`

- **Purpose**: Prints memory contents from a given range.
- **Input Parameters**:

  - `start`: An integer representing the starting memory address.
  - `end`: An integer representing the ending memory address.

- **Return Value**: None.
- **Pre-condition**: The start and end addresses must be within the valid range (0-249).
- **Post-condition**: Memory contents are printed to the console.

---

## 2. **InputOutputOps Class**

### **Purpose**

The `InputOutputOps` class handles input and output operations for the UVSim virtual machine, such as reading input from the user and writing output to the console.

### **Fields**

- `memory`: An instance of `UVSimMemory` to interact with memory.

### **Functions**

#### `read(address, value)`

- **Purpose**: Reads input from the keyboard and stores it in memory.
- **Input Parameters**:

  - `address`: An integer representing the memory address to store the input.
  - `value`: An integer representing the input value.

- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range (0-249), and the value must be a signed six-digit number.
- **Post-condition**: The input value is stored in the specified memory location.

#### `write(address)`

- **Purpose**: Outputs the value of the specified memory address to the screen.
- **Input Parameters**:

  - `address`: An integer representing the memory address to read from.

- **Return Value**: The value stored at the specified address.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The value is returned for further processing.

---

## 3. **LoadStoreOps Class**

### **Purpose**

The `LoadStoreOps` class handles loading values from memory into the accumulator and storing values from the accumulator into memory.

### **Fields**

- `memory`: An instance of `UVSimMemory` to interact with memory.

### **Functions**

#### `load(address)`

- **Purpose**: Loads a value from memory into the accumulator.
- **Input Parameters**:

  - `address`: An integer representing the memory address to load from.

- **Return Value**: The value stored at the specified address.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The value is returned for further processing.

#### `store(address, accumulator)`

- **Purpose**: Stores the value from the accumulator into memory.
- **Input Parameters**:

  - `address`: An integer representing the memory address to store the value.
  - `accumulator`: An integer representing the value to store.

- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range, and the value must be a signed six-digit number.
- **Post-condition**: The specified memory location is updated with the accumulator value.

---

## 4. **ArithmeticOps Class**

### **Purpose**

The `ArithmeticOps` class handles arithmetic operations such as addition, subtraction, multiplication, and division.

### **Fields**

- `memory`: An instance of `UVSimMemory` to interact with memory.

### **Functions**

#### `add(address, accumulator)`

- **Purpose**: Adds a value from memory to the accumulator.
- **Input Parameters**:

  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The accumulator is updated with the sum.

#### `subtract(address, accumulator)`

- **Purpose**: Subtracts a value from memory from the accumulator.
- **Input Parameters**:

  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The accumulator is updated with the difference.

#### `multiply(address, accumulator)`

- **Purpose**: Multiplies the accumulator by a value from memory.
- **Input Parameters**:

  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The accumulator is updated with the product.

#### `divide(address, accumulator)`

- **Purpose**: Divides the accumulator by a value from memory.
- **Input Parameters**:

  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-249), and the divisor must not be zero.
- **Post-condition**: The accumulator is updated with the quotient.

---

## 5. **ControlOps Class**

### **Purpose**

The `ControlOps` class handles control flow operations such as branching and halting.

### **Fields**

- `memory`: An instance of `UVSimMemory` to interact with memory.

### **Functions**

#### `branch(address)`

- **Purpose**: Changes the program counter to a new address.
- **Input Parameters**:

  - `address`: An integer representing the new program counter value.

- **Return Value**: The new program counter value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The program counter is updated.

#### `branchneg(address, accumulator)`

- **Purpose**: Changes the program counter if the accumulator is negative.
- **Input Parameters**:

  - `address`: An integer representing the new program counter value.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The new program counter value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The program counter is updated if the accumulator is negative.

#### `branchzero(address, accumulator)`

- **Purpose**: Changes the program counter if the accumulator is zero.
- **Input Parameters**:

  - `address`: An integer representing the new program counter value.
  - `accumulator`: An integer representing the current accumulator value.

- **Return Value**: The new program counter value.
- **Pre-condition**: The address must be within the valid range (0-249).
- **Post-condition**: The program counter is updated if the accumulator is zero.

#### `halt()`

- **Purpose**: Stops program execution.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: Program execution is halted.

---

## 6. **UVSimGUI Class**

### **Purpose**

The `UVSimGUI` class provides a graphical user interface for the UVSim virtual machine. It allows users to interact with the simulator through a visual interface, including loading and saving programs, executing instructions, and viewing memory contents.

### **Fields**

- `uvsim`: An instance of `UVSim` to interact with the virtual machine.
- `color_scheme`: An instance of `ColorScheme` to manage the interface colors.
- `memory_labels`: A list of QLineEdit widgets representing memory locations.
- `user_input`: A QLineEdit widget for user input.
- `console_output`: A QTextEdit widget for displaying console output.
- `accumulator_label`: A QLabel widget displaying the accumulator value.
- `program_counter_label`: A QLabel widget displaying the program counter value.

### **Functions**

#### `initUI()`

- **Purpose**: Initializes the graphical user interface.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The GUI is initialized and displayed.

#### `update_memory_display()`

- **Purpose**: Updates the memory display with current values.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The memory display is updated.

#### `load_program_from_memory_labels()`

- **Purpose**: Loads a program from the memory display into the virtual machine.
- **Input Parameters**: None.
- **Return Value**: A list of integers representing the program instructions.
- **Pre-condition**: The memory display contains valid instructions.
- **Post-condition**: The program is loaded into the virtual machine.

#### `read_user_input()`

- **Purpose**: Reads input from the user.
- **Input Parameters**: None.
- **Return Value**: The user input value.
- **Pre-condition**: None.
- **Post-condition**: The user input is returned.

#### `run_program()`

- **Purpose**: Executes the loaded program.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: A valid program is loaded.
- **Post-condition**: The program is executed.

#### `step_execution()`

- **Purpose**: Executes a single instruction.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: A valid program is loaded.
- **Post-condition**: A single instruction is executed.

#### `reset_simulator()`

- **Purpose**: Resets the simulator to its initial state.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The simulator is reset.

#### `halt_execution()`

- **Purpose**: Halts program execution.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: A program is running.
- **Post-condition**: Program execution is halted.

#### `configure_color_scheme()`

- **Purpose**: Configures the color scheme of the interface.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The color scheme is updated.

---

## 7. **ColorScheme Class**

### **Purpose**

The `ColorScheme` class manages the color scheme of the graphical user interface.

### **Fields**

- `colors`: A dictionary mapping color names to their values.

### **Functions**

#### `apply_color_scheme(widget)`

- **Purpose**: Applies the color scheme to a widget.
- **Input Parameters**:

  - `widget`: A QWidget to apply the color scheme to.

- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The color scheme is applied to the widget.

#### `configure_color_scheme(widget, console)`

- **Purpose**: Configures the color scheme.
- **Input Parameters**:

  - `widget`: A QWidget to configure the color scheme for.
  - `console`: A QTextEdit widget for displaying console output.

- **Return Value**: None.
- **Pre-condition**: None.
- **Post-condition**: The color scheme is configured.

---

## 8. **UVSim Class**

### **Purpose**

The `UVSim` class represents the main virtual machine. It coordinates the execution of instructions and manages the interaction between memory and operations.

### **Fields**

- `memory`: An instance of `UVSimMemory`.
- `accumulator`: An integer representing the accumulator value.
- `program_counter`: An integer representing the program counter.
- `operations`: Instances of `InputOutputOps`, `LoadStoreOps`, `ArithmeticOps`, and `ControlOps`.

### **Functions**

#### `load_program(program)`

- **Purpose**: Loads a program into memory.
- **Input Parameters**:

  - `program`: A list of integers representing the program instructions.

- **Return Value**: None.
- **Pre-condition**: The program size must not exceed 250 instructions.
- **Post-condition**: The program is loaded into memory.

#### `run(value=None)`

- **Purpose**: Executes the next instruction.
- **Input Parameters**:

  - `value`: An optional integer representing user input.

- **Return Value**: A tuple containing a message and a boolean indicating whether execution should continue.
- **Pre-condition**: A valid program is loaded.
- **Post-condition**: The next instruction is executed.

---

## 9. **File Functions**

### **Purpose**

The file functions module provides utilities for loading and saving programs to and from files.

### **Functions**

#### `load_instruction_file(gui_instance)`

- **Purpose**: Loads instructions from a text file into memory.
- **Input Parameters**:

  - `gui_instance`: An instance of `UVSimGUI`.

- **Return Value**: None.
- **Pre-condition**: A valid text file exists.
- **Post-condition**: The instructions are loaded into memory.

#### `save_instruction_file(gui_instance)`

- **Purpose**: Saves the current memory contents to a text file.
- **Input Parameters**:

  - `gui_instance`: An instance of `UVSimGUI`.

- **Return Value**: None.
- **Pre-condition**: Memory contains program instructions.
- **Post-condition**: The program is saved to a text file.

---

## Conclusion

This document outlines the classes and functions in the UVSim project, providing a comprehensive guide to the system's architecture and functionality. The design ensures modularity, loose coupling, and proper separation of concerns, making the system easy to understand, maintain, and extend.
