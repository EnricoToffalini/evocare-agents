"""Schermate illustrative Windows 11 / Office richieste da Enrico.
UI ricostruite con HTML/CSS; dati e ritagli derivano dai file verificati.
"""
from common import *
from datetime import timedelta

CSS=(ROOT/'windows-ui.css').read_text(encoding='utf-8')


def icon(kind='folder'):
    if kind=='folder':
        return '<svg viewBox="0 0 28 24" class="fileicon"><path fill="#e8ac36" d="M1 4Q1 2 3 2H11L14 5H25Q27 5 27 7V20Q27 22 25 22H3Q1 22 1 20Z"/><path fill="#ffd36d" d="M1 8H27V20Q27 22 25 22H3Q1 22 1 20Z"/></svg>'
    color={'docx':'#185abd','xlsx':'#107c41','pptx':'#d24726','pdf':'#e54840','png':'#8264c4','zip':'#bd933c'}.get(kind,'#75808c')
    mark={'docx':'W','xlsx':'X','pptx':'P','pdf':'PDF','png':'▧','zip':'ZIP'}.get(kind,'TXT')
    return f'<svg viewBox="0 0 28 28" class="fileicon"><path fill="#fff" stroke="#c5cbd3" d="M7 1H21L27 7V27H7Z"/><path fill="#e8edf2" d="M21 1V7H27"/><rect fill="{color}" x="0" y="8" width="23" height="18" rx="2"/><text x="11.5" y="21" text-anchor="middle" fill="white" font-family="Segoe UI" font-weight="600" font-size="{9 if len(mark)>1 else 15}">{mark}</text></svg>'


def controls():
    return '<div class="controls"><span>─</span><span>□</span><span>×</span></div>'


def explorer(title, crumbs, entries, count, compact=False, preview=None):
    nav='<aside class="nav"><div>⌂ &nbsp; Home</div><div>▧ &nbsp; Raccolta</div><hr><div>☁ &nbsp; OneDrive</div><div>▱ &nbsp; Desktop</div><div class="sel">↓ &nbsp; Download</div><div>▤ &nbsp; Documenti</div><div>▧ &nbsp; Immagini</div><hr><div>▣ &nbsp; Questo PC</div><div>▱ &nbsp; Rete</div></aside>'
    types={'pdf':'Documento PDF','docx':'Documento Word','xlsx':'Foglio di lavoro Excel','pptx':'Presentazione PowerPoint','png':'Immagine PNG','zip':'Cartella compressa','txt':'Documento di testo','json':'File JSON'}
    rows=''
    for i,(name,kind) in enumerate(entries):
        rows+=f'<tr class="{"selected" if i==0 else ""}"><td>{icon(kind)}<span>{html.escape(name)}</span></td><td>03/11/2026 14:25</td><td>{"Cartella di file" if kind=="folder" else types.get(kind,"File")}</td></tr>'
    view='<div class="files"><table class="filetable"><thead><tr><th>Nome <span class="sort">⌃</span></th><th>Ultima modifica</th><th>Tipo</th></tr></thead><tbody>'+rows+'</tbody></table>'
    if preview: view+='<div class="pdf-preview"><img src="../../../figures/'+preview+'" alt="Anteprima del PDF sintetico"></div>'
    view+='</div>'
    return '<div class="window explorer '+('compact' if compact else '')+'"><div class="win-tabs"><div class="active-tab">'+icon('folder')+html.escape(title)+'<span>×</span></div><span class="plus">＋</span>'+controls()+'</div><div class="commands"><span>＋ <b>Nuovo</b>⌄</span><i></i><span>✂</span><span>▢</span><span>▣</span><span>✎</span><span>♧</span><span>♲</span><i></i><span>↕ Ordina ⌄</span><span>▤ Visualizza ⌄</span><span>•••</span></div><div class="address"><span>←</span><span>→</span><span>↑</span><span>⟳</span><div class="breadcrumbs">'+icon('folder')+'<span>'+html.escape(crumbs)+'</span><b>⌄</b></div><div class="search">Cerca in '+html.escape(title)+' <b>⌕</b></div></div><div class="explorer-main">'+('' if compact else nav)+view+'</div><div class="win-status">'+str(count).replace('1200','1.200')+' elementi<span>☷ &nbsp; ▦</span></div></div>'


