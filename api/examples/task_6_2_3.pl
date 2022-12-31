my_mult(L, X, Y) :-
    findall(X, member(X, L), Xs),
    length(Xs, Y).