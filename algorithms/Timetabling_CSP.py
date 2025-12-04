# Timetabling as a Constraint Satisfaction Problem (CSP)

from collections import defaultdict

def get_initial_domains(variables, domain):
    """Initialize domains for each variable."""
    return {var: domain[:] for var in variables}

def count_constraints(var, value, assignment, constraints, domains):
    """Count how many future variables would lose the given value due to constraints."""
    count = 0
    for v1, v2 in constraints:
        if v1 == var and v2 not in assignment:
            if value in domains[v2]:
                count += 1
        elif v2 == var and v1 not in assignment:
            if value in domains[v1]:
                count += 1
    return count

def select_unassigned_variable(assignment, domains):
    """Select unassigned variable with Minimum Remaining Values (MRV) heuristic."""
    unassigned = [var for var in domains if var not in assignment]
    if not unassigned:
        return None
    return min(unassigned, key=lambda var: len(domains[var]))

def order_domain_values(var, domains, constraints, assignment):
    """Order values by Least Constraining Value (LCV) heuristic."""
    return sorted(domains[var], key=lambda val: count_constraints(var, val, assignment, constraints, domains))

def is_consistent(var, value, assignment, constraints):
    """Check if assigning var = value is consistent with current assignment."""
    for v1, v2 in constraints:
        if v1 == var and v2 in assignment and assignment[v2] == value:
            return False
        elif v2 == var and v1 in assignment and assignment[v1] == value:
            return False
    return True

def forward_check(var, value, domains, constraints, assignment):
    """Apply forward checking to reduce domains of unassigned variables."""
    reduced_domains = defaultdict(list)
    for v1, v2 in constraints:
        if v1 == var and v2 not in assignment and value in domains[v2]:
            domains[v2].remove(value)
            reduced_domains[v2].append(value)
        elif v2 == var and v1 not in assignment and value in domains[v1]:
            domains[v1].remove(value)
            reduced_domains[v1].append(value)
    return reduced_domains

def restore_domains(reduced_domains, domains):
    """Restore domains after backtracking."""
    for var, values in reduced_domains.items():
        domains[var].extend(values)

def backtracking_search(variables, domains, constraints, assignment):
    """Perform backtracking search with MRV, LCV, and forward checking."""
    if len(assignment) == len(variables):
        return assignment
    
    var = select_unassigned_variable(assignment, domains)
    if var is None:
        return None
    
    for value in order_domain_values(var, domains, constraints, assignment):
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            saved_domains = forward_check(var, value, domains, constraints, assignment)
            
            if not any(len(domains[v]) == 0 for v in domains if v not in assignment):
                assignment.pop(var)
                restore_domains(saved_domains, domains)
                continue
            
            result = backtracking_search(variables, domains, constraints, assignment)
            if result is not None:
                return result
            
            assignment.pop(var)
            restore_domains(saved_domains, domains)
    
    return None

def solve_timetabling(variables, timeslots, constraints):
    """Solve the timetabling problem as a CSP."""
    domains = get_initial_domains(variables, timeslots)
    assignment = {}
    return backtracking_search(variables, domains, constraints, assignment)

# Example usage
variables = ['C1', 'C2', 'C3', 'C4']
timeslots = ['T1', 'T2', 'T3', 'T4']
constraints = [('C1', 'C2'), ('C3', 'C4')]

solution = solve_timetabling(variables, timeslots, constraints)

if solution:
    print("Timetable solution found:")
    for course, timeslot in solution.items():
        print(f"{course}: {timeslot}")
else:
    print("No solution found.")