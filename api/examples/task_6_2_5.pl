my_prime(L, X) :-
    findall(N, (between(2, X, N), is_prime(N)), L).

is_prime(2).
is_prime(3).
is_prime(P) :-
    integer(P),
    P > 3,
    P mod 2 =\= 0,
    \+ has_factor(P, 3).

has_factor(N, L) :- N mod L =:= 0.
has_factor(N, L) :-
    L * L < N,
    L2 is L + 2,
    has_factor(N, L2).