# **ANALISI TECNICA**

## Comunicazione robot - pc

per far comunicare robot al pc abbiamo usato un web server hostato sul pc. Il robot effettua una richiesta http post al web server mandando un json con all’interno i suoi dati.  
Il pc appena gli arrivano i dati li manda direttamente su thingsboard attraverso una richiesta http.

## Codice robot

Il codice del robot è strutturato in modo da mandare i dati al nostro web server ogni volta che un'azione è compiuta, nel nostro caso ci servirà per capire quanti blocchi sono passati per il nastro e gli è stata applicata l'azione di quel robot, che sia spostarli o leggerli il colore.

## Codice web server

Il codice del webserver crea un'istanza di un server nella nostra rete locale. esso ci servirà in modo che il robot raccolga i dati che il nostro robot invia grazie alle chiamate http. Il web server ci servirà poi per mandare i dati salvati sul nostro database su thingsboard.  
