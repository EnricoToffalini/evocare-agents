# Demo 6: sito

Materiali completamente sintetici. Gli output di questa consegna sono **output di riferimento prodotti tramite script**, eseguiti e verificati: non sono una registrazione di una sessione interattiva Codex/Claude.

150 sorgenti JSON interconnessi. Anno corrente fissato per la presentazione: 2026/2027. 80 pagine correnti obsolete; 45 link obsoleti con destinazione documentata in redirects.json. 30 pagine storiche da preservare byte per byte. La build locale è in execute.py: build_site. Nessuna pubblicazione.

## Ripetere il riferimento

Dalla radice della repository, con l'interprete e Artifact Tool indicati nel README generale:

```powershell
python demo-locali/06-sito/genera.py
python demo-locali/06-sito/esegui-riferimento.py
python demo-locali/verify.py 6
```

La generazione si interrompe se input esiste già. Non serve rigenerare per rieseguire il riferimento. Input, output e work sono ignorati da Git. `output/verifica.json`, `operazioni.csv` e `resoconto.txt` documentano l'esecuzione.

## Ripetere con un agent

Creare una cartella nuova e copiarvi solo `input/`, `prompt.md` e, quando presenti, `modello.docx` o `redirects.json`. Per la demo 6 copiare anche build.py, che contiene soltanto la build del sito. Dopo le modifiche: `python build.py input/src site`. Selezionare quella cartella nell'app Codex o Claude Code e inviare il prompt. Non copiare gli output di riferimento né la verità di controllo. Lasciare all'agent la scelta dei comandi, conservare la sessione reale e verificare i risultati confrontandoli con il riferimento. Acquisire le schermate solo dopo l'esecuzione.

## Provenienza delle immagini

Le composizioni in `figures/demo-06-confronto.png` sono schermate illustrative in stile Windows 11 / Microsoft 365: le interfacce di Esplora file, Office e browser sono ricostruite in HTML/CSS su richiesta di Enrico. Nomi, celle e documenti derivano dai file effettivi. I ritagli Word sono esportazioni PDF rasterizzate. Non sono catture desktop e nessuna interfaccia agent è ricostruita.
