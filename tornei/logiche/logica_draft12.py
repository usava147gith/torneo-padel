print("USO VERSIONE STABILE v8.0")

from ortools.sat.python import cp_model
import pandas as pd

N_PLAYERS = 12
GROUP_SIZE = 4
N_GROUPS = N_PLAYERS // GROUP_SIZE


def build_model(n_turns: int):
    model = cp_model.CpModel()
    x = {}

    # x[p, t, g] = 1 se il giocatore p è nel gruppo g al turno t
    for p in range(N_PLAYERS):
        for t in range(n_turns):
            for g in range(N_GROUPS):
                x[p, t, g] = model.NewBoolVar(f"x_p{p}_t{t}_g{g}")

    # Ogni giocatore gioca in un solo gruppo per turno
    for p in range(N_PLAYERS):
        for t in range(n_turns):
            model.Add(sum(x[p, t, g] for g in range(N_GROUPS)) == 1)

    # Ogni gruppo ha esattamente 4 giocatori
    for t in range(n_turns):
        for g in range(N_GROUPS):
            model.Add(sum(x[p, t, g] for p in range(N_PLAYERS)) == GROUP_SIZE)

    return model, x


def build_pair_vars(model, x, n_turns: int):
    pair = {}

    for t in range(n_turns):
        for g in range(N_GROUPS):
            for p1 in range(N_PLAYERS):
                for p2 in range(p1 + 1, N_PLAYERS):
                    b = model.NewBoolVar(f"pair_{p1}_{p2}_t{t}_g{g}")
                    pair[(p1, p2, t, g)] = b

                    model.Add(b <= x[p1, t, g])
                    model.Add(b <= x[p2, t, g])

    return pair