def office_top(title, app):
    ex=app=='Excel'
    tabs='File &nbsp;&nbsp; <b>Home</b> &nbsp;&nbsp; Inserisci &nbsp;&nbsp; Layout di pagina &nbsp;&nbsp; Formule &nbsp;&nbsp; Dati &nbsp;&nbsp; Revisione &nbsp;&nbsp; Visualizza' if ex else 'File &nbsp;&nbsp; <b>Home</b> &nbsp;&nbsp; Inserisci &nbsp;&nbsp; Progettazione &nbsp;&nbsp; Layout &nbsp;&nbsp; Riferimenti &nbsp;&nbsp; Revisione &nbsp;&nbsp; Visualizza'
    return '<div class="office-title '+('excel' if ex else 'word')+'"><span class="app-icon">'+('X' if ex else 'W')+'</span><span class="save">Salvataggio automatico <i></i> &nbsp; ▣ &nbsp; ↶</span><span class="office-name">'+html.escape(title)+'</span>'+controls()+'</div><div class="office-tabs">'+tabs+'</div><div class="ribbon"><div class="paste">▣<small>Incolla⌄</small></div><div class="font-tools"><div><span>Aptos</span><span>11⌄</span><span>A⁺ &nbsp; A⁻</span></div><div><b>G</b> &nbsp; <i>C</i> &nbsp; <u>S</u> &nbsp; ▦ &nbsp; <span class="textcolor">A</span> &nbsp; ▰</div></div><div class="alignment">☰ &nbsp; ≡ &nbsp; ≣ &nbsp; ↥<br>☷ &nbsp; ↔ &nbsp; ▤ &nbsp; ↵</div><div class="formatting">'+('Generale ⌄<br>€ &nbsp; % &nbsp; 000 &nbsp; .0' if ex else 'Normale &nbsp; Nessuna spaziatura<br>Titolo 1 &nbsp; Titolo 2')+'</div><div class="find">⌕ Cerca<br>⇄ Sostituisci</div></div>'


def excel(title, headers, rows, widths, statuses):
    cols='<colgroup><col style="width:32px">'+''.join(f'<col style="width:{x}px">' for x in widths)+'</colgroup>'
    grid='<table class="sheet-grid">'+cols+'<thead><tr><th>◢</th>'+''.join('<th>'+chr(65+i)+'</th>' for i in range(len(headers)))+'</tr></thead><tbody><tr class="sheet-head"><th>5</th>'+''.join('<td>'+html.escape(h)+' <span>▾</span></td>' for h in headers)+'</tr>'
    for i,row in enumerate(rows):
        grid+='<tr class="'+statuses[i].replace(' ','-')+'"><th>'+str(i+6)+'</th>'+''.join('<td'+(' class="number"' if isinstance(v,(int,float)) else '')+'>'+html.escape(str(v if v is not None else ''))+'</td>' for v in row)+'</tr>'
    grid+='</tbody></table>'
    return '<div class="window office excel-window">'+office_top(title,'Excel')+'<div class="formula"><span class="namebox">A6 ⌄</span><span class="fx">× &nbsp; ✓ &nbsp; ƒₓ</span><span>'+html.escape(str(rows[0][0]))+'</span></div><div class="sheet">'+grid+'</div><div class="sheet-tabs"><span>‹ &nbsp; ›</span><b>Registro</b><span>＋</span><div class="scrollbar"></div></div><div class="office-status">Pronto <span>☷ &nbsp; ▦ &nbsp; ▤ &nbsp;&nbsp; − ━━━━━●━━ ＋ &nbsp; 100%</span></div></div>'


def word(title, image, fields=None):
    body='<div class="paper"><img src="../../../figures/'+image+'" class="word-table" alt="Ritaglio del documento effettivo">'
    if fields: body+='<img src="../../../figures/'+fields+'" class="word-fields" alt="Campi del documento effettivo">'
    body+='</div>'
    return '<div class="window office word-window">'+office_top(title,'Word')+'<div class="ruler">1 · · · 2 · · · 3 · · · 4 · · · 5 · · · 6 · · · 7 · · · 8 · · · 9 · · · 10 · · · 11 · · · 12</div><div class="document-area">'+body+'<div class="v-scroll"></div></div><div class="office-status">Pagina 1 di 1 &nbsp; | &nbsp; Italiano (Italia)<span>▤ &nbsp; ▥ &nbsp; − ━━━●━━ ＋ &nbsp; 150%</span></div></div>'


