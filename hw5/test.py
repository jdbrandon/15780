import problems

q = [[0.0,0.0], [0.0,0.0], [0.0,0.0], [0.0,0.0]]
problems.ql_update(q,0.3,0.9,2,1,2.62075930591,0)
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0, 0.7862277917740591], [0.0, 0.0]]
print q
print problems.ql_policy(q)
problems.ql_update(q,0.3,0.9,2,1,2.62075930591, 1)
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0, 1.3365872460159003], [0.0, 0.0]]
print q
print problems.ql_policy(q)

problems.ql_update(q,0.3,0.9,3,1,0.560372440384,2)
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0, 1.3365872460159003], [0.0,
#0.5289902885396414]]
print q
print problems.ql_policy(q)

problems.ql_update(q,0.3,0.9,2,0,0.300354515827,0)
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0901063547480966, 1.3365872460159003],
#[0.0, 0.5289902885396414]]
print q
print problems.ql_policy(q)

problems.ql_update(q,0.3,0.9,2,0,0.300354515827,1)
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.1531808030717642, 1.3365872460159003],
#[0.0, 0.5289902885396414]]
print q
print problems.ql_policy(q)

r = problems.ql_iteration([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0,
0.0]],0.9,2,1,2.62075930591,0)
#Greedy action: 0
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0, 0.7862277917740591], [0.0, 0.0]]
print "greedy acction", r[0]

r= problems.ql_iteration([[0.0, 0.0], [0.0, 0.0], [0.0, 0.7862277917740591], [0.0,
0.0]],0.9,2,1,2.62075930591,2)
#Greedy action: 1
#Updated q: [[0.0, 0.0], [0.0, 0.0], [0.0, 1.5488687497948963], [0.0, 0.0]]
print "greedy acction", r[0]

r= problems.ql_iteration([[0.0, 0.0], [0.0, 0.0], [0.0, 1.5488687497948963], [0.0,
0.0]],0.9,1,1,6.69100577152,2)
#Greedy action: 1
#Updated q: [[0.0, 0.0], [0.0, 2.42549629390116], [0.0, 1.5488687497948963],
#[0.0, 0.0]]
print "greedy acction", r[0]

r = problems.ql_iteration([[0.0, 0.0], [0.0, 2.42549629390116], [0.0, 1.5488687497948963],
[0.0, 0.0]],0.9,2,0,0.300354515827,1)
#Greedy action: 1
#Updated q: [[0.0, 0.0], [0.0, 2.42549629390116], [0.7449903541014099,
#1.5488687497948963], [0.0, 0.  0]]
print "greedy acction", r[0]

r = problems.ql_iteration([[0.0, 0.0], [0.0, 2.42549629390116], [0.7449903541014099,
1.5488687497948963], [0.0, 0.0]],0.9,0,1,2.35632697723,0)
#Greedy action: 1
#Updated q: [[0.0, 0.7068980931684141], [0.0, 2.42549629390116],
#[0.7449903541014099, 1.              5488687497948963], [0.0, 0.0]]
print "greedy acction", r[0]
