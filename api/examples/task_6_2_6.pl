gcd(X, Y, Z) :-
    X < 0,
    Y >= 0,
    X1 is abs(X),
    gcd_(X1, Y, Z).

gcd(X, Y, Z) :-
    Y < 0,
    X >= 0,
    Y1 is abs(Y),
    gcd_(X, Y1, Z).

gcd(X, Y, Z) :-
    X < 0,
    Y < 0,
    X1 is abs(X),
    Y1 is abs(Y),
    gcd_(X1, Y1, Z).

gcd(X, Y, Z) :-
    X >= 0,
    Y >= 0,
    gcd_(X, Y, Z).


gcd_(X, Y, Z) :- X = Y, Z is X.
gcd_(X, Y, Z) :- X < Y, Y1 is Y - X, gcd_(X, Y1, Z).
gcd_(X, Y, Z) :- X > Y, gcd_(Y, X, Z).
