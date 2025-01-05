amistad(juan,maria).
amistad(maria,elena).
amistad(elena,fernando).
amistad(fernando,juan). % Caso que produce un ciclo

usuario(X) :- amistad(X,Y).
usuario(Y) :- amistad(X,Y).

% cadena(X,Y,Largo) :- amistad(X,Y), Largo=1. % NO USADO
% cadena(X,Y,Largo) :- cadena(X,Z,L1), cadena(Z,Y,L2), Largo=L1+L2. % NO USADO

% uso de #count para evitar ciclos en cadena en caso base
cadena(X, Y, Largo) :- amistad(X, Y), Largo = 1.
cadena(X, Y, Largo) :- cadena(X, Z, L1), amistad(Z, Y), Largo = L1 + 1, #count { L1 : cadena(X, N, L1) } = Largo, X != Y, Z != X, Z != Y.
