# **ANALISI FUNZIONALE**

## Descrizione della linea di produzione

## Componenti hardware della linea di produzione

- Nastro trasportatore Dobot  
- 3 robot (2 Dobot Magician, 1 Dobot Magician Lite)  
- Sensore laser (rilevamento presenza oggetti)  
- Sensore di colore (identificazione colore del blocco)

## Descrizione del flusso operativo

1. Il robot R1 preleva un blocco dal magazzino 1 (alimentazione del magazzino manuale da parte dell’operatore) e lo deposita sul nastro trasportatore.  
2. Il sensore laser rileva il passaggio del blocco e segnala l’evento al robot R2.  
3. Il robot R2 intercetta il blocco in movimento e lo posiziona sul sensore di colore.  
4. Il robot R3, che controlla il sensore di colore rileva un cambiamento nel colore rilevato e va a prendere il blocco sul sensore di colore e lo deposita nel magazzino 2, nella sezione corrispondente al colore rilevato.

## Comunicazione con il server

Il server thingsboard sara’ hostato su un quarto pc (se non si puo’ usare un quarto pc allora uno dei tre fara’ da server).  
Ogni robot ha il suo pc collegato e il programma per spedire i dati al server thingsboard.

## Gestione anomalie

- Se il sensore laser non rileva alcun passaggio di blocchi entro un intervallo di tempo predefinito, viene generato un messaggio di errore inviato al PC di controllo.  
- Il PC successivamente lo inserisce nel database.

Il sistema garantisce il tracciamento completo di ogni fase produttiva, dal prelievo alla classificazione finale.
