import operator
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
    if len(res) == 1:
        if len(res[0]) == 0:
            res = []
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
    print(cnf)
    if len(cnf) == 0:  # nothing in list => satisfiable
        return "satisfiable"
    elif len(cnf) == 1:  # length is 1 & false clause => unsatisfiable
        tmp_lit = cnf[0]
        if '!' in tmp_lit[0]:
            literal = tmp_lit[0][1]
        else:
            literal = tmp_lit[0]
        if truth_table[literal] == 'false':
            return "unsatisfiable"
    # unit-propagation rule
    for clause in cnf:
        if len(clause) == 1:  # check if it is unit-clause
            unit_count += 1
            tmp = simplify(cnf, clause[0])
            return dpll(tmp)
    # splitting rule
    return splitting_rule(cnf)

if __name__ == "__main__":
    unit_count = 0
    splitting_count = 0
    f = open('input.txt', 'r')
    CNF = []
    literal_set = set()
    truth_table = {}
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
   
    dpll_result = dpll(CNF)
    print(dpll_result)
    if dpll_result == 'satisfiable':
        print(truth_table)
    print("Unit-propagation Rule count:", unit_count)
    print("Splitting-count Rule count:", splitting_count)
    f.close()