import xml.etree.ElementTree as ET
import factor_graph
from factor_graph import Factor

def load_xmlbif(filename):
    root = ET.parse(filename).getroot()
    vars = {};
    for var in root.iter('VARIABLE'):
        vars[var.find('NAME').text] = [n.text for n in var.iter('OUTCOME')]
    factors = []
    for factor in root.iter('DEFINITION'):
        child = factor.find('FOR').text
        parents = [n.text for n in factor.iter('GIVEN')]
        f = Factor(dict([(v,vars[v]) for v in [child]+parents]))
        if parents == []:
            for v,x in zip(vars[child],factor.find('TABLE').text.split(" ")):
                f[{child:v}] = float(x);
        else:
            for entry in factor.iter('ENTRY'):
                pvals = zip(parents,[n.text for n in entry.iter('CATEGORY')])
                for v,x in zip(vars[child],entry.find('LIST').text.split(" ")):
                    f[dict(pvals + [(child,v)])] = float(x);
        factors.append(f)
    return (vars,factors)


# test simple case
f1 = Factor({"x1":[0,1], "x2":[0,1]})
f2 = Factor({"x2":[0,1], "x3":[0,1]})
f1[{"x1":0, "x2":0}] = 1
f1[{"x1":0, "x2":1}] = 0.1
f1[{"x1":1, "x2":0}] = 0.1
f1[{"x1":1, "x2":1}] = 2

f2[{"x2":0, "x3":0}] = 0.1
f2[{"x2":0, "x3":1}] = 1
f2[{"x2":1, "x3":0}] = 2
f2[{"x2":1, "x3":1}] = 0.1

print "Test case 1"
f = factor_graph.marginal_inference([f1,f2], ["x1","x3"], ["x2"])
if f:
    for e in f.inputs():
        print str(e) + " = " + str(f[e])
# should output:
# {'x3': 0, 'x1': 1} = 0.713523131673
# {'x3': 1, 'x1': 0} = 0.179715302491
# {'x3': 0, 'x1': 0} = 0.0533807829181
# {'x3': 1, 'x1': 1} = 0.0533807829181

f1 = Factor({"x1":[0,1], "x2":[0,1]})
f2 = Factor({"x2":[0,1], "x3":[0,1]})
f1[{"x1":0, "x2":0}] = 1
f1[{"x1":0, "x2":1}] = 0.1
f1[{"x1":1, "x2":0}] = 0.1
f1[{"x1":1, "x2":1}] = 2

f2[{"x2":0, "x3":0}] = 0.1
f2[{"x2":0, "x3":1}] = 1
f2[{"x2":1, "x3":0}] = 2
f2[{"x2":1, "x3":1}] = 0.1

print "Test case 2"
f = factor_graph.marginal_inference([f1,f2], ["x1", "x2", "x3"], [])
if f:
    for e in f.inputs():
        print str(e) + " = " + str(f[e])
# should output:
# {'x2': 0, 'x3': 0, 'x1': 0} = 0.017793594306
# {'x2': 0, 'x3': 1, 'x1': 1} = 0.017793594306
# {'x2': 1, 'x3': 0, 'x1': 0} = 0.0355871886121
# {'x2': 1, 'x3': 1, 'x1': 1} = 0.0355871886121
# {'x2': 1, 'x3': 1, 'x1': 0} = 0.0017793594306
# {'x2': 0, 'x3': 1, 'x1': 0} = 0.17793594306
# {'x2': 1, 'x3': 0, 'x1': 1} = 0.711743772242
# {'x2': 0, 'x3': 0, 'x1': 1} = 0.0017793594306

# test simple case
f1 = Factor({"x1":[0,1], "x2":[0,1]})
f2 = Factor({"x2":[0,1], "x3":[0,1]})
f3 = Factor({"x3":[0,1], "x4":[0,1]})
f1[{"x1":0, "x2":0}] = 1
f1[{"x1":0, "x2":1}] = 0.1
f1[{"x1":1, "x2":0}] = 0.1
f1[{"x1":1, "x2":1}] = 2

f2[{"x2":0, "x3":0}] = 0.1
f2[{"x2":0, "x3":1}] = 1
f2[{"x2":1, "x3":0}] = 2
f2[{"x2":1, "x3":1}] = 0.1

f3[{"x3":0, "x4":0}] = 0.1
f3[{"x3":0, "x4":1}] = 1
f3[{"x3":1, "x4":0}] = 2
f3[{"x3":1, "x4":1}] = 0.1

print "Test case 3"
f = factor_graph.marginal_inference([f1,f2,f3], ["x1", "x2", "x3"], ["x4"])
if f:
    for e in f.inputs():
        print str(e) + " = " + str(f[e])
# should output:
# {'x2': 0, 'x3': 0, 'x1': 0} = 0.0146823278163
# {'x2': 0, 'x3': 1, 'x1': 1} = 0.0280298985585
# {'x2': 1, 'x3': 0, 'x1': 0} = 0.0293646556327
# {'x2': 1, 'x3': 1, 'x1': 1} = 0.0560597971169
# {'x2': 1, 'x3': 1, 'x1': 0} = 0.00280298985585
# {'x2': 0, 'x3': 1, 'x1': 0} = 0.280298985585
# {'x2': 1, 'x3': 0, 'x1': 1} = 0.587293112653
# {'x2': 0, 'x3': 0, 'x1': 1} = 0.00146823278163

# Test case on patient alarm Bayesian network
vars,factors = load_xmlbif("alarm.xmlbif")
elim = ["PAP", "CVP", "MINVOLSET", "HISTORY", "ANAPHYLAXIS", "PCWP", "HREKG",
        "ERRCAUTER", "HRSAT", "PULMEMBOLUS", "EXPCO2", "ERRLOWOUTPUT", "HRBP",
        "FIO2", "LVEDVOLUME", "VENTMACH", "DISCONNECT", "MINVOL",
        "HYPOVOLEMIA", "LVFAILURE", "STROKEVOLUME", "HR", "CO", "SHUNT",
        "PVSAT", "PRESS", "VENTTUBE", "KINKEDTUBE", "VENTLUNG", "VENTALV",
        "INTUBATION", "SAO2", "ARTCO2", "INSUFFANESTH", "CATECHOL", "TPR"]
print "Test case 4"
#f = factor_graph.marginal_inference(factors, ["BP"], elim)
if f:
    for e in f.inputs():
        print str(e) + " = " + str(f[e])
# should output:
# {'BP': 'HIGH'} = 0.405299149772
# {'BP': 'NORMAL'} = 0.20470776247
# {'BP': 'LOW'} = 0.389993087757
