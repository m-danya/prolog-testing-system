my_max([X], X).
my_max([X|Xs], M) :- my_max(Xs, M), M >= X.
my_max([X|Xs], X) :- my_max(Xs, M), M < X.