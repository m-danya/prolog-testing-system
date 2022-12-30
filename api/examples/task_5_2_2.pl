my_elem(X, [X|_]).
my_elem(X, [_|T]) :- my_elem(X, T).