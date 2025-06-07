from flask import Flask, render_template_string
from typing import List, Tuple

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sudoku Validator - Animated</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
        }
        table {
            border-collapse: collapse;
            margin: 40px auto;
        }
        td {
            width: 40px;
            height: 40px;
            text-align: center;
            vertical-align: middle;
            font-size: 22px;
            border: 1px solid #555;
            background-color: #fff;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        td.block {
            border: 2px solid #000;
        }
        .valid {
            text-align: center;
            color: green;
            font-weight: bold;
        }
        .invalid {
            text-align: center;
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h2 style="text-align:center;">Sudoku Validator With Custom Zones - Animation</h2>
    <table id="sudoku">
        {% for i in range(9) %}
        <tr>
            {% for j in range(9) %}
            <td id="cell-{{ i }}-{{ j }}" class="{% if j % 3 == 0 and j != 0 %}block{% endif %}"></td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    <h3 class="{{ 'valid' if is_valid else 'invalid' }}">
        {{ 'Valid Sudoku with custom zones' if is_valid else 'Invalid Sudoku' }}
    </h3>

    <script>
        const board = {{ board | tojson }};
        let delay = 0;

        function fillCell(i, j, val) {
            const cell = document.getElementById(`cell-${i}-${j}`);
            setTimeout(() => {
                cell.textContent = val === '.' ? '' : val;
                cell.style.opacity = 1;
            }, delay);
            delay += 100;
        }

        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                fillCell(i, j, board[i][j]);
            }
        }
    </script>
</body>
</html>
"""

def is_valid_sudoku(board: List[List[str]], custom_zones: List[List[Tuple[int, int]]]) -> bool:
    for i in range(9):
        if not is_valid_unit([board[i][j] for j in range(9)]):
            return False
    for j in range(9):
        if not is_valid_unit([board[i][j] for i in range(9)]):
            return False
    for block_i in range(0, 9, 3):
        for block_j in range(0, 9, 3):
            block = [board[i][j] for i in range(block_i, block_i + 3) for j in range(block_j, block_j + 3)]
            if not is_valid_unit(block):
                return False
    for zone in custom_zones:
        cells = [board[i][j] for i, j in zone]
        if not is_valid_unit(cells):
            return False
    return True

def is_valid_unit(unit: List[str]) -> bool:
    nums = [c for c in unit if c != '.']
    return len(nums) == len(set(nums)) and all(c in '123456789' for c in nums)

@app.route("/")
def index():
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]

    custom_zones = [
        [(i, j) for i in range(block_i, block_i + 3) for j in range(block_j, block_j + 3)]
        for block_i in range(0, 9, 3)
        for block_j in range(0, 9, 3)
    ]

    valid = is_valid_sudoku(board, custom_zones)
    return render_template_string(HTML_TEMPLATE, board=board, is_valid=valid)

if __name__ == "__main__":
    app.run(debug=True)
