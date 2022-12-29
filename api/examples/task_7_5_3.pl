short_path(V, E, X, Y, P) :-
    reverse_and_append(E, Tr),
    bagof(T, short_path_(V, Tr, X, Y, T), Tmp),
    find_min_length_lists(Tmp, Pr),
    remove_duplicates(Pr, P).
short_path_(V, E, X, Y, P) :-
    short_path(V, E, X, Y, [], P).

short_path(_, _, X, X, _, [X]).
short_path(V, E, X, Y, Visited, P) :-
    member([X, Z], E),
    not(member(Z, Visited)),
    short_path(V, E, Z, Y, [Z|Visited], P1),
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

reverse_and_append([], []).
reverse_and_append([H|T], R) :-
    reverse(H, Hr),
    reverse_and_append(T, Tr),
    append([H, Hr], Tr, R).

remove_duplicates([], []).
remove_duplicates([H|T], Result) :-
  member(H, T),
  !,
  remove_duplicates(T, Result).
remove_duplicates([H|T], [H|Result]) :-
  remove_duplicates(T, Result).