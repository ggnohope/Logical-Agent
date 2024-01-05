from const import WUMPUS, STENCH, PIT, BREEZE
import copy
from collections import Counter

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

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

class Solver:
    
    def __init__(self, clauses):
        self.clauses = clauses
        self.literals = self.get_unit_literals(self.clauses)
    
    def get_unit_literals(self, clauses):
        literals = []
        for item in clauses:
            for i in item:
                if i not in literals:
                    literals.append(i)
        return literals
    
    def is_satisfiable(self):
        return self.dpll(self.clauses, self.literals)
        
    def dpll(self, clauses, literals):
        self.unit_propagation(clauses, literals)
                
        if [] in clauses:
            return False
        if not clauses:
            return True
        
        literals
        most_common_literal = self.most_common(clauses)
        clauses_neg = clauses
        
        if most_common_literal in literals:
            literals.remove(most_common_literal)
            
        reduced_clauses_positive = self.reduced_clauses(clauses, most_common_literal)
        reduced_clauses_negative = self.reduced_clauses(clauses_neg, -most_common_literal)
        
        return self.dpll(reduced_clauses_positive, literals) or self.dpll(reduced_clauses_negative, literals)
    
    def unit_propagation(self, clauses, literals):
        remove_clause = []
        is_changed = True
        checked_literal = set()

        while(is_changed):

            is_changed = False

            for clause in clauses:

                if len(clause) == 1 and clause[0] not in checked_literal:

                    literal = clause[0]
                    checked_literal.add(literal)
                    literals.remove(literal)

                    for clause in clauses:

                        if literal in clause:
                            remove_clause.append(clause)
                            is_changed = True

                        if -1*literal in clause:
                            clause.remove(-1*literal) 
                            is_changed = True

                    for re_clause in remove_clause:

                        clauses.remove(re_clause)
                        
                    remove_clause = []
                    break
    
    def reduced_clauses(self, clauses, literal):
        clauses = [clause for clause in clauses if literal not in clause]
            
        for clause in clauses:
            if (literal * -1) in clause:
                clauses.remove(clause)
                clauses.append([x for x in clause if x != -literal])
                
        return clauses
    
    def most_common(self, clauses):
        flat_lst = [item for sublist in clauses for item in sublist]

        count_dict = Counter(flat_lst)

        return count_dict.most_common(1)[0][0]

# class Solver:
#     def __init__(self, cnf):
#         self.clauses = cnf

#     def is_satisfiable(self):
#         assignment = {}
#         return self.dpll(assignment)

#     def dpll(self, assignment):
#         # Unit propagation
#         while True:
#             unit_clause = self.get_unit_clause()
#             print(f"Unit clause: {unit_clause}")
#             if unit_clause is None:
#                 break
#             literal = unit_clause[0]
#             print(f"Unit propagation: {literal}")
#             assignment[abs(literal)] = literal > 0
#             self.simplify_cnf(literal)

#         # Check if all clauses are satisfied
#         if not self.clauses:
#             return True

#         literal = self.choose_literal(assignment)
#         if literal is not None:
#             # Explore with literal=True
#             assignment[abs(literal)] = True
#             if self.dpll(assignment):
#                 return True

#             # If not successful, backtrack
#             del assignment[abs(literal)]
#             self.undo_simplify_cnf()

#             # Explore with literal=False
#             assignment[abs(literal)] = False
#             if self.dpll(assignment):
#                 return True

#             # If not successful, backtrack
#             del assignment[abs(literal)]
#             self.undo_simplify_cnf()

#         return False

#     def get_unit_clause(self):
#         for clause in self.clauses:
#             if len(clause) == 1:
#                 return clause
#         return None

#     def simplify_cnf(self, literal):
#         self.clauses = [clause for clause in self.clauses if literal not in clause]
#         self.clauses = [clause for clause in self.clauses if -literal not in clause]

#     def undo_simplify_cnf(self):
#         pass

#     def choose_literal(self, assignment):
#         for clause in self.clauses:
#             for literal in clause:
#                 if abs(literal) not in assignment:
#                     return literal
#         return None