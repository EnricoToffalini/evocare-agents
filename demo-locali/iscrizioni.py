"""Demo inversa: moduli di iscrizione/pagamento -> registro -> attestati PDF."""
from common import *
from pypdf import PdfWriter
from collections import Counter, defaultdict


PROMPT = ('Ho 600 iscritti nel modulo di iscrizione. Incrocia i dati con questi altri moduli e controlla chi ha pagato. '
          'Poi prepara gli attestati PDF personalizzati, pronti da stampare, per tutti quelli in regola. '
          'Segnala i pagamenti mancanti e i casi dubbi.')


def generate_inputs(base):
    names=['Ada','Bruno','Celia','Dario','Elena','Fabio','Gemma','Ivo','Lia','Nereo']
    surnames=['Esempio','Fittizi','Inventati','Dimostrativi','Sintetici','Prova']
    registrations=[]
    bank=[]
    online=[]
    truth=[]
    for i in range(600):
        identifier=f'IS-{i+1:04d}'
        name=f'{names[i%10]} {surnames[(i//10)%6]} {i//60+1:02d}'
        registrations.append([identifier,name,'Laboratorio Open Science','2026-11-04',40])
        status='Pagato' if i<560 else 'Non pagato' if i<588 else 'Da verificare'
        truth.append({'id':identifier,'name':name,'status':status})
        if i<560 or i>=588:
            amount=20 if 588<=i<594 else 40
            settled='IN ATTESA' if i>=594 else 'ACCREDITATO'
            row=[f'TX-{i+1:04d}',identifier,name,amount,settled,'2026-10-30']
            (bank if i<300 else online).append(row)
    # Le stesse otto ricevute sono esportate anche nel secondo modulo.
    online.extend([row.copy() for row in bank[4:12]])
    payment_headers=['Transazione','ID iscrizione','Ordinante','Importo EUR','Esito','Data']
    xlsx([
        {'path':str(base/'input/iscrizioni.xlsx'),'title':'Iscrizioni al laboratorio (dati sintetici)',
         'headers':['ID iscrizione','Nominativo','Attivita','Data attivita','Quota EUR'],
         'rows':registrations,'widths':{'A':20,'B':30,'C':34,'D':20,'E':16},'moneyCols':['E']},
        {'path':str(base/'input/bonifici.xlsx'),'title':'Modulo bonifici (dati sintetici)',
         'headers':payment_headers,'rows':list(reversed(bank)),
         'widths':{'A':22,'B':20,'C':30,'D':18,'E':22,'F':20},'moneyCols':['D']},
        {'path':str(base/'input/pagamenti-online.xlsx'),'title':'Modulo pagamenti online (dati sintetici)',
         'headers':payment_headers,'rows':list(reversed(online)),
         'widths':{'A':22,'B':20,'C':30,'D':18,'E':22,'F':20},'moneyCols':['D']}
    ],base)
    return truth


def workbook_rows(path):
    w=load_workbook(path,read_only=True,data_only=True)
    rows=list(w.active.iter_rows(min_row=6,values_only=True))
    w.close()
    return rows


