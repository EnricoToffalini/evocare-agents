# Demo 4: aggiornamento

Materiali completamente sintetici. Gli output di questa consegna sono **output di riferimento prodotti tramite script**, eseguiti e verificati: non sono una registrazione di una sessione interattiva Codex/Claude.

240 DOCX, TXT e HTML. Vecchio indirizzo: segreteria@dipartimento-esempio.it. Nuovo: segreteria@ateneo-esempio.it. Aggiornare le copie operative; lasciare da esaminare le copie storiche. Indirizzi simili, inclusi ex-segreteria@dipartimento-esempio.it, non vanno modificati. Nei DOCX ci sono contatti anche in tabelle, intestazioni e piè di pagina.

## Ripetere il riferimento

Dalla radice della repository, con l'interprete e Artifact Tool indicati nel README generale:

```powershell
python demo-locali/04-aggiornamento/genera.py
python demo-locali/04-aggiornamento/esegui-riferimento.py
python demo-locali/verify.py 4
```

La generazione si interrompe se input esiste già. Non serve rigenerare per rieseguire il riferimento. Input, output e work sono ignorati da Git. `output/verifica.json`, `operazioni.csv` e `resoconto.txt` documentano l'esecuzione.

## Ripetere con un agent

Creare una cartella nuova e copiarvi solo `input/`, `prompt.md` e, quando presenti, `modello.docx` o `redirects.json`. Selezionare quella cartella nell'app Codex o Claude Code e inviare il prompt. Non copiare gli output di riferimento né la verità di controllo. Lasciare all'agent la scelta dei comandi, conservare la sessione reale e verificare i risultati confrontandoli con il riferimento. Acquisire le schermate solo dopo l'esecuzione.

## Provenienza delle immagini

Le composizioni in `figures/demo-04-confronto.png` sono schermate illustrative in stile Windows 11 / Microsoft 365: le interfacce di Esplora file, Office e browser sono ricostruite in HTML/CSS su richiesta di Enrico. Nomi, celle e documenti derivano dai file effettivi. I ritagli Word sono esportazioni PDF rasterizzate. Non sono catture desktop e nessuna interfaccia agent è ricostruita.
