"""Controlli indipendenti: confronta output riletti con verità dei generatori."""
from common import *
from collections import Counter
from execute import broken_links


def verify(n):
    base = sorted(ROOT.glob(f'{n:02d}-*'))[0]
    inp, out = base/'input', base/'output'
    truth = json.loads((base/'truth.json').read_text(encoding='utf-8'))
    result = json.loads((out/'verifica.json').read_text(encoding='utf-8'))
    original = json.loads((base/'work/input-sha256.json').read_text(encoding='utf-8'))
    assert original == snapshot(inp)
    if n==1:
        records = list(csv.DictReader((out/'operazioni.csv').open(encoding='utf-8-sig')))
        assert len(records)==len(truth)==1200
        assert result['duplicati']==40
        categories = {r['file']:r.get('category') for r in truth if 'category' in r}
        # Il primo esemplare può essere una copia: il confronto delle categorie
        # si riferisce al contenuto originale del gruppo, non al nome della copia.
        original_by_hash = {sha(inp/name):cat for name,cat in categories.items()}
        for r in records:
            if r['categoria']!='Duplicati': assert r['categoria']==original_by_hash[r['sha256']]
            assert sha(out/r['destinazione'])==r['sha256']
        assert Counter(sha(p) for p in files(out/'Download-ordinato'))==Counter(original.values())
    elif n==2:
        w=load_workbook(out/'finanziamenti.xlsx',data_only=True)
        rows=list(w.active.iter_rows(min_row=6,values_only=True))
        assert len(rows)==24
        expected={r['file']:r for r in truth}
        for r in rows:
            t=expected[r[7]]
            assert r[0]==t['key'] and r[2]==t['amount'] and r[6]==t['status']
            assert r[8] and (inp/r[7]).is_file()
        assert sum(r[6]=='Contraddizione' for r in rows)==4
        w.close()
    elif n==3:
        s=text(out/'relazione-compilata.docx')
        provenance=json.loads((out/'provenienza.json').read_text(encoding='utf-8'))
        for fact in truth:
            assert fact['value'] in s and provenance[fact['label']]==[fact['value'],fact['file']]
            if fact['label']!='Periodo': assert fact['file'] in s
        assert s.count('DA VERIFICARE')==2 and '{{' not in s
        a,b=Document(base/'modello.docx'),Document(out/'relazione-compilata.docx')
        assert a.tables[0]._tbl.tblPr.xml==b.tables[0]._tbl.tblPr.xml
        assert a.sections[0]._sectPr.xml==b.sections[0]._sectPr.xml
    elif n==4:
        records=list(csv.DictReader((out/'operazioni.csv').open(encoding='utf-8-sig')))
        expected={'modificare':'Modificato','gia-corretto':'Gia corretto','simile':'Non pertinente','storico-da-esaminare':'Da esaminare'}
        by_path={r['file']:r for r in records}
        for t in truth:
            r=by_path[t['file']]
            assert r['stato']==expected[t['status']]
            if t['status']=='modificare': assert r['vecchio_indirizzo_dopo']=='0'
            else: assert sha(inp/t['file'])==sha(out/'documenti'/t['file'])
        assert result['modificati']==150 and result['gia_corretti']==40
    elif n==5:
        from iscrizioni import verify_outputs
        verify_outputs(base, truth, result)
    elif n==6:
        assert len(files(out/'src'))==len(files(out/'site'))==150
        for t in truth:
            before=inp/'src'/t['file']; after=out/'src'/t['file']
            if t['historic']: assert sha(before)==sha(after)
            else: assert json.loads(after.read_text(encoding='utf-8'))['academic_year']=='2026/2027'
        checked,bad=broken_links(out/'site')
        assert checked==300 and not bad
    save_json(base/'verifica-eseguita.json',{'demo':n,'controlli_indipendenti':'superati','risultati':result})
    print(f'Demo {n}: controlli indipendenti superati',flush=True)


if __name__=='__main__':
    for n in ([int(sys.argv[1])] if len(sys.argv)>1 else range(1,7)): verify(n)
