from ortools.sat.python import cp_model
from itertools import product, groupby, combinations

# Funksion ndihmës për të iteruar mbi artikujt e grupuar
def groupby_keys(input_list, keylist):
    keyfunc = lambda x: tuple(x[k] for k in keylist)
    for key, group in groupby(sorted(input_list, key=keyfunc), key=keyfunc):
        yield key, list(group)

# Përkufizimi i problemit

n_players = int(input("Numri i lojtarëve: ")) # Numri i lojtarëve
n_weeks = int(input("Numri i javëve: ")) # Numri i javëve
players_per_group = int(input("Numri i lojtarëve për grup: ")) # Numri i lojtarëve për grup

# Parametrat e nxjerrë
n_groups = n_players // players_per_group  # Numri i grupeve
players = list(range(n_players))  # Lista e lojtarëve
weeks = list(range(n_weeks))  # Lista e javëve
groups = list(range(n_groups))  # Lista e grupeve

# Inicializo modelin
model = cp_model.CpModel()

# Ndryshoret
variables = []
player_vars = {}
for player, week, group in product(players, weeks, groups):
    v_name = f"{player}_{week}_{group}"
    the_var = model.NewBoolVar(v_name)
    variables.append(
        {k: v for v, k in zip([v_name, player, week, group, the_var], ['Name', 'Player', 'Week', 'Group', 'CP_Var'])}
    )
    player_vars[player, week, group] = the_var

# Kufizimet

# Çdo lojtar duhet të jetë saktësisht në një grup për çdo javë
for _, grp in groupby_keys(variables, ['Player', 'Week']):
    model.Add(sum(x['CP_Var'] for x in grp) == 1)

# Çdo grup duhet të ketë saktësisht numrin e kërkuar të lojtarëve për çdo javë
for _, grp in groupby_keys(variables, ['Week', 'Group']):
    model.Add(sum(x['CP_Var'] for x in grp) == players_per_group)

# Siguro që dy lojtarë nuk janë në të njëjtin grup më shumë se një herë
for p1, p2 in combinations(players, r=2):
    players_together = []
    for week in weeks:
        for group in groups:
            together = model.NewBoolVar(f"M_{p1}_{p2}_{week}_{group}")
            players_together.append(together)
            p1g = player_vars[p1, week, group]
            p2g = player_vars[p2, week, group]
            # Imposto që nëse të dy lojtarët janë në të njëjtin grup, `together` është 1
            model.Add(p1g + p2g - together <= 1)
    # Kufizo numrin total të herëve që dy lojtarë takohen në maksimum 1
    model.Add(sum(players_together) <= 1)

# Zgjidh modelin
solver = cp_model.CpSolver()
status = solver.Solve(model)
print(solver.ResponseStats())

# Parsimi dhe formatimi i zgjidhjes
def parse_answer(variables):
    solution = {}
    for var in variables:
        player, week, group = var['Player'], var['Week'], var['Group']
        solution[player, week, group] = solver.Value(var['CP_Var'])

    weeks = sorted(set(x[1] for x in solution))
    groups = sorted(set(x[2] for x in solution))
    answers = {}
    for week in weeks:
        answers[week] = {}
        for group in groups:
            ans = [k[0] for k, v in solution.items() if k[1] == week and k[2] == group and v]
            answers[week][group] = sorted(ans)
    return answers

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    ans = parse_answer(variables)
    for week, group_data in ans.items():
        print(f"Java {week + 1}:")
        for group, members in group_data.items():
            print(f"  Grupi {group + 1}: {members}")
else:
    print("Nuk u gjet asnjë zgjidhje.")
