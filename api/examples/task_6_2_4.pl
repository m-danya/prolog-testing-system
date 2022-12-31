most_oft(L, Xs) :-
    setof(C-E, (member(E, L), my_mult(L, E, C)), Cs),
    reverse(Cs, Rs),
    Rs = [C-_|_],
    findall(E, member(C-E, Rs), Xs).

my_mult(L, X, Y) :-
    findall(X, member(X, L), Xs),
    length(Xs, Y).