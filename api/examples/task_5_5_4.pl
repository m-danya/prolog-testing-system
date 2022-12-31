my_sublist(L, X) :-
   append(_, Suffix, L),
   prefix(X, Suffix).
prefix([], _).
prefix([H|PrefixTail], [H|InputTail]) :-
   prefix(PrefixTail, InputTail).

% my_sublist(L, []). - не учитывает что списки должны сохранять порядок
% my_sublist([A|G], [A|H]) :- my_sublist(G, H).
% my_sublist([A|G], L) :- my_sublist(G, L).


