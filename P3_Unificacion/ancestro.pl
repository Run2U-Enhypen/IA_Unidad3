
% ==================================================
% PRACTICA 3 - PARTE C
% Conexion con la Unidad 2
% Recursividad en Prolog
% Archivo: ancestro.pl
% Version corregida
% ==================================================

% HECHOS DE LA FAMILIA

progenitor(a, c).
progenitor(a, d).
progenitor(c, b).
progenitor(c, e).

% CASO BASE
% Un progenitor directo es un ancestro.

ancestro(X, Y) :-
    progenitor(X, Y).

% CASO RECURSIVO
% X es ancestro de Y si X es progenitor de Z
% y Z es ancestro de Y.

ancestro(X, Y) :-
    progenitor(X, Z),
    ancestro(Z, Y).

% CONSULTAS SUGERIDAS

% ?- ancestro(A, b).
% ?- ancestro(a, X).
% ?- ancestro(a, b).
% ?- ancestro(d, b).
% ?- ancestro(X, Y).
