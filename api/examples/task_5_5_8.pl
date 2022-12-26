my_reverse([], []).
my_reverse([H|T], R) :-
    my_reverse_helper(T, R, [H]).

my_reverse_helper([], R, R).
my_reverse_helper([H|T], R, Acc) :-
    my_reverse_helper(T, R, [H|Acc]).

% есть еще более понятная версия с append
% my_reverse([], []).
% my_reverse([H|T], R) :- my_reverse(T, RT), append(RT, [H], R).