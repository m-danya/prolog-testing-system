max_occur(L1, L2) :-
  findall(X, (member(X, L1), not((member(Y, L1), length(Y, N), length(X, N1), N > N1))), L2).