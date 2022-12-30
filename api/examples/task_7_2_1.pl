max(X, Y, Z) :- X > Y, !, Z is X.
max(_, Y, Z) :- Z is Y.