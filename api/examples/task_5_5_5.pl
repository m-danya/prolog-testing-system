my_list([]).
my_list([_ | Tail]) :- my_list(Tail).

my_less([], [_ | Tail]) :- my_list(Tail).
my_less([_ | X], [_ | Y]) :- my_less(X, Y).