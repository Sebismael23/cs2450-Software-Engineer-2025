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

    def test_load_program_large_memory(self):
        """Test loading a program that uses the full 250 memory locations."""
        program = [0] * 250  # Max memory size
        program[0] = 1007
        program[249] = 4300
        self.memory.load_program(program)
        self.assertEqual(self.memory.get_value(0), 1007)
        self.assertEqual(self.memory.get_value(249), 4300)

    def test_load_program_invalid_size(self):
        """Test loading a program that exceeds memory size."""
        program = [0] * 251  # Exceeds memory size
        with self.assertRaises(ValueError):
            self.memory.load_program(program)

    # Use Case 2: Execute a BasicML Program
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
            self.inputoutput.write(250)  # Invalid address

    # Use Case 5: Load a Value into the Accumulator
    def test_load_operation_valid(self):
        """Test LOAD operation with valid memory value."""
        self.memory.set_value(7, 1234)
        accumulator = self.loadstore.load(7)
        self.assertEqual(accumulator, 1234)

    def test_load_operation_invalid_address(self):
        """Test LOAD operation with invalid memory address."""
        with self.assertRaises(IndexError):
            self.loadstore.load(250)  # Invalid address

    # Use Case 6: Store a Value in Memory
    def test_store_operation_valid(self):
        """Test STORE operation with valid value."""
        self.loadstore.store(7, 1234)
        self.assertEqual(self.memory.get_value(7), 1234)

    def test_store_operation_invalid_value(self):
        """Test STORE operation with invalid value."""
        with self.assertRaises(ValueError):
            self.loadstore.store(7, 1000000)  # Invalid value

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
        self.memory.set_value(249, 5678)  # Test end of expanded memory
        self.memory.display_memory(0, 249)  # Should print memory contents

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
            self.memory.get_value(250)  # Beyond expanded memory

    # Use Case 14: Prevent Division by Zero
    def test_divide_by_zero(self):
        """Test DIVIDE operation with zero."""
        self.memory.set_value(7, 0)  # Set memory location 7 to 0
        with self.assertRaises(ZeroDivisionError):
            self.arithmetic.divide(7, 10)  # Attempt to divide by zero

    # Use Case 15: Format Conversion
    def test_format_detection_4digit(self):
        """Test automatic detection of 4-digit format."""
        program = [1007, 2107, 1107, 4300]
        self.uvsim.load_program(program)
        self.assertEqual(self.uvsim.format, "4-digit")

    def test_format_detection_6digit(self):
        """Test automatic detection of 6-digit format."""
        program = [100007, 210007, 110007, 430000]
        self.uvsim.load_program(program)
        self.assertEqual(self.uvsim.format, "6-digit")

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
        self.loadstore.store(7, 999999)  # Max 6-digit positive
        self.assertEqual(self.memory.get_value(7), 999999)
        self.loadstore.store(7, -999999)  # Max 6-digit negative
        self.assertEqual(self.memory.get_value(7), -999999)

    def test_load_operation_boundary_value(self):
        """Test LOAD operation with boundary value."""
        self.memory.set_value(7, -999999)
        accumulator = self.loadstore.load(7)
        self.assertEqual(accumulator, -999999)

if __name__ == '__main__':
    unittest.main()
