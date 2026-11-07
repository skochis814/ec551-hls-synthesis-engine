# ill have the schedules stored in a dict formatted as shown below 
# the [] containing {} are one cycle each, and unit refers to like adder0 or multiplier0, to track if we gotta reuse or create additional
schedule = {
    "inputs": {"A": "A_0", "B": "B_0"},
    "outputs": {"X": "X_2", "Y": "Y_1"},
    "cycles": [
        [  # Cycle 0: X = A + B and Y = A * B
            {"op": "add", "unit": 0, "lhs": "A_0", "rhs": "B_0", "dest": "X_1"},
            {"op": "mul", "unit": 0, "lhs": "A_0", "rhs": "B_0", "dest": "Y_1"},
        ],
        [  # Cycle 1: X = X + Y
            {"op": "add", "unit": 0, "lhs": "X_1", "rhs": "Y_1", "dest": "X_2"},
        ],
    ],
}
