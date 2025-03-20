# Software Requirement Specification

## Functional Requirements

### 1.1 Loading and Running Programs

- The system should allow users to enter a BasicML program.
- The program should be loaded into memory, using no more than 100 memory slots.
- If there are errors in the instructions, the system should show an error message.

### 1.2 Executing Instructions

- The system should run instructions one by one.
- It should fetch, understand, and carry out each instruction.
- After each instruction, the system should update the program counter to keep track of what to do next.

### 1.3 Math and Data Handling

- The program must add the value from a specified memory location to the accumulator.
- The program must subtract the value from a specified memory location from the accumulator.
- The program must multiply the accumulator by the value from a specified memory location.
- The program must divide the accumulator by the value from a specified memory location, ensuring division by zero is prevented.

### 1.4 Input and Output

- The system should allow the user to enter numbers into a pop-up box when the `READ` instruction is used.
- It should display numbers on the screen when the `WRITE` instruction is used.

### 1.5 Controlling the Program Flow

- The system should allow jumping to different parts of the program using `BRANCH` instructions.
- It should stop running when the `HALT` instruction is used.

### 1.6 GUI

- 1.6.1 Display specific error messages for:
  - Invalid instruction format (non-numeric or out of range values)
  - Memory access violations (accessing memory locations beyond 0-99)
  - Invalid operations (division by zero, undefined operations)
  - File loading errors
- 1.6.2 Modify memory register through a text input field that:
  - Accepts only 4-digit integers (+/- sign allowed)
  - Validates input range (-9999 to +9999)
  - Updates the display immediately after valid input
- 1.6.3 Input user data through a dialog box that:
  - Accepts integers in the range of -9999 to +9999
  - Validates input format (must be numeric)
  - Provides clear error feedback for invalid inputs
- Execute when the user presses the "Run" button.
- Display the accumulator value in a dedicated field.
- Display the memory contents in a grid or table format.
- Display execution results in a designated output area.

## Non-Functional Requirements

### 2.1 Speed and Performance

- The system should process each instruction quickly (less than 100ms per instruction).

### 2.2 Reliability and Error Handling

- The system must validate all user inputs for:
  - Numeric format (4-digit integers only)
  - Value range (-9999 to +9999)
  - Memory address range (0-99)
  - Instruction format (valid BasicML operations)
- Error messages must:
  - Identify the specific type of error
  - Indicate the location of the error (line number or input field)
  - Provide guidance on how to correct the error

### 2.3 Compatibility

- The system should be written in Python and work on any computer that can run Python.

### 2.4 Future Maintenance and Improvements

- The codebase must follow these maintainability criteria:
  - Maximum function length of 50 lines
  - Maximum class length of 300 lines
  - Documentation for all public methods with parameters and return values
  - Modular architecture with clear separation of concerns:
    - GUI components
    - Instruction processing
    - Memory management
    - Input/output handling
  - Unit test coverage of at least 80% for core functionality
  - Use of design patterns where appropriate
