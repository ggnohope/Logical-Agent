from const import WUMPUS, STENCH, PIT, BREEZE
import copy
from collections import Counter
import itertools

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

        # at_least_one_wumpus = []
        # at_least_one_pit = []
        # for i in range(100):
        #     at_least_one_wumpus.append(WUMPUS + i)
        #     at_least_one_pit.append(PIT + i)
        # self.clauses.append(at_least_one_wumpus)
        # self.clauses.append(at_least_one_pit)

    def add_clause(self, clause):
        self.clauses.append(clause)

    def get_clauses(self):
        return copy.deepcopy(self.clauses)

    def print_clauses(self):
        for index, clause in enumerate(self.clauses, start=1):
            print(f"Clause {index}: ", end="")
            for literal in clause:
                if literal >= 0:
                    print(f"{literal} ", end="")
                elif literal < 0:
                    print(f"¬{-literal} ", end="")
            print()

# class Solver:
    
#     def __init__(self, clauses):
#         self.clauses = clauses
#         self.literals = self.get_unit_literals(self.clauses)
    
#     def get_unit_literals(self, clauses):
#         literals = []
#         for item in clauses:
#             for i in item:
#                 if i not in literals:
#                     literals.append(i)
#         return literals
    
#     def is_satisfiable(self):
#         return self.dpll(self.clauses, self.literals)
        
#     def dpll(self, clauses, literals):
#         self.unit_propagation(clauses, literals)
                
#         if [] in clauses:
#             return False
#         if not clauses:
#             return True
        
#         literals
#         most_common_literal = self.most_common(clauses)
#         clauses_neg = clauses
        
#         if most_common_literal in literals:
#             literals.remove(most_common_literal)
            
#         reduced_clauses_positive = self.reduced_clauses(clauses, most_common_literal)
#         reduced_clauses_negative = self.reduced_clauses(clauses_neg, -most_common_literal)
        
#         return self.dpll(reduced_clauses_positive, literals) or self.dpll(reduced_clauses_negative, literals)
    
#     def unit_propagation(self, clauses, literals):
#         remove_clause = []
#         changed = True
#         checked_literal = set()

#         while(changed):

#             changed = False

#             for clause in clauses:

#                 if len(clause) == 1 and clause[0] not in checked_literal:

#                     literal = clause[0]
#                     checked_literal.add(literal)
#                     literals.remove(literal)

#                     for clause in clauses:

#                         if literal in clause:
#                             remove_clause.append(clause)
#                             changed = True

#                         if -1*literal in clause:
#                             clause.remove(-1*literal) 
#                             changed = True

#                     for re_clause in remove_clause:

#                         clauses.remove(re_clause)
                        
#                     remove_clause = []
#                     break
    
#     def reduced_clauses(self, clauses, literal):
#         remove_list = []
        
#         for clause in clauses:
#             if literal in clause:
#                 remove_list.append(clause)
                
#         clauses = [x for x in clauses if x not in remove_list]
            
#         for clause in clauses:
#             if (literal * -1) in clause:
#                 clauses.remove(clause)
#                 clauses.append([x for x in clause if x != -literal])
                
#         return clauses
    
#     def most_common(self, clauses):
#         flat_lst = [item for sublist in clauses for item in sublist]

#         count_dict = Counter(flat_lst)

#         return count_dict.most_common(1)[0][0]
            
class SATSolver:
    def __init__(self, cnf):
        # extract unique clauses and literals
        self.clauses = self.extract_unique_clauses(cnf)
        # self.literals = self.extract_unique_literals(self.clauses)
    
    def solve(self):
        return self.dpll(self.clauses)
        
    def dpll(self, cnf):
        # unit propagation
        self.unit_propagation(cnf)
                
        # Check if the CNF is unsatisfiable
        if [] in cnf:
            return False
        # Check if the CNF is satisfiable
        if not cnf:
            return True
        
        # choose a literal and its negation
        most_common_literal = self.most_common(cnf)
            
        reduced_cnf_positive = self.reduced(cnf, most_common_literal)
        reduced_cnf_negative = self.reduced(cnf, -most_common_literal)
        
        # apply DPLL on the positive and negative branches
        return self.dpll(reduced_cnf_positive) or self.dpll(reduced_cnf_negative)
    
    def unit_propagation(self, cnf):
        remove_clause = []
        changed = True
        checked_literal = set()
        while(changed):
            changed = False
            for clause in cnf:
                if len(clause) == 1 and clause[0] not in checked_literal:
                    literal = clause[0]
                    checked_literal.add(literal)
                    for clause in cnf:
                        if literal in clause:
                            remove_clause.append(clause)
                            changed = True
                        if -1*literal in clause:
                            clause.remove(-1*literal) 
                            changed = True
                    for re_clause in remove_clause:
                        cnf.remove(re_clause)
                    remove_clause = []
                    break
    
    def reduced(self, cnf, reduced_clause):
        temp = []
        
        for clause in cnf:
            if reduced_clause in clause:
                temp.append(clause)
                
        if len(temp) > 0:
            cnf = [x for x in cnf if x not in temp]
            
        for clause in cnf:
            if (reduced_clause * -1) in clause:
                cnf.remove(clause)
                cnf.append([x for x in clause if x != -reduced_clause])
                
        return cnf
    
    def most_common(self, cnf):
        # find the most common literal in the CNF
        merged = list(itertools.chain(*cnf))
        if len(merged) > 0:
            return max(set(merged), key=merged.count)
        else:
            return None
    
    def extract_unique_clauses(self, cnf):
        # remove duplicate clauses from the input CNF
        unique_clauses = []
        for item in cnf:
            if item not in unique_clauses:
                unique_clauses.append(list(item))
        return unique_clauses
    
    def extract_unique_literals(self, clauses):
        # extract unique literals from the clauses
        literals = []
        for item in clauses:
            for i in item:
                if i not in literals:
                    literals.append(i)
        return literals