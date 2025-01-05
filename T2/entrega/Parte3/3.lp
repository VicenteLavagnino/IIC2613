amistad(juan,maria).
amistad(maria,elena).
amistad(elena,fernando).
amistad(fernando,juan). % Caso que produce un ciclo

visible(juan). % casos para testear
visible(maria). % casos para testears

usuario(X) :- amistad(X,Y).
usuario(Y) :- amistad(X,Y).

% amistad bidireccional
amistad(X, Y) :- amistad(Y, X).

% parte 1
cadena(X, Y, Largo) :- amistad(X, Y), Largo = 1.
cadena(X, Y, Largo) :- cadena(X, Z, L1), amistad(Z, Y), Largo = L1 + 1, #count { L1 : cadena(X, N, L1) } = Largo, X != Y, Z != X, Z != Y.

% amistad visible
amistad_visible(X, Y) :- amistad(X, Y), visible(X).
amistad_visible(X, Y) :- amistad(X, Y), visible(Y).

% amistad no visible, como variable auxiliar
amistad_no_visible(X, Y) :- amistad(X, Y), not visible(X), not visible(Y).

% cadena_no_visible, utilizamos parte 1 pero para no visible
cadena_no_visible(X, Y, Largo) :- amistad_no_visible(X, Z), cadena_no_visible(Z, Y, L1), Largo = L1 + 1, #count { L1 : cadena_no_visible(X, N, L1) } = Largo, X != Y, Z != X, Z != Y.

conectados_por_n(X, Y, N) :- cadena_no_visible(X, Y, N).

% Parte 3
existe_menor_cadena(X, Y, L1) :- cadena_no_visible(X, Y, L1), cadena_no_visible(X, Y, L2), L2 < L1.
cadena_minima_n(X, Y, Largo) :- cadena_no_visible(X, Y, Largo), not existe_menor_cadena(X, Y, Largo).
