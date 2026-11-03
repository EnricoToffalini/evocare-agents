// Scrittura dei veri XLSX con Artifact Tool. Input: dati estratti dai file.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const runtime = process.env.DEMO_ARTIFACT_TOOL || path.join(process.env.USERPROFILE, '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs');
const {Workbook, SpreadsheetFile} = await import(pathToFileURL(runtime));
const jobs = JSON.parse(await fs.readFile(process.argv[2], 'utf8'));
for (const [index, job] of jobs.entries()) {
  const w = Workbook.create();
  const s = w.worksheets.add(job.sheet || 'Registro');
  s.showGridLines = false;
  s.getRange('A2').values = [[job.title]];
  const n = job.headers.length;
  const last = String.fromCharCode(64+n);
  const end = 5 + job.rows.length;
  s.getRange(`A5:${last}${end}`).values = [job.headers, ...job.rows];
  const r = s.getRange(`A1:${last}${end}`);
  r.format.font = {name: 'Arial', size: 11, color:'#182b3a'};
  r.format.rowHeight = 28;
  r.format.columnWidth = 22;
  r.format.verticalAlignment = 'center';
  s.getRange('A2').format.font = {size:16, bold:true};
  s.getRange(`A5:${last}5`).format = {fill:'#183d51',font:{bold:true,color:'#ffffff'},rowHeight:32};
  s.tables.add(`A5:${last}${end}`,true,`Registro${index+1}`);
  s.freezePanes.freezeRows(5);
  for (const [col, width] of Object.entries(job.widths || {})) s.getRange(`${col}1:${col}${end}`).format.columnWidth = width;
  for (const col of job.dateCols || []) s.getRange(`${col}6:${col}${end}`).setNumberFormat('dd/mm/yyyy');
  for (const col of job.moneyCols || []) s.getRange(`${col}6:${col}${end}`).setNumberFormat('#,##0.00 "EUR"');
  if(job.statusCol) {
    const target = s.getRange(`A6:${last}${end}`);
    target.conditionalFormats.addCustom(`$${job.statusCol}6="Da verificare"`, {fill:'#fff0bb'});
    target.conditionalFormats.addCustom(`$${job.statusCol}6="Contraddizione"`, {fill:'#ffd9d3'});
    target.conditionalFormats.addCustom(`$${job.statusCol}6="Incompleto"`, {fill:'#fff0bb'});
    target.conditionalFormats.addCustom(`$${job.statusCol}6="Duplicato"`, {fill:'#e5e7eb'});
  }
  for(const [cell, value] of Object.entries(job.cells || {})) s.getRange(cell).values = [[value]];
  for(const [cell, formula] of Object.entries(job.formulas || {})) s.getRange(cell).formulas = [[formula]];
  w.recalculate();
  await fs.mkdir(path.dirname(job.path), {recursive:true});
  await (await SpreadsheetFile.exportXlsx(w)).save(job.path);
  // L'export scrive un sidecar diagnostico: non fa parte del dataset.
  const sidecar = job.path + '.inspect.ndjson';
  try { await fs.rename(sidecar, path.join(path.dirname(process.argv[2]), `xlsx-${index+1}.inspect.ndjson`)); }
  catch(e) { if(e.code !== 'ENOENT') throw e; }
  if (job.preview) {
    const blob = await w.render({sheetName:s.name,range:job.previewRange || `A1:${last}13`,scale:1.5,format:'png'});
    await fs.writeFile(job.preview, new Uint8Array(await blob.arrayBuffer()));
    await fs.writeFile(job.path+'.inspect.json', (await w.inspect({kind:'table',range:`${s.name}!A1:${last}12`,include:'values,formulas',tableMaxRows:12,tableMaxCols:12})).ndjson);
  }
  if(index % 50 === 0) console.log(`XLSX ${index+1}/${jobs.length}`);
}
