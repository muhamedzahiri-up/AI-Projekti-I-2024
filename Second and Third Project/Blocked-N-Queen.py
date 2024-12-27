import heapq

class BlockedNQueens:
    def __init__(self, n, blocked_positions):
        """
        Konstruktori për problemin e N-Mbretëreshave të Bllokuara.
        :param n: madhësia e tabelës (n x n).
        :param blocked_positions: listë ose set e kuadrateve (row, col) që janë të bllokuara (nuk mund të vendoset mbretëresha).
        """
        self.n = n
        self.blocked_positions = set(blocked_positions)

    def is_valid(self, state, row, col):
        """
        Kontrollon nëse mund të vendosim një mbretëreshë te (row, col) pa konflikt dhe pa qenë në kuadrat të bllokuar.

        :param state: listë e pozicioneve të kolonave për rreshtat [0..len(state)-1].
                      Për shembull, nëse state = [2, 4], atëherë rreshti 0 ka mbretëreshën te kolona 2, rreshti 1 te kolona 4.
        :param row: rreshti ku do të vendosim mbretëreshën e re.
        :param col: kolona ku do të vendosim mbretëreshën e re.
        :return: True nëse është e vlefshme, përndryshe False.
        """
        # 1) Kontrollo nëse kuadrati është i bllokuar
        if (row, col) in self.blocked_positions:
            return False

        # 2) Kontrollo konfliktet me mbretëreshat ekzistuese në 'state'
        for r, c in enumerate(state):
            # Mbretëresha nuk duhet të jetë në të njëjtën kolonë ose diagonal
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def get_neighbors(self, state):
        """
        Gjeneron pasardhësit (fqinjët) duke shtuar një mbretëreshë në rreshtin tjetër.
        :param state: zgjidhja e pjesshme (listë e kolonave për mbretëreshat e vendosura deri më tani).
        :return: listë me shtete të reja, ku secili ka një mbretëreshë të shtuar në rreshtin (len(state)).
        """
        row = len(state)
        neighbors = []
        for col in range(self.n):
            if self.is_valid(state, row, col):
                neighbors.append(state + [col])
        return neighbors

    # ---------------------------
    #       HEURISTIKA #1
    # ---------------------------
    def heuristic_1(self, state):
        """
        h1 = numri i mbretëreshave që mbeten për t'u vendosur = (n - len(state)).
        Kjo është një heuristikë e thjeshtë dhe zakonisht 'admissible' 
        nëse kostoja matet me "1 vendosje për rresht".
        """
        return self.n - len(state)

    # ---------------------------
    #       HEURISTIKA #2
    # ---------------------------
    def heuristic_2(self, state):
        """
        h2: Kontrollon vetëm rreshtin tjetër (row = len(state)).
            - Nëse ai rresht s'ka asnjë kolonë të vlefshme -> kthe një vlerë të madhe (p.sh. 999999).
            - Përndryshe kthe (n - len(state)).
        """
        next_row = len(state)
        # Nëse i kemi vendosur të gjitha mbretëreshat, h = 0
        if next_row == self.n:
            return 0

        feasible_cols = 0
        for col in range(self.n):
            if self.is_valid(state, next_row, col):
                feasible_cols += 1

        if feasible_cols == 0:
            return 999999  # Praktikisht e pafundme -> bllokim
        else:
            return self.n - len(state)

    # ---------------------------
    #       HEURISTIKA #3
    # ---------------------------
    def heuristic_3(self, state):
        """
        h3: Për secilin rresht të ardhshëm nga len(state) .. (n-1),
            kontrollo nëse të paktën ekziston 1 kolonë e vlefshme. 
            - Nëse ndonjë rresht ka 0 kolona të vlefshme => kthe vlerë të madhe (pa rrugëzgjidhje).
            - Përndryshe, për thjeshtësi, kthe (n - len(state)) (ose një shumë e rreshtave).
        """
        row_start = len(state)
        if row_start == self.n:
            return 0  # s'ka më mbretëresha për t'u vendosur

        # Kontrollo rresht për rresht
        for row in range(row_start, self.n):
            feasible_cols = 0
            for col in range(self.n):
                if self.is_valid(state, row, col):
                    feasible_cols += 1
            if feasible_cols == 0:
                return 999999  # Bllokim i plotë -> kosto e madhe

        # Nëse të gjithë rreshtat kanë të paktën 1 mundësi
        return self.n - len(state)

    def a_star(self, heuristic_choice=1):
        """
        Implementon A* për problemin e N-Mbretëreshave të Bllokuara,
        duke zgjedhur njërën prej heuristikave (1, 2, ose 3).

        :param heuristic_choice: numër që tregon cilën heuristikë të përdorim
        :return: një zgjidhje e plotë (listë e kolonave për secilin rresht) ose None nëse s'ka zgjidhje.
        """
        # Zgjedh heuristikën sipas parametrit
        if heuristic_choice == 1:
            heuristic_fn = self.heuristic_1
        elif heuristic_choice == 2:
            heuristic_fn = self.heuristic_2
        else:
            heuristic_fn = self.heuristic_3

        # 'pq' është një kup priority-queue ku ruajmë tuples (f, state)
        # f = g + h, ku g = len(state), h = vlera e heuristikës
        pq = []
        initial_state = []
        initial_cost = 0 + heuristic_fn(initial_state)  # g + h = 0 + h
        heapq.heappush(pq, (initial_cost, initial_state))

        while pq:
            cost, state = heapq.heappop(pq)
            # Nëse kemi vendosur n mbretëresha, e kemi zgjidhjen
            if len(state) == self.n:
                return state

            # Zgjasim fqinjët (pasardhësit)
            for neighbor in self.get_neighbors(state):
                g = len(neighbor)  # kosto e deritanishme -> 1 për çdo mbretëreshë të vendosur
                h = heuristic_fn(neighbor)
                f = g + h
                heapq.heappush(pq, (f, neighbor))

        return None  # Nëse skadon prioriteti dhe s'ka zgjidhje, kthe None

