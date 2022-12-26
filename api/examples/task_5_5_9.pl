my_period(X, X).
my_period(X, Y) :-
    Y = [], !, false.
my_period(X, Y) :-
    append(Y, Y, P),
    my_prefix(X, P).

my_prefix(L, []).
my_prefix([A|L], [A|[]]).
my_prefix([A|L1], [A|L2]) :- my_prefix(L1, L2).

% то что внизу логично, но не работает
% my_period(X, Y) :- append(Y, Y, P), my_period(X, Y, P). % ну в принципе можно использовать свой append
% my_period(X, _, X).
% my_period(X, Y, [_|T]) :- my_period(X, Y, T).

