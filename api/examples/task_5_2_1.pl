my_list([]).
my_list([_|T]) :- my_list(T).