def print_custom_solution(n, solution, blocked_positions):
    """
    Shfaq një tabelë n x n me format:
      - 'X' për kuadratet e bllokuara
      - '.' për kuadratet bosh
      - numrin (row+1) për mbretëreshën në rreshtin 'row'

    :param n: madhësia e tabelës
    :param solution: listë e kolonave për secilin rresht
    :param blocked_positions: set ose listë e (row, col) të bllokuara
    """
    board = [["." for _ in range(n)] for _ in range(n)]

    # Vendosim mbretëreshat me numrin e rreshtit (1-based) për qartësi
    for row, col in enumerate(solution):
        board[row][col] = str(row + 1)

    # Shënojmë kuadratet e bllokuara me 'X'
    for (br, bc) in blocked_positions:
        board[br][bc] = "X"

    # Printojmë tabelën përfundimtare
    for row in board:
        print(" ".join(row))


# Shembull ekzekutimi
if __name__ == "__main__":
    n = 8
    blocked_positions = [(0, 2), (3, 5), (6, 1)]  # shembull i disa kuadrateve të bllokuara

    problem = BlockedNQueens(n, blocked_positions)

    # Zgjedhim cilën heuristikë dëshirojmë: 1, 2, ose 3
    chosen_heuristic = int(input("Zgjedh heuristics: "))

    print(f"Po zgjidhim problemin e N-Mbretëreshave të Bllokuara (n={n}) me A* (Heuristika #{chosen_heuristic})...")
    solution = problem.a_star(heuristic_choice=chosen_heuristic)

    if solution:
        print("U gjet një zgjidhje:")
        print(solution)
        print("\nPamja e tabelës:\n")
        print_custom_solution(n, solution, blocked_positions)
    else:
        print("S'ka zgjidhje!") 