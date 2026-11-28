
% ==================================================
% PRACTICA 3 - PARTE B
% Unificacion y encadenamiento hacia atras
% Caso del coronel West
% Archivo: west.pl
% ==================================================

% --------------------------------------------------
% REGLAS DE INFERENCIA
% --------------------------------------------------

% R1: Venta ilegal de armas
criminal(X) :-
    americano(X),
    arma(Y),
    vende(X, Y, Z),
    hostil(Z).

% R2: Venta de misiles
vende(west, X, nono) :-
    misil(X),
    posee(nono, X).

% R3: Todo misil es un arma
arma(X) :-
    misil(X).

% R4: Todo enemigo de America es hostil
hostil(X) :-
    enemigo(X, america).

% --------------------------------------------------
% HECHOS INICIALES
% --------------------------------------------------

posee(nono, m1).

misil(m1).

americano(west).

enemigo(nono, america).

% --------------------------------------------------
% CONSULTAS SUGERIDAS
% --------------------------------------------------

% ?- criminal(Q).
% ?- trace, criminal(west).
