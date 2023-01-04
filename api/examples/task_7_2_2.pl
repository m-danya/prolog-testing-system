common([], _, []).
common([Head | Tail], B, I) :-
    my_member(Head, B),
    !,
    I = [Head | I_Tail],
    common(Tail, B, I_Tail).

common([_ | Tail], B, I) :-
    common(Tail, B, I).

my_member(X, [X | _]).
my_member(X, [_ | Tail]) :-
    my_member(X, Tail).