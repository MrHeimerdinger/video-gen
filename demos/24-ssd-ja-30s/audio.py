# 24-ssd-ja-30s soundtrack (30 s, 50% pacing) — marimba tech-explainer bed + sticker/UI sound design locked to cues.json
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib', 'audio'))
import mgaudio as mg
from mgaudio import recipes, sfx
D = os.path.dirname(os.path.abspath(__file__)) + '/'
C = json.load(open(D + 'cues.json', encoding='utf-8')); E = C['ev']
os.makedirs(D + 'out', exist_ok=True)

m = recipes.explainer(duration=float(C['duration']), bpm=C['bpm'], key='D', drop=E['grow'][0], outro=E['card'])
S = m.sfx
key_note = lambda t, i=0: m.form.chord_at(t)[i % len(m.form.chord_at(t))] + 12

# A — title: SSD sticker slaps down, lines swish in, marker stroke
S(sfx.swish(dur=.2, seed=1), at=.04, gain=-12, pan=.35)
S(sfx.sticker_slap(seed=2), at=E['ssd_land'], gain=-2, pan=.35)
S(sfx.swish(dur=.26, seed=3), at=E['title1'] + .12, gain=-10, pan=-.3)
S(sfx.swish(dur=.26, seed=4), at=E['title2'] + .12, gain=-10, pan=-.3)
S(sfx.click('soft'), at=E['kicker'], gain=-11)
S(sfx.pen('marker', dur=.3, seed=5), at=E['marker'][0] + .05, gain=-10, pan=-.2)

# camera flies: whoosh peaks near the middle of each move, page-flip accent
for i, (a, b) in enumerate([E['fly1'], E['fly2'], E['fly3']]):
    S(sfx.whoosh(dur=b - a + .15, kind='swish', direction=1, peak=.45, seed=10 + i), at=(a + b) / 2, gain=-5)
    S(sfx.paper('flip', dur=.2, seed=20 + i), at=(a + b) / 2 - .03, gain=-10, pan=.25)

# B — bar grows with rising ticks, system chunk slams, icons pop, readout counts down
g0, g1 = E['grow']
for k in range(10):
    t = g0 + (g1 - g0) * (1 - (1 - (k + 1) / 10) ** 2)
    S(sfx.tick('hi'), at=t, gain=-16 + k * .6, pan=-.5 + k * .1)
S(sfx.ding(note=key_note(g1, 0)), at=g1, gain=-10)
S(sfx.text_hit('slam', seed=30), at=E['sys_slam'], gain=-6, pan=-.4)
S(sfx.sticker_slap(seed=31), at=E['sys_slam'], gain=-6, pan=-.4)
for i, t in enumerate(E['icons']):
    S(sfx.sticker_slap(seed=32 + i), at=t, gain=-7, pan=-.5 + .2 * i)
    S(sfx.blip(note=key_note(t, i), kind='sine'), at=t + .06, gain=-13, pan=-.5 + .2 * i)
c0, c1 = E['count_down']
for k in range(6):
    S(sfx.tick('clock'), at=c0 + (c1 - c0) * k / 5, gain=-17, pan=.4)
S(sfx.ui('confirm'), at=E['usable'], gain=-11, pan=.2)
S(sfx.swish(dur=.24, seed=35), at=E['b_sub'] + .05, gain=-12)

# C — game blocks drop in, files overflow, stamp
for i, t in enumerate(E['games']):
    S(sfx.whoosh(dur=.3, kind='swish', direction=-1, peak=.8, seed=40 + i), at=t - .05, gain=-14)
    S(sfx.sticker_slap(seed=43 + i), at=t, gain=-3, pan=-.3 + .25 * i)
    S(sfx.blip(note=key_note(t, i) , kind='sine'), at=t + .02, gain=-12, pan=-.3 + .25 * i)
S(sfx.sticker_slap(seed=47), at=E['files'], gain=-3, pan=.5)
S(sfx.hud_alert(cycles=2), at=E['files'] + .04, gain=-14, pan=.5)
S(sfx.stamp('seal', seed=48), at=E['stamp'], gain=0, pan=.3)
S(sfx.impact(kind='punch', size=.7), at=E['stamp'], gain=-6)

# D — bars grow, controller icons pop like counting, 'recommended' badges slap
for i, t in enumerate(E['rows']):
    S(sfx.swish(dur=.4, seed=50 + i), at=t + .12, gain=-13, pan=.2)
n_icons = [3, 7, 15]
for i, t in enumerate(E['rows']):
    for k in range(n_icons[i]):
        at = t + E['icon_delay'] + k * E['icon_step']
        S(sfx.click('wood'), at=at, gain=-19 + 4 * k / max(1, n_icons[i] - 1), pan=-.4 + .8 * k / max(1, n_icons[i] - 1))
    S(sfx.blip(note=key_note(t, i) + 12, kind='sine'), at=t + E['icon_delay'] + n_icons[i] * E['icon_step'], gain=-12)
for i, t in enumerate(E['reco']):
    S(sfx.sticker_slap(seed=60 + i), at=t, gain=-3, pan=-.5)
    S(sfx.ding(note=key_note(t, i + 1) + 12), at=t, gain=-8, pan=-.5)

# E — pull-out, conclusion card slams, lines reveal
p0, p1 = E['pull']
S(sfx.whoosh(dur=p1 - p0 + .2, kind='air', direction=0, peak=.4, seed=70), at=(p0 + p1) / 2, gain=-6)
S(sfx.riser(dur=.8, kind='hybrid', end='cut'), at=E['card'] - .1, gain=-11)
S(sfx.impact(kind='punch', size=1.0), at=E['card'], gain=0)
S(sfx.boom(dur=1.4), at=E['card'], gain=-5)
S(sfx.sticker_slap(seed=71), at=E['card'], gain=-2)
S(sfx.swish(dur=.3, seed=72), at=E['end1'] + .08, gain=-10)
S(sfx.swish(dur=.3, seed=73), at=E['end2'] + .08, gain=-9)
S(sfx.pen('marker', dur=.35, seed=74), at=E['marker_end'][0] + .05, gain=-12, pan=.2)

# mix: brief suck-out before the conclusion slam
cd = E['card']
m.group('music').automate('gain', [(0, 0), (cd - .4, 0), (cd - .12, -10), (cd - .004, -10), (cd, 0), (C['duration'], 0)])
res = m.export(D + 'out/audio.wav', tp=-1.5)
print(res if not isinstance(res, dict) else {k: v for k, v in res.items() if k != 'spectrum'})
