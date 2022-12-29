short_path(X, Y, E, P) :-
    bagof(T, short_path_(X, Y, E, T), Tmp),
    find_min_length_lists(Tmp, P).
short_path_(X, Y, E, P) :-
    short_path(E, X, Y, [], P).

short_path(_, X, X, _, [X]).
short_path(E, X, Y, Visited, P) :-
    member([X, Z], E),
    not(member(Z, Visited)),
    short_path(E, Z, Y, [Z|Visited], P1),
    P = [X|P1].

min_length([], Min) :- Min is 999999999.
min_length([H|T], Min) :-
  min_length(T, Min2),
  length(H, Len),
  (Len < Min2 -> Min = Len ; Min = Min2).

min_length_lists([], _, []).
min_length_lists([H|T], Min, [H|MinTail]) :-
  length(H, Len),
  Len =:= Min,
  min_length_lists(T, Min, MinTail).
min_length_lists([H|T], Min, MinTail) :-
  length(H, Len),
  Len =\= Min,
  min_length_lists(T, Min, MinTail).

find_min_length_lists(Lists, MinLists) :-
  min_length(Lists, Min),
  min_length_lists(Lists, Min, MinLists).