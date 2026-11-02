# QR code SVG per le slide (stessa funzione di ../index.qmd)
# eseguire dalla cartella labmeeting-ai-2026: Rscript R/qr.R
library(qrcode)

qr_svg = function(url, file, quiet = 1) {
  m = unclass(qr_code(url, ecl = "L"))
  n = nrow(m)
  d = character(0)
  for (y in seq_len(n)) {
    r = rle(as.logical(m[y, ]))
    x0 = cumsum(r$lengths) - r$lengths
    k = which(r$values)
    d = c(d, sprintf("M%d %dh%dv1h-%dz", x0[k] + quiet, y - 1 + quiet, r$lengths[k], r$lengths[k]))
  }
  s = n + 2 * quiet
  cat(sprintf('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" shape-rendering="crispEdges"><rect width="%d" height="%d" fill="#fff"/><path fill="#1d1d1b" d="%s"/></svg>',
              s, s, s, s, paste(d, collapse = "")), file = file)
}

blog = "https://enricotoffalini.github.io/blog/posts/"
links = c(
  serie  = paste0(blog, "serie-ai/"),
  agenti = paste0(blog, "agenti-cli/"),
  gptedu = paste0(blog, "gpt-edu/"),
  skills = paste0(blog, "skills/"),
  aiskills = "https://github.com/EnricoToffalini/ai-skills",
  slides = "https://enricotoffalini.github.io/slides/labmeeting-ai-2026/"
)
for (i in names(links)) qr_svg(links[i], file.path("figures", paste0("qr-", i, ".svg")))
