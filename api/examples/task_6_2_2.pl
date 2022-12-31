my_sum([], 0).
my_sum([Head|Tail], Sum) :-
    my_sum(Tail, Sum1),
    Sum is Head + Sum1.