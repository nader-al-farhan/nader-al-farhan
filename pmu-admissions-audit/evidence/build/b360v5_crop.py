import json,datetime,hashlib,os
from PIL import Image,ImageDraw,ImageFont
J={j['eid']:j for j in json.load(open('jobs.json'))}
C={c['eid']:c for c in json.load(open('full/capture.json'))}
os.makedirs('final/orig',exist_ok=True); os.makedirs('final/ann',exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(F,22) if os.path.exists(F) else ImageFont.load_default()
D=1.5; out=[]
def riy(iso):
  t=datetime.datetime.fromisoformat(iso.replace('Z','+00:00'))+datetime.timedelta(hours=3); return t.strftime('%Y-%m-%d'),t.strftime('%H:%M:%S')
def fname(j,ann=False):
  pre=('F'+j['fid'][2:]) if j['fid'] else j['tev'].replace('-','')
  return f"{pre}_{j['eid']}_{j['name']}_20261022{'_ANNOTATED' if ann else ''}.png"
def annotate(im,boxes,j):
  W,H=im.size; band=48
  a=Image.new('RGB',(W,H+band),'white'); a.paste(im,(0,band)); d=ImageDraw.Draw(a)
  d.rectangle([0,0,W,band],fill=(31,56,100))
  lab=f"ANNOTATED COPY  ·  {j['eid']}  ·  {j['fid'] or j['tev']}  ·  frame added; not part of the source"
  d.text((16,12),lab,fill='white',font=font)
  for (x0,y0,x1,y1) in boxes: d.rectangle([x0-9,y0-9+band,x1+9,y1+9+band],outline=(192,0,0),width=5)
  return a
for eid,j in J.items():
  rec=dict(eid=eid,fid=j['fid'],tev=j['tev'],role=j['role'],name=j['name'])
  x0=0
  if j.get('pdf'):
    im=Image.open('pdf150-20.png'); x0,y0,x1,y1=int(100*D),int(560*D),int(700*D),int(712*D)
    o=im.crop((x0,y0,x1,y1)); boxes=[(int(152*D)-x0,int(689*D)-y0,int(372*D)-x0,int(705*D)-y0)]
    rec.update(url=j['pdf'],title='PMU Web Admission Guide (PDF)',page=20,date='2026-10-22',time='',section='PDF p. 20 – Signature Page, “Admission Requirements” list',etype='PDF page',view='PDF page 20 (crop of Admission Requirements block)',revealed=False)
  else:
    c=C[eid]; full=Image.open(f'full/{eid}_page.png'); b=c['doc']['box']; x=c['doc']['ctx']
    FIX={'E021':{'x':346.7,'y':1600.0,'w':583.3,'h':44.7},'E034':{'x':780.0,'y':358.0,'w':183.3,'h':31.3}}
    if eid in FIX: b=x=FIX[eid]; rec['frame_note']='frame positioned on the cited text after visual check'
    top=max(min(b['y'],x['y']),b['y']-420)-150; bot=min(max(b['y']+b['h'],x['y']+min(x['h'],520)),b['y']+b['h']+420)+150
    if bot-top<420: bot=top+420
    top=max(0,top); y0,y1=int(top*D),min(full.height,int(bot*D))
    L=max(0,min(b['x'],x['x'])-40); Rr=min(1280,max(b['x']+b['w'],x['x']+x['w'])+40)
    if Rr-L<760: c0=(L+Rr)/2; L=max(0,c0-380); Rr=min(1280,L+760); L=max(0,Rr-760)
    x0=int(L*D); x1=int(Rr*D)
    o=full.crop((x0,y0,x1,y1))
    boxes=[(int(b['x']*D)-x0,int(b['y']*D)-y0,int((b['x']+b['w'])*D)-x0,int((b['y']+b['h'])*D)-y0)]
    d,t=riy(c['at'])
    rec.update(url=j['url'],final=c['final'],title=c['title'],date=d,time=t,etype='Live web page',revealed=bool(c.get('revealed')),held=bool(j.get('block')),
      view='Desktop view'+('; published section expanded locally (hidden by default)' if c.get('revealed') else '')+('; page held without following its automatic redirect to the application portal' if j.get('block') else ''))
  o.save('final/orig/'+fname(j)); annotate(o,boxes,j).save('final/ann/'+fname(j,True))
  rec['orig']=fname(j); rec['ann']=fname(j,True); rec['size']=o.size
  rec['md5_orig']=hashlib.md5(open('final/orig/'+fname(j),'rb').read()).hexdigest()
  out.append(rec)
json.dump(out,open('final/visual.json','w'),indent=1,ensure_ascii=False)
print(len(out))
