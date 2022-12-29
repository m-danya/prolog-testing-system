reach(V, E, X, Y) :- member(X, V), member(Y, V), reach_(E, X, Y).

reach_([[X, Y]|_], X, Y).
reach_([[X, Z]|T], X, Y) :- reach_(T, Z, Y).
reach_([[_, _]|T], X, Y) :- reach_(T, X, Y).