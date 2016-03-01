import itertools
import copy as cp

class Factor:
    def __init__(self, variables, default=0):
        self.variables = variables
        keys = [tuple(sorted(zip(self.variables.keys(),r)))
                for r in itertools.product(*self.variables.values())];
        self.f = dict(zip(keys, [default]*len(keys)))

    def __getitem__(self,e):
        return self.f[tuple(sorted(self._filter_inputs(e).items()))]

    def __setitem__(self,e,x):
        k = tuple(sorted(self._filter_inputs(e).items()));
        if (k in self.f):
            self.f[k] = x;
        else:
            raise KeyError(e)

    def _filter_inputs(self,e):
        return dict([(k,v) for k,v in e.items() if k in self.variables])

    def inputs(self):
        return [dict(a) for a in self.f.keys()];

    def values(self):
        return [a for a in self.f.values()];


# functions to implment below

def factor_product(f1,f2):
    d = cp.deepcopy(f1.variables)
    d.update(f2.variables)
    f = Factor(d)
    for ass in f.inputs():
        f[ass] = f1[ass]*f2[ass]
    return f

def factor_sum(f1,vout):
    d= cp.deepcopy(f1.variables)
    d.pop(vout)
    f2 = Factor(d)
    for ass in f1.inputs():
        f2[ass] += f1[ass]
    return f2
        
def marginal_inference(factors, variables, elim_order=None):
    f1 = cp.deepcopy(factors)
    f = None
    if elim_order:
        for v in elim_order:
            prod = [i for i in f1 if v in i.variables]
            f1 = [i for i in f1 if v not in i.variables]
            p = list_fac_prod(prod)
            p = factor_sum(p, v)
            f1.append(p)
        f = list_fac_prod(f1)
    return f

def list_fac_prod(l):
    p = None
    while l:
        if not p:
            p = l.pop(0)
            continue
        p = factor_product(p, l.pop(0))
        normalize(p)
    return p

def normalize(p):
    s = 0
    for v in p.values():
        s+=v
    for v in p.inputs():
        p[v]/=s
    return p
