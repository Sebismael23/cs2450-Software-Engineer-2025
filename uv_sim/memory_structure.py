class UVSimMemory:
    def __init__(self):
        """memory with 250 locations, set to zero."""
        self.memory = [0] * 250  # array with 250 0's

    def load_program(self, program):
        """
        Load a list of machine instructions (BasicML) into memory.
        """
        if len(program) > 250:
            raise ValueError("Program size exceeds available memory size of 250.")

        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def get_value(self, address):
        """
        Retrieve the value stored at a given memory address.
        """
        if 0 <= address < 250:
            return self.memory[address]
        else:
            raise IndexError("Memory address out of range 250.")

    def set_value(self, address, value):
        """
        Store a value in a specific memory address.
        """
        if 0 <= address < 250:
            if -999999 <= value <= 999999:  # Ensure value is within range
                self.memory[address] = value
            else:
                raise ValueError("Value must be a signed six-digit number (-999999 to +999999).")
        else:
            raise IndexError("Memory address out of range.")

    def display_memory(self, start=0, end=99):
        """
        Print into console memory contents from a given range.
        """
        for i in range(start, min(end + 1, 100)):
            print(f"Memory[{i:03d}] = {self.memory[i]:+07d}")


# Example Usage
if __name__ == "__main__":
    memory = UVSimMemory()

    # example of BasicML instructions
    sample_program = [100000, 2107, 1107, 4300]  # READ -> STORE -> WRITE -> HALT
    memory.load_program(sample_program)

    # Display memory
    memory.display_memory(0, 10)
