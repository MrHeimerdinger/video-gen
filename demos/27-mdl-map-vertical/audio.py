# 26-mdl-map-15s soundtrack (15 s, tour Tokyo > Osaka > Fukuoka > Kagoshima) — bright marimba explainer bed; the map builds itself in wooden ticks, each store pops with a note
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx
D = os.path.dirname(os.path.abspath(__file__)) + '/'
C = json.load(open(D + 'cues.json', encoding='utf-8')); E = C['ev']; ST = C['stores']
os.makedirs(D + 'out', exist_ok=True)

first_pop = ST[0]['pop']
m = recipes.explainer(duration=float(C['duration']), bpm=C['bpm'], key='D', drop=first_pop - .05, outro=E['end_title'])
S = m.sfx
key_note = lambda t, i=0: m.form.chord_at(t)[i % len(m.form.chord_at(t))] + 12

# map assembles: a rain of wooden clicks sweeping west → east (pan left → right), thinning at the end
a, b = E['land']
n = 26
for k in range(n):
    t = a + (b - a - .2) * (k / (n - 1)) ** 1.15
    S(sfx.click('wood'), at=t + .3, gain=-20 + 6 * (1 - abs(k / (n - 1) - .5) * 2), pan=-.7 + 1.4 * k / (n - 1))
S(sfx.swish(dur=.3, seed=2), at=E['title'] + .1, gain=-11, pan=-.4)
S(sfx.click('soft'), at=E['kicker'], gain=-12, pan=-.4)
S(sfx.whoosh(dur=.55, kind='air', direction=-1, peak=.4, seed=3), at=E['title_out'][0] + .15, gain=-14, pan=-.3)

# camera moves between stores
moves = [(C['cam'][i - 1]['t'], k['t']) for i, k in enumerate(C['cam']) if k.get('m') == 'move']
for i, (t0, t1) in enumerate(moves):
    S(sfx.whoosh(dur=t1 - t0 + .15, kind='swish', direction=1, peak=.45, seed=10 + i), at=(t0 + t1) / 2, gain=-6 if i == len(moves) - 1 else -8)

# each store: shop grows (squeaky rise), ripple, label pops with a note
pans = [.45, .1, -.4, -.5]
for i, s in enumerate(ST):
    p = s['pop']
    S(sfx.stretch(dur=.28, up=True), at=p - E['grow_lead'], gain=-14, pan=pans[i])
    S(sfx.sticker_slap(seed=20 + i), at=p - E['grow_lead'] + .2, gain=-8, pan=pans[i])
    S(sfx.pop('bubble', pitch=1.0 + .08 * i), at=p, gain=-2, pan=pans[i])
    S(sfx.ding(note=key_note(p, i) + 12, dur=.9), at=p + .02, gain=-9, pan=pans[i])

# network arcs draw, end title lands
a0, step, dur = E['arcs']
for i in range(3):
    S(sfx.pen('pen', dur=dur, seed=30 + i), at=a0 + i * step, gain=-14, pan=.4 - .4 * i)
S(sfx.chime(), at=a0 + 2 * step + dur, gain=-9)
S(sfx.swish(dur=.3, seed=40), at=E['end_title'] + .08, gain=-9, pan=-.4)
for i in range(4):
    S(sfx.click('soft'), at=E['end_list'] + i * .08, gain=-14, pan=-.5 + .1 * i)

res = m.export(D + 'out/audio.wav', tp=-1.5)
print(res if not isinstance(res, dict) else {k: v for k, v in res.items() if k in ('duration', 'lufs', 'true_peak', 'warnings')})
