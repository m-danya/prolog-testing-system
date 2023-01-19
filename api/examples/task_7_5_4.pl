color(V, E, C) :- len(V, Len), r_color(V, C, [], Len), all_ok(V, E, C), !.

r_color([], R, R, _).
r_color([_|R], L, B, N) :- one_to_n(N, I), r_color(R, L, [I|B], N).

all_ok(V, [], C).
all_ok(V, [E|R], C) :- color_ok(V, E, C), all_ok(V, R, C).
color_ok(V, [From, To], C) :- color_of_vertex(V, C, From, CFrom), color_of_vertex(V, C, To, CTo), not(CFrom = CTo).
color_of_vertex([V|_], [C|_], V, C) :- !.
color_of_vertex([_|R1], [_|R2], V, C) :- color_of_vertex(R1, R2, V, C).

one_to_n(N, R) :- one_to_n_(N, 1, R).
one_to_n_(_, K, R) :- R is K.
one_to_n_(N, K, R) :- N > K, L is K + 1, one_to_n_(N, L, R).
                          
len([], 0).
len([A|R], S) :- len(R, K), S is K + 1.