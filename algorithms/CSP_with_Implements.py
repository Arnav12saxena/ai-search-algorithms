# Timetabling as a CSP with MRV, Degree, LCV, Forward Checking, and Arc Consistency

from collections import defaultdict, deque
import random

def get_initial_domains(variables, domain):
    """Initialize domains for each variable."""
    return {var: domain[:] for var in variables}

def get_degree(var, constraints, assignment):
    """Calculate the number of constraints involving var with unassigned variables."""
    return sum(1 for v1, v2 in constraints if v1 == var and v2 not in assignment or v2 == var and v1 not in assignment)

def select_unassigned_variable(assignment, domains, constraints):
    """
    Select unassigned variable using MRV and Degree heuristic for tie-breaking.
    
    Args:
    - assignment: current partial assignment
    - domains: dict of variables to their current domains
    - constraints: list of (var1, var2) constraint pairs
    
    Returns:
    - selected variable or None
    """
    unassigned = [var for var in domains if var not in assignment]
    if not unassigned:
        return None
    
    # MRV: select variable with fewest remaining values
    min_values = min(len(domains[var]) for var in unassigned)
    candidates = [var for var in unassigned if len(domains[var]) == min_values]
    
    # Degree heuristic: break ties by choosing variable with most constraints
    return max(candidates, key=lambda var: get_degree(var, constraints, assignment))

def count_constraints(var, value, assignment, domains, constraints):
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

def order_domain_values(var, domains, constraints, assignment):
    """
    Order domain values using Least Constraining Value (LCV) heuristic.
    
    Args:
    - var: variable to assign
    - domains: current domains
    - constraints: list of constraint pairs
    - assignment: current partial assignment
    
    Returns:
    - sorted list of domain values
    """
    return sorted(domains[var], key=lambda val: count_constraints(var, val, assignment, domains, constraints))

def is_consistent(var, value, assignment, constraints):
    """Check if assigning value to var is consistent with current assignment."""
    for v1, v2 in constraints:
        if v1 == var and v2 in assignment:
            if assignment[v2] == value:
                return False
        elif v2 == var and v1 in assignment:
            if assignment[v1] == value:
                return False
    return True

def forward_check(var, value, domains, constraints, assignment):
    """
    Apply forward checking to reduce domains of unassigned variables.
    
    Args:
    - var: assigned variable
    - value: assigned value
    - domains: current domains
    - constraints: list of constraint pairs
    - assignment: current partial assignment
    
    Returns:
    - dict of reduced domains {var: [removed_values]} or None if failure
    """
    reduced_domains = defaultdict(list)
    for v1, v2 in constraints:
        if v1 == var and v2 not in assignment and value in domains[v2]:
            domains[v2].remove(value)
            reduced_domains[v2].append(value)
        elif v2 == var and v1 not in assignment and value in domains[v1]:
            domains[v1].remove(value)
            reduced_domains[v1].append(value)
    
    # Check if any domain became empty
    if any(len(domains[v]) == 0 for v in domains if v not in assignment):
        return None
    
    return reduced_domains

def restore_domains(reduced_domains, domains):
    """Restore domains after backtracking."""
    for var, values in reduced_domains.items():
        domains[var].extend(values)

def ac3(domains, constraints, assignment):
    """
    Enforce arc consistency using AC-3 algorithm.
    
    Args:
    - domains: current domains
    - constraints: list of constraint pairs
    - assignment: current partial assignment
    
    Returns:
    - bool: True if arc-consistent, False if a domain is empty
    """
    queue = deque([(v1, v2) for v1, v2 in constraints if v1 not in assignment and v2 not in assignment])
    while queue:
        v1, v2 = queue.popleft()
        removed = False
        
        # Check each value in v1's domain
        values_to_remove = []
        for x in domains[v1]:
            consistent = False
            for y in domains[v2]:  # Satisfies constraint (v1 != v2)
                if x != y:
                    consistent = True
                    break
            if not consistent:
                values_to_remove.append(x)
                removed = True
        
        for x in values_to_remove:
            domains[v1].remove(x)
        
        if not domains[v1]:
            return False
        
        if removed:
            # Add constraints involving v1 to queue
            for u, v in constraints:
                if u == v2 and v != v1 and u not in assignment:
                    queue.append((u, v))
                elif v == v2 and u != v1 and u not in assignment:
                    queue.append((u, v))
    
    return True

def backtracking_search(variables, domains, constraints, assignment):
    """
    Perform backtracking search with MRV, Degree, LCV, Forward Checking, and AC-3.
    
    Args:
    - variables: list of courses
    - domains: dict mapping courses to possible timeslots
    - constraints: list of (course1, course2) pairs
    - assignment: current partial assignment
    
    Returns:
    - dict: complete assignment if solution found, else None
    """
    if len(assignment) == len(variables):
        return assignment
    
    var = select_unassigned_variable(assignment, domains, constraints)
    if var is None:
        return None
    
    # Create a copy of domains for this recursion level
    domains_copy = {v: d[:] for v, d in domains.items()}
    
    for value in order_domain_values(var, domains_copy, constraints, assignment):
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            reduced_domains = forward_check(var, value, domains_copy, constraints, assignment)
            
            if reduced_domains is not None:
                # Apply AC-3 after forward checking
                if not ac3(domains_copy, constraints, assignment):
                    assignment.pop(var)
                    restore_domains(reduced_domains, domains_copy)
                    continue
                
                result = backtracking_search(variables, domains_copy, constraints, assignment)
                if result is not None:
                    return result
            
            assignment.pop(var)
            restore_domains(reduced_domains, domains_copy)
    
    return None

def solve_timetabling(variables, timeslots, constraints):
    """
    Solve the timetabling problem as a CSP.
    
    Args:
    - variables: list of courses
    - timeslots: list of available timeslots
    - constraints: list of (course1, course2) pairs
    
    Returns:
    - dict: assignment of courses to timeslots if solution found, else None
    """
    domains = get_initial_domains(variables, timeslots)
    # Use AC-3 initially to prune domains
    assignment = {}
    if not ac3(domains, constraints, assignment):
        return None
    return backtracking_search(variables, domains, constraints, assignment)

# Example usage
variables = ['C1', 'C2', 'C3', 'C4', 'C5']  # Courses
timeslots = ['T1', 'T2', 'T3', 'T4']  # Timeslots
constraints = [('C1', 'C2'), ('C1', 'C3'), ('C3', 'C4'), ('C4', 'C5')]  # Constraints

solution = solve_timetabling(variables, timeslots, constraints)

if solution:
    print("Timetable solution found:")
    for course, timeslot in solution.items():
        print(f"{course}: {timeslot}")
else:
    print("No solution found.")