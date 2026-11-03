"""Preparazione deterministica. Non esegue le operazioni richieste nei prompt."""
from common import *
import shutil
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def generate(n):
    base = sorted(ROOT.glob(f'{n:02d}-*'))[0]
    inp = base / 'input'
    inp.mkdir(parents=True, exist_ok=True)
    # Nessuna pulizia distruttiva: per un nuovo dataset usare una copia nuova.
    if files(inp):
        raise RuntimeError('Input già presente: usare i materiali esistenti o una copia nuova della demo.')
    jobs = []
    truth = []
    if n == 1:
        cats = [('Amministrazione', 'fattura', 'Acquisto cancelleria per uffici'),
                ('Ricerca', 'protocollo di ricerca', 'Studio pilota su materiali inventati'),
                ('Formazione', 'programma formativo', 'Laboratorio FAIR per personale'),
                ('Eventi', 'programma evento', 'Giornata pubblica della scienza'),
                ('Comunicazione', 'brochure divulgativa', 'Incontro con associazioni locali')]
        names = ['documento_finale_2', 'fattura ottobre', 'presentazione_nuova_def', 'scan0042',
                 'download (1)', 'allegato', 'copia definitiva', 'Nuovo documento', 'IMG_0042']
        exts = ['.pdf', '.docx', '.xlsx', '.png', '.pptx', '.zip', '.txt']
        for i in range(1160):
            cat, kind, purpose = cats[i % 5]
            ext = exts[i % 7]
            name = f'{names[i % len(names)]}_{i+1:04d}{ext}'
            ambiguous = i % 73 == 0
            lines = [f'Identificativo: LOC-{i+1:04d}', f'Data: 2026-{1+i%10:02d}-{1+i%27:02d}',
                     'Oggetto: da definire' if ambiguous else f'Oggetto: {kind}',
                     'Appunto privo di contesto e destinatario.' if ambiguous else purpose,
                     f'Riferimento pratica: PR-{i+1:04d}', 'Materiale inventato per dimostrazione.']
            make_file(inp / name, 'Documento di lavoro', lines, jobs)
            truth.append({'file': name, 'category': 'Da-verificare' if ambiguous or ext == '.png' else cat})
        xlsx(jobs, base)
        for j in range(40):
            src = inp / truth[j*17]['file']
            dst = inp / f'copia ({j+1}){src.suffix}'
            shutil.copyfile(src, dst)
            truth.append({'file': dst.name, 'duplicate_of': src.name})
    elif n == 2:
        offices = ['Ricerca', 'Direzione', 'Amministrazione', 'Formazione', 'Servizi']
        for i in range(350):
            year = 2026 if i<4 else 2023 + i % 4
            folder = inp / str(year) / offices[(i//4) % 5]
            p = folder / f'{["verbale", "delibera", "comunicazione", "relazione"][i%4]}_{i+1:03d}{".pdf" if i%2 == 0 else ".docx"}'
            if i < 24:
                key = f'FD-{i//2+1:02d}' if i < 4 else f'FD-{i-1:02d}'
                amount = 2000 + 500*(i%7)
                lines = [f'Protocollo: DEL-{i+1:03d}/{year}', f'Data: {year}-10-{1+i%27:02d}',
                         'Esito: APPROVATO', 'Destinatari: dottorandi', f'Pratica: {key}',
                         f'Importo EUR: {amount}',
                         f'Finalita: {["Mobilita per ricerca", "Accesso a infrastrutture", "Partecipazione a convegni"][(i//2 if i<4 else i)%3]}',
                         'Tipologia: rimborso spese documentate',
                         'Condizioni: autorizzazione preventiva e giustificativi entro 30 giorni.',
                         'Ambito: contributo unico per questa pratica; importi non cumulabili.',
                         'La decisione non dichiara di sostituire atti precedenti.']
                if i in (5, 13, 21):
                    lines = [s for s in lines if not s.startswith('Condizioni:')]
                truth.append({'file': p.relative_to(inp).as_posix(), 'key': key, 'amount': amount,
                              'status': 'Contraddizione' if i<4 else 'Da verificare' if i in (5,13,21) else 'Confermato'})
            else:
                variants = [
                    ['Destinatari: personale tecnico', 'Esito: APPROVATO', 'Importo EUR: 3000', 'Finalita: formazione del personale. I dottorandi non sono destinatari.'],
                    ['Destinatari: dottorandi', 'Esito: NON APPROVATO', 'Importo proposto EUR: 5000', 'La proposta di finanziamento e respinta per indisponibilita di fondi.'],
                    ['Destinatari: dottorandi', 'Esito: INFORMATIVO', 'Promemoria sui finanziamenti gia deliberati: nessuna nuova assegnazione.'],
                    ['Destinatari: assegnisti', 'Esito: APPROVATO', 'Importo EUR: 2500', 'Supporto a missioni per assegnisti; nessuna assegnazione ai dottorandi.']]
                lines = [f'Protocollo: DOC-{i+1:03d}/{year}', f'Data: {year}-09-15'] + variants[i%4]
            make_file(p, 'Decisioni e comunicazioni', lines, jobs)
    elif n == 3:
        facts = [
            ('Eventi pubblici', '12', 'Eventi svolti', 'Consuntivo delle iniziative pubbliche completate.'),
            ('Presenze complessive', '486', 'Partecipazione', 'Presenze aggregate, non persone uniche.'),
            ('Laboratori FAIR', '8', 'Formazione', 'Laboratori completati per il personale.'),
            ('Ore di formazione', '32', 'Formazione', 'Durata complessiva degli otto laboratori.'),
            ('Spesa rendicontata EUR', '18400', 'Consuntivo', 'Importi verificati dal riepilogo amministrativo.'),
            ('Periodo', '2026', 'Relazione annuale', 'Periodo gennaio-dicembre 2026, scenario fittizio.')]
        for i in range(200):
            ext = ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'][i%5]
            p = inp / ['Relazioni', 'Verbali', 'Programmi', 'Consuntivi', 'Corrispondenza'][i%5] / f'allegato_{i+1:03d}{ext}'
            if i < len(facts):
                label, value, title, comment = facts[i]
                lines = ['Stato: consuntivo approvato', f'Indicatore: {label}', f'Valore: {value}', comment,
                         'Ambito: Terza missione e Open Science. Dati aggregati inventati.']
                truth.append({'label':label,'value':value,'file':p.relative_to(inp).as_posix()})
            else:
                title = ['Programma di attivita', 'Verbale operativo', 'Preventivo', 'Comunicazione interna'][i%4]
                lines = [f'Pratica: TM-{i+1:03d}', 'Stato: pianificazione, non consuntivo',
                         f'Attivita prevista: {["Incontro pubblico", "Laboratorio dati aperti", "Seminario FAIR"][i%3]}',
                         f'Numero preventivato: {20+i%30}',
                         'Queste stime non sostituiscono il consuntivo approvato.',
                         'Non sono disponibili il gradimento finale e il referente della validazione.']
            make_file(p, title, lines, jobs)
        xlsx(jobs, base)
        d = Document()
        d.core_properties.author = 'Materiali sintetici'
        sec = d.sections[0]
        sec.top_margin = sec.bottom_margin = Inches(.6)
        sec.left_margin = sec.right_margin = Inches(.7)
        d.styles['Normal'].font.name = 'Calibri'
        d.styles['Normal'].font.size = Pt(11)
        d.add_paragraph('ATENEO ESEMPIO · MODELLO FITTIZIO', 'Subtitle')
        d.add_heading('Relazione annuale', 0)
        d.add_paragraph('Terza missione e Open Science')
        d.add_paragraph('Anno: {{Periodo}}')
        d.add_heading('1. Attivita e risultati', 1)
        d.add_paragraph('Sintesi: {{Sintesi}}')
        t = d.add_table(rows=1, cols=3)
        t.style = 'Light Shading Accent 1'
        for c, s in zip(t.rows[0].cells, ['Indicatore', 'Consuntivo', 'Fonte']): c.text = s
        for label, _, _, _ in facts[:5]:
            cells = t.add_row().cells
            cells[0].text = label
            cells[1].text = '{{' + label + '}}'
            cells[2].text = '{{Fonte ' + label + '}}'
        d.add_heading('2. Valutazione e approvazione', 1)
        d.add_paragraph('Gradimento delle attivita: {{Gradimento}}')
        d.add_paragraph('Referente per la validazione: {{Referente}}')
        d.add_paragraph('Note del responsabile: {{Note}}')
        d.save(base / 'modello.docx')
    elif n == 4:
        old = 'segreteria@dipartimento-esempio.it'
        new = 'segreteria@ateneo-esempio.it'
        for i in range(240):
            group = 'modificare' if i<150 else 'gia-corretto' if i<190 else 'simile' if i<220 else 'storico-da-esaminare'
            ext = ['.docx', '.docx', '.txt', '.html'][i%4]
            kind = ['modello', 'informativa', 'lettera', 'brochure', 'comunicazione'][i%5]
            p = inp / kind / f'{kind}_{i+1:03d}{ext}'
            address = old if i<150 or i>=220 else new if i<190 else 'ex-segreteria@dipartimento-esempio.it'
            lines = [f'Pratica: AMM-{i+1:03d}', 'Stato: COPIA STORICA - contatto citato in atto passato' if i>=220 else 'Stato: modello operativo corrente',
                     'Per informazioni scrivere a:', address,
                     'Altri contatti: segreteria.ricerca@dipartimento-esempio.it',
                     'Le modalita e le scadenze della procedura restano invariate.']
            make_file(p, 'Contatti della segreteria', lines, jobs)
            if ext == '.docx':
                d = Document(p)
                d.sections[0].header.paragraphs[0].text = 'ATENEO ESEMPIO / ' + address
                d.sections[0].footer.paragraphs[0].text = address
                t = d.add_table(rows=1, cols=2)
                t.cell(0,0).text = 'Contatto ufficio'
                t.cell(0,1).text = address
                d.save(p)
            if ext == '.html':
                p.write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>Contatti</title><body><h1>Contatti della segreteria</h1>' + ''.join('<p>'+html.escape(s)+'</p>' for s in lines) + '</body></html>', encoding='utf-8')
            truth.append({'file':p.relative_to(inp).as_posix(),'status':group})
    elif n == 5:
        from iscrizioni import generate_inputs
        truth = generate_inputs(base)
    elif n == 6:
        for i in range(150):
            historic = i >= 120
            section = 'archivio' if historic else ['servizi', 'ricerca', 'formazione'][i%3]
            p = inp / 'src' / section / f'pagina-{i+1:03d}.json'
            stale = i < 80 or historic
            target = 'formazione/pagina-003.html'
            broken = i < 45
            data = {'title':f'{"Archivio delle iniziative" if historic else "Laboratori e servizi"} {i+1:03d}',
                    'historic':historic, 'academic_year':'2025/2026' if stale else '2026/2027',
                    'body':'Calendario dei laboratori FAIR e dei servizi per il personale. Consulta il programma e i recapiti degli uffici.',
                    'links':[{'label':'Programma dei laboratori', 'href':'formazione/programma-2025.html' if broken else target},
                             {'label':'Archivio storico', 'href':'archivio/pagina-121.html'}]}
            save_json(p, data)
            truth.append({'file':p.relative_to(inp / 'src').as_posix(),'historic':historic,'stale':stale and not historic,'broken':broken})
        save_json(base/'redirects.json', {'formazione/programma-2025.html':'formazione/pagina-003.html'})
        from execute import build_site
        build_site(inp/'src', inp/'site')
    save_json(base / 'truth.json', truth)
    save_json(base / 'work/input-sha256.json', snapshot(inp))
    print(f'{base.name}: input pronto, {len(files(inp / "src" if n==6 else inp))} file', flush=True)


if __name__ == '__main__':
    generate(int(sys.argv[1]))
