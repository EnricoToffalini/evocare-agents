# Demo 5: iscritti, pagamenti e attestati PDF

La slide «Accio, Excel!» mostra il flusso inverso rispetto al primo esempio: da 600 iscrizioni e due moduli di pagamento a un registro controllato e a centinaia di attestati stampabili.

Tutti i nomi e i dati sono inventati. Gli output sono di riferimento, realmente prodotti tramite script; non documentano una sessione interattiva di un LLM. Le cornici Windows 11 / Excel sono illustrative.

## Materiali e risultati

`input/iscrizioni.xlsx` contiene 600 iscritti al Laboratorio Open Science, ciascuno con ID e quota di 40 EUR. `bonifici.xlsx` e `pagamenti-online.xlsx` contengono gli altri moduli da incrociare. Sono presenti otto copie della stessa transazione, sei importi parziali e sei pagamenti ancora in attesa.

L'esecuzione produce in `output/`:

- `registro-iscrizioni.xlsx`: 600 righe con quota, importo accreditato, esito, fonte precisa e file PDF associato.
- `attestati/`: 560 PDF A4 individuali, uno per ciascun iscritto con pagamento verificato.
- `attestati-stampa.pdf`: fascicolo unico di 560 pagine, pronto da stampare.
- `operazioni.csv`, `verifica.json` e `resoconto.txt`: registro e conteggi verificabili.

28 iscritti non hanno un pagamento rintracciabile e 12 richiedono verifica. Non vengono emessi PDF per questi 40 casi. Gli otto duplicati di pagamento non generano attestati aggiuntivi.

Gli attestati confermano **l'iscrizione**, senza certificare la presenza: non esiste un registro delle presenze nel materiale disponibile.

## Ripetere il riferimento

Usare l'interprete Python indicato nel README generale. Dalla radice della repository:

```powershell
python demo-locali/05-excel/genera.py
python demo-locali/05-excel/esegui-riferimento.py
python demo-locali/verify.py 5
```

`genera.py` si ferma se l'input esiste già. Il riferimento legge i tre XLSX, senza usare `truth.json`. I controlli indipendenti confrontano tutti i 600 esiti con la verità del generatore, verificano ogni PDF individuale, il formato A4, l'assenza di duplicati e la corrispondenza delle 560 pagine del fascicolo. Gli input rimangono identici SHA-256.

La logica specifica è in `../iscrizioni.py`; la scrittura dei fogli usa Artifact Tool. Dataset, copie e PDF restano esclusi da Git.

## Ripetere con un agent

Copiare soltanto `input/` e `prompt.md` in una nuova cartella e inviare il prompt nell'agent. Non includere la verità di controllo, gli script o gli output di riferimento. Verificare il registro, i casi sospesi e il fascicolo prima di stampare. Non è previsto l'invio di email.

## Immagine

`figures/demo-05-confronto.png` affianca un registro in stile Excel e i PDF in stile Esplora file Windows 11. Le celle provengono dal registro effettivo; l'anteprima è renderizzata dal primo attestato prodotto. Per aggiornare solo questa composizione: `python demo-locali/gallery.py`, poi `node demo-locali/capture.cjs 5`.
