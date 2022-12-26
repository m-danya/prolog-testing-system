pow(_, 0, 1).
pow(X, Y, Z) :-
    Y > 0,
    Y1 is Y - 1,
    pow(X, Y1, Z1),
    Z is X * Z1.

bin_to_dec([], 0).
bin_to_dec([H|T], Decimal) :-
    bin_to_dec(T, Rest),
    my_length(T, Len),
    pow(2, Len, Z),
    Decimal is (H * Z) + Rest.

my_reverse([], []).
my_reverse([H|T], R) :-
    my_reverse_helper(T, R, [H]).

my_reverse_helper([], R, R).
my_reverse_helper([H|T], R, Acc) :-
    my_reverse_helper(T, R, [H|Acc]).

my_length(List, Length) :-
  list(List),
  my_length(List, 0, Length).

my_length([_|Tail], Accumulator, Length) :-
  NewAccumulator is Accumulator + 1,
  my_length(Tail, NewAccumulator, Length).

my_length([], Length, Length).

decimal_to_binary(0, [0]).
decimal_to_binary(1, [1]).
decimal_to_binary(N, L) :-
    N > 1,
    M is N // 2,
    R is N mod 2,
    decimal_to_binary(M, L1),
    append([R], L1, L).

my_sum(X, Y, Z) :-
    bin_to_dec(X, XDec),
    bin_to_dec(Y, YDec),
    Sum is XDec + YDec,
    decimal_to_binary(Sum, Tmp),
    my_reverse(Tmp, Z).