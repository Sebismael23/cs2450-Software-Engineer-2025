from memory_structure import UVSimMemory
from operations import UVSimOperations

class UVSim:
    def __init__(self):
        self.memory = UVSimMemory()
        self.operations = UVSimOperations(self.memory)
        self.accumulator = 0
        self.program_counter = 0
        self.instruction_register = 0
        self.opcode = 0
        self.operand = 0

    def load_program(self, program):
        self.memory.load_program(program)

    def run(self):
        while True:
            self.instruction_register = self.memory.get_value(self.program_counter)
            self.opcode = self.instruction_register // 100
            self.operand = self.instruction_register % 100

            if self.opcode == 10:  # READ - Read a word from the keyboard into a location in memory
                self.operations.read(self.operand)
            elif self.opcode == 11:  # WRITE - Write a word from a specific location in memory to screen
                self.operations.write(self.operand)
            elif self.opcode == 20:  # LOAD - Load a word from a specific location in memory into the accumulator
                self.accumulator = self.operations.load(self.operand)
            elif self.opcode == 21:  # STORE - Store a word from the accumulator into a specific location in memroy
                self.operations.store(self.operand, self.accumulator)
            elif self.opcode == 30:  # Add a word from memory into the accumulator
                self.accumulator = self.operations.add(self.operand, self.accumulator)
            elif self.opcode == 31:  # Subtract a word from memory from the accumulator
                self.accumulator = self.operations.subtract(self.operand, self.accumulator)
            elif self.opcode == 32:  # Divide the accumulator by a word in a specified location
                self.accumulator = self.operations.divide(self.operand, self.accumulator)
            elif self.opcode == 33:  # Multiply the accumulator by a word in the specified location
                self.accumulator = self.operations.multiply(self.operand, self.accumulator)
            elif self.opcode == 40:  # BRANCH -  Branch to a specific location in memory
                self.program_counter = self.operations.branch(self.operand)
                continue
            elif self.opcode == 41:  # BRANCHNEG - Branch to a specific location in memory if the accumulator is negative
                new_pc = self.operations.branch_neg(self.operand, self.accumulator)
                if new_pc is not None:
                    self.program_counter = new_pc
                    continue
            elif self.opcode == 42:  # BRANCHZERO - Branch to a specific location in memory if the accumulator is zero
                new_pc = self.operations.branch_zero(self.operand, self.accumulator)
                if new_pc is not None:
                    self.program_counter = new_pc
                    continue
            elif self.opcode == 43:  # HALT - Pause the program
                self.operations.halt()
                break
            else:
                raise ValueError(f"Unknown opcode: {self.opcode}")

            self.program_counter += 1

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
    
    #User types in the program until they input -99999
    while True:
        #User inputs instructions
        user_input = input(f"{instruction_line:02d} ? ").strip()

        #Check if the value was -99999 and the program input ends
        if user_input == "-99999":
            print("*** Program loading complete ***")
            print("*** Program executuion begins ***")
            break

        try:
            #Convert the input to an integer
            instruction = int(user_input)

            #Make sure the input is four digits
            if -9999 < instruction <= 9999:
                program.append(instruction)
                instruction_line += 1
            else:
                print("Error: Please enter a signed four digit number from -9999 to +9999 ***")

        except ValueError:
            print("*** Error: Please enter an integer from -9999 to +9999 ***")


    vm.load_program(program) #Load the program the user input into memory
    vm.run() #Run the program in the virtual machine