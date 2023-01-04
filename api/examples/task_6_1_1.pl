make_ordered(X, Y) :- 
    my_permutation(X, Y),
    is_sorted(Y).

is_sorted([]).
is_sorted([_]).
is_sorted([X, Y | Tail]) :-
    X =< Y, 
    is_sorted([Y | Tail]).

my_permutation([], []).
my_permutation([H | T], S) :-
    my_permutation(T, P),
    my_concat(X, Y, P),
    my_concat(X, [H | Y], S).

my_list([]).
my_list([_ | Tail]) :- my_list(Tail).

my_concat([], L, L).
my_concat([X | Z], R, [X | L]) :- my_concat(Z, R, L).