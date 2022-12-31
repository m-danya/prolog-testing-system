common([], _, []).
common([H1|T], L2, [H2|R]) :- elem(H1, L2), !, common(T, L2, R), H2 is H1.
common([_|T], L2, R) :- common(T, L2, R).


elem(X, [X|_]).
elem(X, [_|T]) :- elem(X, T).