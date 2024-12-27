from ortools.sat.python import cp_model

def solve_killer_sudoku():
    model = cp_model.CpModel()

    # Do të krijojmë një matricë 9x9 të tipit IntVar, secila në [1..9].
    X = [[model.NewIntVar(1, 9, f"X[{r},{c}]")
          for c in range(9)]
         for r in range(9)]

    # 1) Kufizimet klasike të Sudoku
    # a) Çdo rresht përmban vlera të ndryshme 1..9
    for r in range(9):
        model.AddAllDifferent(X[r][c] for c in range(9))

    # b) Çdo kolonë përmban vlera të ndryshme 1..9
    for c in range(9):
        model.AddAllDifferent(X[r][c] for r in range(9))

    # c) Çdo bllok 3×3 përmban vlera të ndryshme
    # Ka gjithsej 9 blloqe, secili nis në (br, bc)
    # br në {0,3,6}, bc në {0,3,6}
    for br in [0, 3, 6]:
        for bc in [0, 3, 6]:
            box_cells = []
            for rr in range(br, br+3):
                for cc in range(bc, bc+3):
                    box_cells.append(X[rr][cc])
            model.AddAllDifferent(box_cells)

    #
    # 2) “Killer Sudoku” - kafazet
    #
    # Definojmë secilin kafaz nga:
    #  - 'sum': shuma e synuar
    #  - 'cells': lista e çifteve (row, col) që i përkasin atij kafazi
    #
    # Këtu janë disa kafaze shembull. Zëvendësoni me kafazet reale 
    # të enigmës suaj, ku çdo qelizë e tabelës 9x9 mbulohet nga një kafaz.
    cages = [
        # Shembull i kafazit 1
        {'sum': 15, 'cells': [(0, 0), (0, 1), (1, 0)]},
        # Shembull i kafazit 2
        {'sum': 9,  'cells': [(0, 2), (1, 2)]},
        # Shembull i kafazit 3
        {'sum': 10, 'cells': [(2, 0), (2, 1), (3, 0)]},
        # ...
        # Këtu shtoni kafazet e tjera sipas nevojës
    ]

    # Shtojmë kufizimet për çdo kafaz
    for cage in cages:
        cage_cells = []
        for (r, c) in cage['cells']:
            cage_cells.append(X[r][c])
        # (a) Shuma e qelizave të kafazit duhet të jetë e barabartë me 'sum' të kafazit
        model.Add(sum(cage_cells) == cage['sum'])
        # (b) Të gjitha shifrat brenda një kafazi duhet të jenë të ndryshme
        model.AddAllDifferent(cage_cells)

    # 3) Opsionale: Nëse kemi ndonjë numër të dhënë paraprakisht, shtojmë si kufizim:
    #   model.Add(X[row][col] == value)
    #   Për shembull, nëse e dimë që (4,4) = 7, bëjmë:
    #   model.Add(X[4][4] == 7)

    # 4) Zgjidhja e modelit
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("U gjet një zgjidhje:")
        # Shtypim tabelën
        for r in range(9):
            row_values = []
            for c in range(9):
                val = solver.Value(X[r][c])
                row_values.append(str(val))
            print(" ".join(row_values))
    else:
        print("S’ka zgjidhje.")

if __name__ == "__main__":
    solve_killer_sudoku()