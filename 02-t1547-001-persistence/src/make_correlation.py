"""Lab 02 diagram 2: process tree + Sysmon event correlation via shared ProcessGuid.
Navy flat-presentation style matching the repo. Defensive/educational content only."""
import math
from PIL import Image, ImageDraw, ImageFont

OUT="/workspace/soc-home-lab/02-t1547-001-persistence/diagrams/processguid-correlation.png"
W,H=1920,1080
BG="#0B1A33"; CARD="#13284A"; BORDER="#2A4A7A"; WHITE="#FFFFFF"; MUTED="#B8C7E0"
TEAL="#1FBFA8"; AMBER="#F5A623"; RED="#E5484D"; GREEN="#2ECC71"; GREY="#5B6F92"; BLUE="#4DA3FF"; PINK="#FF8A8A"
D="/usr/share/fonts/truetype/dejavu/"
def F(s,b=False): return ImageFont.truetype(D+("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),s)
def FM(s,b=False): return ImageFont.truetype(D+("DejaVuSansMono-Bold.ttf" if b else "DejaVuSansMono.ttf"),s)
fT=F(48,True); fS=F(26); fH=F(24,True); fB=F(20); fBb=F(20,True); fTag=F(18,True); fFoot=F(20)
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
M=60
def wrap(text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw or not cur: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def para(x,y,text,font,maxw,fill=WHITE,lh=26):
    for ln in wrap(text,font,maxw): d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y
def arrow(x1,y1,x2,y2,col=MUTED,width=5):
    d.line([x1,y1,x2,y2],fill=col,width=width)
    a=math.atan2(y2-y1,x2-x1); L=16
    p=[(x2,y2),(x2-L*math.cos(a-0.5),y2-L*math.sin(a-0.5)),(x2-L*math.cos(a+0.5),y2-L*math.sin(a+0.5))]
    d.polygon(p,fill=col)
def tag(x,y,text,col,font=fTag):
    tw=d.textlength(text,font=font)
    d.rounded_rectangle([x,y,x+tw+24,y+30],radius=15,fill=col)
    d.text((x+12,y+4),text,font=font,fill=WHITE if col==GREY else BG)
    return x+tw+24

d.text((M,30),"Process Tree + Event Correlation via shared ProcessGuid",font=fT,fill=WHITE)
d.text((M,94),"Two Sysmon events, one process. The ProcessGuid stitches 'what ran' to 'what it changed'.",font=fS,fill=MUTED)
d.rectangle([M,140,M+260,144],fill=TEAL)

# LEFT: process tree
LX=M; LW=760; TY=190
d.text((LX,TY),"PROCESS ANCESTRY",font=fH,fill=WHITE)
fm=FM(18); fmb=FM(18,True)
def proc(x,y,w,title,col,rows,pid):
    h=54+len(rows)*26+10
    d.rounded_rectangle([x,y,x+w,y+h],radius=12,fill=CARD,outline=col,width=2)
    d.rounded_rectangle([x,y,x+w,y+8],radius=4,fill=col)
    d.text((x+18,y+18),title,font=fbb if False else fBb,fill=WHITE)
    tag(x+w-96,y+16,pid,col)
    yy=y+52
    for k,v in rows:
        d.text((x+18,yy),k,font=fmb,fill=col); d.text((x+18+d.textlength(k+" ",font=fmb),yy),v,font=fm,fill=MUTED); yy+=26
    return h
fbb=fBb
h1=proc(LX+40,TY+48,LW-40,"cmd.exe  (parent)",GREY,
     [("Image ","C:\\Windows\\System32\\cmd.exe"),
      ("CmdLine ","cmd.exe /c REG ADD HKCU\\...\\Run ..."),
      ("PGUID ","{aa4fc3ef-d860-6ab5-7b02-...0700}")],"PID 3600")
y2=TY+48+h1+46
h2=proc(LX+120,y2,LW-120,"reg.exe  (child \u2014 LOLBin)",AMBER,
     [("Image ","C:\\Windows\\System32\\reg.exe"),
      ("OrigName ","reg.exe  \u00b7 FileVer 10.0.26100.5074"),
      ("cwd ","C:\\Users\\soclab1\\AppData\\Local\\Temp\\"),
      ("Integrity ","High   User: DESKTOP-0TMT1TC\\soclab1"),
      ("PGUID ","{aa4fc3ef-d860-6ab5-7d02-...0700}")],"PID 7428")
arrow(LX+60,TY+48+h1,LX+140,y2,MUTED)
# highlight child PGUID
d.text((LX+120,y2+h2+16),"\u2b07  same ProcessGuid links to the registry change \u2192",font=fBb,fill=TEAL)

# RIGHT: two event cards joined by ProcessGuid
RX=900; RW=W-M-RX; EY=238
def ev(y,eid,name,col,rows):
    h=64+len(rows)*28+8
    d.rounded_rectangle([RX,y,RX+RW,y+h],radius=12,fill=CARD,outline=col,width=2)
    d.rounded_rectangle([RX,y,RX+RW,y+8],radius=4,fill=col)
    d.ellipse([RX+16,y+22,RX+58,y+64],fill=col)
    tw=d.textlength(eid,font=fBb); d.text((RX+37-tw/2,y+33),eid,font=fBb,fill=BG)
    d.text((RX+70,y+20),name,font=fBb,fill=WHITE)
    yy=y+62
    for k,v in rows:
        d.text((RX+20,yy),k,font=fmb,fill=col); d.text((RX+20+d.textlength(k+" ",font=fmb),yy),v,font=fm,fill=MUTED); yy+=28
    return h
he1=ev(EY,"1","Sysmon 1 \u2014 Process Create",AMBER,
    [("UtcTime ","2026-09-25 02:11:44.966"),
     ("Image ","reg.exe   ParentImage: cmd.exe"),
     ("RuleName ","technique_id=T1012 (MISLABEL)"),
     ("ProcessGuid ","...-6ab5-7d02-000000000700")])
ey2=EY+he1+70
he2=ev(ey2,"13","Sysmon 13 \u2014 Registry SetValue",TEAL,
    [("UtcTime ","2026-09-25 02:11:44.997"),
     ("TargetObject ","HKU\\S-1-5-21-...-1001\\...\\Run\\Atomic Red Team"),
     ("Details ","C:\\Path\\AtomicRedTeam.exe"),
     ("RuleName ","technique_id=T1547.001 (correct)"),
     ("ProcessGuid ","...-6ab5-7d02-000000000700")])
# connecting line joining the two event cards (same-process linkage)
midx=RX-30
ytop=EY+he1-30; ybot=ey2+50
d.line([midx,ytop,midx,ybot],fill=TEAL,width=4)
arrow(midx,ytop,RX-4,ytop,TEAL)
arrow(midx,ybot,RX-4,ybot,TEAL)
# SHARED ProcessGuid callout in free lower-left space, wired to the event spine with an elbow
# connector (horizontal, then vertical) so the line never crosses text or boxes
sx,sy=LX+120,y2+h2+52
lbl="SHARED ProcessGuid  (unique per process)"
bw=int(d.textlength(lbl,font=fBb))+40
d.rounded_rectangle([sx,sy,sx+bw,sy+70],radius=10,fill="#0E2140",outline=TEAL,width=2)
d.text((sx+16,sy+10),lbl,font=fBb,fill=TEAL)
d.text((sx+16,sy+38),"...6ab5-7d02-000000000700",font=FM(18,True),fill=WHITE)
jy=sy+35
d.line([sx+bw,jy,midx,jy],fill=TEAL,width=4)
d.line([midx,jy,midx,ybot],fill=TEAL,width=4)
d.ellipse([midx-7,(ytop+ybot)//2-7,midx+7,(ytop+ybot)//2+7],fill=TEAL)

# bottom takeaway band
BY=sy+70+40; BH=H-30-BY
d.rounded_rectangle([M,BY,W-M,BY+BH],radius=16,fill="#0E2140",outline=BORDER,width=2)
d.text((M+24,BY+20),"WHY THIS MATTERS",font=fH,fill=WHITE)
y=para(M+24,BY+64,
 "PIDs get reused; ProcessGuid is unique per process. Pivoting on it joins the Event 1 execution record (LOLBin reg.exe, spawned by cmd.exe from a Temp directory) to the Event 13 registry write (a Run value pointing at non-standard C:\\Path). Same process, 31 ms apart: the persistence write is attributable to one specific execution.",
 F(24), W-2*M-48, fill=MUTED, lh=36)
d.text((M+24,y+16),"Hunt pivot:",font=F(24,True),fill=TEAL)
para(M+24+d.textlength("Hunt pivot: ",font=F(24,True)),y+16,
 "Sysmon 13 on ...\\CurrentVersion\\Run*  \u2192  join Sysmon 1 on ProcessGuid  \u2192  check parent, cwd, signer, Details path.",
 F(24), W-2*M-260, fill=WHITE, lh=36)
img.save(OUT)
print("saved",OUT)
