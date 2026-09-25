"""Generate three blue-team teaching slides (1920x1080) about the access economy.
Style copied from make_kill_path.py. Educational / defensive content only."""
import math
from PIL import Image, ImageDraw, ImageFont

OUT = "/workspace/soc-home-lab/diagrams/"
W, H = 1920, 1080
BG="#0B1A33"; CARD="#13284A"; BORDER="#2A4A7A"; WHITE="#FFFFFF"; MUTED="#B8C7E0"
TEAL="#1FBFA8"; AMBER="#F5A623"; RED="#E5484D"; GREEN="#2ECC71"; GREY="#5B6F92"; BLUE="#4DA3FF"
PINK="#FF8A8A"; FORUM="#1A1F2B"
D="/usr/share/fonts/truetype/dejavu/"
def F(s,b=False): return ImageFont.truetype(D+("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf"),s)
def FM(s,b=False): return ImageFont.truetype(D+("DejaVuSansMono-Bold.ttf" if b else "DejaVuSansMono.ttf"),s)
fT,fS=F(46,True),F(26); fH=F(23,True); fB=F(20); fBb=F(20,True); fTag=F(18,True); fBand=F(20,True); fFoot=F(20)
fBig=F(40,True); fSub=F(22); fStage=F(22,True)
M=60
img=None; d=None

def canvas():
    global img,d
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)

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

def header(title,sub):
    d.text((M,30),title,font=fT,fill=WHITE)
    d.text((M,92),sub,font=fS,fill=MUTED)
    d.rectangle([M,138,M+200,142],fill=TEAL)

def footer(text,col=MUTED,bold=False):
    fy=H-58
    d.line([M,fy-14,W-M,fy-14],fill=BORDER,width=2)
    d.text((M,fy),text,font=fBb if bold else fFoot,fill=col)

def tag(x,y,text,col,font=fTag,right=False):
    tw=d.textlength(text,font=font)
    if right: x=x-tw-24
    d.rounded_rectangle([x,y,x+tw+24,y+32],radius=16,fill=col)
    d.text((x+12,y+5),text,font=font,fill=WHITE if col==GREY else BG)
    return x+tw+24

def arrow(x1,y1,x2,y2,col=MUTED,width=5):
    d.line([x1,y1,x2,y2],fill=col,width=width)
    a=math.atan2(y2-y1,x2-x1); L=16
    p=[(x2,y2),(x2-L*math.cos(a-0.5),y2-L*math.sin(a-0.5)),(x2-L*math.cos(a+0.5),y2-L*math.sin(a+0.5))]
    d.polygon(p,fill=col)

def dashed_v(x,y1,y2,col,width=3,dash=14,gap=10):
    y=y1
    while y<y2:
        d.line([x,y,x,min(y+dash,y2)],fill=col,width=width); y+=dash+gap

def dashed_rect(box,col,width=3,dash=16,gap=10):
    x1,y1,x2,y2=box
    x=x1
    while x<x2:
        d.line([x,y1,min(x+dash,x2),y1],fill=col,width=width); d.line([x,y2,min(x+dash,x2),y2],fill=col,width=width); x+=dash+gap
    y=y1
    while y<y2:
        d.line([x1,y,x1,min(y+dash,y2)],fill=col,width=width); d.line([x2,y,x2,min(y+dash,y2)],fill=col,width=width); y+=dash+gap

