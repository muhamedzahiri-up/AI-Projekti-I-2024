def is_valid(matrix, row, col, num):
    """Shiko nëse vendosja e num tel matrix[row][col] është e lejuar."""
    for i in range(len(matrix)):
        if matrix[row][i] == num or matrix[i][col] == num:
            return False
    return True

def iddfs_backtracking(n):
    """Krijo një katror latin duke përdorur IDDFS dhe Backtracking."""
    def solve(matrix, row, col, depth):
        if row == n:  # Gjithë rreshtat janë mbushur
            return True

        if col == n:  # Kapërce tek rreshti tjetër
            return solve(matrix, row + 1, 0, depth)

        for num in range(1, n + 1):
            if is_valid(matrix, row, col, num):
                matrix[row][col] = num
                if solve(matrix, row, col + 1, depth):
                    return True
                matrix[row][col] = 0  # Backtrack

        return False

    for depth in range(1, n + 1):
        matrix = [[0] * n for _ in range(n)]
        if solve(matrix, 0, 0, depth):
            return matrix

    return None

# Hyrja
n = int(input("Hyrja: "))
latin_square = iddfs_backtracking(n)

# Output
if latin_square:
    for row in latin_square:
        print(" ".join(map(str, row)))
else:
    print("Nuk mund të krijohet një katror latin për këtë hyrje.")
