from PIL import Image, ImageDraw, ImageFont
W,H=1920,1080
BG="#0B1A33"; CARD="#13284A"; BORDER="#2A4A7A"; WHITE="#FFFFFF"; MUTED="#B8C7E0"
TEAL="#1FBFA8"; AMBER="#F5A623"; RED="#E5484D"; GREEN="#2ECC71"; GREY="#5B6F92"; BLUE="#4DA3FF"
D="/usr/share/fonts/truetype/dejavu/"
def F(s,b=False): return ImageFont.truetype(D+("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),s)
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
fT,fS=F(46,True),F(26); fH=F(23,True); fB=F(20); fBb=F(20,True); fTag=F(18,True); fBand=F(20,True); fFoot=F(20)
def wrap(text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
d.text((60,30),"Ransomware Payday Kill-Path: Hospital Target",font=fT,fill=WHITE)
d.text((60,92),"Attacker goal: get paid fast. Blue-team goal: break the chain at steps 1-5.",font=fS,fill=MUTED)
d.rectangle([60,138,260,142],fill=TEAL)
steps=[
("1","Log in with bought creds","T1078","4624/4625 odd source, spray","disable acct, reset, MFA","LATER LAB",GREY),
("2","Run commands","T1059.001","4104, Sysmon 1","kill proc, CLM/ASR","LAB 1 DONE",GREEN),
("3","Survive reboot","T1547.001","Sysmon 13","delete Run key, kill proc","LAB 2 NEXT",AMBER),
("4","Steal admin creds","T1003.001","Sysmon 10 on lsass","LSA Protection, Cred Guard","LATER LAB",GREY),
("5","Map the hospital","T1087/T1082","4688 net/whoami/nltest burst","isolate host","ADD-ON",BLUE),
("6","Spread to servers","T1021","4624 type 3/10 host-to-host","segment, block admin shares","NEEDS 2ND VM",GREY),
("7","Kill recovery","T1490","4688 vssadmin delete shadows","ASR, offline backups","GOOD LAB",TEAL),
("8","Steal PHI","T1567","Sysmon 3 large outbound","egress filter, DLP","LATER",GREY),
("9","Encrypt","T1486","Sysmon 11 mass writes","isolate now","SIMULATED ONLY",RED),
]
M=60; GAP=42; BW=(W-2*M-4*GAP)//5; BH=330
xs=[M+i*(BW+GAP) for i in range(5)]
Y1=200; Y2=Y1+BH+95
def band(y,h,label,col):
    d.rounded_rectangle([M-20,y-50,W-M+20,y+h+14],radius=16,outline=col,width=2)
    tw=d.textlength(label,font=fBand)
    d.rounded_rectangle([M,y-64,M+tw+30,y-36],radius=8,fill=col)
    d.text((M+15,y-62),label,font=fBand,fill=BG)
band(Y1,BH,"DETECTION WINS HERE  (STEPS 1-5)",TEAL)
band(Y2,BH,"INCIDENT RESPONSE ZONE  (STEPS 6-9)",RED)
def box(x,y,s):
    n,title,tid,det,con,tag,col=s
    d.rounded_rectangle([x,y,x+BW,y+BH],radius=14,fill=CARD,outline=BORDER,width=2)
    d.rounded_rectangle([x,y,x+BW,y+8],radius=4,fill=col)
    d.ellipse([x+14,y+22,x+56,y+64],fill=col)
    tw=d.textlength(n,font=fH); d.text((x+35-tw/2,y+31),n,font=fH,fill=BG)
    ty=y+22
    for ln in wrap(title,fH,BW-80): d.text((x+68,ty),ln,font=fH,fill=WHITE); ty+=29
    ty=max(ty,y+70)+6
    d.text((x+16,ty),"ATT&CK "+tid,font=fBb,fill=AMBER); ty+=34
    for lab,val,lc in (("Detect:",det,TEAL),("Contain:",con,"#FF8A8A")):
        d.text((x+16,ty),lab,font=fBb,fill=lc); ty+=29
        for ln in wrap(val,fB,BW-32): d.text((x+16,ty),ln,font=fB,fill=WHITE); ty+=29
        ty+=8
    tw=d.textlength(tag,font=fTag)
    d.rounded_rectangle([x+16,y+BH-46,x+16+tw+24,y+BH-14],radius=16,fill=col)
    d.text((x+28,y+BH-43),tag,font=fTag,fill=BG if col!=GREY else WHITE)
def arrow(x1,y1,x2,y2,col=MUTED):
    d.line([x1,y1,x2,y2],fill=col,width=5)
    import math
    a=math.atan2(y2-y1,x2-x1); L=16
    p=[(x2,y2),(x2-L*math.cos(a-0.5),y2-L*math.sin(a-0.5)),(x2-L*math.cos(a+0.5),y2-L*math.sin(a+0.5))]
    d.polygon(p,fill=col)
for i in range(5): box(xs[i],Y1,steps[i])
# bottom row snakes right-to-left: 6 under 5, 7 under 4, 8 under 3, 9 under 2
bx=[xs[4],xs[3],xs[2],xs[1]]
for j in range(4): box(bx[j],Y2,steps[5+j])
cy1=Y1+BH//2; cy2=Y2+BH//2
for i in range(4): arrow(xs[i]+BW+4,cy1,xs[i+1]-4,cy1)
arrow(xs[4]+BW//2,Y1+BH+4,xs[4]+BW//2,Y2-4,RED)
for j in range(3): arrow(bx[j]-4,cy2,bx[j+1]+BW+4,cy2)
# legend in empty slot under step 1
lx,ly=xs[0],Y2
d.rounded_rectangle([lx,ly,lx+BW,ly+BH],radius=14,outline=BORDER,width=2)
d.text((lx+16,ly+18),"STATUS KEY",font=fH,fill=WHITE)
yy=ly+60
for lab,c in (("Lab done",GREEN),("Next lab",AMBER),("Good / add-on",TEAL),("Later / needs VM",GREY),("Simulated only",RED)):
    d.rounded_rectangle([lx+16,yy,lx+46,yy+24],radius=6,fill=c); d.text((lx+58,yy+1),lab,font=fB,fill=WHITE); yy+=40
d.text((lx+16,yy+2),"Flow: 1 → 5, then 6 → 9",font=fBb,fill=MUTED)
# footer
fy=H-58
d.line([M,fy-14,W-M,fy-14],fill=BORDER,width=2)
d.text((M,fy),"Real-world anchor: Change Healthcare (2024): stolen creds on a Citrix portal with no MFA; ~9 days from access to ransomware.",font=fFoot,fill=MUTED)
img.save("/workspace/soc-home-lab/diagrams/healthcare-ransomware-kill-path.png")
print("ok",BW,Y2+BH)
