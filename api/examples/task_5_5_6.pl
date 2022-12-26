my_subset([], _).
my_subset([X|Xs], Y) :- member(X, Y), my_subset(Xs, Y). % мы все равно уже писали аналог member, почему бые го не использовать

