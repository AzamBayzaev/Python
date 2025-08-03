def count_queens(board):
    n = len(board)
    cols = set()
    diag1 = set()  # r-c
    diag2 = set()  # r+c
    result = [0]

    def backtrack(r):
        if r == n:
            result[0] += 1
            return
        for c in range(n):
            if board[r][c] == '#' or c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue
            cols.add(c)
            diag1.add(r-c)
            diag2.add(r+c)
            backtrack(r+1)
            cols.remove(c)
            diag1.remove(r-c)
            diag2.remove(r+c)

    backtrack(0)
    return result[0]

board = [
    [".",".","#","."],
    [".",".",".","."],
    [".","#",".","."],
    [".",".",".","."]
]
print(count_queens(board))
