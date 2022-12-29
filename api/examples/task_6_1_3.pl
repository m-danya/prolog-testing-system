common(L1, L2, L3) :-
    findall(X, (member(X, L1), member(X, L2)), L3). % надо бы написать тут чет умное вместо этого