
# **Class Design Document**
This document outlines the classes in the UVSim project, their purposes, and their functions. The design ensures modularity, loose coupling, and proper separation of concerns.


## 1. **UVSimMemory Class**

### **Purpose**

The `UVSimMemory` class represents the memory structure of the UVSim virtual machine. It provides methods to load programs into memory, retrieve and set values at specific memory addresses, and display memory contents.

### **Fields**

-   `memory`: A list of 100 integers representing the memory locations.
    

### **Functions**

#### `load_program(program)`

-   **Purpose**: Loads a list of machine instructions (BasicML) into memory.
    
-   **Input Parameters**:
    
    -   `program`: A list of integers representing the program instructions.
        
-   **Return Value**: None.
    
-   **Pre-condition**: The program size must not exceed 100 instructions.
    
-   **Post-condition**: Memory is populated with the program instructions.
    

#### `get_value(address)`

-   **Purpose**: Retrieves the value stored at a given memory address.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address (0-99).
        
-   **Return Value**: The value stored at the specified address.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: None.
    

#### `set_value(address, value)`

-   **Purpose**: Stores a value in a specific memory address.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address (0-99).
        
    -   `value`: An integer to store in memory (must be between -9999 and +9999).
        
-   **Return Value**: None.
    
-   **Pre-condition**: The address must be within the valid range, and the value must be a signed four-digit number.
    
-   **Post-condition**: The specified memory location is updated with the new value.
    

#### `display_memory(start, end)`

-   **Purpose**: Prints memory contents from a given range.
    
-   **Input Parameters**:
    
    -   `start`: An integer representing the starting memory address.
        
    -   `end`: An integer representing the ending memory address.
        
-   **Return Value**: None.
    
-   **Pre-condition**: The start and end addresses must be within the valid range (0-99).
    
-   **Post-condition**: Memory contents are printed to the console.
    

----------

## 2. **InputOutputOps Class**

### **Purpose**

The `InputOutputOps` class handles input and output operations for the UVSim virtual machine, such as reading input from the user and writing output to the console.

### **Fields**

-   `memory`: An instance of `UVSimMemory` to interact with memory.
    

### **Functions**

#### `read(address, value)`

-   **Purpose**: Reads input from the keyboard and stores it in memory.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to store the input.
        
    -   `value`: An integer representing the input value.
        
-   **Return Value**: None.
    
-   **Pre-condition**: The address must be within the valid range (0-99), and the value must be a signed four-digit number.
    
-   **Post-condition**: The input value is stored in the specified memory location.
    

#### `write(address)`

-   **Purpose**: Outputs the value of the specified memory address to the screen.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to read from.
        
-   **Return Value**: The value stored at the specified address.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The value is returned for further processing.
    

----------

## 3. **LoadStoreOps Class**

### **Purpose**

The `LoadStoreOps` class handles loading values from memory into the accumulator and storing values from the accumulator into memory.

### **Fields**

-   `memory`: An instance of `UVSimMemory` to interact with memory.
    

### **Functions**

#### `load(address)`

-   **Purpose**: Loads a value from memory into the accumulator.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to load from.
        
-   **Return Value**: The value stored at the specified address.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The value is returned for further processing.
    

#### `store(address, accumulator)`

-   **Purpose**: Stores the value from the accumulator into memory.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to store the value.
        
    -   `accumulator`: An integer representing the value to store.
        
-   **Return Value**: None.
    
-   **Pre-condition**: The address must be within the valid range, and the value must be a signed four-digit number.
    
-   **Post-condition**: The specified memory location is updated with the accumulator value.
    

----------

## 4. **ArithmeticOps Class**

### **Purpose**

The `ArithmeticOps` class handles arithmetic operations such as addition, subtraction, multiplication, and division.

### **Fields**

-   `memory`: An instance of `UVSimMemory` to interact with memory.
    

### **Functions**

#### `add(address, accumulator)`

-   **Purpose**: Adds a value from memory to the accumulator.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to read from.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The updated accumulator value.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The accumulator is updated with the sum.
    

#### `subtract(address, accumulator)`

-   **Purpose**: Subtracts a value from memory from the accumulator.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to read from.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The updated accumulator value.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The accumulator is updated with the difference.
    

#### `multiply(address, accumulator)`

-   **Purpose**: Multiplies the accumulator by a value from memory.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to read from.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The updated accumulator value.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The accumulator is updated with the product.
    

#### `divide(address, accumulator)`

-   **Purpose**: Divides the accumulator by a value from memory.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to read from.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The updated accumulator value.
    
-   **Pre-condition**: The address must be within the valid range, and the value must not be zero.
    
-   **Post-condition**: The accumulator is updated with the quotient.
    

----------

## 5. **ControlOps Class**

### **Purpose**

The `ControlOps` class handles control flow operations such as branching and halting.

### **Fields**

-   `memory`: An instance of `UVSimMemory` to interact with memory.
    

### **Functions**

#### `branch(address)`

-   **Purpose**: Moves the program counter to the specified address.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to branch to.
        
-   **Return Value**: The new program counter value.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The program counter is updated.
    

#### `branch_neg(address, accumulator)`

-   **Purpose**: Moves the program counter to the specified address if the accumulator is negative.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to branch to.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The new program counter value if the accumulator is negative; otherwise, `None`.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The program counter is updated if the accumulator is negative.
    

#### `branch_zero(address, accumulator)`

-   **Purpose**: Moves the program counter to the specified address if the accumulator is zero.
    
