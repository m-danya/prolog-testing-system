make_ordered(L1, L2) :-
    my_sort(L1, L2).

my_sort([], []).
my_sort([X|Xs], Sorted) :-
    my_sort(Xs, SortedTail),
    insert(X, SortedTail, Sorted).

insert(X, [Y|Ys], [Y|Zs]) :- X > Y, insert(X, Ys, Zs).
insert(X, [Y|Ys], [X,Y|Ys]) :- X =< Y.
insert(X, [], [X]).
