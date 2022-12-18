list_length(List, Length) :-
  list(List),
  list_length(List, 0, Length).

list_length([_|Tail], Accumulator, Length) :-
  NewAccumulator is Accumulator + 1,
  list_length(Tail, NewAccumulator, Length).

list_length([], Length, Length).