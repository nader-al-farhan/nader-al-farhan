"""Open the .docx in LibreOffice (headless, via UNO), update the table of contents and all
fields, and export a PDF that matches the Word layout. Usage: python3 to_pdf.py in.docx out.pdf"""
import os, subprocess, sys, tempfile, time
sys.path.insert(0, os.environ["DOCX_SKILL"] + "/scripts")
from office.soffice import get_soffice_env
import uno
from com.sun.star.beans import PropertyValue

def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p

src, out = map(os.path.abspath, sys.argv[1:3])
profile = tempfile.mkdtemp(prefix="lo-")
port = 2002
proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore", "--nologo", f"-env:UserInstallation=file://{profile}",
                         f"--accept=socket,host=127.0.0.1,port={port};urp;"], env=get_soffice_env(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ctx = uno.getComponentContext()
    resolver = ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx)
    for _ in range(60):
        try:
            rc = resolver.resolve(f"uno:socket,host=127.0.0.1,port={port};urp;StarOffice.ComponentContext"); break
        except Exception:
            time.sleep(1)
    desktop = rc.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", rc)
    doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (prop("Hidden", True),))
    for _ in range(2):  # twice: page numbers settle after the TOC itself is filled
        idx = doc.getDocumentIndexes()
        for i in range(idx.getCount()):
            idx.getByIndex(i).update()
        doc.getTextFields().refresh()
    doc.storeToURL(uno.systemPathToFileUrl(out), (prop("FilterName", "writer_pdf_Export"),
        prop("FilterData", uno.Any("[]com.sun.star.beans.PropertyValue", tuple([prop("UseTaggedPDF", True), prop("ExportBookmarks", True), prop("ExportNotes", False), prop("Quality", 90)])))))
    print("pages:", doc.getCurrentController().getPropertyValue("PageCount") if hasattr(doc.getCurrentController(), "getPropertyValue") else "?")
    doc.close(True)
finally:
    proc.terminate()
    try: proc.wait(10)
    except Exception: proc.kill()
print("wrote", out)
