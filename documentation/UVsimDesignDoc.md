# UVSim Design Document

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [System Components](#system-components)
- [User Interface](#user-interface)
- [File Operations](#file-operations)
- [User Stories](#user-stories)
- [Use Cases](#use-cases)
- [Error Handling and Validation](#error-handling-and-validation)
- [Performance Considerations](#performance-considerations)
- [Testing Strategy](#testing-strategy)
- [Future Enhancements](#future-enhancements)
- [Conclusion](#conclusion)

## Overview

UVSim is a software simulator designed to help computer science students learn machine language and computer architecture. It allows users to write, load, and execute programs in BasicML, a simple machine language. UVSim emulates a basic virtual machine with a CPU, an accumulator, a memory unit, and a set of predefined instructions.

## System Architecture

### Core Components

1. **Memory (UVSimMemory):**

   - Stores program instructions and data
   - Implements memory management and access control
   - Provides memory read/write operations
   - Maintains memory state and validation
   - Supports 250 memory locations (00-249)

2. **Operations (UVSimOperations):**

   - Implements the execution of BasicML instructions
   - Handles arithmetic and logical operations
   - Manages control flow instructions
   - Provides input/output operations

3. **Virtual Machine (UVSim):**

   - Controls program execution
   - Manages the instruction cycle
   - Coordinates between memory and operations
   - Handles error conditions and exceptions

4. **Graphical User Interface (UVSimGUI):**
   - Provides a visual interface for user interaction
   - Displays memory contents in a scrollable list
   - Shows accumulator and program counter values
   - Offers controls for program execution
   - Supports file operations for loading and saving programs
   - Includes a console output area for feedback
   - Features a configurable color scheme

### Instruction Set Architecture (ISA)

The BasicML instruction set uses a 6-digit word format:

- First 3 digits: Operation code (opcode)
- Last 3 digits: Operand (memory address)

The BasicML instruction set includes:

- **Data Transfer:** LOAD, STORE
- **Arithmetic:** ADD, SUBTRACT, MULTIPLY, DIVIDE
- **Control Flow:** BRANCH, BRANCHNEG, BRANCHZERO, HALT
- **I/O Operations:** READ, WRITE

### Memory Format

- Each memory location can store a 6-digit word
- Values range from -999999 to +999999
- Memory addresses range from 000 to 249
- Instructions are stored as 6-digit words with opcode and operand

## System Components

1. **Memory (UVSimMemory):** Stores program instructions and data in 250 memory locations.
2. **Operations (UVSimOperations):** Implements the execution of BasicML instructions.
3. **Virtual Machine (UVSim):** Controls program execution, manages the instruction cycle, and interacts with memory and operations.
4. **Graphical User Interface (UVSimGUI):** Provides a visual interface for user interaction with the simulator.

## User Interface

### Main Window Layout

- **Left Panel:** Memory display showing 250 memory locations
- **Right Panel:** Controls and program information
  - User input field for READ instructions
  - Execution control buttons (Run, Step, Reset, Halt)
  - File operation buttons (Load, Save)
  - Console output area
  - Accumulator and program counter displays
  - Color scheme configuration

### Memory Display

- Scrollable list of 250 memory locations
- Each location shows a 6-digit word
- Values are displayed with a sign (+ or -)
- Memory addresses range from 000 to 249

### Control Buttons

- **Run:** Executes the program until completion or error
- **Step:** Executes a single instruction
- **Reset:** Clears memory and resets the simulator
- **Halt:** Stops program execution
- **Load Instructions File:** Loads a program from a text file
- **Save Instructions:** Saves the current memory contents to a file
- **Configure Color Scheme:** Allows customization of the interface colors

## File Operations

### Loading Instructions

- Supports loading instructions from text files
- Validates instruction format and range
- Clears existing memory before loading
- Handles errors gracefully with user feedback
- Limits program size to available memory (250 locations)
- Provides warning for programs exceeding memory size

### Saving Instructions

- Saves current memory contents to text files
- Includes header comments for file identification
- Only saves non-zero memory values to reduce file size
- Handles errors gracefully with user feedback
- Provides confirmation of successful save operation

## User Stories

### Story 1: Running a BasicML Program

As a computer science student, I want to enter a BasicML program into UVSim, so that I can execute it and observe its behavior.

### Story 2: Debugging a Program

As a student, I want to view the memory contents at any time, so that I can debug my BasicML program effectively.

### Story 3: Loading and Saving Programs

As a student, I want to save my BasicML programs to files and load them later, so that I can work on them across multiple sessions.

## Use Cases

### 1. Load a BasicML Program

- **Actor:** User
- **Description:** The user inputs a list of BasicML instructions, which are loaded into memory.
- **Precondition:** The program consists of valid BasicML instructions (6-digit words).
- **Postcondition:** The program is stored in UVSim memory starting at location 00.

### 2. Execute a BasicML Program

- **Actor:** User
- **Description:** The user runs the loaded program. UVSim executes instructions sequentially.
- **Precondition:** A valid program is loaded in memory.
- **Postcondition:** The program executes until a HALT instruction is encountered.

### 3. Read Input

- **Actor:** User
- **Description:** The user provides input when prompted by a READ instruction.
- **Precondition:** The program has a READ instruction.
- **Postcondition:** The input is stored in memory at the specified location.

### 4. Write Output

- **Actor:** User
- **Description:** The UVSim prints a value stored in memory to the screen.
- **Precondition:** The program has a WRITE instruction.
- **Postcondition:** The value at the specified memory location is displayed.

### 5. Load a Value into the Accumulator

- **Actor:** System
- **Description:** A LOAD instruction loads a memory value into the accumulator.
- **Precondition:** The specified memory location contains a valid value.
- **Postcondition:** The accumulator holds the loaded value.

### 6. Store a Value in Memory

- **Actor:** System
- **Description:** A STORE instruction saves the accumulator value into memory.
- **Precondition:** The accumulator holds a valid value.
- **Postcondition:** The value is stored in the specified memory location.

### 7. Perform Arithmetic Operations

- **Actor:** System
- **Description:** ADD, SUBTRACT, MULTIPLY, or DIVIDE instructions modify the accumulator.
- **Precondition:** The specified memory location contains a valid number.
- **Postcondition:** The accumulator reflects the new computed value.

### 8. Branch to Another Instruction

- **Actor:** System
- **Description:** A BRANCH instruction changes program execution to another location.
- **Precondition:** The specified memory location is a valid instruction.
- **Postcondition:** The program counter is updated.

### 9. Conditional Branching

- **Actor:** System
- **Description:** BRANCHNEG or BRANCHZERO checks accumulator conditions before jumping.
- **Precondition:** The accumulator holds a value.
- **Postcondition:** The program counter updates only if conditions are met.

### 10. Halt Execution

- **Actor:** System
- **Description:** A HALT instruction stops execution.
- **Precondition:** The program is running.
- **Postcondition:** Execution ceases, and control returns to the user.

### 11. Display Memory Contents

- **Actor:** User
- **Description:** The user requests to view memory contents.
- **Precondition:** Memory contains values.
- **Postcondition:** Memory contents are displayed.

### 12. Handle Invalid Instructions

- **Actor:** System
- **Description:** UVSim detects an invalid instruction and raises an error.
- **Precondition:** The program contains an invalid opcode.
- **Postcondition:** The system displays an error message and halts execution.

### 13. Handle Invalid Memory Access

- **Actor:** System
- **Description:** UVSim prevents access to invalid memory locations.
- **Precondition:** A memory address is out of range.
- **Postcondition:** An error message is displayed, and execution stops.

### 14. Prevent Division by Zero

- **Actor:** System
- **Description:** The simulator checks for division by zero.
- **Precondition:** A DIVIDE instruction is executed.
- **Postcondition:** If division by zero is attempted, an error is raised.

### 15. Exit the Simulator

- **Actor:** User
- **Description:** The user terminates the UVSim program.
- **Precondition:** UVSim is running.
- **Postcondition:** The program exits, releasing system resources.

### 16. Load Instructions from File

- **Actor:** User
- **Description:** The user loads a BasicML program from a text file.
- **Precondition:** A valid text file containing BasicML instructions exists.
- **Postcondition:** The program is loaded into memory.

### 17. Save Instructions to File

- **Actor:** User
- **Description:** The user saves the current memory contents to a text file.
- **Precondition:** Memory contains program instructions.
- **Postcondition:** The program is saved to a text file.

## Error Handling and Validation

### Input Validation

- Program size limits (250 memory locations)
- Instruction format verification (6-digit words)
- Memory address range checking (000-249)
- Numeric value validation (-999999 to +999999)

### Runtime Error Handling

- Division by zero detection
- Invalid memory access prevention
- Instruction execution error handling
- System resource management

## Performance Considerations

- Memory access optimization
- Instruction execution efficiency
- Error handling overhead
- Resource utilization

## Testing Strategy

- Unit testing for core components
- Integration testing for component interaction
- Error handling verification
- Performance benchmarking
- User acceptance testing

## Future Enhancements

- Advanced debugging features
- Program visualization tools
- Extended instruction set
- Performance optimization
- User interface improvements

## Conclusion

UVSim provides an interactive way for students to understand machine language and CPU operations. It allows users to write, load, execute, and debug BasicML programs with a simple and intuitive interface.
