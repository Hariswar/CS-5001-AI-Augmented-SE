src/main.py
"""Simple calculator app that performs basic arithmetic operations.

Usage:
1. Run the script: python src/main.py
2. Enter expressions like "5 + 3" or "10 / 2"
3. Type "exit" to quit

Example:
Input:  5 + 3
Output: 8

Input:  10 / 0
Output: Error: Division by zero
"""

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b

def multiply(a, b):
    """Return the product of a and b."""
    return a * b

def divide(a, b):
    """Return the quotient of a and b. Returns None if b is zero."""
    if b == 0:
        return None
    return a / b

def parse_input(input_str):
    """Parse input string into operands and operator.

    Returns:
        tuple: (operand1, operand2, operator) or (None, None, None) if invalid
    """
    parts = input_str.split()
    if len(parts) != 3:
        return None, None, None
    try:
        a = float(parts[0])
        b = float(parts[2])
        return a, b, parts[1]
    except ValueError:
        return None, None, None

def calculate(a, b, op):
    """Perform calculation based on operator.

    Returns:
        float: result or None if error
    """
    ops = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }
    func = ops.get(op)
    if func is None:
        return None
    return func(a, b)

def main():
    """Main calculator loop."""
    print("Simple Calculator. Enter 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            break
        a, b, op = parse_input(user_input)
        if a is None or b is None or op is None:
            print("Error: Invalid input format. Use 'a op b' (e.g., 5 + 3)")
            continue
        result = calculate(a, b, op)
        if result is None:
            if op == '/':
                print("Error: Division by zero")
            else:
                print("Error: Invalid operator")
        else:
            print(result)

if __name__ == "__main__":
    main()
