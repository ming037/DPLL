import string
import random
import matplotlib.pyplot as plt

def simplify(cnf, literal):
    res = []
    if literal[0] == '!':
        compare_lit = literal[1]
    else:
        compare_lit = '!'+literal
    for clause in cnf:
        if compare_lit in clause:  # if opposite literal in clause, remove just literal
            tmp = []
            for lit in clause:
                if lit != compare_lit:
                    tmp.append(lit)
            res.append(tmp)
        elif literal not in clause:  # if literal in clause, remove clause
            res.append(clause)
    return res

def splitting_rule(cnf):
    global splitting_count
    global truth_table
    splitting_count += 1
    # Select V witch has not been assigned
    for literal in truth_table:
        if truth_table[literal] == 0:  # if not assigned
            save_table = {}
            for k in truth_table:
                save_table[k] = truth_table[k]
            truth_table[literal] = 'false'
            tmp = dpll(simplify(cnf, '!'+literal))
            if tmp == 'satisfiable':
                return 'satisfiable'
            else:
                truth_table = save_table
                truth_table[literal] = 'true'
                tmp2 = dpll(simplify(cnf, literal))
                return tmp2

def dpll(cnf):
    global truth_table
    global unit_count
    global dpll_calls

    dpll_calls += 1
    # satisfiable check
    if len(cnf) == 0:  # nothing in list => satisfiable
        return "satisfiable"
    if [] in cnf:
        return "unsatisfiable"

    # unit-propagation rule
    for clause in cnf:
        if len(clause) == 1:  # check if it is unit-clause
            unit_count += 1
            if clause[0][0] == '!':
                truth_table[clause[0][1]] = 'false'
            else:
                truth_table[clause[0]] = 'true'
            tmp = simplify(cnf, clause[0])
            return dpll(tmp)
    # splitting rule
    return splitting_rule(cnf)


def random_cnf(k, m, n, w):
    global CNF
    global truth_table
    global literal_set
    #  select k liternals from m symbols, generate n clause
    #  Each clause has independent symbol ex)[[A, !A], [B], [D]] is wrong case
    #  Each Sentence has independent clause ex)[[A,C], [A,C], [!B]] is wrong case
    CNF = []
    posneg = ['', '!']
    symbols =[]
    if w != 'n':
        f = open("random.txt", 'w')
    file_CNF = []
    for c in string.ascii_uppercase:
        symbols.append(c)
    for c in string.ascii_lowercase:
        symbols.append(c)
    symbols = symbols[:n]

    while len(CNF) != m:
        tmp_clause = []
        file_clause =""
        while len(tmp_clause) != k:
            lit = random.choice(symbols)
            if lit not in tmp_clause and '!'+lit not in tmp_clause:
                truth_table[lit] = 0
                ran_lit = random.choice(posneg) + lit
                tmp_clause.append(ran_lit)
                file_clause += (ran_lit+' ')
                tmp_clause = sorted(tmp_clause)
        if tmp_clause not in CNF:
            CNF.append(tmp_clause)
            file_CNF.append(file_clause)
    if w != 'n':
        f.write('\n'.join(file_CNF))
        f.close()

if __name__ == "__main__":
    unit_count = 0
    splitting_count = 0
    dpll_calls = 0
    CNF = []
    literal_set = set()
    truth_table = {}
    order = input("Choose F(file) or R(random) of G(graph):")
    select = ""

    if order == "F":
        f = open('input.txt', 'r')
        clause = f.readline()
        while clause:
            tmp = clause.rstrip().split(' ')
            for c in tmp:
                if c[0] == '!':
                    literal_set.add(c[1])
                else:
                    literal_set.add(c)
            CNF.append(tmp)
            clause = f.readline()
        for literal in literal_set:
            truth_table[literal] = 0
        f.close()
    elif order == 'R':
        k = input("k:")
        m = input("m:")
        n = input("n:")
        random_cnf(int(k), int(m), int(n), 'y')  # k m n

    else:  # in case G
        k = 3
        n = 26
        xpoints = []
        ypoints = []
        for m in range(1, 400, 2):  # m continuously grow
            x_ratio = m/n  # x axis
            dpll_calls = 0  # y axis
            CNF = []
            random_cnf(k, m, n, 'n')
            dpll(CNF)
            xpoints.append(x_ratio)
            ypoints.append(dpll_calls)

        plt.plot(xpoints, ypoints)
        plt.ylim([0, 1000])
        plt.xlim([0, 15])
        plt.title('DPLL time estimation')
        plt.xlabel('Clause/symbol ratio m/n')
        plt.ylabel('Runtime (number of DPLL calls)')
        plt.grid(True)
        plt.show()

    if order == 'F' or order == 'R':
        dpll_result = dpll(CNF)
        print(dpll_result)
        if dpll_result == 'satisfiable':
            truth_table = sorted(truth_table.items())
            for truth in truth_table:
                if truth[1] != 0:
                    print(truth[0], "=", truth[1])
        print("Unit propagation Rule count:", unit_count)
        print("Splitting Rule count:", splitting_count)


