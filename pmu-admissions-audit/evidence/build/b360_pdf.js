// Render an HTML report to PDF with Chromium. Usage: node b360_pdf.js in.html out.pdf "footer label"
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [inp, out, label] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true, displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font-size:7.5px;color:#595959;font-family:Inter,sans-serif;padding:0 14mm;display:flex;justify-content:space-between"><span>${label}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>` });
  await b.close(); console.log('pdf ok', out);
})();
