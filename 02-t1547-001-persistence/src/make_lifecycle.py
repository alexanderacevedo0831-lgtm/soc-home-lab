"""Lab 02 diagram 1: Registry Run Key persistence lifecycle (attack -> detect -> contain -> verify).
Navy flat-presentation style, matching Lab 01 / threat-context slides. Defensive/educational content only."""
import math
from PIL import Image, ImageDraw, ImageFont

OUT = "/workspace/soc-home-lab/02-t1547-001-persistence/diagrams/persistence-lifecycle.png"
W, H = 1920, 1080
BG="#0B1A33"; CARD="#13284A"; BORDER="#2A4A7A"; WHITE="#FFFFFF"; MUTED="#B8C7E0"
TEAL="#1FBFA8"; AMBER="#F5A623"; RED="#E5484D"; GREEN="#2ECC71"; GREY="#5B6F92"; BLUE="#4DA3FF"; PINK="#FF8A8A"
D="/usr/share/fonts/truetype/dejavu/"
def F(s,b=False): return ImageFont.truetype(D+("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),s)
def FM(s,b=False): return ImageFont.truetype(D+("DejaVuSansMono-Bold.ttf" if b else "DejaVuSansMono.ttf"),s)
fT=F(48,True); fS=F(26); fH=F(24,True); fB=F(20); fBb=F(20,True); fTag=F(18,True); fFoot=F(20); fMono=FM(18)
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
def para(x,y,text,font,maxw,fill=WHITE,lh=28):
    for ln in wrap(text,font,maxw): d.text((x,y),ln,font=font,fill=fill); y+=lh
    return y
def arrow(x1,y1,x2,y2,col=MUTED,width=6):
    d.line([x1,y1,x2,y2],fill=col,width=width)
    a=math.atan2(y2-y1,x2-x1); L=18
    p=[(x2,y2),(x2-L*math.cos(a-0.5),y2-L*math.sin(a-0.5)),(x2-L*math.cos(a+0.5),y2-L*math.sin(a+0.5))]
    d.polygon(p,fill=col)
def tag(x,y,text,col,font=fTag):
    tw=d.textlength(text,font=font)
    d.rounded_rectangle([x,y,x+tw+24,y+30],radius=15,fill=col)
    d.text((x+12,y+4),text,font=font,fill=WHITE if col==GREY else BG)
    return x+tw+24

# header
d.text((M,30),"T1547.001 Run Key Persistence: Attack \u2192 Detect \u2192 Contain \u2192 Verify",font=fT,fill=WHITE)
d.text((M,94),"SOC-LAB1 \u00b7 CASE-002 \u00b7 full lifecycle captured by host sensors, no telemetry gap",font=fS,fill=MUTED)
d.rectangle([M,140,M+260,144],fill=TEAL)

phases=[
 ("1","ATTACK",AMBER,"T1547.001",
  ["Atomic test #1 'Reg Key Run' from admin PowerShell.",
   "cmd.exe /c REG ADD writes a value to HKCU\\...\\Run pointing at C:\\Path\\AtomicRedTeam.exe.",
   "Survives reboot; runs at next logon."]),
 ("2","DETECT",TEAL,"Sysmon 1 + 13",
  ["Event 1: reg.exe process create, parent cmd.exe, Temp cwd.",
   "Event 13: SetValue on the Run key, Details = the payload path.",
   "Both share ProcessGuid \u2192 one action, correlated."]),
 ("3","CONTAIN",PINK,"Manual response",
  ["Export Run key to evidence .reg first.",
   "Confirm payload not present / not running.",
   "Remove-ItemProperty deletes the value; sweep RunOnce, HKLM, Startup."]),
 ("4","VERIFY",GREEN,"Log off / on",
  ["Fresh logon: HKCU Run shows only OneDrive + Edge.",
   "Atomic value gone.",
   "Sysmon replays both the add and the delete: lifecycle proven."]),
]
GAP=36; CW=(W-2*M-3*GAP)//4; CH=560; Y0=190
for i,(n,title,col,tid,bullets) in enumerate(phases):
    x=M+i*(CW+GAP)
    d.rounded_rectangle([x,Y0,x+CW,Y0+CH],radius=16,fill=CARD,outline=BORDER,width=2)
    d.rounded_rectangle([x,Y0,x+CW,Y0+10],radius=5,fill=col)
    d.ellipse([x+18,Y0+30,x+66,Y0+78],fill=col)
    tw=d.textlength(n,font=fH); d.text((x+42-tw/2,Y0+42),n,font=fH,fill=BG)
    d.text((x+80,Y0+34),title,font=F(30,True),fill=WHITE)
    d.text((x+80,Y0+70),"ATT&CK "+tid,font=fBb,fill=col) if False else None
    tag(x+18,Y0+96,tid,col)
    ty=Y0+150
    for b in bullets:
        d.ellipse([x+20,ty+8,x+30,ty+18],fill=col)
        ty=para(x+42,ty,b,fB,CW-60,lh=27)+14
Y_ARR=Y0+CH//2
for i in range(3):
    x=M+(i+1)*(CW+GAP)-GAP+2
    arrow(x-30,Y_ARR,x+GAP-4,Y_ARR,MUTED)

# bottom evidence band
BY=Y0+CH+70; BH=190
d.rounded_rectangle([M,BY,W-M,BY+BH],radius=16,fill="#0E2140",outline=BORDER,width=2)
d.text((M+24,BY+16),"KEY EVIDENCE (UTC)",font=fH,fill=WHITE)
tag(M+320,BY+16,"correlated by ProcessGuid {aa4fc3ef-d860-6ab5-7d02-000000000700}",BLUE,font=fMono)
lines=[
 ("02:11:44.966","Sysmon 1","reg.exe (PID 7428) created by cmd.exe (PID 3600), IntegrityLevel High, cwd = ...\\Temp",AMBER),
 ("02:11:44.997","Sysmon 13","SetValue HKU\\...\\Run\\Atomic Red Team = C:\\Path\\AtomicRedTeam.exe  (RuleName tag T1547.001)",TEAL),
 ("post-run","Sysmon 12/13","Added/Deleted value event captured when the Run value was removed \u2192 add + delete both logged",GREEN),
]
ty=BY+58
for tsp,ev,txt,col in lines:
    d.text((M+24,ty),tsp,font=FM(19,True),fill=col)
    d.text((M+220,ty),ev,font=fBb,fill=col)
    d.text((M+400,ty),txt,font=fMono,fill=WHITE)
    ty+=40

fy=H-46
d.text((M,fy),"Lesson: Sysmon Event 1 RuleName read technique_id=T1012 (Query Registry) \u2014 a config MISLABEL. The command line (REG ADD) is truth; ATT&CK tags are hints.",font=fFoot,fill=MUTED)
img.save(OUT)
print("saved",OUT)
