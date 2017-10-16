import string
import random
def simplify(cnf, literal):
    global truth_table
    res = []
    if literal[0] == '!':
        compare_lit = literal[1]
        truth_table[compare_lit] = 'false'
    else:
        truth_table[literal] = 'true'
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
            tmp = dpll(simplify(cnf, '!'+literal))
            if tmp == 'satisfiable':
                return 'satisfiable'
            else:
                truth_table[literal] = 0
                return dpll(simplify(cnf, literal))

def dpll(cnf):
    global truth_table
    global unit_count
    # satisfiable check
    #print(cnf)
    if len(cnf) == 0:  # nothing in list => satisfiable
        return "satisfiable"
    elif len(cnf) == 1:  # length is 1 & false clause => unsatisfiable
        if len(cnf[0]) == 0:
            return "unsatisfiable"
    # unit-propagation rule
    for clause in cnf:
        if len(clause) == 1:  # check if it is unit-clause
            unit_count += 1
            tmp = simplify(cnf, clause[0])
            return dpll(tmp)
    # splitting rule
    return splitting_rule(cnf)


def random_cnf(k, m, n):
    global CNF
    global truth_table
    global literal_set
    #  select k liternals from m symbols, generate n clause
    #  Each clause has independent symbol ex)[[A, !A], [B], [D]] is wrong case
    #  Each Sentence has independent clause ex)[[A,C], [A,C], [!B]] is wrong case
    CNF = []
    posneg = ['', '!']
    symbols =[]
    for c in string.ascii_uppercase:
        symbols.append(c)
    for c in string.ascii_lowercase:
        symbols.append(c)
    symbols = symbols[:n]

    while len(CNF) != m:
        tmp_clause = []
        while len(tmp_clause) != k:
            lit = random.choice(symbols)
            if lit not in tmp_clause and '!'+lit not in tmp_clause:
                truth_table[lit] = 0
                tmp_clause.append(random.choice(posneg) + lit)
        if tmp_clause not in CNF:
            CNF.append(tmp_clause)
    print(CNF)


if __name__ == "__main__":
    unit_count = 0
    splitting_count = 0
    CNF = []
    literal_set = set()
    truth_table = {}

    order = input("Choose T(text) or R(random):")

    if order == "T":
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
    else:
        random_cnf(3, 10, 50)

    dpll_result = dpll(CNF)
    print(dpll_result)

    if dpll_result == 'satisfiable':
        truth_table = sorted(truth_table.items())
        for truth in truth_table:
            if truth[1] != 0:
                print(truth[0], "=", truth[1])
    print("Unit propagation Rule count:", unit_count)
    print("Splitting Rule count:", splitting_count)


