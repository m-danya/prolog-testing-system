my_concat([A|X], [A|Y], Z) :- my_concat(X, Y, Z).
my_concat([A|X], [], [A|Z]) :- my_concat(X, [], Z).
my_concat([], [], []).