parent(X, Y) :- mother(X, Y).
parent(X, Y) :- father(X, Y).
grandfather(X, Y) :- father(Z, Y), father(X, Z).
is_father(X) :- father(X, Z).
brother(X, Y) :- parent(Z, X), parent(Z, Y), man(X).
descendant(X, Y) :- parent(Y, X).
% descendant(X, Y) :- descendant(Z, Y), parent(Z, X).
descendant(X, Y) :- parent(Z, X), descendant(Z, Y).
