nonsquare(L1, L2) :- nonsquare_(L1, L1, L2).

nonsquare_([], _, []).
nonsquare_([X|R1], L, R2) :- Z is X * X, elem(Z, L), !, nonsquare_(R1, L, R2).
nonsquare_([X|R1], L, [X|R2]) :- nonsquare_(R1, L, R2).


elem(X, [X|_]).
elem(X, [_|T]) :- elem(X, T).