single([], []). % тоже надо чет поумнее и более соответсвующее заданию, но я надо спешить
single([H|T], L2) :- member(H, T), single(T, L2).
single([H|T], [H|L2]) :- \+ member(H, T), single(T, L2).