-   **Input Parameters**:
    
    -   `address`: An integer representing the memory address to branch to.
        
    -   `accumulator`: An integer representing the current accumulator value.
        
-   **Return Value**: The new program counter value if the accumulator is zero; otherwise, `None`.
    
-   **Pre-condition**: The address must be within the valid range (0-99).
    
-   **Post-condition**: The program counter is updated if the accumulator is zero.
    

#### `halt()`

-   **Purpose**: Stops the program execution.
    
-   **Input Parameters**: None.
    
-   **Return Value**: `True` to indicate successful halting.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The program execution is halted.
    

----------

## 6. **UVSim Class**

### **Purpose**

The `UVSim` class represents the virtual machine itself. It coordinates the execution of programs by interacting with memory and operations.

### **Fields**

-   `memory`: An instance of `UVSimMemory`.
    
-   `inputoutput`: An instance of `InputOutputOps`.
    
-   `loadstore`: An instance of `LoadStoreOps`.
    
-   `arithmetic`: An instance of `ArithmeticOps`.
    
-   `control`: An instance of `ControlOps`.
    
-   `accumulator`: An integer representing the accumulator.
    
-   `program_counter`: An integer representing the program counter.
    
-   `instruction_register`: An integer representing the current instruction.
    
-   `opcode`: An integer representing the opcode of the current instruction.
    
-   `operand`: An integer representing the operand of the current instruction.
    

### **Functions**

#### `load_program(program)`

-   **Purpose**: Loads a program into memory.
    
-   **Input Parameters**:
    
    -   `program`: A list of integers representing the program instructions.
        
-   **Return Value**: None.
    
-   **Pre-condition**: The program size must not exceed 100 instructions.
    
-   **Post-condition**: The program is loaded into memory.
    

#### `run(value=None)`

-   **Purpose**: Executes the loaded program.
    
-   **Input Parameters**:
    
    -   `value`: An optional integer representing input for the `READ` instruction.
        
-   **Return Value**: A tuple containing a message and a boolean indicating whether execution should continue.
    
-   **Pre-condition**: A valid program must be loaded into memory.
    
-   **Post-condition**: The program is executed, and the virtual machine halts if a `HALT` instruction is encountered.
    

----------

## 7. **UVSimGUI Class**

### **Purpose**

The `UVSimGUI` class provides a graphical user interface for the UVSim virtual machine. It allows users to input programs, run them, and view the results.

### **Fields**

-   `uvsim`: An instance of `UVSim`.
    
-   `color_scheme`: An instance of `ColorScheme` for managing the GUI's color scheme.
    
-   Various GUI components (e.g., buttons, labels, text fields).
    

### **Functions**

#### `step_execution()`

-   **Purpose**: Executes one instruction at a time.
    
-   **Input Parameters**: None.
    
-   **Return Value**: None.
    
-   **Pre-condition**: A valid program must be loaded into memory.
    
-   **Post-condition**: The current instruction is executed, and the GUI is updated.
    

#### `run_program()`

-   **Purpose**: Executes the entire program.
    
-   **Input Parameters**: None.
    
-   **Return Value**: None.
    
-   **Pre-condition**: A valid program must be loaded into memory.
    
-   **Post-condition**: The program is executed, and the GUI is updated.
    

#### `reset_simulator()`

-   **Purpose**: Resets the simulator to its initial state.
    
-   **Input Parameters**: None.
    
-   **Return Value**: None.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The simulator is reset, and the GUI is updated.
    

#### `configure_color_scheme()`

-   **Purpose**: Allows the user to configure the color scheme of the GUI.
    
-   **Input Parameters**: None.
    
-   **Return Value**: None.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The GUI's color scheme is updated.
    

----------

## 8. **ColorScheme Class**

### **Purpose**

The `ColorScheme` class manages the color scheme of the GUI, allowing users to customize the primary and off colors.

### **Fields**

-   `CONFIG_FILE`: A string representing the configuration file for storing color settings.
    
-   `color_config`: A dictionary containing the current color configuration.
    

### **Functions**

#### `load_color_config()`

-   **Purpose**: Loads the color configuration from a file.
    
-   **Input Parameters**: None.
    
-   **Return Value**: A dictionary containing the color configuration.
    
-   **Pre-condition**: The configuration file must exist.
    
-   **Post-condition**: The color configuration is loaded.
    

#### `save_color_config()`

-   **Purpose**: Saves the current color configuration to a file.
    
-   **Input Parameters**: None.
    
-   **Return Value**: None.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The color configuration is saved to the file.
    

#### `apply_color_scheme(widget)`

-   **Purpose**: Applies the current color scheme to the GUI.
    
-   **Input Parameters**:
    
    -   `widget`: A PyQt5 widget to apply the color scheme to.
        
-   **Return Value**: None.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The widget's color scheme is updated.
    

#### `configure_color_scheme(widget, console_output)`

-   **Purpose**: Allows the user to configure the color scheme.
    
-   **Input Parameters**:
    
    -   `widget`: A PyQt5 widget to apply the color scheme to.
        
    -   `console_output`: A QTextEdit widget for displaying messages.
        
-   **Return Value**: None.
    
-   **Pre-condition**: None.
    
-   **Post-condition**: The color scheme is updated and applied to the GUI.
    

----------

## 9. **Unit Tests**

### **Purpose**

The `unit_tests.py` file contains unit tests for the UVSim virtual machine. It ensures that each class and function behaves as expected.

----------

This modular design ensures that each class has a single responsibility, making the code easier to maintain and extend. The separation of concerns between the memory, operations, and GUI layers promotes loose coupling and high cohesion.
