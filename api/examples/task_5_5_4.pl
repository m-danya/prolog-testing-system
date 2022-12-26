my_sublist(L, []).
my_sublist([A|G], [A|H]) :- my_sublist(G, H).
my_sublist([A|G], L) :- my_sublist(G, L).


