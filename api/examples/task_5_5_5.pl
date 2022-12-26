my_length(List, Length) :-
  list(List),
  my_length(List, 0, Length).

my_length([_|Tail], Accumulator, Length) :-
  NewAccumulator is Accumulator + 1,
  my_length(Tail, NewAccumulator, Length).

my_length([], Length, Length).

my_less(X, Y) :- my_length(X, N), my_length(Y, M), N < M.

% без my_length но less or equal :(
% my_less([], _).
% my_less([_|Xs], [_|Ys]) :- my_less(Xs, Ys).
% my_less([_|_], []) :- fail.
