"""Output di riferimento con regole esplicite, non una sessione LLM documentata.
Legge i contenuti degli input; non legge truth.json (usato solo nella verifica).
"""
from common import *
import shutil
from collections import Counter, defaultdict
from urllib.parse import urlparse, unquote
from docx.enum.text import WD_COLOR_INDEX


def build_site(src, out):
    css = 'body{margin:0;font:20px/1.5 Arial;background:#f5f7fa;color:#192e42}header{padding:18px 48px;background:#173a50;color:white;font-size:17px}main{max-width:1000px;margin:40px auto;background:white;padding:36px 44px;border-radius:12px}h1{font-size:34px;margin:0 0 20px}h2{font-size:26px}.year{font-size:30px;color:#8a315c;font-weight:bold}a{color:#155f89}nav{display:flex;gap:28px;padding:12px 0}aside{background:#eef3f7;padding:18px;margin-top:24px;font-size:17px}'
    for p in files(src):
        d = json.loads(p.read_text(encoding='utf-8'))
        rel = p.relative_to(src).with_suffix('.html')
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        links = ''.join(f'<li><a href="{os.path.relpath(out / x["href"], target.parent).replace(chr(92), chr(47))}">{html.escape(x["label"])}</a></li>' for x in d['links'])
        target.write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>'+html.escape(d['title'])+'</title><style>'+css+'</style><header>ATENEO ESEMPIO / Terza missione e Open Science · Sito dimostrativo locale</header><main><nav>Servizi &nbsp; / &nbsp; Ricerca &nbsp; / &nbsp; Formazione</nav><h1>'+html.escape(d['title'])+'</h1><p class="year">Anno accademico '+d['academic_year']+'</p><p>'+html.escape(d['body'])+'</p><h2>Informazioni e programmi</h2><ul>'+links+'</ul><aside>'+('Pagina di archivio: si conserva il contesto storico.' if d['historic'] else 'Pagina corrente per il personale. Materiali e recapiti nel programma collegato.')+'</aside></main></html>', encoding='utf-8')


def broken_links(site):
    bad = []
    checked = 0
    for p in files(site):
        for href in re.findall(r'href="([^"]+)"', p.read_text(encoding='utf-8')):
            if urlparse(href).scheme: continue
            checked += 1
            if not (p.parent / unquote(href.split('#')[0])).resolve().is_file():
                bad.append({'source':p.relative_to(site).as_posix(),'href':href})
    return checked, bad


