"""Build locale autonoma, da copiare insieme ai sorgenti per la demo dal vivo.
Uso: python build.py input/src site
"""
from pathlib import Path
import html
import json
import os
import sys


def files(path):
    return sorted(p for p in Path(path).rglob('*') if p.is_file())


def build_site(src, out):
    src, out = Path(src), Path(out)
    css = 'body{margin:0;font:20px/1.5 Arial;background:#f5f7fa;color:#192e42}header{padding:18px 48px;background:#173a50;color:white;font-size:17px}main{max-width:1000px;margin:40px auto;background:white;padding:36px 44px;border-radius:12px}h1{font-size:34px;margin:0 0 20px}h2{font-size:26px}.year{font-size:30px;color:#8a315c;font-weight:bold}a{color:#155f89}nav{display:flex;gap:28px;padding:12px 0}aside{background:#eef3f7;padding:18px;margin-top:24px;font-size:17px}'
    for p in files(src):
        d = json.loads(p.read_text(encoding='utf-8'))
        rel = p.relative_to(src).with_suffix('.html')
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        links = ''.join(f'<li><a href="{os.path.relpath(out / x["href"], target.parent).replace(chr(92), chr(47))}">{html.escape(x["label"])}</a></li>' for x in d['links'])
        target.write_text('<!doctype html><html lang="it"><meta charset="utf-8"><title>'+html.escape(d['title'])+'</title><style>'+css+'</style><header>ATENEO ESEMPIO / Terza missione e Open Science · Sito dimostrativo locale</header><main><nav>Servizi &nbsp; / &nbsp; Ricerca &nbsp; / &nbsp; Formazione</nav><h1>'+html.escape(d['title'])+'</h1><p class="year">Anno accademico '+d['academic_year']+'</p><p>'+html.escape(d['body'])+'</p><h2>Informazioni e programmi</h2><ul>'+links+'</ul><aside>'+('Pagina di archivio: si conserva il contesto storico.' if d['historic'] else 'Pagina corrente per il personale. Materiali e recapiti nel programma collegato.')+'</aside></main></html>', encoding='utf-8')


if __name__=='__main__':
    build_site(sys.argv[1],sys.argv[2])
    print(f'Build completata: {len(files(sys.argv[2]))} pagine HTML')
