#### Versione anonimizzata del report di riproducibilita' ####
# Copia il progetto Report-riproducibilita in una cartella temporanea,
# maschera nomi degli autori, DOI, link e temi, renderizza e salva in demo/.
# La versione completa resta solo in local/ (ignorata da git).
# Uso, dalla cartella delle slide: Rscript R/report-anonimo.R

src = "C:/Users/enric/Desktop/Open-Science-DPG-2025-2026/Report-riproducibilita"
out = "demo/report-riproducibilita.html"
full = "local/report-riproducibilita.html"

tmp = file.path(tempdir(), "report-anonimo")
unlink(tmp, recursive = TRUE)
dir.create(file.path(tmp, "data"), recursive = TRUE)
dir.create(file.path(tmp, "verifiche/2026-10-31"), recursive = TRUE)
invisible(file.copy(file.path(src, c("report-riproducibilita.qmd", "styles.css", "render-report.py")), tmp))

#### Dati: ogni paper diventa "Paper NN" (chiave: DOI) ####
rd = function(f) read.csv(file.path(src, "data", f), encoding = "UTF-8", check.names = FALSE)
wr = function(d, f) write.csv(d, file.path(tmp, "data", f), row.names = FALSE, fileEncoding = "UTF-8")

papers = rd("paper.csv")
id = setNames(sprintf("Paper %02d", seq_len(nrow(papers))), papers$doi)
nome = setNames(papers$paper, papers$doi)   # serve solo per mascherare il testo del qmd

anon = function(d) {
  stopifnot(all(d$doi %in% names(id)))
  d$paper = id[d$doi]; d$doi = ""; d$tema = "—"
  d
}
papers = anon(papers)
papers$link = gsub("\\|[^;]*", "|", papers$link)   # resta il tipo di deposito, senza URL
wr(papers, "paper.csv")
for (f in c("discrepanze.csv", "problemi-codice.csv", "controlli-pendenti.csv")) wr(anon(rd(f)), f)
for (f in c("candidati.csv", "copertura-candidati.csv")) invisible(file.copy(file.path(src, "data", f), file.path(tmp, "data")))

#### Testo del qmd ####
qmd = readLines(file.path(tmp, "report-riproducibilita.qmd"), encoding = "UTF-8")
qmd = paste(qmd, collapse = "\n")
pid = function(cognome) unname(id[grep(cognome, nome)][1])

rep = list(
  # link: senza href resta lo stile, ma non porta a nessun articolo o deposito
  c("cite = function(paper, doi) sprintf('<a class=\"cite\" href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a>', doi, h(paper))",
    "cite = function(paper, doi) sprintf('<a class=\"cite\">%s</a>', h(paper))"),
  c("sprintf('<a class=\"chip\" href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a>', z[2], h(z[1]))",
    "sprintf('<a class=\"chip\">%s</a>', h(z[1]))"),
  c("Il nome rimanda all'articolo (DOI); le etichette accanto rimandano a dati e codice. Filtra per esito o cerca per autore e tema.",
    "In questa versione pubblica autori, temi e link sono mascherati; le etichette indicano dove stanno dati e codice. Filtra per esito."),
  c("Cerca autore o tema…", "Cerca…"),
  c("**Recupero effettuato — Floris & Gentili.**", paste0("**Recupero effettuato — ", pid("Floris"), ".**")),
  c("Correggendo nella copia percorsi e nomi di colonne, evitando una duplicazione di `AQ_trait` e il refuso `MMPUS_3`, si",
    "Correggendo nella copia percorsi, nomi di colonne e un refuso, si"),
  c("Le copie e i log sono conservati localmente in `verifiche/2026-10-31/`. Il [confronto dei coefficienti](verifiche/2026-10-31/floris/confronto-coefficienti.csv) e gli [esiti dei blocchi](verifiche/2026-10-31/floris/esiti-blocchi.csv) documentano il recupero; non sostituiscono il controllo di ogni numero del paper.",
    "Le copie e i log sono conservati localmente; documentano il recupero, ma non sostituiscono il controllo di ogni numero del paper."),
  c("Le discrepanze già osservate per Battaglini, Blini e Loconsole",
    paste0("Le discrepanze già osservate per ", pid("Battaglini"), ", ", pid("Blini"), " e ", pid("Loconsole"))),
  c("soglie incomplete per Donato, dati assenti per Swami, accesso ai dati con login per Testolin",
    paste0("soglie incomplete per ", pid("Donato"), ", dati assenti per ", pid("Swami"), ", accesso ai dati con login per ", pid("Testolin"))),
  c("esecuzione dello script di Floris & Gentili", paste0("esecuzione dello script di ", pid("Floris")))
)
for (r in rep) {
  if (!grepl(r[1], qmd, fixed = TRUE)) stop("Testo non trovato nel qmd: ", substr(r[1], 1, 60))
  qmd = sub(r[1], r[2], qmd, fixed = TRUE)
}