# ---------------------------------------------------------------- SLIDE 1
def slide1():
    canvas()
    header("Who's Who in the Attack Economy",
           "Four terms every SOC analyst should know, and where they show up in an attack.")
    cards=[
     ("CIS","Commonwealth of Independent States","GEOGRAPHY",BLUE,
      "Russia, Belarus, Kazakhstan, Armenia and others. Many Russian-speaking ransomware crews avoid victims inside the CIS; some malware checks keyboard/language settings and quits.",
      "Local police tend to leave them alone if they only hit targets abroad.",
      "Explains why US/EU organizations are prime targets."),
     ("DPRK","North Korea (Democratic People's Republic of Korea)","NATION-STATE",RED,
      "State groups like Lazarus steal to fund the regime: crypto heists, fake remote IT workers, long quiet intrusions.",
      None,
      "Expect long dwell time. Watch for insider-like hires and odd remote logins."),
     ("IAB","Initial Access Broker","ROLE / JOB",AMBER,
      "A specialist who breaks in, then SELLS the foothold instead of using it.",
      None,
      "The person who got in may not be the person who attacks you, so an old, quiet login can precede ransomware weeks later."),
     ("Infostealer","Credential-stealing malware","MALWARE",TEAL,
      "Cheap malware that grabs saved browser passwords, session cookies and VPN configs from infected PCs. Sold in bulk as 'logs'.",
      None,
      "Feeds the #2 initial vector (stolen credentials, ~16% in Mandiant M-Trends). Looks like a normal login (Event ID 4624)."),
    ]
    GAP=36; CW=(W-2*M-GAP)//2; CH=330; Y0=166; VG=20
    b1=F(22); b1b=F(22,True)
    def labeled(x,ty,label,text,col,maxw):
        d.text((x,ty),label,font=b1b,fill=col)
        sw=d.textlength(label+" ",font=b1b)
        lines=wrap(text,b1,maxw-sw)
        d.text((x+sw,ty),lines[0],font=b1,fill=WHITE); ty+=31
        rest=" ".join(lines[1:])
        if rest: ty=para(x,ty,rest,b1,maxw,lh=31)
        return ty
    for i,(term,full,kind,col,body,why,soc) in enumerate(cards):
        x=M+(i%2)*(CW+GAP); y=Y0+(i//2)*(CH+VG)
        d.rounded_rectangle([x,y,x+CW,y+CH],radius=16,fill=CARD,outline=BORDER,width=2)
        d.rounded_rectangle([x,y,x+12,y+CH],radius=6,fill=col)
        d.text((x+34,y+12),term,font=fBig,fill=col)
        tag(x+CW-20,y+20,kind,col,right=True)
        d.text((x+34,y+64),full,font=F(24),fill=MUTED)
        ty=para(x+34,y+106,body,b1,CW-64,lh=31)+8
        if why: ty=labeled(x+34,ty,"Why:",why,MUTED,CW-64)+8
        ty=labeled(x+34,ty,"SOC relevance:",soc,col,CW-64)
        checks.append(("s1",term,ty,y+CH))
    # bottom strip
    sy=Y0+2*CH+VG+20; sh=H-22-sy
    d.rounded_rectangle([M,sy,W-M,sy+sh],radius=16,outline=BORDER,width=2)
    d.text((M+24,sy+12),"Mandiant M-Trends initial vectors (approx. share of intrusions with a known vector)",font=fH,fill=WHITE)
    bars=[("Exploits",33,RED),("Stolen credentials",16,AMBER),("Phishing",14,BLUE)]
    LX=M+24; BX=M+270; scale=34; by=sy+50; bh=30
    for lab,v,col in bars:
        d.text((LX,by+3),lab,font=fBb,fill=WHITE)
        d.rounded_rectangle([BX,by,BX+v*scale,by+bh],radius=8,fill=col)
        d.text((BX+v*scale+14,by+3),f"~{v}%",font=fBb,fill=col)
        by+=bh+10
    nx=BX+33*scale+110
    para(nx,sy+56,"Infostealers + IABs feed the stolen-credentials bar. A valid login needs no exploit, so it blends in.",fB,W-M-24-nx,fill=MUTED,lh=28)
    checks.append(("s1","strip",by,sy+sh))
    img.save(OUT+"attacker-terms-map.png")

# ---------------------------------------------------------------- SLIDE 2
def slide2():
    canvas()
    header("How Access Gets Sold: The Criminal Supply Chain",
           "Five roles, often five different people. Follow one stolen login from a home PC to a ransomware attack.")
    GAP=40
    ws=[290,310,440,290,310]; ws[-1]+= (W-2*M-4*GAP)-sum(ws)
    xs=[]; x=M
    for w in ws: xs.append(x); x+=w+GAP
    Y1=180; BH=470
    stages=[
     ("1","Infostealer operator","SUPPLIER",TEAL,
      "Infects PCs with stealer malware and harvests saved logins.",
      "Sells 'logs' in bulk"),
     ("2","IAB (Initial Access Broker)","BREAK-IN SPECIALIST",AMBER,
      "Tests the stolen logins, lands a foothold (VPN / Citrix / RDP), escalates a bit.",
      "Lists the access for sale"),
     None,
     ("4","Escrow / broker","MIDDLEMAN",BLUE,
      "Forum admin holds the payment until the buyer confirms the access works.",
      "Releases funds to IAB"),
     ("5","Ransomware affiliate (buyer)","ATTACKER",RED,
      "Uses a Ransomware-as-a-Service kit. Typically splits the ransom with the RaaS operator (often cited ~70-80% affiliate / 20-30% operator).",
      "Runs the attack"),
    ]
    for i,s in enumerate(stages):
        x=xs[i]; bw=ws[i]
        if s is None: continue
        n,title,role,col,body,out=s
        d.rounded_rectangle([x,Y1,x+bw,Y1+BH],radius=14,fill=CARD,outline=BORDER,width=2)
        d.rounded_rectangle([x,Y1,x+bw,Y1+8],radius=4,fill=col)
        d.ellipse([x+14,Y1+22,x+56,Y1+64],fill=col)
        tw=d.textlength(n,font=fH); d.text((x+35-tw/2,Y1+31),n,font=fH,fill=BG)
        ty=Y1+22
        for ln in wrap(title,fH,bw-84): d.text((x+68,ty),ln,font=fH,fill=WHITE); ty+=29
        ty=max(ty,Y1+70)+10
        tag(x+16,ty,"ROLE: "+role,col); ty+=48
        ty=para(x+16,ty,body,fB,bw-32,lh=28)
        # output line pinned at bottom
        d.line([x+16,Y1+BH-78,x+bw-16,Y1+BH-78],fill=BORDER,width=2)
        d.text((x+16,Y1+BH-66),"Output:",font=fBb,fill=col)
        para(x+16,Y1+BH-38,out,fB,bw-32,lh=26)
        checks.append(("s2",n,ty,Y1+BH-78))
    # stage 3: mock forum post
    x=xs[2]; bw=ws[2]
    d.rounded_rectangle([x,Y1,x+bw,Y1+BH],radius=14,fill=FORUM,outline=AMBER,width=3)
    d.ellipse([x+14,Y1+22,x+56,Y1+64],fill=AMBER)
    tw=d.textlength("3",font=fH); d.text((x+35-tw/2,Y1+31),"3",font=fH,fill=BG)
    d.text((x+68,Y1+22),"Criminal forum listing",font=fH,fill=WHITE)
    d.text((x+68,Y1+51),"MARKETPLACE",font=fTag,fill=AMBER)
    # EXAMPLE banner
    d.rounded_rectangle([x+16,Y1+86,x+bw-16,Y1+122],radius=8,fill=AMBER)
    lab="EXAMPLE: illustrative, not real"
    tw=d.textlength(lab,font=fBb); d.text((x+bw/2-tw/2,Y1+93),lab,font=fBb,fill=BG)
    # post body
    px=x+16; py=Y1+136
    d.rounded_rectangle([px,py,x+bw-16,Y1+BH-16],radius=8,fill="#232A3A",outline="#3A4560",width=2)
    fm=FM(20); fmb=FM(20,True)
    d.text((px+14,py+12),"[WTS] Corp network access",font=fmb,fill=WHITE)
    d.text((px+14,py+40),"posted by: seller_example",font=fm,fill=MUTED)
    d.line([px+14,py+72,x+bw-30,py+72],fill="#3A4560",width=2)
    rows=[("Access","US healthcare org"),("Revenue","~$500M"),("Type","Citrix VPN, domain user"),("Hosts","~2,000"),("Price","auction")]
    ry=py+82
    for k,v in rows:
        d.text((px+14,ry),f"{k}:",font=fmb,fill=AMBER)
        vx=px+14+10*12
        for ln in wrap(v,fm,x+bw-30-vx): d.text((vx,ry),ln,font=fm,fill=WHITE); ry+=26
        ry+=5
    d.text((px+14,ry+6),"Escrow accepted.",font=fm,fill=MUTED)
    checks.append(("s2","forum",ry+6+26,Y1+BH-24))
    # arrows
    cy=Y1+BH//2
    for i in range(4): arrow(xs[i]+ws[i]+5,cy,xs[i+1]-5,cy)
    # SOC visibility row
    Y2=Y1+BH+84; BH2=250
    d.rounded_rectangle([M-20,Y2-50,W-M+20,Y2+BH2+14],radius=16,outline=TEAL,width=2)
    lab="WHAT THE SOC CAN SEE"
    tw=d.textlength(lab,font=fBand)
    d.rounded_rectangle([M,Y2-64,M+tw+30,Y2-36],radius=8,fill=TEAL)
    d.text((M+15,Y2-62),lab,font=fBand,fill=BG)
    soc=[
     ("BLIND SPOT",GREY,"Nothing on your network. It happens on an employee's home PC."),
     ("VISIBLE",GREEN,"Successful logins from a new location or device: Event 4624, VPN / Citrix logs."),
     ("INTEL ONLY",AMBER,"Nothing on your network, but threat intel feeds may flag your org name in a listing."),
     ("BLIND SPOT",GREY,"Nothing. The deal happens entirely off your network."),
     ("VISIBLE",GREEN,"New tools and scripts: PowerShell 4104, Sysmon 1 process creation, discovery commands."),
    ]
    for i,(t,col,txt) in enumerate(soc):
        x=xs[i]; bw=ws[i]
        d.rounded_rectangle([x,Y2,x+bw,Y2+BH2],radius=14,fill=CARD,outline=col,width=2)
        d.text((x+16,Y2+14),f"Stage {i+1}",font=fBb,fill=MUTED)
        tag(x+bw-16,Y2+12,t,col,right=True)
        ty=para(x+16,Y2+60,txt,fB,bw-32,lh=28)
        checks.append(("s2","soc"+str(i+1),ty,Y2+BH2))
        # dotted connector from stage to soc box
        dashed_v(x+bw//2,Y1+BH+6,Y2-54,BORDER,width=2,dash=8,gap=8)
    footer("Key idea: the break-in and the attack are often done by different people, sometimes weeks apart.",col=WHITE,bold=True)
    img.save(OUT+"iab-forum-supply-chain.png")

# ---------------------------------------------------------------- SLIDE 3
def slide3():
    canvas()
    header("From Bought Access to Payday: Hospital Scenario",
           "Picks up after the affiliate buys access from an IAB.")
    M3=50; GAP=18; MID=56
    BW=(W-2*M3-5*GAP-MID)//7
    xs=[]; x=M3
    for i in range(7):
        xs.append(x); x+=BW+(MID if i==3 else GAP)
    phases=[
     ("Day 0","Buy access, log in with IAB's creds","T1078","4624 from new IP / device, no MFA","Disable account, force MFA",None),
     ("Day 0-1","Run tools with PowerShell","T1059.001","4104, Sysmon 1",None,("LAB 1 DONE",GREEN)),
     ("Day 1","Plant persistence (Run key)","T1547.001","Sysmon 13",None,("LAB 2 NEXT",AMBER)),
     ("Day 1-3","Dump creds, find EHR + backups","T1003.001, T1087","Sysmon 10 on lsass, recon burst in 4688",None,None),
     ("Day 3-7","Move to servers, delete backups","T1021, T1490","4624 type 3/10, vssadmin in 4688",None,None),
     ("Day 7-8","Steal patient records","T1567","Large outbound transfer, Sysmon 3",None,None),
     ("Day ~9","Encrypt + ransom note","T1486","Mass file renames, Sysmon 11",None,("TOO LATE: IR MODE",RED)),
    ]
    # bands
    BT=200; BB=842
    split=xs[3]+BW+MID//2
    d.rounded_rectangle([M3-14,BT,split-12,BB],radius=16,outline=TEAL,width=2)
    d.rounded_rectangle([split+12,BT,W-M3+14,BB],radius=16,outline=RED,width=2)
    for lab,col,bx in (("DETECT & STOP (cheap)  -  Days 0-3",TEAL,M3),("RESPOND & RECOVER (expensive)  -  Days 3-9",RED,split+30)):
        tw=d.textlength(lab,font=fBand)
        d.rounded_rectangle([bx,BT-14,bx+tw+30,BT+14],radius=8,fill=col)
        d.text((bx+15,BT-12),lab,font=fBand,fill=BG)
    dashed_v(split,BT-30,BB+10,AMBER,width=4)
    # timeline axis
    AY=290
    d.line([M3+10,AY,split-24,AY],fill=TEAL,width=6)
    d.line([split+24,AY,W-M3-10,AY],fill=RED,width=6)
    arrow(W-M3-40,AY,W-M3-6,AY,RED,width=6)
    fT3=F(24,True); fB3=F(22); fB3b=F(22,True)
    CY=330; CH=492
    for i,(day,act,tid,det,con,tg) in enumerate(phases):
        x=xs[i]; cx=x+BW//2
        col=TEAL if i<4 else RED
        tw=d.textlength(day,font=fH)
        d.text((cx-tw/2,AY-50),day,font=fH,fill=WHITE)
        d.ellipse([cx-11,AY-11,cx+11,AY+11],fill=col,outline=WHITE,width=3)
        outline=tg[1] if tg else BORDER; ow=4 if tg else 2
        d.line([cx,AY+12,cx,CY],fill=BORDER,width=2)
        d.rounded_rectangle([x,CY,x+BW,CY+CH],radius=14,fill=CARD,outline=outline,width=ow)
        d.rounded_rectangle([x,CY,x+BW,CY+8],radius=4,fill=col)
        ty=CY+20
        d.text((x+16,ty),"Attacker:",font=fBb,fill=MUTED); ty+=30
        for ln in wrap(act,fT3,BW-32): d.text((x+16,ty),ln,font=fT3,fill=WHITE); ty+=31
        ty+=8
        for ln in wrap(tid,fB3b,BW-32): d.text((x+16,ty),ln,font=fB3b,fill=AMBER); ty+=30
        ty+=10
        d.text((x+16,ty),"SOC detect:",font=fB3b,fill=TEAL); ty+=31
        ty=para(x+16,ty,det,fB3,BW-32,lh=30)+8
        if con:
            d.text((x+16,ty),"Contain:",font=fB3b,fill=PINK); ty+=31
            ty=para(x+16,ty,con,fB3,BW-32,lh=30)+8
        if tg:
            lab,tc=tg
            lines=[p.strip()+(":" if k==0 and ":" in lab else "") for k,p in enumerate(lab.split(":"))] if ":" in lab else [lab]
            th=len(lines)*24+10
            d.rounded_rectangle([x+16,CY+CH-16-th,x+BW-16,CY+CH-16],radius=14,fill=tc)
            yy=CY+CH-16-th+5
            for ln in lines:
                lw=d.textlength(ln,font=fTag); d.text((x+BW/2-lw/2,yy),ln,font=fTag,fill=BG); yy+=24
            checks.append(("s3",day,ty,CY+CH-16-th))
        else:
            checks.append(("s3",day,ty,CY+CH))
    # status key strip
    ky=868; kh=112
    d.rounded_rectangle([M3-14,ky,W-M3+14,ky+kh],radius=16,outline=BORDER,width=2)
    d.text((M3+14,ky+14),"SOC-LAB1 STATUS KEY",font=fH,fill=WHITE)
    kx=M3+14; kyy=ky+60
    for lab,col,txt in (("LAB 1 DONE",GREEN,"lab completed"),("LAB 2 NEXT",AMBER,"next lab to build"),("TOO LATE: IR MODE",RED,"incident response, not detection")):
        kx=tag(kx,kyy,lab,col)+12
        d.text((kx,kyy+4),txt,font=fB,fill=WHITE); kx+=d.textlength(txt,font=fB)+48
    nx=kx+10
    para(nx,ky+18,"Stopping it on the left side means fewer servers to rebuild and far less patient data at risk.",fB,W-M3-14-nx,fill=MUTED,lh=28)
    footer("Timeline modeled on Change Healthcare (2024): stolen Citrix creds without MFA; ~9 days to ransomware; $22M ransom paid.")
    img.save(OUT+"iab-to-payday-hospital.png")

checks=[]
if __name__=="__main__":
    slide1(); slide2(); slide3()
    for c in checks:
        print(("OVERFLOW " if c[2]>c[3] else "ok       "),c)
