// Catture Chromium delle schermate illustrative Windows 11 / Office.
// UI ricostruita su richiesta di Enrico; contenuti dai file verificati.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const puppeteer = require(process.env.DEMO_PUPPETEER || 'puppeteer');
const root = path.resolve(__dirname, '..');
const base = process.env.DEMO_BASE_URL || 'http://127.0.0.1:8765/';
const names=['01-ordine','02-informazione','03-burocrazia','04-aggiornamento','05-excel','06-sito'];
(async()=>{
  const browser=await puppeteer.launch({executablePath:process.env.DEMO_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--no-sandbox','--disable-gpu']});
  try {
    const page=await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request',r=>r.url().startsWith(base)||r.url().startsWith('data:')?r.continue():r.abort());
    if(process.argv[2]==='site') {
      await page.setViewport({width:1000,height:540,deviceScaleFactor:1.5});
      for (const [dir,label] of [['input','prima'],['output','dopo']]) {
        const url=base+`demo-locali/06-sito/${dir}/site/servizi/pagina-001.html`;
        await page.goto(url,{waitUntil:'networkidle0'});
        await page.screenshot({path:path.join(root,`figures/demo-06-sito-${label}.png`)});
      }
      // Navigazione vera nel browser: prima il link è rotto, dopo risponde 200.
      await page.goto(base+'demo-locali/06-sito/output/site/servizi/pagina-001.html');
      await Promise.all([page.waitForNavigation(),page.click('a')]);
      if(!page.url().endsWith('formazione/pagina-003.html')) throw Error('Destinazione errata');
      console.log('Navigazione nel browser: pagina corretta raggiunta');
      return;
    }
    if(process.argv[2]==='slides') {
      await page.setViewport({width:1600,height:900,deviceScaleFactor:1});
      await page.goto(base+'index.html',{waitUntil:'domcontentloaded'});
      await page.waitForFunction(()=>window.Reveal?.isReady());
      await page.evaluate(()=>Reveal.configure({transition:'none'}));
      const audit=[];
      const slideCount=await page.evaluate(()=>document.querySelectorAll('.reveal .slides>section').length);
      for(let i=0;i<Math.min(slideCount,8);i++) {
        await page.evaluate(i=>Reveal.slide(i,0,0),i);
        await new Promise(r=>setTimeout(r,1000));
        const report=await page.evaluate(()=>{
          const s=Reveal.getCurrentSlide();
          const a=s.getBoundingClientRect();
          return {id:s.id,slide:{x:a.x,y:a.y,width:a.width,height:a.height},
            missing:[...s.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),
            items:[...s.querySelectorAll('.demo-prompt,.demo-visual,.demo-caption,h2')].map(e=>{const r=e.getBoundingClientRect();return {tag:e.className||e.tagName,x:r.x,y:r.y,right:r.right,bottom:r.bottom,font:getComputedStyle(e).fontSize,shadow:getComputedStyle(e).boxShadow}})};
        });
        audit.push(report);
        await page.screenshot({path:path.join(root,`.demo-qa/slide-${i}.png`)});
      }
      fs.writeFileSync(path.join(root,'.demo-qa/layout.json'),JSON.stringify(audit,null,2));
      return;
    }
    await page.setViewport({width:1600,height:520,deviceScaleFactor:1});
    const selected = process.argv[2] && /^\d$/.test(process.argv[2]) ? Number(process.argv[2])-1 : null;
    const provenanceFile=path.join(root,'demo-locali/screenshot-provenienza.json');
    const previous=selected===null?[]:JSON.parse(fs.readFileSync(provenanceFile,'utf8'));
    const provenance=previous.filter(item=>item.file!==`figures/demo-${String((selected??0)+1).padStart(2,'0')}-confronto.png` && !(selected===4 && item.file==='figures/demo-05-attestato.png'));
    for(let i=0;i<6;i++){
      if(selected!==null && selected!==i) continue;
      const url=base+`demo-locali/${names[i]}/work/gallery.html`;
      await page.goto(url,{waitUntil:'networkidle0'});
      await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
      const target=`figures/demo-${String(i+1).padStart(2,'0')}-confronto.png`;
      await page.screenshot({path:path.join(root,target)});
      provenance.push({file:target,url,metodo:'Schermata illustrativa: interfaccia Windows 11 / Office ricostruita in HTML/CSS su richiesta di Enrico; dati dai file verificati, documenti da render PDF e sito locale. Non è una cattura desktop.',dimensioni:'1600 × 520',sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,target))).digest('hex')});
    }
    const support=[
      ['demo-02-delibera.png','demo-locali/02-informazione/input/2026/Ricerca/verbale_001.pdf','PDF originale rasterizzato e ritagliato'],
      ['demo-03-modello.png','demo-locali/03-burocrazia/modello.docx','Export Microsoft Word in PDF, rasterizzato e ritagliato'],
      ['demo-03-compilata.png','demo-locali/03-burocrazia/output/relazione-compilata.docx','Export Microsoft Word in PDF, rasterizzato e ritagliato'],
      ['demo-03-modello-campi.png','demo-locali/03-burocrazia/modello.docx','Export Microsoft Word: ritaglio dei campi da compilare'],
      ['demo-03-compilata-campi.png','demo-locali/03-burocrazia/output/relazione-compilata.docx','Export Microsoft Word: ritaglio dei campi da verificare'],
      ['demo-04-documento-prima.png','demo-locali/04-aggiornamento/input/modello/modello_001.docx','Export Microsoft Word in PDF, rasterizzato e ritagliato'],
      ['demo-04-documento-dopo.png','demo-locali/04-aggiornamento/output/documenti/modello/modello_001.docx','Export Microsoft Word in PDF, rasterizzato e ritagliato'],
      ['demo-05-attestato.png','demo-locali/05-excel/output/attestati/IS-0001_ada-esempio-01.pdf','Attestato di iscrizione PDF generato, rasterizzato e ritagliato'],
      ['demo-06-sito-prima.png','demo-locali/06-sito/input/site/servizi/pagina-001.html','Screenshot Chromium della build locale iniziale'],
      ['demo-06-sito-dopo.png','demo-locali/06-sito/output/site/servizi/pagina-001.html','Screenshot Chromium della build locale aggiornata']
    ];
    for(const [name,source,metodo] of support) {
      if(selected!==null && !(selected===4 && name==='demo-05-attestato.png')) continue;
      provenance.push({file:'figures/'+name,source,metodo,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'figures',name))).digest('hex')});
    }
    fs.writeFileSync(provenanceFile,JSON.stringify(provenance,null,2));
    console.log(selected===null?'Sei screenshot acquisiti':`Screenshot demo ${selected+1} acquisito`);
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