def issue_certificates(base):
    inp,out=base/'input',base/'output'
    certs=out/'attestati'
    certs.mkdir(parents=True,exist_ok=True)
    payments=defaultdict(list)
    seen={}
    duplicates=0
    for source in ['bonifici.xlsx','pagamenti-online.xlsx']:
        for number,row in enumerate(workbook_rows(inp/source),6):
            tx,key,name,amount,status,date=row
            if tx in seen:
                assert seen[tx]==row, 'Transazione duplicata con dati discordanti'
                duplicates+=1
                continue
            seen[tx]=row
            payments[key].append({'amount':float(amount),'status':status,
                                  'source':f'{source} / Registro / riga {number}','tx':tx})
    records=[]
    rows=[]
    paths=[]
    for key,name,activity,date,fee in workbook_rows(inp/'iscrizioni.xlsx'):
        matches=payments[key]
        amount=sum(p['amount'] for p in matches if p['status']=='ACCREDITATO')
        status='Non pagato' if not matches else 'Pagato' if amount==fee and all(p['status']=='ACCREDITATO' for p in matches) else 'Da verificare'
        source='; '.join(p['source'] for p in matches)
        filename=''
        reason='Nessun pagamento trovato' if not matches else 'Importo o esito da verificare' if status=='Da verificare' else ''
        if status=='Pagato':
            filename=f'{key}_{slug(name)}.pdf'
            p=certs/filename
            pdf(p,"Attestato d'iscrizione",[
                f'Identificativo: {key}',f'Nominativo: {name}',f'Attivita: {activity}',
                f'Data attivita: {date}',f'Quota di iscrizione: {fee:.0f} EUR - pagamento verificato.',
                "Si conferma l'iscrizione al laboratorio indicato.",
                'Il presente documento non certifica la partecipazione effettiva.',
                'Nominativo inventato. Materiale esclusivamente dimostrativo.'])
            paths.append(p)
        records.append({'id':key,'nominativo':name,'quota':fee,'pagato':amount,'stato':status,
                        'fonte':source,'pdf':filename,'nota':reason})
        rows.append([key,name,fee,amount,status,filename,source,reason])
    writer=PdfWriter()
    for p in paths: writer.append(str(p))
    with (out/'attestati-stampa.pdf').open('wb') as f: writer.write(f)
    writer.close()
    xlsx([{'path':str(out/'registro-iscrizioni.xlsx'),'title':'Iscrizioni, pagamenti e attestati (sintetico)',
           'headers':['ID','Nominativo','Quota EUR','Pagato EUR','Esito','Attestato PDF','Fonte pagamento','Note'],
           'rows':rows,'statusCol':'E','moneyCols':['C','D'],
           'widths':{'A':16,'B':30,'C':16,'D':16,'E':22,'F':52,'G':68,'H':40},
           'preview':str(out/'registro-render.png'),'previewRange':'A1:E13'}],base)
    counts=Counter(r['stato'] for r in records)
    summary={'iscritti':len(records),'pagamenti_unici':len(seen),'pagamenti_duplicati_ignorati':duplicates,
             'pagati':counts['Pagato'],'non_pagati':counts['Non pagato'],'da_verificare':counts['Da verificare'],
             'attestati_pdf':len(paths),'pagine_fascicolo_stampa':len(PdfReader(out/'attestati-stampa.pdf').pages),
             'tipo_attestato':"iscrizione, senza attestare la presenza"}
    return records,summary


def verify_outputs(base,truth,result):
    rows=workbook_rows(base/'output/registro-iscrizioni.xlsx')
    expected={r['id']:r for r in truth}
    assert len(rows)==len(expected)==600
    pdf_ids=set()
    for row in rows:
        key,name,fee,amount,status,filename,source,note=row
        t=expected[key]
        assert name==t['name'] and status==t['status']
        if status=='Pagato':
            assert amount==fee==40 and filename and source
            p=base/'output/attestati'/filename
            d=PdfReader(p)
            assert len(d.pages)==1
            s=d.pages[0].extract_text()
            assert key in s and name in s and 'pagamento verificato' in s
            assert abs(float(d.pages[0].mediabox.width)-595)<1
            assert abs(float(d.pages[0].mediabox.height)-842)<1
            pdf_ids.add(key)
        else:
            assert not filename and note
    assert len(pdf_ids)==len(files(base/'output/attestati'))==560
    combined=PdfReader(base/'output/attestati-stampa.pdf')
    assert len(combined.pages)==560
    combined_ids={field(page.extract_text(),'Identificativo') for page in combined.pages}
    assert combined_ids==pdf_ids
    assert result['pagati']==560 and result['non_pagati']==28 and result['da_verificare']==12
    assert result['pagamenti_duplicati_ignorati']==8
