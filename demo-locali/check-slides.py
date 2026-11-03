"""Verifica del perimetro, degli asset e della geometria nel render finale."""
from pathlib import Path
import json
import re
import subprocess

root=Path(__file__).resolve().parent.parent
old=(root/'.demo-qa/index-original.qmd').read_bytes()
new=(root/'index.qmd').read_bytes()
marker=b'## come si procede?'
assert old.split(marker)[1]==new.split(marker)[1]
assert old.split(b'## {.dark')[0]==new.split(b'## Accio, ordine!')[0]
assert new.split(marker)[0].count(b'## Accio,')==6
assert new.count(b'link-external-newwindow: true')==1
html=(root/'index.html').read_text(encoding='utf-8')
imgs=re.findall(r'<img[^>]+src="([^"]+)"',html)
missing=[p for p in imgs if not p.startswith(('http:', 'https:', 'data:')) and not (root/p).is_file()]
assert not missing,missing
layout=json.loads((root/'.demo-qa/layout.json').read_text(encoding='utf-8'))
for slide in layout[1:7]:
    assert not slide['missing']
    for item in slide['items']:
        assert item['x']>=0 and item['y']>=0 and item['right']<=1600.1 and item['bottom']<850
        if 'demo-visual' in item['tag']:
            assert item['right']-item['x']>1400 and item['bottom']-item['y']>420
            assert '0px 0px' in item['shadow'] and item['shadow']!='none'
original_html=subprocess.run(['git','show','HEAD:index.html'],capture_output=True,check=True,cwd=root).stdout.decode('utf-8')
old_ids=re.findall(r'<section id="([^"]+)"',original_html)
new_ids=re.findall(r'<section id="([^"]+)"',html)
print('ID originali:',old_ids[:18])
print('ID finali:',new_ids[:22])
old_tail=old_ids[old_ids.index('come-si-procede'):]
new_tail=new_ids[new_ids.index('come-si-procede'):]
print('ID successivi invariati:',old_tail==new_tail)
assert old_tail==new_tail
old_body=original_html[original_html.index('<section id="come-si-procede"'):]
new_body=html[html.index('<section id="come-si-procede"'):]
print('HTML da come si procede identico:',old_body==new_body)
diff=subprocess.run(['git','diff','--','index.qmd'],capture_output=True,check=True,cwd=root).stdout
(root/'.demo-qa/index.qmd.diff').write_bytes(diff)
untracked=subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],capture_output=True,check=True,cwd=root).stdout.decode('utf-8').split('\0')
large=[p for p in untracked if p and (root/p).stat().st_size>2_000_000]
assert not large,large
assert not any('/input/' in p or '/output/' in p or '/work/' in p or '__pycache__' in p for p in untracked)
result={'nuove_demo':6,'copertina_qmd_identica':True,'qmd_da_come_si_procede_identico':True,
        'asset_mancanti':missing,'layout_1600x900':'superato','file_non_tracciati_oltre_2MB':large,
        'dataset_esclusi_da_git':True,'id_successivi_invariati':old_tail==new_tail,
        'html_successivo_identico':old_body==new_body,
        'file_nuovi_candidati_git':len([p for p in untracked if p]),
        'byte_file_nuovi_candidati_git':sum((root/p).stat().st_size for p in untracked if p)}
(root/'demo-locali/verifica-slide.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result)
