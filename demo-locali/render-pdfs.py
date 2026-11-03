"""Rasterizzazione dei PDF reali. Python con PyMuPDF, nessuna UI ricostruita."""
from pathlib import Path
import pymupdf
import sys

root = Path(__file__).resolve().parent
fig = root.parent/'figures'
qa = root.parent/'.demo-qa/pdf-pages'
qa.mkdir(parents=True,exist_ok=True)
jobs = [
    (root/'03-burocrazia/work/modello.pdf', 'demo-03-modello', 'relazione'),
    (root/'03-burocrazia/work/relazione.pdf', 'demo-03-compilata', 'relazione'),
    (root/'04-aggiornamento/work/prima.pdf', 'demo-04-documento-prima', 'email'),
    (root/'04-aggiornamento/work/dopo.pdf', 'demo-04-documento-dopo', 'email'),
    (root/'05-excel/output/attestati/IS-0001_ada-esempio-01.pdf', 'demo-05-attestato', 'attestato'),
    (next((root/'02-informazione/input').rglob('verbale_001.pdf')), 'demo-02-delibera', 'delibera'),
]
for src, stem, kind in jobs:
    if len(sys.argv)>1 and not stem.startswith(f'demo-{int(sys.argv[1]):02d}-'):
        continue
    doc = pymupdf.open(src)
    for i, page in enumerate(doc):
        page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(str(qa/f'{stem}-page-{i+1}.png'))
    pg=doc[0]
    if kind=='relazione':
        # Due ingrandimenti reali: valori della tabella e campi da decidere.
        # La colonna delle fonti resta nel DOCX completo, non nel ritaglio.
        clip=pymupdf.Rect(45,230,390,315)
        pg.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(45,342,495,405)).save(str(fig/(stem+'-campi.png')))
    elif kind=='email':
        hits=[r for r in pg.search_for('segreteria@') if 100<r.y0<600]
        y=hits[0].y0
        clip=pymupdf.Rect(48,y-24,pg.rect.width-45,y+31)
    elif kind=='attestato':
        clip=pymupdf.Rect(32,125,560,410)
    else:
        clip=pymupdf.Rect(32,135,560,580)
    pg.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=clip).save(str(fig/(stem+'.png')))
    print(src.name,len(doc),'pagine')
