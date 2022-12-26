my_less(X, Y) :- % я чет совсем не уверен в том что это норм решение
    bin_to_dec(X, XDec),
    bin_to_dec(Y, YDec),
    XDec < YDec.
bin_to_dec([], 0).
bin_to_dec([H|T], Decimal) :-
    bin_to_dec(T, Rest),
    my_length(T, Len),
    Decimal is (H * 2 ** Len) + Rest.

my_length(List, Length) :-
  list(List),
  my_length(List, 0, Length).

my_length([_|Tail], Accumulator, Length) :-
  NewAccumulator is Accumulator + 1,
  my_length(Tail, NewAccumulator, Length).

my_length([], Length, Length).
