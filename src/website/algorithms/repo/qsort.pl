#qsort - prolog. Rui Ferreira

qsort_divide([],_,[],[]).
qsort_divide([X|A],P,[X|A1],A2) :- X<P, qsort_divide(A,P,A1,A2).
qsort_divide([X|A],P,A1,[X|A2]) :- X>=P, qsort_divide(A,P,A1,A2).

append([],B,B).
append([H|A],B,[H|NL]) :- append(A,B,NL).

qsort([],[]).
qsort([P|A],NA):- qsort_divide(A,P,A1,A2), qsort(A1,NA1), qsort(A2,NA2), append(NA1,[P|NA2],NA).

:- qsort([1,4,6,7,8,12,-1,0,49,12],NO), print(NO).
