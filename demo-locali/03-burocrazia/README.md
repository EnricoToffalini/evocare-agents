# Demo 3: burocrazia

Materiali completamente sintetici. Gli output di questa consegna sono **output di riferimento prodotti tramite script**, eseguiti e verificati: non sono una registrazione di una sessione interattiva Codex/Claude.

200 PDF, DOCX, TXT, XLSX e PPTX. Sei indicatori nei consuntivi approvati; preventivi ed email amministrative di scenario negli altri documenti. Modello originale in modello.docx. Il riferimento riempie i campi esistenti, preserva stili/tabelle e lascia due decisioni evidenziate.

## Ripetere il riferimento

Dalla radice della repository, con l'interprete e Artifact Tool indicati nel README generale:

```powershell
python demo-locali/03-burocrazia/genera.py
python demo-locali/03-burocrazia/esegui-riferimento.py
python demo-locali/verify.py 3
```

La generazione si interrompe se input esiste già. Non serve rigenerare per rieseguire il riferimento. Input, output e work sono ignorati da Git. `output/verifica.json`, `operazioni.csv` e `resoconto.txt` documentano l'esecuzione.

## Ripetere con un agent

Creare una cartella nuova e copiarvi solo `input/`, `prompt.md` e, quando presenti, `modello.docx` o `redirects.json`. Selezionare quella cartella nell'app Codex o Claude Code e inviare il prompt. Non copiare gli output di riferimento né la verità di controllo. Lasciare all'agent la scelta dei comandi, conservare la sessione reale e verificare i risultati confrontandoli con il riferimento. Acquisire le schermate solo dopo l'esecuzione.

## Provenienza delle immagini

Le composizioni in `figures/demo-03-confronto.png` sono schermate illustrative in stile Windows 11 / Microsoft 365: le interfacce di Esplora file, Office e browser sono ricostruite in HTML/CSS su richiesta di Enrico. Nomi, celle e documenti derivano dai file effettivi. I ritagli Word sono esportazioni PDF rasterizzate. Non sono catture desktop e nessuna interfaccia agent è ricostruita.
