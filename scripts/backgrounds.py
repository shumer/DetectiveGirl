"""Generate stylised SVG backgrounds for cases that have no painted artwork yet."""
import random, math, os
W,H=1536,1024
def grad(id_,top,bottom,extra=''):
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>{extra}<stop offset="1" stop-color="{bottom}"/></linearGradient>'
def stars(rng,n,ymax,color='#ffffff'):
    return ''.join(f'<circle cx="{rng.uniform(0,W):.0f}" cy="{rng.uniform(0,ymax):.0f}" r="{rng.uniform(.8,2.2):.1f}" fill="{color}" opacity="{rng.uniform(.3,.9):.2f}"/>' for _ in range(n))
def glow(cx,cy,r,color,op=.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{op}" filter="url(#blur)"/>'
def frame(body,top,bottom,defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{grad("sky",top,bottom)}{defs}<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter><filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter></defs><rect width="{W}" height="{H}" fill="url(#sky)"/>{body}</svg>'
def greenhouse(i,rng):
    top,bottom=['#08152a','#0a1f36','#0b1a33','#0a1c2c'][i],['#123d4d','#155246','#16385e','#144a3a'][i]
    b=stars(rng,140,520)
    b+=f'<circle cx="1180" cy="170" r="70" fill="#dfe8f0"/><circle cx="1150" cy="150" r="14" fill="#c3ccd6" opacity=".6"/><circle cx="1205" cy="195" r="20" fill="#c3ccd6" opacity=".5"/>'
    b+=f'<path d="M0 700 Q 400 640 768 690 T 1536 680 L1536 1024 L0 1024Z" fill="#0c2233"/>'
    # Dome.
    b+=f'<path d="M120 720 A 650 520 0 0 1 1416 720 Z" fill="#7fe3d1" opacity=".08"/><path d="M120 720 A 650 520 0 0 1 1416 720" stroke="#9fe8c4" stroke-width="4" fill="none" opacity=".6"/>'
    for k in range(1,6):
        x=120+k*216
        b+=f'<line x1="{x}" y1="720" x2="{x}" y2="{720-520*math.sin(math.acos((x-768)/650)):.0f}" stroke="#9fe8c4" stroke-width="2" opacity=".35"/>'
    # Rows of sprouts.
    rows=[540,600,660] if i!=1 else [560,640]
    for r in rows:
        b+=f'<rect x="300" y="{r}" width="936" height="18" rx="9" fill="#1f3a55"/>'
        for x in range(320,1220,46):
            b+=f'<path d="M{x} {r} q 6 -30 12 0 q -6 -18 -12 0" fill="#8ff2b0" opacity=".85"/>'
        b+=glow(768,r-40,220,'#b8f0a8',.12)
    if i==1: b+=f'<rect x="980" y="560" width="160" height="110" rx="10" fill="#2a3f58"/><rect x="990" y="500" width="140" height="70" rx="8" fill="#3b5474"/><circle cx="1010" cy="690" r="18" fill="#111"/><circle cx="1110" cy="690" r="18" fill="#111"/>'
    if i==2: b+=''.join(f'<rect x="{x}" y="430" width="120" height="290" rx="14" fill="#1a2f4a" stroke="#63769a" stroke-width="3"/>' for x in (360,600,840,1080))
    if i==3: b+=f'<rect x="560" y="470" width="420" height="230" rx="16" fill="#0f2140" stroke="#5d8090" stroke-width="4"/>'+''.join(f'<rect x="{590+k*95}" y="{510+(k%2)*60}" width="70" height="{120-(k%2)*60}" rx="6" fill="#7fe3d1" opacity=".5"/>' for k in range(4))
    for k in range(3): b+=glow(rng.uniform(200,1300),rng.uniform(300,500),160,'#7fe3d1',.16)
    return frame(b,top,bottom)
def theatre(i,rng):
    top,bottom=['#1a0a10','#120a18','#1e0b12','#160a0d'][i],['#4a1c2c','#3a2148','#5a2436','#43202a'][i]
    b=''
    b+=f'<rect x="200" y="140" width="1136" height="640" fill="#0d0508"/>'
    b+=glow(768,460,320,'#ffd27f',.16)
    # Stage floor and set pieces.
    b+=f'<rect x="200" y="700" width="1136" height="120" fill="#5a3a26"/><rect x="0" y="820" width="1536" height="204" fill="#2a1016"/>'
    if i in (0,2): b+=f'<path d="M420 700 Q 768 520 1116 700" stroke="#f2c66b" stroke-width="18" fill="none"/>'+''.join(f'<line x1="{x}" y1="{700-int(180*math.sin(math.pi*(x-420)/696))}" x2="{x}" y2="700" stroke="#f2c66b" stroke-width="6"/>' for x in range(480,1100,80))
    if i==1: b+=''.join(f'<rect x="{360+k*90}" y="{300+k*40}" width="60" height="40" fill="#f0c47a" opacity=".8"/><rect x="{360+k*90}" y="{300+k*40}" width="60" height="40" fill="none" stroke="#7a6386"/>' for k in range(9))+f'<rect x="300" y="240" width="900" height="480" fill="none" stroke="#7a6386" stroke-width="6"/>'
    if i==3: b+=f'<rect x="440" y="560" width="660" height="140" rx="10" fill="#3b2418"/>'+''.join(f'<rect x="{470+k*130}" y="500" width="90" height="60" fill="#ffe0a8" opacity=".9"/>' for k in range(5))
    # Garlands.
    for k in range(6):
        y=190+k*22; b+=f'<path d="M230 {y} Q 768 {y+120} 1306 {y}" stroke="#f2c66b" stroke-width="2" fill="none" opacity=".5"/>'
        for x in range(280,1300,110): b+=f'<polygon points="{x},{y+40} {x+8},{y+62} {x+30},{y+62} {x+13},{y+76} {x+20},{y+98} {x},{y+84} {x-20},{y+98} {x-13},{y+76} {x-30},{y+62} {x-8},{y+62}" fill="#ffd27f" opacity=".85" transform="scale(.6) translate({x*0.66:.0f},{(y+40)*0.66:.0f})"/>'
    # Curtains.
    for x in (0,1336): b+=f'<rect x="{x}" y="0" width="200" height="820" fill="#5c1a28"/>'+''.join(f'<line x1="{x+20+j*36}" y1="0" x2="{x+20+j*36}" y2="820" stroke="#3a0f18" stroke-width="10"/>' for j in range(5))
    b+=f'<path d="M0 0 H1536 V150 Q 768 240 0 150 Z" fill="#6a1f30"/><path d="M0 150 Q 768 240 1536 150" stroke="#f2c66b" stroke-width="8" fill="none"/>'
    return frame(b,top,bottom)
def aquarium(i,rng):
    top,bottom=['#062036','#07283a','#071c3a','#062a38'][i],['#0a4f66','#0c5a5a','#0d4470','#0a5c60'][i]
    b=''
    for k in range(4): b+=f'<path d="M0 {180+k*30} Q 384 {120+k*30} 768 {180+k*30} T 1536 {180+k*30}" stroke="#7fe6e0" stroke-width="2" fill="none" opacity=".15"/>'
    b+=glow(400,150,300,'#9fe8ff',.14)
    b+=f'<path d="M0 860 Q 400 800 768 850 T 1536 830 L1536 1024 L0 1024Z" fill="#c9a86a"/>'
    # Castle.
    b+=f'<rect x="320" y="520" width="300" height="340" fill="#4a3a5c"/>'+''.join(f'<rect x="{330+k*100}" y="440" width="70" height="120" fill="#5a4a6c"/><polygon points="{330+k*100},440 {365+k*100},380 {400+k*100},440" fill="#ff9f7a"/>' for k in range(3))
    b+=''.join(f'<rect x="{350+k*60}" y="{600+(k%2)*80}" width="30" height="50" rx="15" fill="#ffc07a" opacity=".8"/>' for k in range(4))
    # Boat.
    b+=f'<path d="M900 700 L1200 700 L1160 760 L940 760 Z" fill="#6a3d2a"/><line x1="1050" y1="700" x2="1050" y2="540" stroke="#3a2416" stroke-width="10"/><polygon points="1060,545 1060,690 1180,690" fill="#f5f0e0"/>'
    # Shell and chest.
    b+=f'<path d="M1300 840 a 60 60 0 0 1 120 0 Z" fill="#ff9f7a"/>'
    b+=f'<rect x="120" y="760" width="160" height="100" rx="8" fill="#5a3a20"/><path d="M120 760 a 80 60 0 0 1 160 0 Z" fill="#7a4a24"/><rect x="190" y="790" width="20" height="24" fill="#f2c66b"/>'
    # Bubble rings.
    src=[(1050,690),(1360,840),(200,760),(470,440)][i]
    for k in range(7):
        y=src[1]-70-k*85; r=18+k*9
        b+=f'<circle cx="{src[0]+math.sin(k)*20:.0f}" cy="{y}" r="{r}" fill="none" stroke="#bff6ff" stroke-width="3" opacity="{.9-k*.1:.2f}"/>'
    for _ in range(40): b+=f'<circle cx="{rng.uniform(0,W):.0f}" cy="{rng.uniform(100,900):.0f}" r="{rng.uniform(2,7):.1f}" fill="none" stroke="#bff6ff" stroke-width="1.5" opacity="{rng.uniform(.2,.6):.2f}"/>'
    b+=''.join(f'<path d="M{x} 860 q 20 -120 0 -240 q 30 100 20 240Z" fill="#1f7a5c" opacity=".8"/>' for x in (700,760,1260,80))
    return frame(b,top,bottom)
def bakery(i,rng):
    top,bottom=['#2b170c','#22140e','#2c1a0f','#1f130c'][i],['#5a3a1e','#4a3222','#5e3c22','#4b3520'][i]
    b=''
    b+=f'<rect x="0" y="0" width="1536" height="1024" fill="#3a2414"/>'
    for y in (220,420,620): b+=f'<rect x="120" y="{y}" width="1296" height="16" fill="#6b4a2c"/><rect x="120" y="{y-140}" width="1296" height="140" fill="#2a170c" opacity=".6"/>'
    # Moon cookies on shelves.
    for y in (200,400,600):
        for x in range(180,1400,110):
            if rng.random()<.85: b+=f'<path d="M{x} {y} a 34 34 0 1 1 0 -68 a 26 26 0 1 0 0 68" fill="#f4c56a"/>'
            else: b+=f'<polygon points="{x},{y-70} {x+9},{y-45} {x+35},{y-42} {x+15},{y-25} {x+21},{y} {x},{y-13} {x-21},{y} {x-15},{y-25} {x-35},{y-42} {x-9},{y-45}" fill="#ffd58a"/>'
    b+=f'<rect x="0" y="720" width="1536" height="304" fill="#5a3a20"/><rect x="0" y="700" width="1536" height="30" fill="#7a5230"/>'
    if i==0: b+=f'<rect x="520" y="560" width="500" height="150" rx="12" fill="#c9a06a"/><rect x="540" y="540" width="460" height="40" rx="8" fill="#e0b982"/>'+''.join(f'<path d="M{590+k*70} 640 a 26 26 0 1 1 0 -52 a 20 20 0 1 0 0 52" fill="#f4c56a"/>' for k in range(6))
    if i==1: b+=f'<rect x="560" y="480" width="420" height="260" rx="10" fill="#e9dcc4"/><rect x="590" y="510" width="360" height="200" fill="#c9a06a"/>'+''.join(f'<path d="M{640+k*90} 620 a 30 30 0 1 1 0 -60 a 22 22 0 1 0 0 60" fill="#f4c56a"/>' for k in range(4))
    if i==2: b+=f'<ellipse cx="768" cy="640" rx="260" ry="70" fill="#f1e2c6"/><ellipse cx="768" cy="630" rx="200" ry="50" fill="#f7ead2"/><rect x="420" y="560" width="60" height="140" rx="30" fill="#8a6a44"/>'
    if i==3: b+=f'<rect x="560" y="360" width="420" height="360" rx="20" fill="#1a0e08"/><rect x="600" y="420" width="340" height="220" rx="10" fill="#ff8a3a"/><rect x="600" y="420" width="340" height="220" rx="10" fill="#ffd58a" opacity=".5" filter="url(#soft)"/>'+glow(770,530,240,'#ffb060',.4)
    b+=glow(300,150,260,'#ffd58a',.18)+glow(1250,150,260,'#ffd58a',.18)
    b+=f'<circle cx="300" cy="120" r="30" fill="#ffe9b0"/><circle cx="1250" cy="120" r="30" fill="#ffe9b0"/>'
    return frame(b,top,bottom)
def lighthouse(i,rng):
    top,bottom=['#050f22','#071630','#06122a','#061428'][i],['#123058','#163a66','#132f5c','#123660'][i]
    b=stars(rng,200,600)
    b+=f'<circle cx="1250" cy="160" r="60" fill="#fff4c8"/>'
    b+=f'<path d="M0 640 Q 300 600 600 640 T 1200 630 T 1536 640 L1536 1024 L0 1024Z" fill="#0a2240"/>'
    for k in range(6): b+=f'<path d="M0 {700+k*50} Q 384 {680+k*50} 768 {700+k*50} T 1536 {700+k*50}" stroke="#9fd8ff" stroke-width="2" fill="none" opacity="{.25-k*.03:.2f}"/>'
    b+=f'<path d="M300 640 L400 640 L450 900 L250 900 Z" fill="#334a66"/>'
    b+=f'<polygon points="330,620 400,620 420,360 310,360" fill="#e8ecf2"/><rect x="310" y="440" width="110" height="40" fill="#c8323a"/><rect x="310" y="530" width="110" height="40" fill="#c8323a"/><rect x="320" y="300" width="90" height="60" fill="#ffe27a"/><polygon points="310,300 365,250 420,300" fill="#3a4a66"/>'
    if i in (0,3): b+=f'<polygon points="365,330 1536,120 1536,540" fill="#ffe27a" opacity=".22"/>'+glow(365,330,120,'#ffe27a',.6)
    if i==1: b+=f'<rect x="700" y="380" width="520" height="300" rx="16" fill="#0b1a33" stroke="#557398" stroke-width="4"/>'+''.join(f'<rect x="730" y="{420+k*50}" width="{rng.uniform(200,440):.0f}" height="22" rx="4" fill="#9fd8ff" opacity=".55"/>' for k in range(5))
    if i==2:
        b+=f'<rect x="700" y="360" width="560" height="340" rx="14" fill="#f5efd8"/>'+''.join(f'<line x1="740" y1="{420+k*40}" x2="1220" y2="{420+k*40}" stroke="#5a7299" stroke-width="2"/>' for k in range(5))
        for k,(x,y) in enumerate([(800,500),(900,460),(1000,540),(1120,420)]): b+=f'<ellipse cx="{x}" cy="{y}" rx="16" ry="11" fill="#1a2a44" transform="rotate(-20 {x} {y})"/><line x1="{x+14}" y1="{y-4}" x2="{x+14}" y2="{y-70}" stroke="#1a2a44" stroke-width="4"/>'
    for k in range(4): b+=f'<circle cx="{500+k*260}" cy="{720+k*20}" r="{4+k}" fill="#ffe27a" opacity=".5"/>'
    return frame(b,top,bottom)
def library(i,rng):
    top,bottom=['#1a0f22','#1e1222','#17111c','#201324'][i],['#3a2648','#3d2a44','#332b3f','#402a48'][i]
    b=''
    for x in range(0,1536,256):
        b+=f'<rect x="{x}" y="60" width="240" height="760" fill="#2b1a2e" stroke="#5a4660" stroke-width="4"/>'
        for y in range(80,800,120):
            b+=f'<rect x="{x}" y="{y+100}" width="240" height="10" fill="#4a3650"/>'
            cx=x+12
            while cx<x+225:
                w=rng.uniform(18,40); h=rng.uniform(60,96); col=rng.choice(['#e9c27a','#8a4a5a','#4a6a8a','#6a8a5a','#c26a4a','#b89a6a'])
                b+=f'<rect x="{cx:.0f}" y="{y+100-h:.0f}" width="{w:.0f}" height="{h:.0f}" rx="2" fill="{col}"/>'; cx+=w+4
    b+=f'<rect x="0" y="820" width="1536" height="204" fill="#2a1a20"/>'
    b+=glow(768,420,420,'#e9c27a',.14)
    if i==1: b+=f'<rect x="380" y="560" width="780" height="40" rx="8" fill="#6a4a3a"/><rect x="480" y="470" width="360" height="90" fill="#f5eedc" transform="rotate(-4 660 515)"/><rect x="700" y="480" width="360" height="90" fill="#efe6cf" transform="rotate(3 880 525)"/><rect x="560" y="400" width="40" height="60" fill="#c26a4a"/><rect x="900" y="410" width="40" height="60" fill="#4a6a8a"/>'
    if i==2: b+=f'<rect x="520" y="420" width="500" height="340" rx="8" fill="#c9a06a"/><rect x="540" y="440" width="460" height="300" fill="#f5eedc"/>'+''.join(f'<rect x="580" y="{480+k*50}" width="{rng.uniform(200,380):.0f}" height="12" fill="#5a4660" opacity=".6"/>' for k in range(5))+f'<rect x="760" y="600" width="200" height="120" fill="none" stroke="#e9c27a" stroke-width="6"/>'
    if i==3: b+=f'<ellipse cx="768" cy="700" rx="360" ry="90" fill="#5a3a30"/>'+''.join(f'<rect x="{500+k*130}" y="600" width="60" height="90" rx="30" fill="#8a6a5a"/>' for k in range(5))
    b+=f'<rect x="700" y="60" width="136" height="20" fill="#5a4660"/><line x1="768" y1="80" x2="768" y2="200" stroke="#5a4660" stroke-width="4"/><path d="M700 260 L836 260 L810 200 L726 200Z" fill="#e9c27a"/>'+glow(768,300,140,'#ffe6a0',.5)
    return frame(b,top,bottom)
def park(i,rng):
    top,bottom=['#7fb9e8','#8cc3ea','#86bde5','#79b0dd'][i],['#dff0ff','#eaf4ff','#e3f2ff','#d8ecfb'][i]
    b=''
    for k in range(5): cx,cy=rng.uniform(100,1400),rng.uniform(80,300); b+=f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rng.uniform(90,160):.0f}" ry="{rng.uniform(40,60):.0f}" fill="#fff" opacity=".85"/>'
    b+=f'<path d="M0 620 Q 400 560 768 610 T 1536 600 L1536 1024 L0 1024Z" fill="#4f9a5c"/><path d="M0 760 Q 500 700 1000 760 T 1536 740 L1536 1024 L0 1024Z" fill="#3f8a4e"/>'
    for x in range(80,1536,170):
        b+=f'<rect x="{x}" y="520" width="24" height="120" fill="#6a4a30"/><circle cx="{x+12}" cy="500" r="{rng.uniform(60,90):.0f}" fill="#2f7a3f"/><circle cx="{x-20}" cy="530" r="50" fill="#3a8a48"/>'
    b+=f'<path d="M0 900 Q 768 820 1536 900 L1536 960 Q 768 880 0 960Z" fill="#d9c9a6"/>'
    if i==0: b+=f'<path d="M560 700 L560 480 A 208 208 0 0 1 976 480 L976 700" stroke="#b8a48a" stroke-width="40" fill="none"/><rect x="520" y="440" width="500" height="60" fill="#e0b040" opacity=".9"/><rect x="520" y="440" width="500" height="60" fill="none" stroke="#333" stroke-width="4" stroke-dasharray="30 30"/>'
    if i==1: b+=f'<ellipse cx="768" cy="760" rx="220" ry="60" fill="#5fb0e0"/><rect x="740" y="560" width="56" height="200" fill="#c9c0b0"/><ellipse cx="768" cy="560" rx="90" ry="20" fill="#c9c0b0"/>'+''.join(f'<path d="M768 540 q {dx} -120 {dx*2} 0" stroke="#bfe8ff" stroke-width="6" fill="none"/>' for dx in (-60,-30,30,60))
    if i==2: b+=''.join(f'<rect x="{300+k*380}" y="560" width="220" height="160" fill="#c9a06a"/><polygon points="{280+k*380},560 {410+k*380},470 {540+k*380},560" fill="#a04030"/>' for k in range(3))
    if i==3: b+=f'<rect x="440" y="600" width="660" height="140" fill="#8a5a3a"/><rect x="420" y="560" width="700" height="40" fill="#c26a4a"/>'+''.join(f'<polygon points="{470+k*70},560 {500+k*70},560 {485+k*70},600" fill="{["#ffd866","#66c2ff","#ff8866"][k%3]}"/>' for k in range(9))
    # Small robots.
    for k in range(6):
        x=200+k*220+(i*40); y=880
        b+=f'<rect x="{x}" y="{y-60}" width="50" height="50" rx="10" fill="#e8e8f0" stroke="#667" stroke-width="3"/><circle cx="{x+15}" cy="{y-40}" r="6" fill="#3a6aff"/><circle cx="{x+35}" cy="{y-40}" r="6" fill="#3a6aff"/><circle cx="{x+12}" cy="{y}" r="10" fill="#333"/><circle cx="{x+38}" cy="{y}" r="10" fill="#333"/><rect x="{x+18}" y="{y-80}" width="14" height="20" fill="#ffd866"/>'
    return frame(b,top,bottom)
gens={'greenhouse':greenhouse,'theatre':theatre,'aquarium':aquarium,'bakery':bakery,'lighthouse':lighthouse,'library':library,'park':park}
os.makedirs('public/backgrounds',exist_ok=True)
for name,fn in gens.items():
    for i in range(4):
        rng=random.Random(f'{name}{i}')
        open(f'public/backgrounds/{name}-{i}.svg','w').write(fn(i,rng))
print('ok')