def chrome(before):
    directory='input' if before else 'output'
    url='http://127.0.0.1:8765/demo-locali/06-sito/'+directory+'/site/servizi/pagina-001.html'
    return '<div class="window browser"><div class="chrome-tabs"><span class="chrome-tab"><i>◉</i> Laboratori e servizi 001 <b>×</b></span><span>＋</span>'+controls()+'</div><div class="chrome-address"><span>←</span><span>→</span><span>⟳</span><div>ⓘ &nbsp; localhost:8765/servizi/pagina-001.html <span>☆</span></div><span>⋮</span></div><div class="browser-content"><iframe src="'+url+'" title="Sito locale '+directory+'"></iframe></div></div>'


def pane(label, content, cls=''):
    return '<section class="pane '+cls+'"><div class="pane-label">'+label+'</div>'+content+'</section>'


def page(n, content):
    base=sorted(ROOT.glob(f'{n:02d}-*'))[0]
    (base/'work/gallery.html').write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>Demo '+str(n)+' — schermata illustrativa</title><style>'+CSS+'</style><main class="scene">'+content+'<div class="illustration-label">Schermate illustrative · Windows 11 / Microsoft 365 · dati sintetici</div></main></html>',encoding='utf-8')


def date(s):
    return (s if isinstance(s,datetime) else datetime(1899,12,30)+timedelta(days=s)).strftime('%d/%m/%Y')


b=ROOT/'01-ordine'
paths=sorted([p for p in files(b/'input') if not p.name.startswith('copia (')],key=lambda p:p.stem[-4:])
before=[(p.name,p.suffix[1:]) for p in paths[:9]]
after=[(p.name,'folder') for p in sorted((b/'output/Download-ordinato').iterdir()) if p.is_dir()]
page(1,pane('PRIMA',explorer('Download','Questo PC  ›  Download',before,1200))+pane('DOPO',explorer('Download ordinato','Download  ›  Download ordinato',after,len(after))))

b=ROOT/'02-informazione'
entries=[(p.name,'folder') for p in sorted((b/'input').iterdir())]
w=load_workbook(b/'output/finanziamenti.xlsx',data_only=True)
source=list(w.active.iter_rows(min_row=6,values_only=True))[:5]
rows=[[r[0],date(r[1]),f'{r[2]:,.0f} €'.replace(',','.'),r[3],r[6],r[7]] for r in source]
page(2,pane('350 DOCUMENTI',explorer('Archivio','Documenti  ›  Archivio',entries,4,True),'narrow')+pane('UN REGISTRO CON LE FONTI',excel('finanziamenti.xlsx',['Pratica','Data','Importo','Finalità','Stato','Documento originale'],rows,[85,104,90,210,155,340],[r[6] for r in source]),'wide'))
w.close()

page(3,pane('PRIMA',word('modello.docx','demo-03-modello.png','demo-03-modello-campi.png'))+pane('DOPO',word('relazione-compilata.docx','demo-03-compilata.png','demo-03-compilata-campi.png')))
page(4,pane('PRIMA',word('modello_001.docx','demo-04-documento-prima.png'))+pane('DOPO',word('modello_001.docx','demo-04-documento-dopo.png')))

b=ROOT/'05-excel'
w=load_workbook(b/'output/registro-iscrizioni.xlsx',data_only=True)
source=list(w.active.iter_rows(min_row=6,values_only=True))
chosen=[r for r in source if r[4]=='Pagato'][:3]+[r for r in source if r[4]=='Non pagato'][:1]+[r for r in source if r[4]=='Da verificare'][:1]
rows=[[r[0],r[1],r[2],r[3],r[4],r[5] or '—'] for r in chosen]
entries=[(p.name,'pdf') for p in files(b/'output/attestati')[:4]]
page(5,pane('600 ISCRITTI → VERIFICA DEI PAGAMENTI',excel('registro-iscrizioni.xlsx',['ID','Nominativo','Quota €','Pagato €','Esito','Attestato PDF'],rows,[90,195,75,75,135,280],[r[4] for r in chosen]),'wide')+pane('560 ATTESTATI PDF PRONTI DA STAMPARE',explorer('Attestati','Documenti  ›  Attestati',entries,len(files(b/'output/attestati')),True,'demo-05-attestato.png'),'certificates'))
w.close()

b=ROOT/'06-sito'
entries=[(p.name,'folder') for p in sorted((b/'input/src').iterdir())]
page(6,pane('150 SORGENTI LOCALI',explorer('src','sito-universita  ›  src',entries,len(entries),True),'project')+pane('PRIMA',chrome(True),'website')+pane('DOPO',chrome(False),'website'))
print('Sei schermate illustrative Windows 11 / Office generate')
