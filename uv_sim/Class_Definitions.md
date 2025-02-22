# UVSim Class Documentation

This document outlines the classes in the UVSim project, their purposes, and their functions. The design ensures modularity, loose coupling, and proper separation of concerns.

---

## 1. **UVSimMemory Class**

### **Purpose**
The `UVSimMemory` class represents the memory structure of the UVSim virtual machine. It provides methods to load programs into memory, retrieve and set values at specific memory addresses, and display memory contents.

### **Fields**
- `memory`: A list of 100 integers representing the memory locations.

### **Functions**

#### `load_program(program)`
- **Purpose**: Loads a list of machine instructions (BasicML) into memory.
- **Input Parameters**:
  - `program`: A list of integers representing the program instructions.
- **Return Value**: None.
- **Pre-condition**: The program size must not exceed 100 instructions.
- **Post-condition**: Memory is populated with the program instructions.

#### `get_value(address)`
- **Purpose**: Retrieves the value stored at a given memory address.
- **Input Parameters**:
  - `address`: An integer representing the memory address (0-99).
- **Return Value**: The value stored at the specified address.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: None.

#### `set_value(address, value)`
- **Purpose**: Stores a value in a specific memory address.
- **Input Parameters**:
  - `address`: An integer representing the memory address (0-99).
  - `value`: An integer to store in memory (must be between -9999 and +9999).
- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range, and the value must be a signed four-digit number.
- **Post-condition**: The specified memory location is updated with the new value.

#### `display_memory(start, end)`
- **Purpose**: Prints memory contents from a given range.
- **Input Parameters**:
  - `start`: An integer representing the starting memory address.
  - `end`: An integer representing the ending memory address.
- **Return Value**: None.
- **Pre-condition**: The start and end addresses must be within the valid range (0-99).
- **Post-condition**: Memory contents are printed to the console.

---

## 2. **UVSimOperations Class**

### **Purpose**
The `UVSimOperations` class encapsulates the operations that can be performed by the UVSim virtual machine, such as reading input, writing output, and performing arithmetic operations.

### **Fields**
- `memory`: An instance of `UVSimMemory` to interact with memory.

### **Functions**

#### `read(address)`
- **Purpose**: Reads input from the keyboard and stores it in memory.
- **Input Parameters**:
  - `address`: An integer representing the memory address to store the input.
- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The input value is stored in the specified memory location.

#### `write(address)`
- **Purpose**: Outputs the value of the specified memory address to the screen.
- **Input Parameters**:
  - `address`: An integer representing the memory address to read from.
- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The value is printed to the console.

#### `load(address)`
- **Purpose**: Loads a value from memory into the accumulator.
- **Input Parameters**:
  - `address`: An integer representing the memory address to load from.
- **Return Value**: The value stored at the specified address.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The value is returned for further processing.

#### `store(address, accumulator)`
- **Purpose**: Stores the value from the accumulator into memory.
- **Input Parameters**:
  - `address`: An integer representing the memory address to store the value.
  - `accumulator`: An integer representing the value to store.
- **Return Value**: None.
- **Pre-condition**: The address must be within the valid range, and the value must be a signed four-digit number.
- **Post-condition**: The specified memory location is updated with the accumulator value.

#### `add(address, accumulator)`
- **Purpose**: Adds a value from memory to the accumulator.
- **Input Parameters**:
  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The accumulator is updated with the sum.

#### `subtract(address, accumulator)`
- **Purpose**: Subtracts a value from memory from the accumulator.
- **Input Parameters**:
  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The accumulator is updated with the difference.

#### `multiply(address, accumulator)`
- **Purpose**: Multiplies the accumulator by a value from memory.
- **Input Parameters**:
  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The accumulator is updated with the product.

#### `divide(address, accumulator)`
- **Purpose**: Divides the accumulator by a value from memory.
- **Input Parameters**:
  - `address`: An integer representing the memory address to read from.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The updated accumulator value.
- **Pre-condition**: The address must be within the valid range, and the value must not be zero.
- **Post-condition**: The accumulator is updated with the quotient.

#### `branch(address)`
- **Purpose**: Moves the program counter to the specified address.
- **Input Parameters**:
  - `address`: An integer representing the memory address to branch to.
- **Return Value**: The new program counter value.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The program counter is updated.

#### `branch_neg(address, accumulator)`
- **Purpose**: Moves the program counter to the specified address if the accumulator is negative.
- **Input Parameters**:
  - `address`: An integer representing the memory address to branch to.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The new program counter value if the accumulator is negative; otherwise, `None`.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The program counter is updated if the accumulator is negative.

#### `branch_zero(address, accumulator)`
- **Purpose**: Moves the program counter to the specified address if the accumulator is zero.
- **Input Parameters**:
  - `address`: An integer representing the memory address to branch to.
  - `accumulator`: An integer representing the current accumulator value.
- **Return Value**: The new program counter value if the accumulator is zero; otherwise, `None`.
- **Pre-condition**: The address must be within the valid range (0-99).
- **Post-condition**: The program counter is updated if the accumulator is zero.

#### `halt()`
- **Purpose**: Stops the program execution.
- **Input Parameters**: None.
- **Return Value**: `True` to indicate successful halting.
- **Pre-condition**: None.
- **Post-condition**: The program execution is halted.

---

## 3. **UVSim Class**

### **Purpose**
The `UVSim` class represents the virtual machine itself. It coordinates the execution of programs by interacting with memory and operations.

### **Fields**
- `memory`: An instance of `UVSimMemory`.
- `operations`: An instance of `UVSimOperations`.
- `accumulator`: An integer representing the accumulator.
- `program_counter`: An integer representing the program counter.
- `instruction_register`: An integer representing the current instruction.
- `opcode`: An integer representing the opcode of the current instruction.
- `operand`: An integer representing the operand of the current instruction.

### **Functions**

#### `load_program(program)`
- **Purpose**: Loads a program into memory.
- **Input Parameters**:
  - `program`: A list of integers representing the program instructions.
- **Return Value**: None.
- **Pre-condition**: The program size must not exceed 100 instructions.
- **Post-condition**: The program is loaded into memory.

#### `run()`
- **Purpose**: Executes the loaded program.
- **Input Parameters**: None.
- **Return Value**: None.
- **Pre-condition**: A valid program must be loaded into memory.
- **Post-condition**: The program is executed, and the virtual machine halts.

---

## 4. **UVSimGUI Class**

### **Purpose**
The `UVSimGUI` class provides a graphical user interface for the UVSim virtual machine. It allows users to input programs, run them, and view the results.

### **Fields**
- `uvsim`: An instance of `UVSim`.
- Various GUI components (e.g., buttons, labels, text fields).

### **Functions**
- **GUI-related functions**: These functions handle user interactions, such as running the program, stepping through instructions, and resetting the simulator.

---

## 5. **Unit Tests**

### **Purpose**
The `unit_tests.py` file contains unit tests for the UVSim virtual machine. It ensures that each class and function behaves as expected.

---

This modular design ensures that each class has a single responsibility, making the code easier to maintain and extend. The separation of concerns between the memory, operations, and GUI layers promotes loose coupling and high cohesion.