from const import WUMPUS, STENCH, PIT, BREEZE
import copy

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
            
class SATSolver:
    def __init__(self, cnf):
        self.clauses = cnf
        self.correct_clause = [] 

    def solve(self):
        assignment = {}
        a = self.dpll(assignment)
        print(a)
        return a

    def dpll(self, assignment):
        # Unit propagation
        while True:
            unit_clause = self.get_unit_clause()
            if unit_clause is None:
                break
            literal = unit_clause[0]
            if self.conflict(literal):
                return False
            assignment[abs(literal)] = literal > 0
            self.simplify_cnf(literal)

        if [] in self.clauses:
            return False

        # Check if all clauses are satisfied
        if not self.clauses:
            return True

        literal = self.choose_literal(assignment)
        if literal is not None:
            # Explore with literal=True
            copy_clauses = copy.deepcopy(self.clauses)
            assignment[abs(literal)] = True
            self.simplify_cnf(abs(literal))
            if self.dpll(assignment):
                return True

            # If not successful, backtrack
            self.clauses = copy_clauses
            del assignment[abs(literal)]
            self.undo_simplify_cnf()

            # Explore with literal=False
            copy_clauses = copy.deepcopy(self.clauses)
            assignment[abs(literal)] = False
            self.simplify_cnf(-abs(literal))
            if self.dpll(assignment):
                return True

            # If not successful, backtrack
            self.clauses = copy_clauses
            del assignment[abs(literal)]
            self.undo_simplify_cnf()

        return False

    def get_unit_clause(self):
        for clause in self.clauses:
            if len(clause) == 1:
                return clause
        return None
    
    def conflict(self, literal):
        for clause in self.clauses:
            if len(clause) == 1 and clause[0] == -literal:
                return True
        return False

    def simplify_cnf(self, literal):
        self.clauses = [clause for clause in self.clauses if literal not in clause]

    def undo_simplify_cnf(self):
        pass

    def choose_literal(self, assignment):
        for clause in self.clauses:
            for literal in clause:
                if abs(literal) not in assignment:
                    return literal
        return None