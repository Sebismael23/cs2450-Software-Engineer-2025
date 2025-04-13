# UVSim Unit Tests Based on Use Cases

| Test Name | Description | Use Case Reference | Inputs | Expected Outputs | Success Criteria |
|-----------------------------------------|---------------------------------------------------------|--------------------|-------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------------|
| `test_load_program_valid` | Test loading a valid program into memory. | 1 | Program: [1007, 2107, 1107, 4300] | Memory locations 0-3 should contain the program instructions. | Memory locations 0-3 should match the input program. |
| `test_load_program_large_memory` | Test loading a program that uses full 250 memory locations. | 1 | Program: [0]*250 (with first/last modified) | Memory locations 0 and 249 should contain set values. | Memory locations should match input values at boundaries. |
| `test_load_program_invalid_size` | Test loading a program that exceeds memory size. | 1 | Program: [0] * 251 | Should raise ValueError. | Test should raise ValueError. |
| `test_execute_program_invalid_opcode` | Test executing a program with an invalid opcode. | 2 | Program: [9999] | Should raise ValueError. | Test should raise ValueError. |
| `test_read_operation_valid` | Test READ operation with valid input. | 3 | User input: 1234 | Memory location 7 should contain the user input. | Memory location 7 should be 1234. |
| `test_read_operation_invalid_input` | Test READ operation with invalid input. | 3 | Invalid input (10000) | Should raise ValueError. | Test should raise ValueError. |
| `test_write_operation_valid` | Test WRITE operation with valid memory value. | 4 | Memory location 7: 1234 | Should return the value being written. | Return value should match memory value. |
| `test_write_operation_invalid_address` | Test WRITE operation with invalid memory address. | 4 | Address: 250 | Should raise IndexError. | Test should raise IndexError. |
| `test_load_operation_valid` | Test LOAD operation with valid memory value. | 5 | Memory location 7: 1234 | Accumulator should be 1234. | Accumulator should match the value in memory. |
| `test_load_operation_invalid_address` | Test LOAD operation with invalid memory address. | 5 | Address: 250 | Should raise IndexError. | Test should raise IndexError. |
| `test_store_operation_valid` | Test STORE operation with valid value. | 6 | Value: 1234 | Memory location 7 should be 1234. | Memory location should match input value. |
| `test_store_operation_invalid_value` | Test STORE operation with invalid value. | 6 | Value: 1000000 | Should raise ValueError. | Test should raise ValueError. |
| `test_add_operation_valid` | Test ADD operation with valid values. | 7 | Memory location 7: 1000, Accumulator: 500 | Accumulator should be 1500. | Accumulator should be the sum of values. |
| `test_subtract_operation_valid` | Test SUBTRACT operation with valid values. | 7 | Memory location 7: 1000, Accumulator: 500 | Accumulator should be -500. | Accumulator should be subtraction result. |
| `test_branch_operation_valid` | Test BRANCH operation with valid address. | 8 | Address: 50 | Program counter should be 50. | Program counter should update to address. |
| `test_branch_neg_operation_valid` | Test BRANCHNEG operation with negative accumulator. | 9 | Address: 50, Accumulator: -1 | Program counter should be 50. | Program counter updates if accumulator negative. |
| `test_branch_zero_operation_valid` | Test BRANCHZERO operation with zero accumulator. | 9 | Address: 50, Accumulator: 0 | Program counter should be 50. | Program counter updates if accumulator zero. |
| `test_halt_operation_valid` | Test HALT operation. | 10 | None | Should return True. | Operation should return True to indicate halt. |
| `test_display_memory_valid` | Test displaying memory contents. | 11 | Memory locations 0: 1234, 249: 5678 | Should print memory contents. | Output should match expected memory contents. |
| `test_invalid_opcode` | Test handling an invalid opcode. | 12 | Program: [9999] | Should raise ValueError. | Test should raise ValueError. |
| `test_invalid_memory_access` | Test accessing invalid memory location. | 13 | Address: 250 | Should raise IndexError. | Test should raise IndexError. |
| `test_divide_by_zero` | Test DIVIDE operation with zero. | 14 | Memory location 7: 0, Accumulator: 10 | Should raise ZeroDivisionError. | Test should raise ZeroDivisionError. |
| `test_format_detection_4digit` | Test automatic 4-digit format detection. | 15 | Program: [1007, 2107, 1107, 4300] | Format should be "4-digit". | Format should be correctly detected. |
| `test_format_detection_6digit` | Test automatic 6-digit format detection. | 15 | Program: [100007, 210007, 110007, 430000] | Format should be "6-digit". | Format should be correctly detected. |
| `test_multiply_operation_valid` | Test MULTIPLY operation with valid values. | 7 | Memory location 7: 10, Accumulator: 5 | Accumulator should be 50. | Accumulator should be product of values. |
| `test_divide_operation_valid` | Test DIVIDE operation with valid values. | 7 | Memory location 7: 2, Accumulator: 10 | Result should be 5. | Result should be division of values. |
| `test_branch_neg_operation_invalid` | Test BRANCHNEG with non-negative accumulator. | 9 | Address: 50, Accumulator: 1 | Should return None. | Program counter should not change. |
| `test_branch_zero_operation_invalid` | Test BRANCHZERO with non-zero accumulator. | 9 | Address: 50, Accumulator: 1 | Should return None. | Program counter should not change. |
| `test_store_operation_boundary_value` | Test STORE with boundary values. | 6 | Values: ±999999 | Memory should store values correctly. | Memory should store max/min 6-digit values. |
| `test_load_operation_boundary_value` | Test LOAD with boundary value. | 5 | Memory location 7: -999999 | Accumulator should be -999999. | Accumulator should match memory value. |
