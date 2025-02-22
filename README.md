UVSim README


Introduction

UVSim is a simple virtual machine for running programs written in BasicML, a basic machine language designed for educational purposes. The simulator allows users to enter and execute machine-level programs interactively.


Prerequisites

Python 3.x must be installed on your system.
PyQt5 must also be installed.


Installation

Clone or download the UVSim repository.

Ensure that all required files (UVSim.py, memory_structure.py, operations.py, uvsim_gui.py) are in the same directory.

Install PyQt5 using pip with the command below

pip install PyQt5



How to Run

Open a terminal or command prompt.

Navigate to the directory containing UVSim.py.

Run the command:

python uvsim_gui.py

The application will display the memory registers on the left hand side of the window.

Enter each instruction as a signed four-digit integer (e.g., +1007 for READ instruction) in these registers

To finish entering the program, click either the "Run" button at the top right to run the entire program, or the "Step Execution" button to run one instruction at a time.

The program will then execute according to the BasicML instruction set.

When running, enter user input into the dialog box at the top right.

Click the "Halt" button to stop the instructions from continuing.

Click the "Reset" button to return the program to a completely blank slate.


Basic Usage

READ (10): Read a value from the keyboard into memory.

WRITE (11): Print a value from memory to the screen.

LOAD (20): Load a value from memory into the accumulator.

STORE (21): Store the accumulator's value into memory.

ADD (30): Add a value from memory to the accumulator.

SUBTRACT (31): Subtract a value from memory from the accumulator.

MULTIPLY (33): Multiply a value from memory with the accumulator.

DIVIDE (32): Divide the accumulator by a value in memory.

BRANCH (40): Jump to a specific memory location.

BRANCHNEG (41): Jump to a memory location if the accumulator is negative.

BRANCHZERO (42): Jump to a memory location if the accumulator is zero.

HALT (43): Stop execution.


Example Program

Here is a simple example program that reads a number, stores it, and then writes it back to the screen:

00 ? +1007 # READ input into memory[07] 01 ? +2107 # STORE value from accumulator into memory[07] 02 ? +1107 # WRITE value from memory[07] to screen 03 ? +4300 # HALT program execution


Exiting UVSim

To exit the program, close the application window.


Troubleshooting

Ensure you are using a valid BasicML instruction format (four-digit signed integers).

If a memory error occurs, check that you are not trying to access an out-of-range memory location (valid range: 00-99).

If division by zero is attempted, an error message will be displayed, and execution will halt.


Contact

For any issues or questions, please reach out to the development team.
