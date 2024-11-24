from collections import deque

def is_valid(board, row, col, num):
    """Kontrollon nëse num mund të vendoset në qelizën (row, col) pa shkelur rregullat e Sudoku-së."""
    # Kontrollo rreshtin
    for i in range(9):
        if board[row][i] == num:
            return False

    # Kontrollo kolonën
    for i in range(9):
        if board[i][col] == num:
            return False

    # Kontrollo kutinë 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def bfs_solver(board):
    """Zgjidh Sudoku-n duke përdorur algoritmin BFS."""
    queue = deque([(board, 0, 0)])  # Shto tabelën fillestare në radhë

    while queue:
        current_board, row, col = queue.popleft()

        if row == 9:  # Nëse të gjitha rreshtat janë plotësuar, kthe tabelën
            return current_board

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        if current_board[row][col] != 0:  # Nëse qeliza nuk është bosh, kalo te qeliza tjetër
            queue.append((current_board, next_row, next_col))
        else:
            for num in range(1, 10):
                if is_valid(current_board, row, col, num):
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = num
                    queue.append((new_board, next_row, next_col))

    return None  # Nëse nuk gjendet zgjidhje

def backtracking_solver(board):
    """Zgjidh Sudoku-n duke përdorur algoritmin Backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if backtracking_solver(board):
                            return True

                        board[row][col] = 0  # Rikthehu prapa

                return False

    return True

def print_board(board):
    """Shfaq tabelën Sudoku."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def get_sample_sudoku(level):
    """Kthen një tabelë Sudoku për një nivel të zgjedhur."""
    easy = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    medium = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]

    hard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 9, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 5, 9, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 7, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 5, 0],
        [1, 0, 0, 0, 0, 8, 9, 0, 0],
    ]

    levels = {1: easy, 2: medium, 3: hard}
    return levels.get(level, easy)

def main():
    print("Zgjidh një nivel të Sudoku-së:")
    print("1 - Easy")
    print("2 - Medium")
    print("3 - Hard")

    level = int(input("Nivel (1, 2, 3): "))
    board = get_sample_sudoku(level)

    print("\nTabela fillestare:")
    print_board(board)

    print("\nZgjidhje me Backtracking:")
    if backtracking_solver(board):
        print_board(board)
    else:
        print("Nuk u gjet zgjidhje.")

    bfs_board = [row[:] for row in board]
    print("\nZgjidhje me BFS:")
    solution = bfs_solver(bfs_board)
    if solution:
        print_board(solution)
    else:
        print("Nuk u gjet zgjidhje.")

if __name__ == "__main__":
    main()