my_concat(L, [], L).
my_concat([X | Z], [X | L], R) :- my_concat(Z, L, R).