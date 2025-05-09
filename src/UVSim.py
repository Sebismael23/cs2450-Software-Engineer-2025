from memory_structure import UVSimMemory
from operations import InputOutputOps, LoadStoreOps, ArithmeticOps, ControlOps

# Updates to UVSim class to support both 4-digit and 6-digit formats

class UVSim:
    def __init__(self):
        self.memory = UVSimMemory()
        self.inputoutput = InputOutputOps(self.memory)
        self.loadstore = LoadStoreOps(self.memory)
        self.arithmetic = ArithmeticOps(self.memory)
        self.control = ControlOps(self.memory)
        self.accumulator = 0
        self.program_counter = 0
        self.instruction_register = 0
        self.opcode = 0
        self.operand = 0
        self.format = "6-digit"  # Default to new format

    def set_format(self, format_type):
        """Set the instruction format to '4-digit' or '6-digit'"""
        if format_type in ["4-digit", "6-digit"]:
            self.format = format_type
        else:
            raise ValueError("Format must be either '4-digit' or '6-digit'")

    def load_program(self, program):
        self.memory.load_program(program)
        
        # Try to detect format if not already set
        if len(program) > 0:
            # Check if any instruction exceeds 4-digit range
            if any(abs(instr) > 9999 for instr in program):
                self.format = "6-digit"
            else:
                # Check opcode range (in 6-digit, opcodes can be 10-43)
                # In 4-digit, they'd be represented as 10-43 in the tens/hundreds place
                has_6digit_opcode = any((instr // 1000) in range(10, 44) for instr in program)
                if has_6digit_opcode:
                    self.format = "6-digit"
                else:
                    self.format = "4-digit"




    def run(self, value=None):
        self.instruction_register = self.memory.get_value(self.program_counter)
        
        if self.instruction_register == 0:
            raise ValueError("Empty instruction (0) encountered")
            
        if self.format == "4-digit":
            self.opcode = self.instruction_register // 100
            self.operand = self.instruction_register % 100
        else:  # 6-digit
            self.opcode = self.instruction_register // 1000
            self.operand = self.instruction_register % 1000

        # Validation
        if self.opcode == 0 and self.instruction_register != 0:
            raise ValueError(f"Instruction parsing failed. Raw: {self.instruction_register}, Format: {self.format}")

        if self.opcode == 10:  # READ - Read a word from the keyboard into a location in memory
            if value is None:
                raise ValueError("No input provided for READ instruction.")
            self.inputoutput.read(self.operand, value)
            self.program_counter += 1
            return f"READ: Stored {value:+05d} in memory[{self.operand}]", True
        elif self.opcode == 11:  # WRITE - Write a word from a specific location in memory to screen
            value = self.inputoutput.write(self.operand)
            self.program_counter += 1
            return f"WRITE: Memory[{self.operand}] = {value:+05d}", True
        elif self.opcode == 20:  # LOAD - Load a word from a specific location in memory into the accumulator
            self.accumulator = self.loadstore.load(self.operand)
            self.program_counter += 1
            return f"LOAD: Accumulator set to {self.accumulator:+05d}", True
        elif self.opcode == 21:  # STORE - Store a word from the accumulator into a specific location in memory
            self.loadstore.store(self.operand, self.accumulator)
            self.program_counter += 1
            return f"STORE: Memory[{self.operand}] set to {self.accumulator:+05d}", True
        elif self.opcode == 30:  # ADD - Add a word from memory into the accumulator
            self.accumulator = self.arithmetic.add(self.operand, self.accumulator)
            self.program_counter += 1
            return f"ADD: Accumulator updated to {self.accumulator:+05d}", True
        elif self.opcode == 31:  # SUBTRACT - Subtract a word from memory from the accumulator
            self.accumulator = self.arithmetic.subtract(self.operand, self.accumulator)
            self.program_counter += 1
            return f"SUBTRACT: Accumulator updated to {self.accumulator:+05d}", True
        elif self.opcode == 32:  # DIVIDE - Divide the accumulator by a word in a specified location
            self.accumulator = self.arithmetic.divide(self.operand, self.accumulator)
            self.program_counter += 1
            return f"DIVIDE: Accumulator updated to {self.accumulator:+05d}", True
        elif self.opcode == 33:  # MULTIPLY - Multiply the accumulator by a word in the specified location
            self.accumulator = self.arithmetic.multiply(self.operand, self.accumulator)
            self.program_counter += 1
            return f"MULTIPLY: Accumulator updated to {self.accumulator:+05d}", True
        elif self.opcode == 40:  # BRANCH - Branch to a specific location in memory
            self.program_counter = self.operand
            return f"BRANCH: Jumping to address {self.operand:02d}", True
        elif self.opcode == 41:  # BRANCHNEG - Branch to a specific location in memory if the accumulator is negative
            if self.accumulator < 0:
                self.program_counter = self.operand
                return f"BRANCHNEG: Accumulator negative, jumping to address {self.operand:02d}", True
            else:
                self.program_counter += 1
                return "BRANCHNEG: Accumulator not negative, no branch.", True
        elif self.opcode == 42:  # BRANCHZERO - Branch to a specific location in memory if the accumulator is zero
            if self.accumulator == 0:
                self.program_counter = self.operand
                return f"BRANCHZERO: Accumulator zero, jumping to address {self.operand:02d}", True
            else:
                self.program_counter += 1
                return "BRANCHZERO: Accumulator not zero, no branch.", True
        elif self.opcode == 43:  # HALT - Pause the program
            self.control.halt()
            return "HALT: Program execution halted.", False
        else:
            raise ValueError(f"Unknown opcode: {self.opcode}")
            
if __name__ == "__main__":
    #Displays welcome message
    print("*** Welcome to UVSIM! ***")
    print("*** Please enter your program one instruction ***")
    print("*** ( or data word ) at a time into the input ***")
    print("*** text field. I will display the location ***")
    print("*** number and a question mark (?). You then ***")
    print("*** type the word for that location. Enter ***")
    print("*** -99999 to stop entering the program. ***")
    
    vm = UVSim() #Initialize virtual machine
    program = [] #Create an empty list to contain the instructions the user will input
    instruction_line = 0 #Instructions begin at line zero
    
    #User types in the program until they input -999999
    while True:
        #User inputs instructions
        user_input = input(f"{instruction_line:02d} ? ").strip()

        #Check if the value was -999999 and the program input ends
        if user_input == "-999999":
            print("*** Program loading complete ***")
            print("*** Program executuion begins ***")
            break

        try:
            # Convert the input to an integer
            instruction = int(user_input)

            # Make sure the input is six digits
            if -999999 <= instruction <= 999999:
                program.append(instruction)
                instruction_line += 1
            else:
                print("Error: Please enter a signed six digit number from -999999 to +999999 ***")

        except ValueError:
            print("*** Error: Please enter an integer from -999999 to +999999 ***")


    vm.load_program(program) # Load the program the user input into memory
    vm.run() # Run the program in the virtual machine"
