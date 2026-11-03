# Demo di lavoro sui file locali

Materiali per gli esempi iniziali di «Evocare gli agents», 4 novembre 2026. Enrico ha rimosso dalla presentazione la demo 4 e spostato «Accio, Excel!» al secondo posto. I materiali della demo rimossa sono conservati qui come archivio.
Tutti i documenti, gli importi, gli indirizzi e i nominativi sono inventati. I PDF li dichiarano privi di valore amministrativo. Non sono stati usati dati o documenti riservati.

**Livello di completamento:** generazione, esecuzione di riferimento e controlli indipendenti completati per tutte le sei demo. Gli output sono prodotti da script deterministici scritti ed eseguiti durante questo lavoro. Non sono registrazioni di sei sessioni interattive Codex o Claude Code e non misurano le capacità interpretative di un LLM.

| Cartella | Input effettivi | Risultato verificato |
|---|---:|---|
| `01-ordine` | 1.200 file in 7 formati | 981 classificati, 40 duplicati, 179 da verificare; nessuna perdita |
| `02-informazione` | 350 PDF/DOCX | 24 decisioni con fonti; 4 righe discordanti, 3 condizioni mancanti |
| `03-burocrazia` | 200 documenti + modello DOCX | 6 indicatori recuperati; 2 campi da verificare; stili e tabelle preservati |
| `04-aggiornamento` | 240 DOCX/TXT/HTML | 150 modificati, 40 già corretti, 30 simili preservati, 20 storici segnalati |
| `05-excel` | 600 iscritti in un XLSX + 2 moduli di pagamento | 560 attestati PDF e fascicolo stampabile; 28 non pagati e 12 da verificare |
| `06-sito` | 150 sorgenti JSON | 80 pagine aggiornate, 45 link corretti, 300 link verificati, 30 storici intatti |

## File e ripetizione

Ogni cartella contiene `genera.py`, `esegui-riferimento.py`, `prompt.md`, `README.md` e `verifica-eseguita.json`. Gli input effettivi, gli output e i file di lavoro sono presenti localmente ma ignorati da Git. Il modello Word e la mappa dei collegamenti ritirati sono piccoli materiali mantenuti nella repository.

`generate.py` prepara i documenti. `execute.py` esegue le trasformazioni, leggendo i file e senza accedere a `truth.json`. `verify.py` rilegge gli output e li confronta con la verità di controllo separata. Le funzioni comuni di lettura/scrittura dei formati sono in `common.py`; gli XLSX sono scritti da `workbooks.mjs` con Artifact Tool.

Nell'ambiente utilizzato:

```powershell
$pyDemo = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
& $pyDemo demo-locali/01-ordine/genera.py
& $pyDemo demo-locali/01-ordine/esegui-riferimento.py
& $pyDemo demo-locali/verify.py 1
```

La generazione si ferma se gli input esistono già. Per ripartire da zero usare una nuova copia della cartella demo e degli script condivisi. Non è necessario rigenerare per rieseguire il riferimento. Per verificare tutte le demo già presenti:

```powershell
& $pyDemo demo-locali/verify.py
```

Fuori dal runtime Codex, installare le dipendenze di `requirements.txt` in un ambiente Python. `DEMO_NODE` può indicare un altro eseguibile Node; `DEMO_ARTIFACT_TOOL` deve indicare il modulo `dist/artifact_tool.mjs` di un'installazione disponibile di `@oai/artifact-tool`. Non sono necessari servizi web, credenziali o accesso Internet durante generazione ed esecuzione. La scrittura XLSX richiede tale libreria; openpyxl è usato soltanto in lettura.

## Una vera esecuzione con un agent

Per ciascuna demo creare una **cartella nuova** contenente solo input, prompt e gli eventuali modello o redirects. Per la sesta copiare anche `06-sito/build.py`: è una build autonoma, utilizzabile con `python build.py input/src site`. Non includere `truth.json`, `execute.py`, gli output o i registri di riferimento. Aprire la nuova cartella nell'agent e inviare il prompt. Salvare la sessione autentica, verificare i file prodotti e soltanto allora acquisire screenshot dell'interfaccia dell'agent. I README delle singole demo precisano i casi da controllare.

Le regole degli script sono intenzionalmente semplici e trasparenti: classificazione dal testo, selezione di campi espliciti, duplicati binari o per identificativo. Le immagini della prima demo richiedono OCR/visione e restano da verificare. Le copie storiche nella quarta richiedono una scelta e conservano il vecchio recapito. I PDF della quinta sono nativi, non scansioni.

## Screenshot e verifica del render

In `figures/` ci sono sei `demo-XX-confronto.png` e dieci immagini di supporto. Su richiesta di Enrico, le sei composizioni ora **ricostruiscono interfacce riconoscibili di Windows 11, Esplora file, Word, Excel e Chrome**, invece di presentare inventari e tabelle come pagine web. Sono schermate illustrative, non catture desktop. `gallery-windows.py` e `windows-ui.css` ne definiscono l'aspetto; `gallery.py` è il punto di ingresso.

I nomi vengono dal filesystem e le celle dai veri XLSX verificati. I ritagli dei documenti sono render autentici dei PDF esportati da Word; i siti sono renderizzati dai veri file locali dentro la cornice illustrativa del browser. `screenshot-provenienza.json` distingue questi materiali e documenta le impronte SHA-256. Le note delle sei slide specificano la ricostruzione delle interfacce. Nessuna interfaccia agent o trascrizione di sessione è stata ricostruita.

Per rifare le immagini:

1. `powershell -NoProfile -ExecutionPolicy Bypass -File demo-locali/render-office.ps1`: esporta quattro DOCX in PDF con Microsoft Word, in un'istanza separata invisibile.
2. `python demo-locali/render-pdfs.py`: rasterizza i PDF veri con PyMuPDF.
3. Da una seconda shell: `python -m http.server 8765 --bind 127.0.0.1` dalla radice della repository.
4. `node demo-locali/capture.cjs site`: cattura sito prima/dopo e segue nel browser il collegamento corretto.
5. `& $pyDemo demo-locali/gallery.py`, poi `node demo-locali/capture.cjs`: ricrea le interfacce illustrative e cattura le sei composizioni.
6. `quarto render index.qmd`, poi `node demo-locali/capture.cjs slides`: render e catture a 1600 × 900, con frammenti visibili.

Le catture richiedono Chromium/Chrome e Puppeteer. Sono configurabili con `DEMO_CHROME`, `DEMO_PUPPETEER` e `DEMO_BASE_URL`. Il rendering DOCX standard della skill è stato tentato, ma LibreOffice non è presente: le immagini consegnate provengono dall'esportazione di **Microsoft Word**, poi rasterizzata. Il sandbox locale impediva sia Word COM sia la cache Sass di Quarto; l'esecuzione autorizzata fuori dal sandbox ha completato entrambi. Nessuna installazione è stata necessaria.

Le slide riportano la provenienza sintetica e l'esecuzione tramite script; le note distinguono preparazione, esecuzione, controlli e limiti. Le screenshot del browser usano solo contenuti locali: non verificano gli iframe remoti preesistenti, che non sono stati modificati.

## Peso e Git

I circa 65 MB di materiali e copie locali sono esclusi da Git tramite `.gitignore`; i soli generatori, prompt, documentazione, modello, registri sintetici dei controlli e immagini richiedono circa 1,2 MB. Non sono stati eseguiti commit o push. Il sito della sesta demo resta locale.
