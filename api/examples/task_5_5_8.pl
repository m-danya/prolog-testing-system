my_reverse([], []).
my_reverse(R, [H|T]) :-
    my_reverse_loop(R, T, [H]).

my_reverse_loop(R, [], R).
my_reverse_loop(R, [H|T], Acc) :-
    my_reverse_loop(R, T, [H|Acc]).

% есть еще более понятная версия с append
% my_reverse([], []).
% my_reverse(R, [H|T]) :- my_reverse(RT, T), append(RT, [H], R).