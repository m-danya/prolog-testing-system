my_prefix(L, []).
my_prefix([A|L], [A|[]]).
my_prefix([A|L1], [A|L2]) :- my_prefix(L1, L2).

