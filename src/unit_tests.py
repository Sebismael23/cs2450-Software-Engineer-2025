import unittest
from UVSim import UVSim
from memory_structure import UVSimMemory
from operations import InputOutputOps, LoadStoreOps, ArithmeticOps, ControlOps

class TestUVSim(unittest.TestCase):
    def setUp(self):
        self.memory = UVSimMemory()
        self.inputoutput = InputOutputOps(self.memory)
        self.loadstore = LoadStoreOps(self.memory)
        self.arithmetic = ArithmeticOps(self.memory)
        self.control = ControlOps(self.memory)
        self.uvsim = UVSim()

    # Use Case 1: Load a BasicML Program
    def test_load_program_valid(self):
        """Test loading a valid program into memory."""
        program = [1007, 2107, 1107, 4300]
        self.memory.load_program(program)
        for i in range(len(program)):
            self.assertEqual(self.memory.get_value(i), program[i])

    def test_load_program_invalid_size(self):
        """Test loading a program that exceeds memory size."""
        program = [0] * 101  # Exceeds memory size
        with self.assertRaises(ValueError):
            self.memory.load_program(program)

    # Use Case 2: Execute a BasicML Program
    def test_execute_program_valid(self):
        """Test executing a valid program."""
        program = [1007, 2107, 1107, 4300]  # READ -> WRITE -> HALT
        self.uvsim.load_program(program)
        self.uvsim.run(value=1234)  # Provide input for READ instruction
        self.assertEqual(self.memory.get_value(7), 0)  # Verify STORE worked

    def test_execute_program_invalid_opcode(self):
        """Test executing a program with an invalid opcode."""
        program = [9999]  # Invalid opcode
        self.uvsim.load_program(program)
        with self.assertRaises(ValueError):
            self.uvsim.run()

    # Use Case 3: Read Input
    def test_read_operation_valid(self):
        """Test READ operation with valid input."""
        self.inputoutput.read(7, 1234)  # Simulate user input
        self.assertEqual(self.memory.get_value(7), 1234)

    def test_read_operation_invalid_input(self):
        """Test READ operation with invalid input."""
        with self.assertRaises(ValueError):
            self.inputoutput.read(7, 10000)  # Simulate invalid input (out of range)

    # Use Case 4: Write Output
    def test_write_operation_valid(self):
        """Test WRITE operation with valid memory value."""
        self.memory.set_value(7, 1234)
        value = self.inputoutput.write(7)  # Should return the value being written
        self.assertEqual(value, 1234)

    def test_write_operation_invalid_address(self):
        """Test WRITE operation with invalid memory address."""
        with self.assertRaises(IndexError):
            self.inputoutput.write(100)  # Invalid address

    # Use Case 5: Load a Value into the Accumulator
    def test_load_operation_valid(self):
        """Test LOAD operation with valid memory value."""
        self.memory.set_value(7, 1234)
        accumulator = self.loadstore.load(7)
        self.assertEqual(accumulator, 1234)

    def test_load_operation_invalid_address(self):
        """Test LOAD operation with invalid memory address."""
        with self.assertRaises(IndexError):
            self.loadstore.load(100)  # Invalid address

    # Use Case 6: Store a Value in Memory
    def test_store_operation_valid(self):
        """Test STORE operation with valid value."""
        self.loadstore.store(7, 1234)
        self.assertEqual(self.memory.get_value(7), 1234)

    def test_store_operation_invalid_value(self):
        """Test STORE operation with invalid value."""
        with self.assertRaises(ValueError):
            self.loadstore.store(7, 10000)  # Invalid value

    # Use Case 7: Perform Arithmetic Operations
    def test_add_operation_valid(self):
        """Test ADD operation with valid values."""
        self.memory.set_value(7, 1000)
        accumulator = self.arithmetic.add(7, 500)
        self.assertEqual(accumulator, 1500)

    def test_subtract_operation_valid(self):
        """Test SUBTRACT operation with valid values."""
        self.memory.set_value(7, 1000)
        accumulator = self.arithmetic.subtract(7, 500)
        self.assertEqual(accumulator, -500)

    # Use Case 8: Branch to Another Instruction
    def test_branch_operation_valid(self):
        """Test BRANCH operation with valid address."""
        new_pc = self.control.branch(50)
        self.assertEqual(new_pc, 50)

    def test_branch_operation_invalid_address(self):
        """Test BRANCH operation with invalid address."""
        with self.assertRaises(IndexError):
            self.control.branch(100)  # Invalid address

    # Use Case 9: Conditional Branching
    def test_branch_neg_operation_valid(self):
        """Test BRANCHNEG operation with negative accumulator."""
        new_pc = self.control.branch_neg(50, -1)
        self.assertEqual(new_pc, 50)

    def test_branch_zero_operation_valid(self):
        """Test BRANCHZERO operation with zero accumulator."""
        new_pc = self.control.branch_zero(50, 0)
        self.assertEqual(new_pc, 50)

    # Use Case 10: Halt Execution
    def test_halt_operation_valid(self):
        """Test HALT operation."""
        result = self.control.halt()
        self.assertTrue(result)

    # Use Case 11: Display Memory Contents
    def test_display_memory_valid(self):
        """Test displaying memory contents."""
        self.memory.set_value(0, 1234)
        self.memory.set_value(1, 5678)
        self.memory.display_memory(0, 1)  # Should print memory contents

    # Use Case 12: Handle Invalid Instructions
    def test_invalid_opcode(self):
        """Test handling an invalid opcode."""
        self.uvsim.load_program([9999])
        with self.assertRaises(ValueError):
            self.uvsim.run()

    # Use Case 13: Handle Invalid Memory Access
    def test_invalid_memory_access(self):
        """Test accessing an invalid memory location."""
        with self.assertRaises(IndexError):
            self.memory.get_value(100)

    # Use Case 14: Prevent Division by Zero
    def test_divide_by_zero(self):
        """Test DIVIDE operation with zero."""
        self.memory.set_value(7, 0)  # Set memory location 7 to 0
        with self.assertRaises(ZeroDivisionError):
            self.arithmetic.divide(7, 10)  # Attempt to divide by zero

    # Use Case 15: Exit the Simulator
    def test_exit_simulator(self):
        """Test exiting the simulator."""
        self.uvsim.load_program([4300])  # Load a valid program with HALT instruction
        self.uvsim.run()  # Simulate running and halting
        self.assertTrue(True)  # Placeholder for exit behavior

    # Additional Tests for Edge Cases
    def test_multiply_operation_valid(self):
        """Test MULTIPLY operation with valid values."""
        self.memory.set_value(7, 10)
        accumulator = self.arithmetic.multiply(7, 5)
        self.assertEqual(accumulator, 50)

    def test_divide_operation_valid(self):
        """Test DIVIDE operation with valid values."""
        self.memory.set_value(7, 2)  # Set memory location 7 to 2
        accumulator = 10  # Set accumulator to 10
        result = self.arithmetic.divide(7, accumulator)
        self.assertEqual(result, 5)  # Expected result: 10 / 2 = 5

    def test_branch_neg_operation_invalid(self):
        """Test BRANCHNEG operation with non-negative accumulator."""
        new_pc = self.control.branch_neg(50, 1)
        self.assertIsNone(new_pc)

    def test_branch_zero_operation_invalid(self):
        """Test BRANCHZERO operation with non-zero accumulator."""
        new_pc = self.control.branch_zero(50, 1)
        self.assertIsNone(new_pc)

    def test_store_operation_boundary_value(self):
        """Test STORE operation with boundary value."""
        self.loadstore.store(7, 9999)
        self.assertEqual(self.memory.get_value(7), 9999)

    def test_load_operation_boundary_value(self):
        """Test LOAD operation with boundary value."""
        self.memory.set_value(7, -9999)
        accumulator = self.loadstore.load(7)
        self.assertEqual(accumulator, -9999)

if __name__ == '__main__':
    unittest.main()