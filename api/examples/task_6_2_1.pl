my_length(List, Length) :-
  list(List),
  my_length(List, 0, Length).

my_length([_|Tail], Accumulator, Length) :-
  NewAccumulator is Accumulator + 1,
  my_length(Tail, NewAccumulator, Length).

my_length([], Length, Length).