# Feedback Docente – Robot Backend

## Analisi dei Requisiti

La presente sezione evidenzia esclusivamente gli aspetti che risultano mancanti o che necessitano di maggiore chiarimento rispetto alla documentazione esistente, senza ripetere contenuti già correttamente trattati.

**Perimetro backend (In scope / Out of scope)**

**In scope (Backend):**

* Raccolta di eventi e telemetria provenienti da robot e sensori.
* Normalizzazione e inoltro dei dati verso ThingsBoard.
* Persistenza dei dati e supporto al monitoraggio e all’analisi tramite dashboard.
* Registrazione e tracciamento delle anomalie rilevate (es. timeout sensori).

**Out of scope (Backend):**

* Coordinamento diretto tra le macchine e orchestrazione dei movimenti.
* Decisioni operative sulla sequenza di lavoro dei robot.
* Gestione degli stati operativi della linea (avvio, arresto, reset).
* Interfaccia utente e logica di controllo operatore (ambito frontend).

**KPI – requisiti di misurazione**

* I KPI definiti (pezzi prodotti per unità di tempo, distribuzione per colore, conteggio degli errori) devono essere disponibili sia per il monitoraggio dell’andamento della linea durante l’esecuzione, sia per l’analisi dei dati storici a fine simulazione.
* Per ciascun KPI deve essere definito l’intervallo temporale di riferimento (ad esempio finestra temporale o sessione di simulazione) al fine di garantirne un’interpretazione univoca.

**Requisiti non funzionali**

* Il backend deve consentire la raccolta e la visualizzazione dei dati in modalità near real-time, compatibilmente con l’utilizzo in una rete locale di laboratorio.
* Il sistema deve garantire una gestione dei dati adeguata a scopi di simulazione e monitoraggio, senza requisiti stringenti di alta disponibilità o fault tolerance.
* La persistenza e la conservazione dei dati nel tempo devono essere demandate alla piattaforma ThingsBoard.
* Gli aspetti di sicurezza (autenticazione, autorizzazione, segregazione di rete) non sono considerati requisiti primari, in quanto il sistema opera in un ambiente controllato.

## Analisi Funzionale

La presente sezione riporta gli aspetti che risultano da rendere più espliciti o meglio strutturati a livello di analisi funzionale, sulla base della documentazione esistente, senza introdurre nuove funzionalità.

**Tipologie di dati ed eventi gestiti dal backend**

* Il sistema deve gestire eventi relativi all’esecuzione delle operazioni dei robot (movimenti completati, azioni eseguite), includendo le informazioni temporali associate.
* Il sistema deve gestire eventi provenienti dai sensori di linea, in particolare:

  * rilevazione della presenza di un pezzo tramite sensore laser/infrared;
  * identificazione del colore del pezzo tramite sensore colore.
* Il sistema deve gestire eventi di errore o anomalia generati dai componenti della linea (ad esempio mancata rilevazione di un pezzo entro una soglia temporale).
* Ogni evento deve essere associato almeno all’identificativo del robot/sorgente e a un timestamp, al fine di supportare monitoraggio, analisi e calcolo dei KPI.

**Ripartizione delle responsabilità decisionali**

* Le decisioni operative relative al flusso fisico della linea (movimenti dei robot, gestione del nastro trasportatore, presa e rilascio dei pezzi, gestione dello scarto in base al colore) sono demandate ai robot e ai rispettivi PC di controllo locali.
* Il backend non prende decisioni operative né interviene sul comportamento delle macchine, ma svolge un ruolo di supporto informativo.
* Il backend si limita a ricevere, registrare e rendere disponibili i dati e gli eventi generati dai componenti della linea, inclusi gli esiti delle decisioni prese a livello locale.
* In caso di anomalie o errori, il backend registra l’evento e lo rende visibile ai sistemi di monitoraggio, senza attivare azioni correttive automatiche sui robot.

**Gestione delle anomalie (modello generale)**

* Il sistema deve gestire le anomalie come una categoria di eventi distinta dagli eventi di funzionamento nominale.
* Ogni anomalia deve essere caratterizzata almeno da:

  * tipologia di anomalia (es. timeout sensore, errore sensore, errore di esecuzione);
  * timestamp di rilevazione;
  * sorgente che ha generato l’anomalia (robot o sensore).
* Il modello di gestione delle anomalie deve essere estendibile ad altre tipologie oltre a quelle attualmente implementate, mantenendo invariato il ruolo del backend come componente di registrazione e monitoraggio.
* Le anomalie devono essere consultabili tramite gli strumenti di monitoraggio e contribuire al calcolo degli indicatori di errore.

## Analisi Tecnica (valutazione indicativa)

La presente sezione riporta gli aspetti tecnici che risultano mancanti o che necessitano di maggiore esplicitazione rispetto alla documentazione esistente, con finalità di valutazione complessiva dell’architettura backend.

**Contratti dei dati e robustezza del flusso eventi**

* Va esplicitata la semantica di consegna degli eventi tra robot → server → ThingsBoard (ad esempio best-effort in LAN, oppure gestione dei retry). In assenza di specifica, non è chiaro se un evento possa andare perso o duplicarsi.
* Va chiarito se il sistema gestisce o meno i duplicati (ad esempio in caso di reinvio dello stesso evento) e, se non gestiti, va dichiarato come limitazione accettata nel contesto di simulazione.
* Va chiarito se l’ordine temporale degli eventi è garantito o se possono verificarsi eventi fuori ordine; in tal caso, il timestamp deve essere considerato riferimento primario per analisi e KPI.
* Va indicato come viene trattata l’indisponibilità temporanea del server o di ThingsBoard (ad esempio perdita accettata, oppure buffering locale non previsto).

**Modello dati logico e schema concettuale (ER adattato)**

* Va esplicitato un modello dati logico che descriva le principali entità gestite dal sistema (ad esempio robot/device, sensori, eventi, anomalie, KPI) e le relazioni concettuali tra di esse.
* Va chiarita la distinzione tra le diverse tipologie di dati memorizzate sulla piattaforma (telemetria time-series, attributi, eventi/allarmi), indicando per ciascuna categoria il ruolo funzionale.
* Va definito un insieme minimo di campi comuni per gli eventi (identificativo della sorgente, timestamp, tipologia di evento, payload specifico) al fine di garantire coerenza dei dati e facilità di analisi.
* L’assenza di un modello dati esplicito rende più complessa la verifica della completezza e della coerenza delle informazioni gestite dal backend.

**Configurazione e parametrizzazione**

* Va esplicitato dove e come vengono definiti i parametri operativi rilevanti per la simulazione (ad esempio soglie temporali per timeout, velocità del nastro, eventuali parametri di campionamento/invio dati).
* Va chiarito se tali parametri sono statici (hard-coded) o configurabili (file di configurazione/variabili d’ambiente), e con quale livello di tracciabilità delle modifiche.
* L’assenza di una sezione di configurazione rende meno riproducibile la simulazione e più difficile confrontare sessioni diverse a parità di condizioni.

