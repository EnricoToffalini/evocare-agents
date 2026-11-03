"""Formati reali, estrazione e registri condivisi delle sei demo sintetiche."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches as PptInches
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
RUNTIME = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
NODE = Path(os.environ.get('DEMO_NODE', RUNTIME / 'node/bin/node.exe'))


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def files(path):
    return sorted(p for p in Path(path).rglob('*') if p.is_file())


def snapshot(path):
    return {p.relative_to(path).as_posix(): sha(p) for p in files(path)}


def pdf(path, title, lines, variant=0):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(595, 842), invariant=1)
    c.setAuthor('Materiali sintetici')
    c.setTitle(title)
    c.setFillColorRGB(.12, .23, .32)
    c.rect(0, 735, 595, 107, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont('Helvetica', 11)
    c.drawString(45, 802, 'ATENEO ESEMPIO  /  MATERIALE FITTIZIO')
    c.setFont('Helvetica-Bold', 21 if variant != 1 else 19)
    c.drawString(45, 765, title)
    c.setFillColorRGB(.12, .16, .2)
    y = 682 if variant != 2 else 650
    for line in lines:
        for part in simpleSplit(line, 'Helvetica', 12, 500):
            c.setFont('Helvetica', 12)
            c.drawString(45, y, part)
            y -= 19
        y -= 12
    c.setFont('Helvetica', 10)
    c.drawString(45, 70, 'Documento dimostrativo. Nessun valore amministrativo.')
    c.save()


def word(path, title, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    d = Document()
    sec = d.sections[0]
    sec.top_margin = sec.bottom_margin = Inches(.65)
    style = d.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(8)
    d.core_properties.author = 'Materiali sintetici'
    d.add_paragraph('ATENEO ESEMPIO · DOCUMENTO FITTIZIO', 'Subtitle')
    d.add_heading(title, 0)
    for line in lines:
        d.add_paragraph(line)
    d.save(path)


def image(path, title, lines):
    im = Image.new('RGB', (1100, 750), '#faf7ef')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 28)
    draw.text((45, 40), 'ATENEO ESEMPIO / FITTIZIO', fill='#536174', font=font)
    draw.text((45, 110), title, fill='#17283d', font=font)
    for i, line in enumerate(lines):
        draw.text((45, 200 + i * 55), line, fill='#17283d', font=font)
    # Il contenuto visivo va letto con OCR o visione: il riferimento lo lascia dubbio.
    im.save(path)


def text(path):
    ext = path.suffix.lower()
    if ext == '.pdf':
        return '\n'.join(p.extract_text() or '' for p in PdfReader(path).pages)
    if ext == '.docx':
        d = Document(path)
        return '\n'.join([p.text for p in d.paragraphs] +
                         [c.text for t in d.tables for r in t.rows for c in r.cells] +
                         [p.text for s in d.sections for p in s.header.paragraphs] +
                         [p.text for s in d.sections for p in s.footer.paragraphs])
    if ext == '.xlsx':
        w = load_workbook(path, read_only=True, data_only=True)
        s = '\n'.join(str(v) for sheet in w for row in sheet for cell in row if (v := cell.value) is not None)
        w.close()
        return s
    if ext == '.pptx':
        return '\n'.join(sh.text for sl in Presentation(path).slides for sh in sl.shapes if sh.has_text_frame)
    if ext == '.zip':
        with ZipFile(path) as z:
            return '\n'.join(z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('.txt'))
    if ext in ('.png', '.jpg'):
        return ''
    return path.read_text(encoding='utf-8')


def make_file(path, title, lines, xlsx_jobs=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix
    if ext == '.pdf':
        pdf(path, title, lines)
    elif ext == '.docx':
        word(path, title, lines)
    elif ext == '.xlsx':
        xlsx_jobs.append({'path': str(path), 'title': title,
                          'headers': ['Campo', 'Contenuto'],
                          'rows': [[f'Voce {i+1}', v] for i, v in enumerate(lines)]})
    elif ext == '.pptx':
        p = Presentation()
        sl = p.slides.add_slide(p.slide_layouts[1])
        sl.shapes.title.text = title
        sl.placeholders[1].text = '\n'.join(lines)
        p.core_properties.author = 'Materiali sintetici'
        p.save(path)
    elif ext in ('.png', '.jpg'):
        image(path, title, lines)
    elif ext == '.zip':
        with ZipFile(path, 'w', ZIP_DEFLATED) as z:
            z.writestr('contenuto.txt', title + '\n' + '\n'.join(lines))
    else:
        path.write_text(title + '\n' + '\n'.join(lines), encoding='utf-8')


def xlsx(jobs, base):
    job_path = base / 'work/xlsx-jobs.json'
    save_json(job_path, jobs)
    with (base/'work/xlsx-build.log').open('w', encoding='utf-8') as log:
        subprocess.run([str(NODE), str(ROOT / 'workbooks.mjs'), str(job_path)], check=True, stdout=log, stderr=subprocess.STDOUT)


def report(base, summary, records):
    out = base / 'output'
    out.mkdir(exist_ok=True)
    save_json(out / 'verifica.json', {'provenienza': 'Output di riferimento generato tramite script; non è una trascrizione di agent interattivo.', **summary})
    if records:
        with (out / 'operazioni.csv').open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(records[0]))
            w.writeheader()
            w.writerows(records)
    (out / 'resoconto.txt').write_text('\n'.join(f'{k}: {v}' for k, v in summary.items()), encoding='utf-8')
    print(base.name, summary, flush=True)


def field(s, label):
    m = re.search(r'^' + re.escape(label) + r':\s*(.*)$', s, re.M)
    return m.group(1).strip() if m else ''


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
