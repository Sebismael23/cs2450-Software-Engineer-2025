## UVSim README

**Introduction**

UVSim is a simple virtual machine for running programs written in BasicML, a basic machine language designed for educational purposes. The simulator allows users to enter and execute machine-level programs interactively.

**Prerequisites**

Python 3.x must be installed on your system.
PyQt5 must also be installed.

**Installation**

Clone or download the UVSim repository.

Ensure that all required files (UVSim.py, memory_structure.py, operations.py) are in the same directory.

Install PyQt5 using pip with the command below

> pip install PyQt5

**How to Run**

Open a terminal or command prompt.

Navigate to the directory containing UVSim.py.

Run the command:

> python uvsim_gui.py

The application will display the memory registers on the left hand side of the window.

Enter each instruction as a signed six-digit integer (e.g., +010007 for READ instruction) in these registers. The first three digits represent the opcode (with a leading 0), and the last three digits represent the memory address (000-249).

To finish entering the program, click either the "Run" button at the top right to run the entire program. The "Step Execution" button is a work in progress.

The program will then execute according to the BasicML instruction set.

When running, enter user input into the dialog box that pops up when the program executes.

Click the "Halt" button to stop the instructions from continuing.

Click the "Reset" button to reset the memory.

**Basic Usage**

READ (010): Read a value from the keyboard into memory.

WRITE (011): Print a value from memory to the screen.

LOAD (020): Load a value from memory into the accumulator.

STORE (021): Store the accumulator's value into memory.

ADD (030): Add a value from memory to the accumulator.

SUBTRACT (031): Subtract a value from memory from the accumulator.

MULTIPLY (033): Multiply a value from memory with the accumulator.

DIVIDE (032): Divide the accumulator by a value in memory.

BRANCH (040): Jump to a specific memory location.

BRANCHNEG (041): Jump to a memory location if the accumulator is negative.

BRANCHZERO (042): Jump to a memory location if the accumulator is zero.

HALT (043): Stop execution.

**Example Program**

Here is a simple example program that reads a number, stores it, and then writes it back to the screen:

00 ? +010007 _# READ input into memory[007]_
01 ? +021007 _# STORE value from accumulator into memory[007]_
02 ? +011007 _# WRITE value from memory[007] to screen_
03 ? +043000 _# HALT program execution_

**Saving and Loading**

To save a program that is already in memory, click the "Save Instructions" button. This will save the program into a .txt file to a location of your choice on your computer.

To load a program, click on the "Load Instructions File" button. A file browser window will open. Navigate to the desired file and open it. This will load a previously saved program into the memory registers of the simulator.

**Color Scheme**

The simulator allows you to change the primary and secondary colors of the window. To do this, click on the "Configure Color Scheme" button at the bottom of the window. This will bring up a dialog box. Enter the color in hex code that you wish for the primary color to be, then click OK. The next box will ask you to do the same for the secondary color. After clicking OK for the second time, the color will update to your specifications.

**Exiting UVSim**

To exit the program, close the application window.

**Troubleshooting**

Ensure you are using a valid BasicML instruction format (six-digit signed integers).

If a memory error occurs, check that you are not trying to access an out-of-range memory location (valid range: 000-249).

If division by zero is attempted, an error message will be displayed, and execution will halt.

**Contact**

For any issues or questions, please reach out to the development team.
