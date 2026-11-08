def parse_file(input_path):
    equations = []
    operators = {"+": "add", "-": "sub", "*": "mul"}
    with open(input_path) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            line = "".join(line.split())

            dest, args = line.split("=")
            for char in args:
                if char in "+-*":
                    op = char
                    break
            lhs, rhs = args.split(op)

            equation = {
                "dest": dest,
                "lhs": lhs,
                "op": operators[op],
                "rhs": rhs
            }

            equations.append(equation)
    return equations



            