class UVSimOperations:
    def __init__(self, memory):
        #Initialize the operations
        self.memory = memory

    def read(self, address):
        #Read input from the keyboard and store it
        #Raises an error if the number is not four digits
        try:
            value = int(input("Enter an integer: "))
            if -9999 <= value <= 9999:
                self.memory.set_value(address, value)
            else:
                raise ValueError("Value must be a four digit number")
        except ValueError as e:
            print(f"Invalid input: {e}")

    def write(self, address):
        #Outputs the value of the specified address
        value = self.memory.get_value(address)
        print(f"Contents of {address} is {value:+05d}")

    def load(self, address):
        #Loads a word from the specified address to the accumulator
        value = self.memory.get_value(address)
        return value
    
    def store(self, address, accumulator):
        #Store the value from the accumulator into the specified address
        self.memory.set_value(address, accumulator)

    def add(self, address, accumulator):
        #Adds the value at the specified address to the accumulator
        value = self.memory.get_value(address)
        return accumulator + value
    
    def subtract(self, address, accumulator):
        #Subtracts the value at the specified address from the accumulator
        value = self.memory.get_value(address)
        return accumulator - value
    
    def multiply(self, address, accumulator):
        #Multiply the value at the specified memory address with the accumulator.
        value = self.memory.get_value(address)
        return accumulator * value

    def divide(self, address, accumulator):
        #Divide the accumulator by the value at the specified memory address.
        value = self.memory.get_value(address)
        if value == 0:
            raise ZeroDivisionError("Attempt to divide by zero.")
        return accumulator // value
    
    def branch(self, address):
        #Moves the program counter to the specified address
        return address
    
    def branch_neg(self, address, accumulator):
        #Moves the program counter to the specified address if the accumulator is negative
        if accumulator < 0:
            return address
        return None
    
    def branch_zero(self, address, accumulator):
        #Moves the program counter to the specified address if the accumulator is zero
        if accumulator == 0:
            return address
        return None
    
    def halt(self):
        #Stops the program
        print("*** Simulator execution halted ***")
        return True