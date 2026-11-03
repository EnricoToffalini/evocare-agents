"""Crea le istruzioni e i punti di ingresso; non genera dataset né output."""
from pathlib import Path

root = Path(__file__).resolve().parent
names = ['01-ordine', '02-informazione', '03-burocrazia', '04-aggiornamento', '05-excel', '06-sito']
prompts = [
    'Ho 1.200 file accumulati in Download. Esaminali, riconosci i diversi tipi di documenti, rinominali in modo coerente e organizzali in sottocartelle. Individua i duplicati e lascia i casi dubbi da verificare. Non cancellare nulla.',
    'In questi 350 documenti trova tutte le decisioni relative a finanziamenti per dottorandi. Prepara un unico Excel con importi, date, finalità e riferimento preciso al documento originale. Segnala eventuali decisioni contraddittorie.',
    'Devo compilare questa relazione annuale. Le informazioni sono sparse nei 200 documenti della cartella. Recuperale, compila direttamente il modello Word mantenendo la formattazione e segnala ciò che manca o richiede una mia decisione. Non inventare informazioni.',
    'La segreteria ha cambiato indirizzo email. Controlla tutti i 240 documenti, sostituisci il vecchio indirizzo con quello nuovo ovunque sia pertinente e non cambiare nient’altro. Alla fine dimmi quanti file hai modificato e verifica che il vecchio indirizzo non sia rimasto nei documenti interessati.',
    'Ho 600 iscritti nel modulo di iscrizione. Incrocia i dati con questi altri moduli e controlla chi ha pagato. Poi prepara gli attestati PDF personalizzati, pronti da stampare, per tutti quelli in regola. Segnala i pagamenti mancanti e i casi dubbi.',
    'Questo sito ha 150 pagine. Aggiorna all’anno accademico corrente tutte le informazioni ancora obsolete, correggi i link interni non funzionanti e preserva l’archivio storico. Poi ricostruisci il sito e verifica che funzioni.'
]
details = [
    'PDF, DOCX, XLSX, PNG, PPTX, ZIP e TXT reali. Nomi deliberatamente poco informativi. Le categorie derivano dal contenuto. I PNG richiedono OCR o visione e il riferimento li lascia da verificare. Il controllo dei duplicati è binario (SHA-256), non semantico.',
    '350 PDF/DOCX suddivisi per anni e uffici. 24 decisioni approvate, documenti simili respinti, informativi o destinati ad altri beneficiari. Due coppie di decisioni hanno importi discordanti per la stessa pratica; tre mancano delle condizioni. Lo script usa campi espliciti e non sostituisce una lettura giuridica.',
    '200 PDF, DOCX, TXT, XLSX e PPTX. Sei indicatori nei consuntivi approvati; preventivi ed email amministrative di scenario negli altri documenti. Modello originale in modello.docx. Il riferimento riempie i campi esistenti, preserva stili/tabelle e lascia due decisioni evidenziate.',
    '240 DOCX, TXT e HTML. Vecchio indirizzo: segreteria@dipartimento-esempio.it. Nuovo: segreteria@ateneo-esempio.it. Aggiornare le copie operative; lasciare da esaminare le copie storiche. Indirizzi simili, inclusi ex-segreteria@dipartimento-esempio.it, non vanno modificati. Nei DOCX ci sono contatti anche in tabelle, intestazioni e piè di pagina.',
    '600 iscritti in un modulo Excel e due moduli di pagamento: 560 pagati, 28 non pagati, 12 da verificare e 8 transazioni duplicate. Output: registro-iscrizioni.xlsx, 560 attestati di iscrizione PDF individuali e fascicolo unico A4 per la stampa. Non si certifica la presenza.',
    '150 sorgenti JSON interconnessi. Anno corrente fissato per la presentazione: 2026/2027. 80 pagine correnti obsolete; 45 link obsoleti con destinazione documentata in redirects.json. 30 pagine storiche da preservare byte per byte. La build locale è in execute.py: build_site. Nessuna pubblicazione.'
]
for i, name in enumerate(names, 1):
    base = root/name
    base.mkdir(exist_ok=True)
    extra = '\n\nVecchio indirizzo: `segreteria@dipartimento-esempio.it`. Nuovo indirizzo: `segreteria@ateneo-esempio.it`. Le copie storiche richiedono una mia decisione.' if i==4 else ''
    if i==6: extra = '\n\nAnno corrente: 2026/2027. Le destinazioni dei collegamenti ritirati sono in `redirects.json`. La build autonoma e in build.py: esegui `python build.py input/src site` dalla cartella di lavoro. Il sito risultante deve restare locale.'
    (base/'prompt.md').write_text(prompts[i-1]+extra+'\n\nLavora su una copia dei materiali, conserva gli input e scrivi i risultati in una nuova cartella. Non leggere truth.json, execute.py o gli output di riferimento: sono riservati alla verifica della demo. Non inviare email e non pubblicare nulla.\n',encoding='utf-8')
    for script, module, function in [('genera.py','generate','generate'),('esegui-riferimento.py','execute','execute')]:
        (base/script).write_text(f'from pathlib import Path\nimport sys\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\nfrom {module} import {function}\n{function}({i})\n',encoding='utf-8')
    build_note = ' Per la demo 6 copiare anche build.py, che contiene soltanto la build del sito. Dopo le modifiche: `python build.py input/src site`.' if i==6 else ''
    (base/'README.md').write_text(f'''# Demo {i}: {name[3:]}

Materiali completamente sintetici. Gli output di questa consegna sono **output di riferimento prodotti tramite script**, eseguiti e verificati: non sono una registrazione di una sessione interattiva Codex/Claude.

{details[i-1]}

## Ripetere il riferimento

Dalla radice della repository, con l'interprete e Artifact Tool indicati nel README generale:

```powershell
python demo-locali/{name}/genera.py
python demo-locali/{name}/esegui-riferimento.py
python demo-locali/verify.py {i}
```

La generazione si interrompe se input esiste già. Non serve rigenerare per rieseguire il riferimento. Input, output e work sono ignorati da Git. `output/verifica.json`, `operazioni.csv` e `resoconto.txt` documentano l'esecuzione.

## Ripetere con un agent

Creare una cartella nuova e copiarvi solo `input/`, `prompt.md` e, quando presenti, `modello.docx` o `redirects.json`.{build_note} Selezionare quella cartella nell'app Codex o Claude Code e inviare il prompt. Non copiare gli output di riferimento né la verità di controllo. Lasciare all'agent la scelta dei comandi, conservare la sessione reale e verificare i risultati confrontandoli con il riferimento. Acquisire le schermate solo dopo l'esecuzione.

## Provenienza delle immagini

Le composizioni in `figures/demo-{i:02d}-confronto.png` sono schermate illustrative in stile Windows 11 / Microsoft 365: le interfacce di Esplora file, Office e browser sono ricostruite in HTML/CSS su richiesta di Enrico. Nomi, celle e documenti derivano dai file effettivi. I ritagli Word sono esportazioni PDF rasterizzate. Non sono catture desktop e nessuna interfaccia agent è ricostruita.
''',encoding='utf-8')
print('Sei cartelle e prompt creati')
