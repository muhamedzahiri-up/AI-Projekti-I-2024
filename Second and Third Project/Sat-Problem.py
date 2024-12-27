from ortools.sat.python import cp_model
from itertools import product, groupby

def groupby_keys(input_list, keylist):
    """
    Funksion ndihmës për të grupuar elementet në 'input_list'
    sipas vlerave të çelësave të specifikuar në 'keylist'.
    """
    keyfunc = lambda x: tuple(x[k] for k in keylist)
    for key, group in groupby(sorted(input_list, key=keyfunc), key=keyfunc):
        yield key, list(group)

def solve_party_seating(n_guests=100,
                        n_tables=10,
                        table_capacity=10,
                        must_not_pairs=None,
                        must_pairs=None):
    """
    Zgjidh problemin e uljes së mysafirëve me OR-Tools CP-SAT:
      - n_guests: numri total i mysafirëve
      - n_tables: numri total i tavolinave
      - table_capacity: numri i vendeve për tavolinë (duhet të jetë n_guests // n_tables)
      - must_not_pairs = listë me çifte (i, j) që NUK duhet të ulen bashkë
      - must_pairs = listë me çifte (i, j) që DUHET të ulen bashkë

    Kthen (status, assignment) ku:
      - status: statusi i zgjidhësit (cp_model.OPTIMAL, FEASIBLE, INFEASIBLE, etj.)
      - assignment: një fjalor (dict) ku assignment[guest] = table_id
    """
    if must_not_pairs is None:
        must_not_pairs = []
    if must_pairs is None:
        must_pairs = []

    # Do ta trajtojmë "week" = 0 pasi kemi vetëm një rregullim
    weeks = [0]  # një "rreth" ose "javë" e vetme
    guests = list(range(n_guests))
    tables = list(range(n_tables))

    # 1) Krijojmë modelin CP
    model = cp_model.CpModel()

    # 2) Krijojmë variabla Booleane: x[g, w, t] = 1 nëse mysafiri g ulet në tavolinën t në "javën" w
    x_var = {}
    variables = []
    for g, w, t in product(guests, weeks, tables):
        var_name = f"x_{g}_{w}_{t}"
        x_var[g, w, t] = model.NewBoolVar(var_name)
        variables.append({
            'Name': var_name,
            'Guest': g,
            'Week': w,
            'Table': t,
            'CP_Var': x_var[g, w, t]
        })

    # 3) Kufizimet

    # A) Secili mysafir është saktësisht në 1 tavolinë
    #    sum_{t in tables} x[g, w, t] = 1 për çdo mysafir g, javë w
    def groupby_keys_func(item):
        return (item['Guest'], item['Week'])
    for _, group_list in groupby(sorted(variables, key=groupby_keys_func), key=groupby_keys_func):
        model.Add(sum(v['CP_Var'] for v in group_list) == 1)

    # B) Secila tavolinë ka saktësisht 'table_capacity' mysafirë
    #    sum_{g in guests} x[g, w, t] = table_capacity për çdo tavolinë t, javë w
    def groupby_keys_func2(item):
        return (item['Week'], item['Table'])
    for _, group_list in groupby(sorted(variables, key=groupby_keys_func2), key=groupby_keys_func2):
        model.Add(sum(v['CP_Var'] for v in group_list) == table_capacity)

    # C) must_not_pairs: nëse (i, j) nuk duhet të ulen bashkë,
    #    atëherë x[i, w, t] + x[j, w, t] <= 1, pra s'mund të ndajnë tavolinën e njëjtë
    for (i, j) in must_not_pairs:
        for w in weeks:
            for t in tables:
                model.Add(x_var[i, w, t] + x_var[j, w, t] <= 1)

    # D) must_pairs: nëse (i, j) duhet të ulen bashkë,
    #    atëherë x[i, w, t] == x[j, w, t] për secilën tavolinë t, javë w
    #    p.sh. ata zgjedhin pikërisht të njëjtën tavolinë
    for (i, j) in must_pairs:
        for w in weeks:
            for t in tables:
                model.Add(x_var[i, w, t] == x_var[j, w, t])

    # 4) Zgjidhim
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # 5) Interpretojmë rezultatin
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Ndërtojmë një fjalor: assignment[guest] = table
        assignment = {}
        for g in guests:
            for t in tables:
                w = 0  # kemi vetëm një "javë"
                if solver.Value(x_var[g, w, t]) == 1:
                    assignment[g] = t
                    break
        return status, assignment
    else:
        return status, None

def main():
    # Shembull kufizimesh "must_not" (s'duhet bashkë)
    must_not = [
        (0, 1),
        (10, 11),
        (20, 30),
        (50, 60)
    ]
    # Shembull kufizimesh "must" (duhet bashkë)
    must_pairs = [
        (2, 3),
        (95, 99)
    ]

    status, assignment = solve_party_seating(
        n_guests=100,
        n_tables=10,
        table_capacity=10,
        must_not_pairs=must_not,
        must_pairs=must_pairs
    )

    if assignment is None:
        print("Nuk u gjet asnjë rregullim i vlefshëm (INFEASIBLE).")
    else:
        print("U gjet një rregullim i vlefshëm!")
        # Grupojmë mysafirët sipas tavolinave ku janë caktuar
        table_assignments = {t: [] for t in range(10)}
        for guest, table in assignment.items():
            table_assignments[table].append(guest)

        # Printojmë në formatin e kërkuar
        for t in range(10):
            print(f"Tavolina {t+1}: {table_assignments[t]}")

if __name__ == "__main__":
    main()