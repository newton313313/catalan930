"""
Scene F53 —— 係數 2 是兩張水管圖：pipe dream（Fulton §10.4 p.172 的註、練習 5；書外延伸 Billey–Jockusch–Stanley）
執行（在 codes/ 內）：manimgl scenes/sceneF53_pipe_dreams.py SceneF53PipeDreams
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.schubert import length, pipe_dreams, pipe_exits, pipe_weight, poly_str, schubert_poly
from utils.scene_base import ChuScene
from utils.schubert_draw import PipeDreamMob
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import poly_sum

SLOW = 4.4
ACCENT = YELLOW
PIPE_COLORS = [RED_C, BLUE_C, GREEN_C, ORANGE, PURPLE_B]
W = (2, 1, 5, 4, 3)
TARGET = (2, 1, 1, 0, 0)
EMPTY3 = ()
NON3 = ((1, 2), (2, 1))                       # 2、3 號交叉兩次：不是縮減 pipe dream


def fit(m, w):
    if m.get_width() > w:
        m.set_width(w)
    return m


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def pipe_routes(D, m):
    """每條水管經過的格子與走法（LR 直走、BT 直上、LT 左進上出、BR 下進右出）；規則同 schubert.pipe_exits。
    回傳 [(segs, 出口行), …] 與 {十字格: (橫的那條, 直的那條)}。"""
    D = set(D)
    routes, at_cross = [], {}
    for i in range(1, m + 1):
        r, c, d = i, 1, "R"
        segs = []
        while True:
            cross = (r, c) in D and r + c <= m
            if d == "R" and cross:
                segs.append((r, c, "LR"))
                at_cross.setdefault((r, c), [None, None])[0] = i
                c += 1
            elif d == "R":
                segs.append((r, c, "LT"))
                if r == 1:
                    break
                r, d = r - 1, "U"
            elif cross:
                segs.append((r, c, "BT"))
                at_cross.setdefault((r, c), [None, None])[1] = i
                if r == 1:
                    break
                r -= 1
            else:
                segs.append((r, c, "BR"))
                c, d = c + 1, "R"
        routes.append((segs, c))
    return routes, {k: tuple(v) for k, v in at_cross.items()}


def crossing_pairs(D, m):
    out = {}
    for a, b in pipe_routes(D, m)[1].values():
        key = tuple(sorted((a, b)))
        out[key] = out.get(key, 0) + 1
    return out


def mono(e):
    return poly_str({tuple(e): 1})


def dream_group(D, m, cs, center, labels=True, colored=True):
    """PipeDreamMob＋十字格底色＋上色的水管＋入口／出口標號。回傳 VGroup(base, hl, pipes, ins, outs)。"""
    pd = PipeDreamMob(D, m, cs=cs).move_to(center)
    c11 = pd.frame_cells[0].get_center()
    h = cs / 2

    def cc(i, j):
        return c11 + np.array([(j - 1) * cs, -(i - 1) * cs, 0])

    hl = VGroup(*[Square(cs).move_to(cc(i, j)).set_stroke(width=0).set_fill(ACCENT, 0.22) for i, j in D])
    pipes, ins, outs = VGroup(), VGroup(), VGroup()
    routes, _ = pipe_routes(D, m)
    for k, (segs, exit_c) in enumerate(routes):
        col = PIPE_COLORS[k % len(PIPE_COLORS)]
        g = VGroup()
        for r, c, kind in segs:
            p = cc(r, c)
            if kind == "LR":
                s = Line(p + LEFT * h, p + RIGHT * h)
            elif kind == "BT":
                s = Line(p + DOWN * h, p + UP * h)
            elif kind == "LT":
                s = Arc(start_angle=-PI / 2, angle=PI / 2, radius=h, arc_center=p + np.array([-h, h, 0]))
            else:
                s = Arc(start_angle=PI, angle=-PI / 2, radius=h, arc_center=p + np.array([h, -h, 0]))
            g.add(s)
        g.set_stroke(col, max(2.0, 9 * cs))
        pipes.add(g)
        fs = max(18, 40 * cs)
        ins.add(tex(str(k + 1), fs, col).move_to(cc(k + 1, 1) + LEFT * (h + 0.22)))
        outs.add(tex(str(k + 1), fs, col).move_to(cc(1, exit_c) + UP * (h + 0.22)))
    grp = VGroup(pd, hl, pipes, ins, outs)
    grp.pd, grp.hl, grp.pipes, grp.ins, grp.outs, grp.cc = pd, hl, pipes, ins, outs, cc
    return grp


def show_dream(scene, g, trace=True, run_time=1.6):
    scene.play(FadeIn(g.pd), FadeIn(g.hl), FadeIn(g.ins), run_time=0.8)
    if trace:
        scene.play(LaggedStart(*[ShowCreation(p) for p in g.pipes], lag_ratio=0.25), run_time=run_time)
        scene.play(LaggedStart(*[FadeIn(o, shift=0.15 * UP) for o in g.outs], lag_ratio=0.15), run_time=0.7)


def check_math():
    S = schubert_poly(W)
    assert len(S) == 13 and S[TARGET] == 2 and all(c > 0 for c in S.values()) and sum(S.values()) == 14
    assert list(sorted(S, reverse=True)).index(TARGET) == 4
    dreams = pipe_dreams(W)
    assert len(dreams) == 14
    assert poly_sum([{pipe_weight(D, 5): 1} for D in dreams]) == S                     # Σ x^D = 𝔖_w
    two = [D for D in dreams if pipe_weight(D, 5) == TARGET]
    assert two == [((1, 1), (1, 3), (2, 3), (3, 1)), ((1, 1), (1, 4), (2, 2), (3, 2))]
    small = {(1, 2, 3): [()], (1, 3, 2): [((1, 2),), ((2, 1),)], (3, 2, 1): [((1, 1), (1, 2), (2, 1))]}
    for w, ds in small.items():
        assert pipe_dreams(w) == ds
        assert poly_sum([{pipe_weight(D, 3): 1} for D in ds]) == schubert_poly(w)
    assert [mono(pipe_weight(D, 3)) for D in small[(1, 3, 2)]] == ["x_1", "x_2"]
    assert mono(pipe_weight(small[(3, 2, 1)][0], 3)) == "x_1^{2}x_2"
    for D, m, w in [(D, 5, W) for D in dreams] + [(D, 3, w) for w, ds in small.items() for D in ds]:
        routes, _ = pipe_routes(D, m)
        assert tuple(c for _, c in routes) == pipe_exits(D, m) == w
        assert all(v == 1 for v in crossing_pairs(D, m).values()) and len(crossing_pairs(D, m)) == length(w)
    assert pipe_exits(NON3, 3) == (1, 2, 3) and crossing_pairs(NON3, 3) == {(2, 3): 2}
    assert tuple(c for _, c in pipe_routes(NON3, 3)[0]) == (1, 2, 3)
    assert pipe_weight(NON3, 3) == (1, 1, 0)


# ---------------------------------------------------------------- 1. 問題
def part_question(scene):
    S = schubert_poly(W)
    terms = sorted(S, reverse=True)
    title = tex(r"\mathfrak S_{21543}=", 46).move_to(np.array([-4.9, 2.3, 0]))
    chips = VGroup()
    for k, e in enumerate(terms):
        s = (str(S[e]) if S[e] > 1 else "") + mono(e)
        t = tex(("+" if k else "") + s, 38, ACCENT if e == TARGET else WHITE)
        t.move_to(np.array([-5.0 + 2.5 * (k % 5), 1.3 - 0.9 * (k // 5), 0]))
        chips.add(t)
    frame = SurroundingRectangle(chips[terms.index(TARGET)], buff=0.12).set_stroke(ACCENT, 3)
    note = mixed("共 13 項；係數加起來是 14", font_size=28, color=MUTED_COLOR).move_to(np.array([0, -1.2, 0]))
    cred = fit(zh("Macdonald：係數永遠不是負的　Billey–Jockusch–Stanley（1993）：組合公式", font_size=24,
                  color=MUTED_COLOR), 12.6).move_to(np.array([0, -2.1, 0]))
    assert_in_frame(title, chips, frame, note, cred)
    assert_apart(title, chips, 0.15)
    assert_apart(chips, note, 0.2)

    scene.say("問：練習 5 說 ", r"$\mathfrak S_{21543}$", " 裡 ", "$x_1^2x_2x_3$", " 的係數是 2", wait=SLOW * 0.3)
    scene.play(FadeIn(title), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.15 * DOWN) for c in chips], lag_ratio=0.12), run_time=2.2)
    scene.play(ShowCreation(frame), run_time=0.7)
    scene.say("這個 2 數的是什麼？", wait=SLOW * 0.7)
    scene.play(FadeIn(note, shift=0.2 * UP), run_time=0.6)
    scene.say("13 項，係數全是正整數；書上說這是一般的事實", wait=SLOW * 0.5)
    scene.play(FadeIn(cred), run_time=0.8)
    scene.say("Billey–Jockusch–Stanley 的公式：去數一種「水管圖」", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 2. 規則
def part_rules(scene):
    center = np.array([-4.1, 0.1, 0])
    E = dream_group(EMPTY3, 3, 1.0, center)
    N = dream_group(NON3, 3, 1.0, center)
    lines = [("格子：階梯上 ", "$i+j\\le m$", " 的格子，外緣半格只能轉彎"),
             ("每一格放「十字」或「一對彎管」",),
             ("第 ", "$i$", " 條從左邊第 ", "$i$", " 列流進，從頂端第 ", "$w(i)$", " 行流出"),
             ("任兩條水管最多交叉一次",),
             ("權重 ", "$x^D$", "：第 ", "$i$", " 列的每個十字給一個 ", "$x_i$")]
    rules = VGroup()
    for k, ln in enumerate(lines):
        t = fit(mixed(*ln, font_size=26), 7.4).move_to(np.array([-1.0, 2.2 - 0.85 * k, 0]), aligned_edge=LEFT)
        rules.add(t)
    tag = tex(r"w=123,\quad x^D=1", 34, ACCENT).move_to(np.array([-4.1, -2.35, 0]))
    bad = mixed("2、3 號交叉兩次：不算", font_size=26, color=PINK).move_to(np.array([-4.1, -2.35, 0]))
    assert_in_frame(E, N, rules, tag, bad)
    for g in (E, N):
        assert_apart(g, rules, 0.3)
        assert_apart(g, tag, 0.15)

    scene.say("水管圖（pipe dream）：先拿 ", "$m=3$", " 的階梯格子", wait=SLOW * 0.2)
    scene.play(FadeIn(E.pd.frame_cells), FadeIn(rules[0], shift=0.2 * RIGHT), run_time=1.0)
    scene.wait(SLOW * 0.5)
    scene.play(FadeIn(E.pd.tiles), FadeIn(rules[1], shift=0.2 * RIGHT), run_time=1.0)
    scene.say("這一張全是彎管：一個十字都沒有", wait=SLOW * 0.5)
    scene.play(FadeIn(E.ins), FadeIn(rules[2], shift=0.2 * RIGHT), run_time=0.9)
    scene.say("每條水管從左邊流進，往右或往上走，從頂端流出", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[ShowCreation(p) for p in E.pipes], lag_ratio=0.3), run_time=2.0)
    scene.play(LaggedStart(*[FadeIn(o, shift=0.15 * UP) for o in E.outs], lag_ratio=0.2), run_time=0.7)
    scene.play(FadeIn(tag), run_time=0.6)
    scene.say("出口依序是 1, 2, 3：這張圖屬於 ", "$w=123$", "，權重 1", wait=SLOW * 0.8)
    scene.play(FadeOut(E), FadeOut(tag), run_time=0.6)
    show_dream(scene, N)
    scene.play(FadeIn(rules[3], shift=0.2 * RIGHT), FadeIn(bad), run_time=0.8)
    scene.say("放兩個十字：2、3 號交叉了兩次，出口又回到 123", wait=SLOW * 0.6)
    scene.say("這種圖不算——只用「縮減」的：任兩條最多交叉一次", wait=SLOW * 0.7)
    scene.play(FadeOut(N), FadeOut(bad), run_time=0.6)
    scene.play(FadeIn(rules[4], shift=0.2 * RIGHT), run_time=0.8)
    scene.say("權重：數每一列有幾個十字，第 ", "$i$", " 列的十字記作 ", "$x_i$", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 3. 小例子
def part_small(scene):
    cs = 0.85
    specs = [((1, 2),), ((2, 1),), ((1, 1), (1, 2), (2, 1))]
    xs = [-4.5, -0.9, 3.9]
    gs = [dream_group(D, 3, cs, np.array([x, 0.35, 0])) for D, x in zip(specs, xs)]
    heads = [tex(r"w=132", 34).move_to(np.array([-2.7, 2.65, 0])), tex(r"w=321", 34).move_to(np.array([3.9, 2.65, 0]))]
    ws = [tex(mono(pipe_weight(D, 3)), 38, ACCENT).move_to(np.array([x, -1.55, 0])) for D, x in zip(specs, xs)]
    sums = [tex(r"\mathfrak S_{132}=x_1+x_2", 40).move_to(np.array([-2.7, -2.45, 0])),
            tex(r"\mathfrak S_{321}=x_1^{2}x_2", 40).move_to(np.array([3.9, -2.45, 0]))]
    assert_in_frame(*gs, *heads, *ws, *sums)
    assert_apart(gs[0], gs[1], 0.2)
    assert_apart(gs[1], gs[2], 0.4)
    for g in gs:
        assert_apart(g, VGroup(*heads), 0.1)
        assert_apart(g, VGroup(*ws), 0.1)

    scene.say("小例子：", "$w=132$", "，只要一個十字，讓 2、3 號交叉", wait=SLOW * 0.2)
    scene.play(FadeIn(heads[0]), run_time=0.5)
    show_dream(scene, gs[0], run_time=1.4)
    scene.say("十字放在第 1 列：權重 ", "$x_1$", wait=SLOW * 0.2)
    scene.play(FadeIn(ws[0], shift=0.2 * UP), run_time=0.6)
    scene.wait(SLOW * 0.3)
    show_dream(scene, gs[1], run_time=1.4)
    scene.say("另一張：十字放在第 2 列，權重 ", "$x_2$", wait=SLOW * 0.2)
    scene.play(FadeIn(ws[1], shift=0.2 * UP), run_time=0.6)
    scene.play(Write(sums[0]), run_time=1.0)
    scene.say("兩張加起來，正是 F52 算過的 ", r"$\mathfrak S_{132}=x_1+x_2$", wait=SLOW * 0.8)
    scene.play(FadeIn(heads[1]), run_time=0.5)
    show_dream(scene, gs[2], run_time=1.6)
    scene.play(FadeIn(ws[2], shift=0.2 * UP), Write(sums[1]), run_time=1.0)
    scene.say("$w=321$", " 三條兩兩交叉，只有一張：", "$x_1^2x_2$", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 4. 練習 5
def part_exercise(scene):
    cs = 0.7
    two = [D for D in pipe_dreams(W) if pipe_weight(D, 5) == TARGET]
    gs = [dream_group(D, 5, cs, np.array([x, 0.3, 0])) for D, x in zip(two, (-3.3, 3.1))]
    rowtags = []
    for g, D in zip(gs, two):
        wt = pipe_weight(D, 5)
        tags = VGroup()
        for i, k in enumerate(wt, start=1):
            if k:
                s = "x_%d" % i + ("^{%d}" % k if k > 1 else "")
                tags.add(tex(s, 28, ACCENT).move_to(g.cc(i, 6 - i) + RIGHT * (cs / 2 + 0.45)))
        rowtags.append(tags)
    wts = [tex(r"x^D=x_1^{2}x_2x_3", 36, ACCENT).move_to(np.array([x, -2.1, 0])) for x in (-3.3, 3.1)]
    assert_in_frame(*gs, *rowtags, *wts)
    assert_apart(VGroup(gs[0], rowtags[0]), VGroup(gs[1], rowtags[1]), 0.3)
    for g, w in zip(gs, wts):
        assert_apart(g, w, 0.1)

    scene.say("回到練習 5：", "$w=21543$", "，權重是 ", "$x_1^2x_2x_3$", " 的圖有幾張？", wait=SLOW * 0.2)
    show_dream(scene, gs[0], run_time=2.2)
    scene.say("五條水管各從左邊進來；頂端出口依序是 2, 1, 5, 4, 3", wait=SLOW * 0.5)
    scene.play(LaggedStart(*[FadeIn(t) for t in rowtags[0]], lag_ratio=0.3), run_time=0.9)
    scene.say("每列的十字：2, 1, 1, 0, 0", wait=SLOW * 0.2)
    scene.play(FadeIn(wts[0], shift=0.2 * UP), run_time=0.6)
    scene.wait(SLOW * 0.4)
    show_dream(scene, gs[1], run_time=2.2)
    scene.play(LaggedStart(*[FadeIn(t) for t in rowtags[1]], lag_ratio=0.3), FadeIn(wts[1], shift=0.2 * UP),
               run_time=1.0)
    scene.say("另一張：十字的位置不同，每列的個數一樣", wait=SLOW * 0.7)
    scene.play(*[Indicate(w, scale_factor=1.15) for w in wts], run_time=1.0)
    scene.say("恰好兩張，所以係數是 2", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 5. 全部 14 張
def part_all(scene):
    dreams = sorted(pipe_dreams(W), key=lambda D: (pipe_weight(D, 5), D), reverse=True)
    formula = tex(r"\mathfrak S_w=\sum_D x^D", 46).move_to(np.array([-3.2, 2.35, 0]))
    ext = zh("（書外的延伸：Billey–Jockusch–Stanley 1993）", font_size=24, color=MUTED_COLOR)
    ext.next_to(formula, RIGHT, buff=0.5)
    cells = VGroup()
    hi = VGroup()
    for k, D in enumerate(dreams):
        x, y = -5.55 + 1.85 * (k % 7), 0.7 - 2.1 * (k // 7)
        pd = PipeDreamMob(D, 5, cs=0.28).move_to(np.array([x, y, 0]))
        pd.tiles.set_stroke(width=1.8)
        pd.frame_cells.set_stroke(width=0.6)
        lab = tex(mono(pipe_weight(D, 5)), 24, ACCENT if pipe_weight(D, 5) == TARGET else WHITE)
        lab.next_to(pd, DOWN, buff=0.18)
        cell = VGroup(pd, lab)
        cells.add(cell)
        if pipe_weight(D, 5) == TARGET:
            hi.add(cell)
    box = SurroundingRectangle(hi, buff=0.12).set_stroke(ACCENT, 3)
    assert_in_frame(formula, ext, cells, box)
    assert_apart(VGroup(formula, ext), cells, 0.2)
    for a, b in zip(cells, cells[1:]):
        assert_apart(a, b, 0.1)

    scene.say("把 ", "$w=21543$", " 的縮減水管圖全部列出來：14 張", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.1), run_time=2.8)
    scene.wait(SLOW * 0.4)
    scene.play(Write(formula), FadeIn(ext), run_time=1.2)
    scene.say("每張的權重加起來，就是 ", r"$\mathfrak S_{21543}$", " 的 13 項", wait=SLOW * 0.7)
    scene.play(ShowCreation(box), run_time=0.8)
    scene.say("14 張圖、13 項：只有 ", "$x_1^2x_2x_3$", " 出現兩次", wait=SLOW * 0.8)
    scene.say("係數＝圖的張數，所以一定是非負整數", wait=SLOW * 1.3)


class SceneF53PipeDreams(ChuScene):
    def construct(self):
        self.show_header("係數 2 是兩張水管圖：pipe dream")
        check_math()
        part_question(self)
        self.clear_stage()
        part_rules(self)
        self.clear_stage()
        part_small(self)
        self.clear_stage()
        part_exercise(self)
        self.clear_stage()
        part_all(self)
        self.wait(1.0)
