#!/usr/bin/env python3
"""Test script to verify persistent Python session works correctly."""

from src.tools.implementations import execute_python

print("=" * 60)
print("Testing Persistent Python Session")
print("=" * 60)

# Test 1: Define a variable
print("\n[Test 1: Define variable 'x']")
result1 = execute_python("x = 42\nprint(f'x = {x}')")
print(f"Success: {result1.success}")
print(f"Output: {result1.output}")

# Test 2: Access the variable in a new call (should persist)
print("\n[Test 2: Access variable 'x' in new call]")
result2 = execute_python("print(f'x is still {x}')")
print(f"Success: {result2.success}")
print(f"Output: {result2.output}")

# Test 3: Import a library and use it
print("\n[Test 3: Import pandas and create DataFrame]")
result3 = execute_python("""
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(f"DataFrame shape: {df.shape}")
print(df)
""")
print(f"Success: {result3.success}")
print(f"Output: {result3.output}")

# Test 4: Access the DataFrame in a new call (should persist)
print("\n[Test 4: Access DataFrame in new call]")
result4 = execute_python("""
print(f"DataFrame still exists: {df.shape}")
print(f"Column A sum: {df['A'].sum()}")
""")
print(f"Success: {result4.success}")
print(f"Output: {result4.output}")

# Test 5: Error handling (should not crash the session)
print("\n[Test 5: Error handling]")
result5 = execute_python("print(undefined_variable)")
print(f"Success: {result5.success}")
print(f"Error: {result5.error}")

# Test 6: Session should still work after error
print("\n[Test 6: Session still works after error]")
result6 = execute_python("print(f'x is still {x}, df shape is still {df.shape}')")
print(f"Success: {result6.success}")
print(f"Output: {result6.output}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

# Summary
tests_passed = sum([
    result1.success,
    result2.success,
    result3.success,
    result4.success,
    not result5.success,  # Should fail
    result6.success,
])

print(f"\nTests passed: {tests_passed}/6")

if tests_passed == 6:
    print("✅ Persistent Python session is working correctly!")
else:
    print("❌ Some tests failed - check implementation")
