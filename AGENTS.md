# Link Internet

Tutti i link a URL Internet devono aprirsi in una nuova scheda del browser. Nelle slide Quarto mantenere `link-external-newwindow: true`; per i link HTML espliciti usare `target="_blank"` e `rel="noopener noreferrer"`.

# Ombra delle immagini

Tutte le immagini, gli screenshot e i QR devono avere un'ombra morbida, sfumata e centrata (senza spostamento orizzontale o verticale), per rendere sempre riconoscibili i contorni. Non aggiungere bordi neri. La regola è globale in `styles.css` su `.reveal img`, con un alone chiaro sulle slide scure per mantenere il contrasto. Applicarla anche alle nuove immagini e verificarla dopo il render.

# Riferimento delle slide

Queste slide hanno un forte riferimento al post di Enrico Toffalini **«Tre cose sull'AI»** e alla serie di approfondimenti collegati nel suo blog. Tenerne conto quando si modificano contenuti, esempi e impostazione della presentazione.

- Blog locale: `C:\TOFFEE_BLOG`.
- Post introduttivo: `C:\TOFFEE_BLOG\posts\serie-ai\index.qmd`.
- Versione pubblicata: <https://enricotoffalini.github.io/blog/posts/serie-ai/>.
- Approfondimenti: `posts/agenti-cli/index.qmd` (agenti locali, Codex e Claude Code, con guide a terminale e app desktop), `posts/gpt-edu/index.qmd` (ChatGPT Edu) e `posts/skills/index.qmd` (personalizzazione e competenze riutilizzabili), tutti relativi alla cartella del blog.

Prima di revisioni sostanziali delle slide, leggere il post introduttivo e gli approfondimenti pertinenti. Mantenere coerenza con il taglio pratico della serie: lavoro sui file e sui progetti reali, contesto e connettori, skill, controllo del processo e verifica dei risultati. Il blog è anche una fonte di esempi e screenshot già usati nelle slide, tra cui la demo dell'analisi R sui dati simulati della BII.

## Niente voti d'esame negli esempi

Non usare mai voti, esami o dati di studenti negli esempi, nemmeno simulati: rimandano a dati riservati. La demo degli agenti usa la **BII** (Batteria d'Intelligenza Inventata, `C:\Users\enric\Desktop\Psicologia Intelligenza\__GITHUB BII-Batteria-Intelligenza-Inventata`), materiale inventato e di libero uso. I dati della demo sono in `C:\Users\enric\Desktop\demo-agenti\` (`bii_campione.csv` e `LEGGIMI.md`, ricavati da `norms_BII/standardization_sample_raw.csv`).

## Esempi da sviluppare: terza missione e Open Science

Enrico ha indicato che faremo esempi di uso degli agenti più appropriati alla presentazione, tratti dai suoi lavori di terza missione e Open Science nella cartella **`C:\Users\enric\Desktop\Open-Science-DPG-2025-2026`**. Usare questi lavori come riferimento prioritario per sviluppare gli esempi; la demo sui dati simulati della BII è il riferimento attuale del blog, non la scelta definitiva per le slide.

Prima ricognizione della cartella effettuata il 1 novembre 2026. Materiali individuati come possibili fonti di esempi:

- `OS-promotion/`: catalogo delle pratiche Open Science nelle pubblicazioni DPG; screening degli articoli, registrazione delle evidenze, sintesi divulgative in italiano e generazione di un sito Quarto. Punti di ingresso: `README.md`, `records/` e `index.qmd`.
- `Report-riproducibilita/`: controllo della riproducibilità di risultati selezionati dai dati depositati, esecuzione e adattamento del codice su copie locali, confronto con i risultati pubblicati e report delle discrepanze. Punto di ingresso: `report-riproducibilita.qmd`, con tabelle in `data/` e verifiche in `verifiche/`.
- `FAIR-test-DPG2025/`: prova della skill `fair-check` e degli strumenti per preparare un deposito su 14 depositi reali; esempio di applicazione e verifica critica di una skill. Punto di ingresso: `report-fair-check-calderan.md`, con elenco dei depositi in `index.csv`.

Questi sono candidati per i futuri esempi, da scegliere e sviluppare con Enrico. La ricognizione non equivale a una nuova verifica dei risultati dei progetti.
