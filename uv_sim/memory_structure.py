class UVSimMemory:
    def __init__(self):
        """memory with 100 locations, set to zero."""
        self.memory = [0] * 100  # array with 100 words

    def load_program(self, program):
        """
        Load a list of machine instructions (BasicML) into memory.
        """
        if len(program) > 100:
            raise ValueError("Program size exceeds available memory.")
        
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def get_value(self, address):
        """
        Retrieve the value stored at a given memory address.
        """
        if 0 <= address < 100:
            return self.memory[address]
        else:
            raise IndexError("Memory address out of range.")

    def set_value(self, address, value):
        """
        Store a value in a specific memory address.
        """
        if 0 <= address < 100:
            if -9999 <= value <= 9999:  # Ensure value is within range
                self.memory[address] = value
            else:
                raise ValueError("Value must be a signed four-digit number (-9999 to +9999).")
        else:
            raise IndexError("Memory address out of range.")

    def display_memory(self, start=0, end=99):
        """
        Print memory contents from a given range.
        """
        for i in range(start, min(end + 1, 100)):
            print(f"Memory[{i:02d}] = {self.memory[i]:+05d}")

# Example Usage
if __name__ == "__main__":
    memory = UVSimMemory()
    
    # example of BasicML instructions
    sample_program = [1007, 2107, 1107, 4300]  # READ -> STORE -> WRITE -> HALT
    memory.load_program(sample_program)

    # Display memory
    memory.display_memory(0, 10)