def execute(n):
    base = sorted(ROOT.glob(f'{n:02d}-*'))[0]
    inp, out = base/'input', base/'output'
    out.mkdir(exist_ok=True)
    before = snapshot(inp)
    records = []
    if n == 1:
        seen = {}
        counts = Counter()
        for i, p in enumerate(files(inp)):
            digest = sha(p)
            s = text(p).lower()
            category = 'Da-verificare'
            reason = 'Contesto insufficiente o immagine da leggere con OCR/visione'
            for phrase, cat in [('fattura','Amministrazione'),('protocollo di ricerca','Ricerca'),
                                ('programma formativo','Formazione'),('programma evento','Eventi'),('brochure divulgativa','Comunicazione')]:
                if 'oggetto: '+phrase in s:
                    category, reason = cat, 'Categoria dal contenuto: '+phrase
            duplicate = seen.get(digest, '')
            if duplicate:
                category, reason = 'Duplicati', 'Copia identica SHA-256 di '+duplicate
            else:
                seen[digest] = p.name
            date = field(text(p), 'Data') if p.suffix != '.png' else ''
            identifier = re.search(r'loc-\d+', s)
            title = (date or 'senza-data') + '_' + category.lower() + '_' + (identifier.group() if identifier else f'file-{i+1:04d}')
            target = out/'Download-ordinato'/category/(title+'_'+f'{i+1:04d}'+p.suffix)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
            records.append({'origine':p.name,'destinazione':target.relative_to(out).as_posix(),'categoria':category,'motivo':reason,'sha256':digest})
            counts[category] += 1
        assert len(records) == 1200
        assert Counter(sha(p) for p in files(out/'Download-ordinato')) == Counter(before.values())
        summary = {'file_esaminati':1200,'classificati':1200-counts['Duplicati']-counts['Da-verificare'],
                   'duplicati':counts['Duplicati'],'da_verificare':counts['Da-verificare'],'file_cancellati':0,
                   'categorie':dict(counts),'contenuti_conservati_sha256':True}
    elif n == 2:
        rows = []
        keys = defaultdict(list)
        for p in files(inp):
            s = text(p)
            relevant = field(s,'Destinatari') == 'dottorandi' and field(s,'Esito') == 'APPROVATO'
            records.append({'file':p.relative_to(inp).as_posix(),'esito':'Incluso' if relevant else 'Escluso','motivo':field(s,'Esito')+' / '+field(s,'Destinatari')})
            if not relevant: continue
            key = field(s,'Pratica')
            amount = float(field(s,'Importo EUR'))
            condition = field(s,'Condizioni')
            row = [key, field(s,'Data'), amount, field(s,'Finalita'),field(s,'Tipologia'),condition or 'Non riportate',
                   'Confermato' if condition else 'Da verificare',p.relative_to(inp).as_posix(), 'p. 1' if p.suffix=='.pdf' else f'paragrafi 3-{len(Document(p).paragraphs)}',field(s,'Protocollo')]
            keys[key].append(row)
            rows.append(row)
        for key, group in keys.items():
            if len(set(r[2] for r in group)) > 1:
                for row in group: row[6] = 'Contraddizione'
        rows.sort(key=lambda r:({'Contraddizione':0,'Da verificare':1,'Confermato':2}[r[6]],r[0],r[1]))
        # Date seriali Excel, restano ordinabili.
        for row in rows: row[1] = (datetime.fromisoformat(row[1])-datetime(1899,12,30)).days
        xlsx([{'path':str(out/'finanziamenti.xlsx'),'title':'Finanziamenti per dottorandi (archivio fittizio)',
               'headers':['Pratica','Data','Importo EUR','Finalita','Tipologia','Condizioni','Stato','Documento','Posizione','Protocollo'],
               'rows':rows,'statusCol':'G','dateCols':['B'],'moneyCols':['C'],
               'widths':{'A':14,'B':14,'C':18,'D':32,'E':30,'F':65,'G':22,'H':65,'I':22,'J':22},
               'preview':str(out/'registro-render.png'),'previewRange':'A1:E12'}],base)
        save_json(out/'righe-estratte.json', rows)
        summary = {'documenti_letti':len(records),'decisioni_estratte':len(rows),'righe_contraddittorie':sum(r[6]=='Contraddizione' for r in rows),
                   'condizioni_mancanti':sum(r[6]=='Da verificare' for r in rows),'fonti_precise':True}
    elif n == 3:
        found = {}
        for p in files(inp):
            s = text(p)
            if 'Stato: consuntivo approvato' in s:
                label = field(s,'Indicatore')
                found[label] = (field(s,'Valore'),p.relative_to(inp).as_posix())
            records.append({'file':p.relative_to(inp).as_posix(),'consuntivo':'si' if 'Stato: consuntivo approvato' in s else 'no'})
        d = Document(base/'modello.docx')
        replacements = {'{{'+key+'}}':v[0] for key,v in found.items()}
        replacements.update({'{{Fonte '+key+'}}':v[1] for key,v in found.items()})
        replacements.update({'{{Sintesi}}':f"{found['Eventi pubblici'][0]} eventi pubblici con {found['Presenze complessive'][0]} presenze complessive; {found['Laboratori FAIR'][0]} laboratori FAIR per {found['Ore di formazione'][0]} ore.",
                             '{{Gradimento}}':'DA VERIFICARE: dato non disponibile',
                             '{{Referente}}':'DA VERIFICARE: decisione del responsabile',
                             '{{Note}}':'Fonti: consuntivi approvati. Le stime dei programmi non sono conteggiate.'})
        paragraphs = list(d.paragraphs) + [p for t in d.tables for r in t.rows for c in r.cells for p in c.paragraphs]
        for p in paragraphs:
            for run in p.runs:
                for old,new in replacements.items():
                    if old in run.text:
                        run.text = run.text.replace(old,new)
                        if 'DA VERIFICARE' in new: run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        d.save(out/'relazione-compilata.docx')
        assert '{{' not in text(out/'relazione-compilata.docx')
        template = Document(base/'modello.docx')
        assert len(template.tables)==len(d.tables) and len(template.tables[0].rows)==len(d.tables[0].rows)
        # La struttura degli stili e delle tabelle deve restare identica.
        with ZipFile(base/'modello.docx') as a, ZipFile(out/'relazione-compilata.docx') as b:
            assert a.read('word/styles.xml')==b.read('word/styles.xml')
        save_json(out/'provenienza.json', found)
        summary = {'documenti_letti':len(records),'indicatori_recuperati':len(found),'campi_da_verificare':2,'stili_preservati':True,'tabelle_preservate':True}
    elif n == 4:
        old = 'segreteria@dipartimento-esempio.it'
        new = 'segreteria@ateneo-esempio.it'
        pattern = re.compile(r'(?<![\w.+-])'+re.escape(old)+r'(?![\w.-])')
        counts = Counter()
        for p in files(inp):
            s = text(p)
            rel = p.relative_to(inp)
            dst = out/'documenti'/rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            historic = 'COPIA STORICA' in s
            status = 'Da esaminare' if historic else 'Modificato' if pattern.search(s) else 'Gia corretto' if new in s else 'Non pertinente'
            if status == 'Modificato':
                if p.suffix=='.docx':
                    with ZipFile(p) as src, ZipFile(dst,'w',ZIP_DEFLATED) as z:
                        for item in src.infolist():
                            data = src.read(item.filename)
                            if item.filename.startswith('word/') and item.filename.endswith('.xml'):
                                data = pattern.sub(new, data.decode('utf-8')).encode('utf-8')
                            z.writestr(item, data)
                    with ZipFile(p) as src, ZipFile(dst) as z:
                        for name in src.namelist():
                            expected = src.read(name)
                            if name.startswith('word/') and name.endswith('.xml'):
                                expected = pattern.sub(new,expected.decode('utf-8')).encode('utf-8')
                            assert z.read(name) == expected
                else:
                    dst.write_text(pattern.sub(new,p.read_text(encoding='utf-8')), encoding='utf-8')
                    assert dst.read_text(encoding='utf-8') == pattern.sub(new,p.read_text(encoding='utf-8'))
                assert not pattern.search(text(dst))
            else:
                shutil.copyfile(p,dst)
                assert sha(p)==sha(dst)
            counts[status] += 1
            records.append({'file':rel.as_posix(),'stato':status,'sha256_prima':sha(p),'sha256_dopo':sha(dst),
                            'vecchio_indirizzo_dopo':len(pattern.findall(text(dst)))})
        summary = {'file_controllati':len(records),'modificati':counts['Modificato'],'gia_corretti':counts['Gia corretto'],
                   'simili_preservati':counts['Non pertinente'],'storici_da_esaminare':counts['Da esaminare'],
                   'vecchio_indirizzo_nei_file_interessati':sum(r['vecchio_indirizzo_dopo'] for r in records if r['stato']=='Modificato'),
                   'sole_sostituzioni_autorizzate':True}
    elif n == 5:
        from iscrizioni import issue_certificates
        records, summary = issue_certificates(base)
    elif n == 6:
        src, dst = inp/'src', out/'src'
        redirects = json.loads((base/'redirects.json').read_text(encoding='utf-8'))
        stale, fixed, historic = 0, 0, 0
        _, bad_before = broken_links(inp/'site')
        for p in files(src):
            d = json.loads(p.read_text(encoding='utf-8'))
            target = dst/p.relative_to(src)
            if d['historic']:
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(p,target)
                historic += 1
                status = 'Archivio preservato'
            else:
                status = 'Gia corrente'
                if d['academic_year']=='2025/2026':
                    d['academic_year']='2026/2027'
                    stale += 1
                    status = 'Aggiornato'
                for link in d['links']:
                    if link['href'] in redirects:
                        link['href'] = redirects[link['href']]
                        fixed += 1
                save_json(target,d)
            records.append({'pagina':p.relative_to(src).as_posix(),'esito':status})
        build_site(dst,out/'site')
        checked, bad = broken_links(out/'site')
        assert len(files(out/'site'))==150 and not bad
        for p in files(src/'archivio'): assert sha(p)==sha(dst/p.relative_to(src))
        summary = {'pagine_generate':150,'pagine_anno_aggiornato':stale,'link_rotti_prima':len(bad_before),'link_corretti':fixed,
                   'link_controllati':checked,'link_rotti_dopo':len(bad),'pagine_storiche_preservate':historic,'build':'completata, 150 HTML'}
    assert before == snapshot(inp), 'Gli input sono stati modificati'
    summary['input_immutati_sha256'] = True
    report(base,summary,records)


if __name__ == '__main__': execute(int(sys.argv[1]))