# candidati aggiuntivi: niente elenco con titoli e DOI
det = "(?s)html\\('<details class=\"candidate-details\">.*?</details>'\\)"
stopifnot(grepl(det, qmd, perl = TRUE))
qmd = sub(det, "", qmd, perl = TRUE)

# esclusi: motivi e numero di candidati, senza codici OSF ne' autori
excl = regmatches(qmd, regexpr("(?s)::: excl\n.*?\n:::", qmd, perl = TRUE))
stopifnot(length(excl) == 1)
righe = strsplit(excl, "\n")[[1]]
righe = righe[grepl("^- ", righe)]
n = lengths(regmatches(righe, gregexpr("\\[`|Zenodo|tassometria", righe)))   # un codice OSF, un deposito Zenodo o la revisione
motivi = sub("^- (\\*\\*[^*]+\\*\\*).*", "\\1", righe)
excl_anon = paste0("::: excl\n", paste0("- ", motivi, " ", n, ifelse(n == 1, " candidato", " candidati"), collapse = "\n"), "\n:::")
qmd = sub(excl, excl_anon, qmd, fixed = TRUE)

writeLines(enc2utf8(qmd), file.path(tmp, "report-riproducibilita.qmd"), useBytes = TRUE)

#### Render e controlli ####
wd = setwd(tmp)
st = system2("python", "render-report.py")
setwd(wd)
stopifnot(st == 0)

html = readLines(file.path(tmp, "report-riproducibilita.html"), encoding = "UTF-8", warn = FALSE)
html = paste(html, collapse = "\n")

#### Segni visibili del mascheramento ####
sost = function(x, da, a, n_min = 1) {
  n = lengths(regmatches(x, gregexpr(da, x, perl = TRUE)))
  if (n < n_min) stop("Mascheramento: trovate ", n, " occorrenze di ", da)
  gsub(da, a, x, perl = TRUE)
}
html = sost(html, '(?:<a class="cite" href>|<span class="cite">)(Paper \\d+)(?:</a>|</span>)',
            '<span class="cite masked-name" title="Autori e DOI mascherati nella versione pubblica">\\1</span>', 38)
html = sost(html, '<span class="chip">([^<]+)</span>',
            '<span class="chip masked-link" title="Link al deposito mascherato nella versione pubblica">\\1</span>', 38)
html = sost(html, '<span class="topic">—</span>',
            '<span class="topic"><span class="masked" title="Tema mascherato nella versione pubblica">tema mascherato</span></span>', 38)
html = sost(html, '(<li><strong>[^<]+</strong> \\d+ candidat[io])',
            '\\1 <span class="masked" title="Codici e autori mascherati nella versione pubblica">elenco mascherato</span>', 5)
css = '<style>
.masked { display: inline-block; font-size: .72rem; font-weight: 600; letter-spacing: .02em; line-height: 1.6;
  padding: 0 8px; border-radius: 4px; color: #4b4b5a; border: 1px dashed #a9a9b8;
  background: repeating-linear-gradient(135deg, #e4e4ea 0 5px, #f4f4f7 5px 10px); cursor: help; }
.masked::before, .masked-name::after, .masked-link::after { content: "\\1F512"; font-size: .85em; }
.masked::before { margin-right: 4px; }
.cite.masked-name { font-weight: 700; color: var(--ink); cursor: help; }
.masked-name::after { margin-left: 4px; opacity: .7; }
.chip.masked-link { display: inline-block; font-size: .7rem; font-weight: 700; padding: 0 8px; border-radius: 999px;
  line-height: 1.7; margin: 0 3px 2px 0; color: var(--acc); background: #f6f3ff; border: 1px dashed #b9a8f0; cursor: help; }
.masked-link::after { margin-left: 4px; opacity: .7; }
</style>
</head>'
html = sub("</head>", css, html, fixed = TRUE)

cognomi = unique(unlist(regmatches(nome, gregexpr("[A-Z][A-Za-z]+", nome))))
cognomi = c(setdiff(cognomi, c("Del", "Popolo")), "Cristaldi", "Lakens")
resti = c(cognomi[sapply(cognomi, function(s) grepl(paste0("\\b", s, "\\b"), html))],
          regmatches(html, gregexpr("(doi\\.org|osf\\.io|github\\.com/(?!twbs)|zenodo\\.org|figshare\\.com|researchdata)[^\"' <]*", html, perl = TRUE))[[1]])
if (length(resti)) stop("Riferimenti ancora presenti: ", paste(unique(resti), collapse = ", "))

writeLines(enc2utf8(html), out, useBytes = TRUE)
dir.create("local", showWarnings = FALSE)
invisible(file.copy(file.path(src, "report-riproducibilita.html"), full, overwrite = TRUE))
cat("Salvati:", out, "(anonimo) e", full, "(completo, solo locale)\n")
