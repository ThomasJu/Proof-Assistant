import itertools
import copy
def elts_sets_parser(statements):
    vars = {}
    all_possible_elts = [' True ', ' False ']
    all_possible_sets = [' {True, False} ', ' {False} ', ' {True} ', ' {} ']
    
    for candidate in (' '.join(statements)).split():
        if candidate.isalpha() and len(candidate) == 1:
            if candidate.islower():
                vars[candidate] = all_possible_elts
            else:
                vars[candidate] = all_possible_sets
    return vars

def statements_resemble(statements):
    new_statements = []
    for statement in statements:
        statement = statement.replace('∧', 'and')
        statement = statement.replace('V', 'or')
        statement = statement.replace('∈', 'in')
        statement = statement.replace('=', '==')
        statement = statement.replace('⇔', '==')
        statement = statement.replace('¬', 'not')
        
        if 'suppose' in statement:
            statement = statement.replace('suppose', ' ')
        
        while '⇒' in statement:
            left_s, right_s = statement[:statement.find('⇒')], statement[statement.find('⇒')+1:]
            left_s = left_s[left_s.rfind('('):left_s.rfind(')')+1]
            right_s = right_s[right_s.find('('): right_s.find(')')+1]
            new_s = ' ( ( not' + left_s + ' ) or ' + right_s + ' ) '
            statement = statement.replace(left_s+' ⇒ '+right_s, new_s)
            
        while '∃' in statement:
            placeholder = ' ' + statement[statement.find('∃')+2] + ' '
            statement = statement[:statement.find('∃')] + ' ' + statement[statement.find('∃')+3:]
            statement = '( ' + statement.replace(placeholder, ' True ') + ' ) or ( ' +  statement.replace(placeholder, ' False ') + ' )'
            
        while '∀' in statement:
            placeholder = ' ' + statement[statement.find('∀')+2] + ' '
            statement = statement[:statement.find('∀')] + ' ' + statement[statement.find('∀')+3:]
            statement = '( ' + statement.replace(placeholder, ' True ') + ' ) and ( ' +  statement.replace(placeholder, ' False ') + ' )'
        
        # print(statement)
        new_statements.append(statement)

    return new_statements

def eval_problem(env, statements, is_true):
    # deal with suppose
    env += [statement for statement in statements if 'suppose' in statement]
    statements = [statement for statement in statements if 'suppose' not in statement]
    
    env = statements_resemble(env)
    statements = statements_resemble(statements)
    
    if is_true == False:
        statements = [' not ( ' + s + ' ) ' for s in statements]

    statements = env + statements
    vars = elts_sets_parser(statements)
    k = [' '+name+' ' for name in vars.keys()]
    statements_s = '( ' + ' ) and ( '.join(statements) + ' )'

    print(statements_s)
    for pair in itertools.product(*vars.values()):
        query = copy.deepcopy(statements_s)
        # print(pair)
        # print(query)
        for name, boolvalues in zip(k, pair):
            query = query.replace(name, boolvalues)
        # print('')
        if eval(query):
            return True
    
    return False
    

class Prover():
    def __init__(self, env):
        self.env = env
    def prove(self, statements:list):
        is_true = eval_problem(self.env, statements, True)
        is_false = eval_problem(self.env, statements, False)
        
        if is_true and is_false:
            return 'Unknown'
        elif (not is_true) and (not is_false):
            return 'Contradiction'
        else:
            return is_true
        
def main():
    p1 = Prover(['a ∈ B'])
    print(p1.prove(['∃ x  x ∈ B']), end='\n\n')
    
    p2 = Prover(['a ∧ b'])
    print(p2.prove(['b ∧ a']), end='\n\n')
    
    p3 = Prover(['∀ x  ( x ∈ A ) ⇒ ( x ∈ B )'])
    print(p3.prove(['suppose c ∈ A', 'c ∈ B']), end='\n\n')
    
    p4 = Prover(['a ∧ b', 'a '])
    print(p4.prove(['b ∧ a']))
    print(p4.prove(['¬ b ∧ a']), end='\n\n')
    
    p5 = Prover(['a ∧ b', ' not ( a ∧ b )'])
    print(p5.prove(['b ∧ a']), end='\n\n')
    
    p6 = Prover(['a = b', 'a ∧ c'])
    print(p6.prove(['b ∧ c']), end='\n\n')
    
    p7 = Prover(['a ∧ b', '¬ b ∧ ¬a'])
    print(p7.prove(['a']), end='\n\n')
    

if __name__ == "__main__":
    main()
