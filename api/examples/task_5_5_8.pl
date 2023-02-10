% This TLs

my_concat(L, [], L).
my_concat([X | Z], [X | L], R) :- my_concat(Z, L, R).

my_reverse([], []).
my_reverse([X | Tail], Y) :-
    my_concat(Y, K, [X]),
    my_reverse(K, Tail).
