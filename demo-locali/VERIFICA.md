# Esito della consegna

Aggiornamento dopo le modifiche di Enrico: la presentazione contiene ora cinque demo, con «Accio, Excel!» al secondo posto e senza la slide sull'aggiornamento delle email. La demo Excel è stata invertita in iscrizioni → pagamenti → attestati stampabili. `verifica-slide.json` documenta la verifica rispetto alla versione modificata da Enrico: tutte le altre slide sono preservate. I conteggi di sei demo e 63 slide riportati sotto si riferiscono alla prima consegna e non alla nuova sequenza.

Sei demo preparate, eseguite come riferimento tramite script e verificate con controlli indipendenti. I risultati e i limiti sono descritti nel README generale e nelle note delle slide.

## Verifiche superate

- `quarto render index.qmd` completato; presentazione di 63 slide, quattro in più rispetto alle 59 originarie.
- Sei nuove slide sostituiscono esattamente le due demo iniziali. Copertina invariata nel sorgente.
- Da «come si procede?» in poi: sorgente QMD e HTML generato identici agli originali; identificativi delle slide preservati.
- Sei slide controllate nel browser a 1600 × 900, con i frammenti visibili. Titoli, prompt, immagini e didascalie entro l'area utile; ombre centrate presenti. Nella demo Word sono stati ingranditi ritagli della tabella e dei campi.
- Tutte le immagini locali del deck esistono. Sedici immagini nuove documentate in `screenshot-provenienza.json`, con origine e SHA-256.
- Tutti i 1.200 file della prima demo conservati con gli stessi contenuti SHA-256: 981 classificati, 40 duplicati, 179 casi dubbi.
- Le 24 righe dei finanziamenti corrispondono alle fonti sintetiche: due coppie discordanti sulla stessa pratica non cumulabile e tre condizioni mancanti.
- Relazione Word compilata da sei indicatori, con stili e struttura delle tabelle preservati e due campi evidenziati. Modello e risultato esportati da Microsoft Word: una pagina ciascuno, controllate visivamente.
- In 150 dei 240 documenti è cambiato soltanto il recapito previsto, incluse tabelle, intestazioni e piè di pagina. Zero residui nei file aggiornati; 40 già corretti, 30 simili e 20 storici preservati.
- Demo «Accio, Excel!» invertita su richiesta di Enrico: 600 iscritti incrociati con due moduli di pagamento, 560 attestati PDF individuali e fascicolo A4 di 560 pagine. Verificati tutti i nominativi/ID e gli esiti: 28 pagamenti mancanti, 12 da verificare; otto transazioni duplicate ignorate. Si conferma l'iscrizione, senza attestare la presenza.
- Sito locale ricostruito: 150 HTML, 80 pagine aggiornate e 45 collegamenti corretti. Tutti i 300 link controllati; zero mancanti; 30 sorgenti storici identici byte per byte. Collegamento corretto seguito anche nel browser.
- Input preservati dopo le trasformazioni. Dataset e copie di lavoro esclusi da Git; nessun nuovo file candidato a Git oltre 2 MB. Nessun commit o push.
- `git diff --check` superato.

## Limiti e verifiche non effettuate

- Non sono state documentate sei sessioni interattive con un LLM. Gli output di riferimento provengono da script con regole esplicite. Il flusso per eseguire successivamente ogni prompt con Codex/Claude è nei README.
- Su richiesta successiva di Enrico, le sei composizioni sono ricostruzioni illustrative delle interfacce Windows 11 / Microsoft 365, con dati provenienti dai file verificati. Le cornici di Esplora file, Office e Chrome sono disegnate in HTML/CSS; i ritagli Word/PDF e i contenuti del sito sono render dei file effettivi. Non sono catture desktop. Le note e il registro di provenienza sono aggiornati.
- Il renderer della skill basato su LibreOffice non era disponibile; l'esportazione autentica con Microsoft Word ha completato la verifica dell'impaginazione. L'esecuzione fuori dal sandbox è stata necessaria per Word COM e per la cache Sass di Quarto.
- Nessun OCR: i PNG della prima demo restano da verificare e i PDF della quinta hanno testo nativo. Il controllo dei link riguarda esistenza e navigazione del sito statico locale, senza backend.
- I contenuti degli iframe remoti preesistenti non sono stati ricontrollati; sono rimasti invariati insieme al resto della presentazione.

Il diff completo di `index.qmd` è salvato localmente in `.demo-qa/index.qmd.diff`; è anche visibile con `git diff -- index.qmd`.
