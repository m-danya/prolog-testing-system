elem(X, [X|_]).
elem(X, [_|T]) :- elem(X, T).