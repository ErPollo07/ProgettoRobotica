# PROBLEMI RISCONTRATI

## Problemi attuali

1. Collegamento multiplo  
E' necessario determinare se piu' robot possono essere collegati e controllati contemporaneamente dallo stesso PC.  
In alternativa, si deve valutare una configurazione multi-PC (uno per robot).

2. Comunicazione robot \<-> PC  
Si deve determinare se la comunicazione tra robot e pc e' possibile. Altrimenti e' necessaria la scrittura del codice di un programma che intercetta il passaggio di dati tra il robot e il pc.

3. Avvio simultaneo dei programmi  
Se piu' robot possono essere collegati allo stesso pc allora una possibile soluzione consiste nell'implementare un software di controllo centralizzato che gestisca l'input di mouse/tastiera per eseguire le operazioni nel giusto ordine e in maniere prevedibile.

NOTA:  
Per la corrente configurazione della linea di produzione non serve sincronia tra i robot perche' svolgono azioni indipendenti.