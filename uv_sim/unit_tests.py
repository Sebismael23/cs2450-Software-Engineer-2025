import unittest
from UVSim import UVSim
from memory_structure import UVSimMemory
from operations import UVSimOperations

class TestUVSim(unittest.TestCase):
    def setUp(self):
        self.memory = UVSimMemory()
        self.operations = UVSimOperations(self.memory)
        self.uvsim = UVSim()

    def test_memory_initialization(self):
        # Test that memory is initialized to 100 locations with zero values
        for i in range(100):
            self.assertEqual(self.memory.get_value(i), 0)

    def test_load_program(self):
        # Test loading a program into memory
        program = [1007, 2107, 1107, 4300]
        self.memory.load_program(program)
        for i in range(len(program)):
            self.assertEqual(self.memory.get_value(i), program[i])

    def test_read_operation(self):
        # Test READ operation
        self.operations.read(7)
        self.assertNotEqual(self.memory.get_value(7), 0)

    def test_write_operation(self):
        # Test WRITE operation
        self.memory.set_value(7, 1234)
        self.operations.write(7)  # Should print 1234

    def test_load_operation(self):
        # Test LOAD operation
        self.memory.set_value(7, 1234)
        accumulator = self.operations.load(7)
        self.assertEqual(accumulator, 1234)

    def test_store_operation(self):
        # Test STORE operation
        self.operations.store(7, 1234)
        self.assertEqual(self.memory.get_value(7), 1234)

    def test_add_operation(self):
        # Test ADD operation
        self.memory.set_value(7, 1000)
        accumulator = self.operations.add(7, 500)
        self.assertEqual(accumulator, 1500)

    def test_subtract_operation(self):
        # Test SUBTRACT operation
        self.memory.set_value(7, 500)  # Set memory location 7 to 500
        accumulator = 1000  # Set the accumulator to 1000
        result = self.operations.subtract(7, accumulator)  # Subtract memory[7] from accumulator
        self.assertEqual(result, 500)  # Expected result: 1000 - 500 = 500

    def test_multiply_operation(self):
        # Test MULTIPLY operation
        self.memory.set_value(7, 10)
        accumulator = self.operations.multiply(7, 5)
        self.assertEqual(accumulator, 50)

    def test_divide_operation(self):
        # Test DIVIDE operation
        self.memory.set_value(7, 2)  # Set memory location 7 to 500
        accumulator = 10  # Set the accumulator to 1000
        result = self.operations.divide(7, accumulator)  # Subtract memory[7] from accumulator
        self.assertEqual(result, 5)  # Expected result: 1000 - 500 = 500

    def test_divide_by_zero(self):
        # Test DIVIDE operation with zero
        accumulator = 10
        self.memory.set_value(7, 0)
        with self.assertRaises(ZeroDivisionError):
            self.operations.divide(7, accumulator)

    def test_branch_operation(self):
        # Test BRANCH operation
        new_pc = self.operations.branch(50)
        self.assertEqual(new_pc, 50)

    def test_branch_neg_operation(self):
        # Test BRANCHNEG operation
        new_pc = self.operations.branch_neg(50, -1)
        self.assertEqual(new_pc, 50)

    def test_branch_zero_operation(self):
        # Test BRANCHZERO operation
        new_pc = self.operations.branch_zero(50, 0)
        self.assertEqual(new_pc, 50)

    def test_halt_operation(self):
        # Test HALT operation
        result = self.operations.halt()
        self.assertTrue(result)

    def test_invalid_memory_access(self):
        # Test accessing invalid memory location
        with self.assertRaises(IndexError):
            self.memory.get_value(100)

    def test_invalid_value(self):
        # Test setting an invalid value in memory
        with self.assertRaises(ValueError):
            self.memory.set_value(7, 10000)

    def test_invalid_opcode(self):
        # Test invalid opcode
        self.uvsim.load_program([9999])
        with self.assertRaises(ValueError):
            self.uvsim.run()

    def test_program_execution(self):
        # Test full program execution
        program = [1007, 2107, 1107, 4300]  # READ -> STORE -> WRITE -> HALT
        self.uvsim.load_program(program)
        self.uvsim.run()  # Should execute without errors

    def test_display_memory(self):
        # Test displaying memory contents
        self.memory.set_value(0, 1234)
        self.memory.set_value(1, 5678)
        self.memory.display_memory(0, 1)  # Should print memory contents

if __name__ == '__main__':
    unittest.main()