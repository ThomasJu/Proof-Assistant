class Prover():
    def __init__(self, envs):
        self.lookup, self.functions, self.lengths = {}, {}, set()
        
        def putindict(a, b, d):
            if a in d.keys():
                d[a].append(b)
            else:
                d[a] = [b]
            return d
        
        for env in envs:
            left, right = tuple(env[:env.find('=')].split()), tuple(env[env.find('=')+1:].split())
            self.lengths.add(len(left))
            self.lengths.add(len(right))
            if '_' not in env:       # statement
                self.lookup = putindict(left, right, self.lookup)
                self.lookup = putindict(right, left, self.lookup)
            else:                     # function
                self.functions = putindict(left, right, self.functions)
                self.functions = putindict(right, left, self.functions)  
                      
        # print(self.lookup)
        # print(self.functions)
        # print(self.lengths)
        # print('')
        
    def lookupSwap(self, s):
        if s in self.lookup.keys():
            return self.lookup[s]
        
        for old, new in self.functions.items():
            match = True
            vardict = {}
            if len(old) != len(s):
                continue
            
            for A, B in zip(old, s):
                if '_' in A and A not in vardict.keys():
                    vardict[A] = B
                if not(('_' in A and A in vardict.keys() and B == vardict[A]) or (A == B)):
                    match = False
                    break
                
            if match:
                for i, candidate in enumerate(new):
                    c = list(candidate)
                    for j, elt in enumerate(candidate):
                        if '_' in elt:
                            c[j] = vardict[elt]
                    new[i] = tuple(c)
                return new
        return None

    def prove(self, statement):
        left, right = tuple(statement[:statement.find('=')].split()), tuple(statement[statement.find('=')+1:].split())
        queue = [(left, [left])]
        checked = set()

        while len(queue)!=0 and queue[0][0] != right:
            current, trace, queue = queue[0][0], queue[0][1], queue[1:]
            
            indices = [i for i, e in enumerate(current) if e == ')'][::-1]
            for i, piece in enumerate(current):
                if piece[-1] == '(':
                    possibles = self.lookupSwap(current[i:indices[0]+1])
                    if possibles == None:
                        continue
                    for possible in possibles:
                        possible = tuple(list(current[:i]) + list(possible) + list(current[indices[0]+1:]))
                        if possible not in checked and len(possible) < 30:
                            queue.append((possible, trace+[possible]))
                    indices = indices[1:]
                    
                elif piece != ',' and piece !=')':
                    possibles = self.lookupSwap(tuple([current[i]]))
                    if possibles == None:
                        continue
                    for possible in possibles:
                        possible = tuple(list(current[:i]) + list(possible) + list(current[i+1:]))
                        if possible not in checked and len(possible) < 30:
                            queue.append((possible, trace+[possible]))
        
                checked.add(current)
                
        if len(queue) != 0:
            return True, queue[0][1]
        else:
            return False, None
    
    def format_proof(trace):
        return '  ' + '\n'.join(['= '+' '.join(t) for t in trace])[2:]
        

def main():
    p1 = Prover(['Next( "1" ) = "2"', 'Next( "0" ) = "1"', 'Add( _x_ , "0" ) = _x_'\
                , 'Add( _x_ , Next( _y_ ) ) = Next( Add( _x_ , _y_ ) )'])
    solution, trace = p1.prove('Add( "1" , "1" ) = "2"')
    if solution:
        print(Prover.format_proof(trace))
    else:
        print("This equation can't be prove")

if __name__ == "__main__":
    main()