def add_constraints_stable(model, x, n_turns: int):
    print(">>> ESEGUO add_constraints_stable VERSIONE CORRETTA")
    pair = build_pair_vars(model, x, n_turns)

    # Ogni giocatore ha 1 compagno nel gruppo
    for t in range(n_turns):
        for g in range(N_GROUPS):
            for p in range(N_PLAYERS):
                comp_list = []
                for q in range(N_PLAYERS):
                    if p == q:
                        continue
                    i, j = sorted((p, q))
                    comp_list.append(pair[(i, j, t, g)])

                model.Add(sum(comp_list) == 1).OnlyEnforceIf(x[p, t, g])
                model.Add(sum(comp_list) == 0).OnlyEnforceIf(x[p, t, g].Not())

    # Ogni gruppo ha esattamente 2 coppie
    for t in range(n_turns):
        for g in range(N_GROUPS):
            model.Add(
                sum(pair[(i, j, t, g)]
                    for i in range(N_PLAYERS)
                    for j in range(i + 1, N_PLAYERS)) == 2
            )

    # COMPAGNI TOTALI
    comp = [[model.NewIntVar(0, n_turns, f"comp_{i}_{j}")
             for j in range(N_PLAYERS)]
            for i in range(N_PLAYERS)]

    for p1 in range(N_PLAYERS):
        for p2 in range(p1 + 1, N_PLAYERS):
            model.Add(
                comp[p1][p2] ==
                sum(pair[(p1, p2, t, g)]
                    for t in range(n_turns)
                    for g in range(N_GROUPS))
            )
            model.Add(comp[p2][p1] == comp[p1][p2])

    # STESSO GRUPPO
    same_group = {}
    for p1 in range(N_PLAYERS):
        for p2 in range(p1 + 1, N_PLAYERS):
            for t in range(n_turns):
                sg = model.NewBoolVar(f"same_group_{p1}_{p2}_t{t}")
                aux = []
                for g in range(N_GROUPS):
                    a = model.NewBoolVar(f"sg_aux_{p1}_{p2}_t{t}_g{g}")
                    model.Add(a <= x[p1, t, g])
                    model.Add(a <= x[p2, t, g])
                    model.Add(a >= x[p1, t, g] + x[p2, t, g] - 1)
                    aux.append(a)
                model.AddMaxEquality(sg, aux)
                same_group[(p1, p2, t)] = sg

    # COMPAGNI PER TURNO
    teammate_turn = {}
    for p1 in range(N_PLAYERS):
        for p2 in range(p1 + 1, N_PLAYERS):
            for t in range(n_turns):
                tt = model.NewBoolVar(f"tm_turn_{p1}_{p2}_t{t}")
                aux = []
                for g in range(N_GROUPS):
                    aux.append(pair[(p1, p2, t, g)])
                model.AddMaxEquality(tt, aux)
                teammate_turn[(p1, p2, t)] = tt

    # AVVERSARI PER TURNO
    opponent_turn = {}
    for p1 in range(N_PLAYERS):
        for p2 in range(p1 + 1, N_PLAYERS):
            for t in range(n_turns):
                opp_t = model.NewBoolVar(f"opp_turn_{p1}_{p2}_t{t}")
                sg = same_group[(p1, p2, t)]
                tt = teammate_turn[(p1, p2, t)]

                # avversari = stesso gruppo ma NON compagni
                model.AddBoolAnd([sg, tt.Not()]).OnlyEnforceIf(opp_t)
                model.AddBoolOr([sg.Not(), tt]).OnlyEnforceIf(opp_t.Not())

                opponent_turn[(p1, p2, t)] = opp_t

    # AVVERSARI TOTALI
    opp = [[model.NewIntVar(0, n_turns, f"opp_{i}_{j}")
            for j in range(N_PLAYERS)]
            for i in range(N_PLAYERS)]

    for p1 in range(N_PLAYERS):
        for p2 in range(p1 + 1, N_PLAYERS):
            model.Add(
                opp[p1][p2] ==
                sum(opponent_turn[(p1, p2, t)] for t in range(n_turns))
            )
            model.Add(opp[p2][p1] == opp[p1][p2])

    # DEVIAZIONE COMPAGNI
    dev_comp = {}
    for i in range(N_PLAYERS):
        for j in range(i + 1, N_PLAYERS):
            d = model.NewIntVar(0, n_turns, f"dev_comp_{i}_{j}")
            model.Add(d >= comp[i][j] - 1)
            model.Add(d >= 1 - comp[i][j])
            dev_comp[(i, j)] = d

    # PENALITÀ AVVERSARI RIPETUTI 3 VOLTE
    opp_dev = {}
    for i in range(N_PLAYERS):
        for j in range(i + 1, N_PLAYERS):
            d = model.NewIntVar(0, n_turns, f"opp_dev_{i}_{j}")
            model.Add(d >= opp[i][j] - 2)
            model.Add(d >= 0)
            opp_dev[(i, j)] = d

    # FUNZIONE OBIETTIVO STABILE
    model.Minimize(
        800 * sum(dev_comp[(i, j)] for i in range(N_PLAYERS) for j in range(i + 1, N_PLAYERS)) +
        150 * sum(opp_dev[(i, j)] for i in range(N_PLAYERS) for j in range(i + 1, N_PLAYERS)) +
        20  * sum(opp[i][j] for i in range(N_PLAYERS) for j in range(i + 1, N_PLAYERS))
    )

    return pair


def solve_draft12(names, num_turni: int = 8):
    if len(names) != N_PLAYERS:
        raise ValueError(f"Servono esattamente {N_PLAYERS} nomi.")

    model, x = build_model(num_turni)
    pair = add_constraints_stable(model, x, num_turni)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    solver.parameters.num_search_workers = 8

    result = solver.Solve(model)
    if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("Nessuna soluzione trovata.")

    rows = []
    for t in range(num_turni):
        for g in range(N_GROUPS):
            coppie = []

            for p1 in range(N_PLAYERS):
                for p2 in range(p1 + 1, N_PLAYERS):
                    if solver.Value(pair[(p1, p2, t, g)]) == 1:
                        coppie.append((p1, p2))

            if len(coppie) != 2:
                continue

            (a1, a2), (b1, b2) = coppie

            rows.append({
                "Turno": t + 1,
                "Campo": g + 1,
                "Coppia A": f"{names[a1]} & {names[a2]}",
                "Coppia B": f"{names[b1]} & {names[b2]}",
            })

    return pd.DataFrame(rows)
