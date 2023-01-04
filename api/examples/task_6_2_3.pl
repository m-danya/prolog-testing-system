my_mult([], _, 0).
my_mult([X|L], X, N) :- my_mult(L, X, N1), N is N1 + 1.
my_mult([Y|L], X, N) :- X \= Y, my_mult(L, X, N).