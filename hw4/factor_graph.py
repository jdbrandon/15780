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
    print "pre",d
    d.pop(vout)
    print "pos",d
    f2 = Factor(d)
    for ass in f1.inputs():
        f2[ass] += f1[ass]
    return f2
        
def marginal_inference(factors, variables, elim_order=None):
    facs = []
    if elim_order:
        for v in elim_order:
            f1 = None
            prod = []
            for fac in factors:
                if v in fac.variables:
                    prod.append(fac)
            if prod:
                if not f1:
                    f1 = prod.pop(0)
                while prod:
                    f1 = factor_product(f1, prod.pop(0))
                f1 = factor_sum(f1, v)
                facs.append(f1)
        f1 = None
        if facs:
            if not f1:
                f1 = facs.pop(0)
            while facs:
                f1 = factor_product(f1, facs.pop(0))
    return f1
