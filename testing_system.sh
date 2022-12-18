cat test.txt | sed --expression='s/^\(.*\)\.$/bagof\(_,\1, _\)\./g' | gprolog --consult-file lists.pl
