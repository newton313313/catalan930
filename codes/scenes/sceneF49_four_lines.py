"""
Scene F49 —— 四條線問題：Schubert 計算（Fulton §9.4，書 p.146–153）
執行（在 codes/ 內）：manimgl scenes/sceneF49_four_lines.py SceneF49FourLines

P^3 的直線 = Gr(2,4)；「和一條線相交」= Ω_1；σ_1^4 ∈ H^8 = Zσ_22。2×2 方框裡的 Pieri：
σ1σ1 = σ2+σ11、σ1σ2 = σ1σ11 = σ21、σ1σ21 = σ22 ⇒ σ1^4 = 2σ22（兩條路徑 = (2,2) 的兩個標準表）→ 2 條線；
對偶（Lemma 3、式 (11)）；Gr(2,5)：f^{(3,3)} = 5 = 6!·1!/(4!·3!)；Gr(3,6)：42；
Gr(3,6) 裡 σ21² = σ33 + 2σ321 + σ222（超出方框的 s42, s411, s3111, s2211 丟掉）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *
from math import factorial

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR
from utils.scene_base import ChuScene
from utils.schubert import box_product, rectangle_count
from utils.schubert_draw import BOX_COLOR, BoxDiagramMob
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import lr_coefficient, partitions, standard_tableaux

LAT_POS = {(): (-5.6, 0.1), (1,): (-3.7, 0.1), (2,): (-1.8, 1.0), (1, 1): (-1.8, -0.8), (2, 1): (0.1, 0.1),
           (2, 2): (2.0, 0.1)}
LAT_EDGES = [((), (1,)), ((1,), (2,)), ((1,), (1, 1)), ((2,), (2, 1)), ((1, 1), (2, 1)), ((2, 1), (2, 2))]
PATHS = [[(), (1,), (2,), (2, 1), (2, 2)], [(), (1,), (1, 1), (2, 1), (2, 2)]]
DUALS = [((1,), (2, 1), r"\sigma_1\sigma_{21}=\sigma_{22}", "平面裡過一點的線，再和一條線相交：1 條"),
         ((2,), (2,), r"\sigma_2\sigma_2=\sigma_{22}", "過兩個點的線：1 條"),
         ((2,), (1, 1), r"\sigma_2\sigma_{11}=0", "過一點的線，又要落在一個平面裡：沒有")]
LR_PIECES = ["s_{21}^2=", "s_{42}", "+", "s_{411}", "+", "s_{33}", "+", "2s_{321}", "+", "s_{3111}", "+", "s_{222}",
             "+", "s_{2211}"]
LR_OUT = [1, 3, 9, 13]                       # 超出 3×3 方框的項（在 LR_PIECES 裡的位置）
SLOW = 3.8


def sigma1_power(k, r, n):
    cur = {(1,): 1}
    for _ in range(k - 1):
        new = {}
        for lam, c in cur.items():
            for nu, d in box_product((1,), lam, r, n).items():
                new[nu] = new.get(nu, 0) + c * d
        cur = new
    return cur


def path_tableau(path):
    T = [[], []]
    for k, (a, b) in enumerate(zip(path, path[1:])):
        a, b = tuple(a) + (0, 0), tuple(b) + (0, 0)
        i = next(i for i in range(2) if b[i] > a[i])
        T[i].append(k + 1)
    return tuple(tuple(r) for r in T if r)


def pad(lam):
    return tuple(lam) + (0,) * (2 - len(lam))


def rot_cells(mu):
    mu = pad(mu)
    return {(1 - i, 1 - j) for i in range(2) for j in range(mu[i])}


def lam_cells(lam):
    lam = pad(lam)
    return {(i, j) for i in range(2) for j in range(lam[i])}


def fit(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def split_tex(pieces, font_size):
    """整條式子一次排版；依字形數切成各段（失敗時改成分開排）。"""
    full = Tex("".join(pieces), font_size=font_size)
    counts = [sum(ch not in "{}_^ " for ch in p) for p in pieces]
    if len(full) == sum(counts):
        out, k = [], 0
        for n in counts:
            out.append(full[k:k + n])
            k += n
        return full, out
    parts = [Tex(p, font_size=font_size) for p in pieces]
    return VGroup(*parts).arrange(RIGHT, buff=0.06), parts


def check_math():
    assert box_product((1,), (1,), 2, 2) == {(2,): 1, (1, 1): 1}
    assert box_product((1,), (2,), 2, 2) == {(2, 1): 1} == box_product((1,), (1, 1), 2, 2)
    assert box_product((1,), (2, 1), 2, 2) == {(2, 2): 1}
    assert lr_coefficient((1,), (2,), (3,)) == 1                # σ1σ2 的 s3 放不進方框
    assert sigma1_power(4, 2, 2) == {(2, 2): 2}
    syt = {tuple(tuple(r) for r in T) for T in standard_tableaux((2, 2))}
    assert syt == {path_tableau(p) for p in PATHS} == {((1, 2), (3, 4)), ((1, 3), (2, 4))}
    for a, b in LAT_EDGES:
        assert box_product((1,), a, 2, 2).get(b) == 1 if a else b == (1,)
    for lam, mu, _, _ in DUALS:
        fits = rot_cells(mu) == {(i, j) for i in range(2) for j in range(2)} - lam_cells(lam)
        assert box_product(lam, mu, 2, 2) == ({(2, 2): 1} if fits else {})
    assert not rot_cells((1, 1)).isdisjoint(lam_cells((2,)))
    assert sigma1_power(6, 2, 3) == {(3, 3): 5} and len(standard_tableaux((3, 3))) == 5
    assert rectangle_count(2, 5) == 5 == factorial(6) * factorial(1) // (factorial(4) * factorial(3))
    assert factorial(6) * factorial(1) == 720 and factorial(4) * factorial(3) == 144
    assert rectangle_count(3, 6) == 42 == len(standard_tableaux((3, 3, 3)))
    full = {tuple(nu): lr_coefficient((2, 1), (2, 1), tuple(nu)) for nu in partitions(6)}
    full = {nu: c for nu, c in full.items() if c}
    assert full == {(4, 2): 1, (4, 1, 1): 1, (3, 3): 1, (3, 2, 1): 2, (3, 1, 1, 1): 1, (2, 2, 2): 1, (2, 2, 1, 1): 1}
    assert box_product((2, 1), (2, 1), 3, 3) == {(3, 3): 1, (3, 2, 1): 2, (2, 2, 2): 1}
    out = [(4, 2), (4, 1, 1), (3, 1, 1, 1), (2, 2, 1, 1)]
    assert all(nu[0] > 3 or len(nu) > 3 for nu in out) and set(full) - set(out) == {(3, 3), (3, 2, 1), (2, 2, 2)}
    assert [LR_PIECES[k] for k in LR_OUT] == ["s_{42}", "s_{411}", "s_{3111}", "s_{2211}"]


# ---------------------------------------------------------------- 示意圖：直線掃出的二次曲面
def quadric_pic(center=(-3.6, 0.1, 0), a=1.5, b=0.32, h=1.45, phi=2.0):
    c = np.array(center, dtype=float)

    def top(t):
        return c + np.array([a * np.cos(t), h + b * np.sin(t), 0])

    def bot(t):
        return c + np.array([a * np.cos(t), -h + b * np.sin(t), 0])

    def ext_line(p, q, e=0.2):
        d = (q - p) / np.linalg.norm(q - p)
        return Line(p - e * d, q + e * d)

    rims = VGroup(Ellipse(width=2 * a, height=2 * b).move_to(c + h * UP),
                  Ellipse(width=2 * a, height=2 * b).move_to(c + h * DOWN)).set_stroke(GREY_D, 1.5)
    sweep = VGroup(*[Line(top(t), bot(t - phi)) for t in np.linspace(0, TAU, 14, endpoint=False)])
    sweep.set_stroke(TEAL_E, 1.5, opacity=0.7)
    given = VGroup(*[ext_line(top(t), bot(t + phi)) for t in (0.3, 2.5, 4.5)]).set_stroke(BLUE_C, 4)
    glabs = VGroup(*[Tex("L_%d" % (k + 1), font_size=26).set_color(BLUE_C).next_to(l.get_end(), DOWN, buff=0.08)
                     for k, l in enumerate(given)])
    ta, tb = TAU * 2 / 14, TAU * 8 / 14
    A = top(ta) + 0.3 * (bot(ta - phi) - top(ta))
    B = top(tb) + 0.7 * (bot(tb - phi) - top(tb))
    l4 = Line(A + 1.1 * (A - B), B + 1.1 * (B - A)).set_stroke(NEG_COLOR, 4)
    l4lab = Tex("L_4", font_size=26).set_color(NEG_COLOR).next_to(l4.get_start(), UP, buff=0.08)
    dots = VGroup(Dot(A, radius=0.08), Dot(B, radius=0.08)).set_color(OP_COLOR)
    answers = VGroup(ext_line(top(ta), bot(ta - phi), 0.35), ext_line(top(tb), bot(tb - phi), 0.35))
    answers.set_stroke(OP_COLOR, 5)
    return dict(rims=rims, sweep=sweep, given=given, glabs=glabs, l4=VGroup(l4, l4lab), dots=dots, answers=answers)


# ---------------------------------------------------------------- 1. 問題與翻譯
def part_question(scene):
    pic = quadric_pic()
    allpic = VGroup(*pic.values())
    cx = 3.4
    t1 = mixed("$\\mathbb P^3$", " 的直線 ＝ ", "$\\mathbb C^4$", " 的 2 維子空間", font_size=28)
    t2 = mixed("所有直線：", "$Gr(2,4)$", "，維數 4", font_size=28)
    t3 = mixed("和一條給定的線相交：", "$\\Omega_1$", "，餘維 1", font_size=28)
    t4 = Tex(r"\sigma_1^4\in H^8(Gr(2,4))=\mathbb Z\,\sigma_{22}", font_size=36).set_color(OP_COLOR)
    t5 = mixed("四個條件：", "$4-4=0$", " 維，只剩有限多條", font_size=28)
    texts = [t1, t2, t3, t4, t5]
    for k, t in enumerate(texts):
        fit(t, 5.8).move_to(np.array([cx, 2.1 - 0.95 * k, 0]))
    assert_in_frame(allpic, *texts)
    assert_apart(allpic, VGroup(*texts), 0.3)
    for u, v in zip(texts, texts[1:]):
        assert_apart(u, v, 0.1)

    scene.say("問：空間中四條一般的直線，有幾條直線和它們四條都相交？", wait=SLOW * 0.8)
    scene.play(ShowCreation(pic["given"]), FadeIn(pic["glabs"]), run_time=1.4)
    scene.say("先看三條：和 ", "$L_1,L_2,L_3$", " 都相交的直線，掃出一個曲面", wait=SLOW * 0.2)
    scene.play(ShowCreation(pic["rims"]), ShowCreation(pic["sweep"], lag_ratio=0.1), run_time=2.0)
    scene.wait(SLOW * 0.4)
    scene.play(ShowCreation(pic["l4"][0]), FadeIn(pic["l4"][1]), run_time=1.0)
    scene.play(FadeIn(pic["dots"], scale=0.5), run_time=0.7)
    scene.play(Flash(pic["dots"][0], color=OP_COLOR), Flash(pic["dots"][1], color=OP_COLOR), run_time=0.9)
    scene.say("第四條線 ", "$L_4$", " 穿過這個曲面兩次……答案先留著", wait=SLOW * 0.8)
    scene.say("換成 Grassmannian 的語言來數", wait=SLOW * 0.2)
    for t in texts[:3]:
        scene.play(FadeIn(t, shift=0.2 * LEFT), run_time=0.7)
        scene.wait(SLOW * 0.35)
    scene.say("「和 ", "$L$", " 相交」是一個條件：Schubert 簇 ", "$\\Omega_1$", "，它的類是 ", "$\\sigma_1$",
              wait=SLOW * 0.6)
    scene.play(FadeIn(t4, shift=0.2 * LEFT), run_time=0.9)
    scene.say("四條線＝四個條件：算 ", "$\\sigma_1^4$", "，落在最高次的 ", "$H^8=\\mathbb Z\\,\\sigma_{22}$", wait=SLOW * 0.8)
    scene.play(FadeIn(t5, shift=0.2 * LEFT), run_time=0.8)
    scene.say("$\\sigma_{22}$", " 是一個點的類：", "$\\sigma_1^4$", " 前面的係數就是答案", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 2. 方框裡的 Pieri
def part_pieri(scene):
    nodes = {lam: BoxDiagramMob(lam, 2, 2, cs=0.33).move_to(np.array([x, y, 0])) for lam, (x, y) in LAT_POS.items()}
    arrows = {(a, b): Arrow(nodes[a].get_right(), nodes[b].get_left(), buff=0.12).set_color(GREY_B)
              for a, b in LAT_EDGES}
    x1 = Tex(r"\times\sigma_1", font_size=26).set_color(MUTED_COLOR).next_to(arrows[((), (1,))], UP, buff=0.12)
    eqs = [Tex(s, font_size=38).move_to(np.array([0, 2.5, 0])) for s in
           (r"\sigma_1\cdot\sigma_1=\sigma_2+\sigma_{11}", r"\sigma_1\sigma_2=\sigma_{21},\qquad\sigma_1\sigma_{11}=\sigma_{21}",
            r"\sigma_1\sigma_{21}=\sigma_{22}")]
    cols = (OP_COLOR, PINK)
    tabs = [tableau_mob(path_tableau(p), cs=0.45).move_to(np.array([4.6, y, 0])) for p, y in zip(PATHS, (1.0, -0.8))]
    tframes = [SurroundingRectangle(t, buff=0.12, color=c) for t, c in zip(tabs, cols)]
    final = Tex(r"\sigma_1^4=2\,\sigma_{22}", font_size=48).set_color(POS_COLOR).move_to(np.array([0, -2.2, 0]))
    ffr = SurroundingRectangle(final, buff=0.15, color=POS_COLOR)
    graph = VGroup(*nodes.values(), *arrows.values(), x1)
    assert_in_frame(graph, *eqs, *tabs, *tframes, final, ffr)
    assert_apart(graph, VGroup(*tframes), 0.4)
    assert_apart(VGroup(*eqs), graph, 0.2)
    assert_apart(graph, ffr, 0.15)
    assert_apart(*tframes, 0.1)

    scene.say("Pieri 規則：乘上 ", "$\\sigma_1$", " ＝ 加一格；在 ", "$Gr(2,4)$", " 裡不能超出 ", "$2\\times2$", " 方框",
              wait=SLOW * 0.5)
    scene.play(FadeIn(nodes[()]), run_time=0.6)
    scene.play(GrowArrow(arrows[((), (1,))]), FadeIn(x1), FadeIn(nodes[(1,)]), run_time=0.9)
    scene.play(FadeIn(eqs[0]), run_time=0.8)
    scene.play(GrowArrow(arrows[((1,), (2,))]), GrowArrow(arrows[((1,), (1, 1))]), FadeIn(nodes[(2,)]),
               FadeIn(nodes[(1, 1)]), run_time=1.0)
    scene.say("$\\sigma_1\\cdot\\sigma_1=\\sigma_2+\\sigma_{11}$", "：一格可以加在右邊或下面", wait=SLOW * 0.7)
    scene.play(FadeOut(eqs[0]), FadeIn(eqs[1]), run_time=0.8)
    scene.play(GrowArrow(arrows[((2,), (2, 1))]), GrowArrow(arrows[((1, 1), (2, 1))]), FadeIn(nodes[(2, 1)]),
               run_time=1.0)
    scene.say("$\\sigma_1\\sigma_2$", "：", "$s_3$", " 放不進方框，被丟掉，只剩 ", "$\\sigma_{21}$", wait=SLOW * 0.8)
    scene.play(FadeOut(eqs[1]), FadeIn(eqs[2]), run_time=0.8)
    scene.play(GrowArrow(arrows[((2, 1), (2, 2))]), FadeIn(nodes[(2, 2)]), run_time=0.8)
    scene.say("最後一格：", "$\\sigma_1\\sigma_{21}=\\sigma_{22}$", wait=SLOW * 0.6)
    scene.say("$\\sigma_1^4$", "：從空圖走到 ", "$(2,2)$", " 的路徑有幾條？", wait=SLOW * 0.3)
    for p, c, t, fr in zip(PATHS, cols, tabs, tframes):
        edges = [arrows[(a, b)] for a, b in zip(p, p[1:])]
        scene.play(*[e.animate.set_color(c) for e in edges], run_time=0.9)
        scene.play(FadeIn(t), ShowCreation(fr), run_time=0.8)
        scene.wait(SLOW * 0.5)
        scene.play(*[e.animate.set_color(GREY_B) for e in edges], run_time=0.5)
    scene.say("兩條路徑 ＝ ", "$(2,2)$", " 的兩個標準表（第幾步加的格子填幾）", wait=SLOW * 0.8)
    scene.play(Write(final), ShowCreation(ffr), run_time=1.2)
    scene.say("$\\sigma_1^4=2\\,\\sigma_{22}$", "：一般位置下，答案是 2", wait=SLOW * 0.8)


def part_reveal(scene):
    pic = quadric_pic()
    ans = mixed("答案：", "$2$", " 條", font_size=44, color=OP_COLOR).move_to(np.array([3.4, 0.6, 0]))
    sub = mixed("過 ", "$L_4$", " 和曲面的兩個交點，各有一條", font_size=26).move_to(np.array([3.4, -0.4, 0]))
    allpic = VGroup(*pic.values())
    assert_in_frame(allpic, ans, sub)
    assert_apart(allpic, VGroup(ans, sub), 0.3)
    scene.play(*[FadeIn(pic[k]) for k in ("rims", "sweep", "given", "glabs", "l4", "dots")], run_time=1.0)
    scene.play(ShowCreation(pic["answers"]), run_time=1.2)
    scene.play(FadeIn(ans, scale=1.2), FadeIn(sub), run_time=0.9)
    scene.say("回到圖上：過那兩個交點的掃描線，和四條線都相交", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 3. 對偶：拼滿方框
def part_duality(scene):
    lem = mixed("Lemma 3：", "$\\sigma_\\lambda\\sigma_\\mu=\\sigma_{22}$", " 恰好當 ", "$\\mu$", " 轉 180° 後和 ",
                "$\\lambda$", " 拼滿方框", font_size=28).move_to(np.array([0, 2.5, 0]))
    cs = 0.6
    xs = (-4.4, 0.0, 4.4)
    items = []
    for (lam, mu, eq, geo), x in zip(DUALS, xs):
        bc = np.array([x - 0.55, 0.8, 0])

        def pos(i, j, bc=bc):
            return bc + np.array([(j - 0.5) * cs, (0.5 - i) * cs, 0])

        frame = VGroup(*[Square(cs).move_to(pos(i, j)).set_stroke(BOX_COLOR, 1) for i in range(2) for j in range(2)])
        lc = VGroup(*[Square(cs).move_to(pos(i, j)).set_stroke(WHITE, 2).set_fill(BLUE_C, 0.6)
                      for i, j in sorted(lam_cells(lam))])
        target = VGroup(*[Square(cs).move_to(pos(i, j)).set_stroke(WHITE, 2).set_fill(ORANGE, 0.55)
                          for i, j in sorted(rot_cells(mu))])
        start = target.copy().rotate(PI)
        start.move_to(np.array([x + 1.3, 0.8, 0]))
        e = Tex(eq, font_size=36).set_color(POS_COLOR if "22" in eq.split("=")[1] else NEG_COLOR)
        e.move_to(np.array([x, -0.55, 0]))
        g = fit(zh(geo, font_size=24, color=MUTED_COLOR), 4.0).move_to(np.array([x, -1.35, 0]))
        bad = lam_cells(lam) & rot_cells(mu)
        cross = VGroup(*[VGroup(Line(pos(i, j) + 0.25 * (UL), pos(i, j) + 0.25 * DR),
                                Line(pos(i, j) + 0.25 * UR, pos(i, j) + 0.25 * DL)).set_stroke(RED, 5)
                         for i, j in sorted(bad)])
        items.append(dict(frame=frame, lc=lc, target=target, start=start, eq=e, geo=g, cross=cross))
    formula = Tex(r"\sigma_\lambda\cdot\sigma_\mu=\delta_{\mu,\lambda^\vee}\,\sigma_{22}\qquad(|\lambda|+|\mu|=4)",
                  font_size=34).move_to(np.array([0, -2.35, 0]))
    blocks = [VGroup(it["frame"], it["lc"], it["start"], it["eq"], it["geo"]) for it in items]
    assert_in_frame(lem, *blocks, formula)
    for u, v in zip(blocks, blocks[1:]):
        assert_apart(u, v, 0.3)
    assert_apart(lem, VGroup(*blocks), 0.3)
    assert_apart(VGroup(*blocks), formula, 0.2)

    scene.say("另一個好用的事實：兩個類相乘，什麼時候剛好是一個點？", wait=SLOW * 0.5)
    scene.play(FadeIn(lem, shift=0.2 * DOWN), run_time=0.9)
    for k, it in enumerate(items):
        scene.play(FadeIn(it["frame"]), FadeIn(it["lc"]), FadeIn(it["start"]), run_time=0.8)
        scene.play(Rotate(it["start"], PI), run_time=0.8)
        scene.play(it["start"].animate.move_to(it["target"].get_center()), run_time=0.8)
        if len(it["cross"]):
            scene.play(ShowCreation(it["cross"]), run_time=0.6)
        scene.play(FadeIn(it["eq"]), FadeIn(it["geo"]), run_time=0.7)
        if k == 0:
            scene.say("$\\mu=(2,1)$", " 轉半圈，正好補上 ", "$\\lambda=(1)$", " 缺的三格", wait=SLOW * 0.8)
        elif k == 1:
            scene.say("$(2)$", " 轉半圈變成下面一列：", "$\\sigma_2\\sigma_2=\\sigma_{22}$", wait=SLOW * 0.8)
        else:
            scene.say("$(1,1)$", " 轉半圈是右邊一行：和 ", "$(2)$", " 重疊，乘積是 0", wait=SLOW * 0.8)
    scene.play(Write(formula), run_time=1.2)
    scene.say("式 (11)：次數互補的兩個 Schubert 類，互為對偶基底", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 4. 推廣與方框裡的 LR
def part_general(scene):
    g1 = mixed("$Gr(2,5)$", "：六個條件，", "$\\sigma_1^6=5\\,\\sigma_{33}$", "，", "$f^{(3,3)}=5$", font_size=28)
    g2 = Tex(r"\frac{6!\cdot1!}{4!\cdot3!}=\frac{720}{144}=5", font_size=36)
    g3 = mixed("$Gr(3,6)$", "：九個條件，", "$\\sigma_1^9=42\\,\\sigma_{333}$", "，", "$f^{(3,3,3)}=42$", font_size=28)
    lr, pieces = split_tex(LR_PIECES, 34)
    res = Tex(r"\sigma_{21}^2=\sigma_{33}+2\,\sigma_{321}+\sigma_{222}", font_size=38).set_color(POS_COLOR)
    note = mixed("係數 2 就是第 5 章的 LR 係數 ", "$c^{321}_{21,21}=2$", font_size=26, color=OP_COLOR)
    for m, y in ((g1, 2.45), (g2, 1.55), (g3, 0.6), (lr, -0.45), (res, -1.4), (note, -2.3)):
        fit(m, 12.6).move_to(np.array([0, y, 0]))
    strikes = VGroup(*[Line(pieces[k].get_left(), pieces[k].get_right()).set_stroke(RED, 3) for k in LR_OUT])
    assert_in_frame(g1, g2, g3, lr, res, note)
    for u, v in ((g1, g2), (g2, g3), (g3, lr), (lr, res), (res, note)):
        assert_apart(u, v, 0.1)

    scene.say("推廣：同樣的計算換一個方框", wait=SLOW * 0.2)
    scene.play(FadeIn(g1, shift=0.2 * DOWN), run_time=0.9)
    scene.say("$Gr(2,5)$", "（", "$\\mathbb P^4$", " 的直線）：方框 ", "$2\\times3$", "，路徑數 ＝ ", "$(3,3)$",
              " 的標準表數 ＝ 5", wait=SLOW * 0.8)
    scene.play(FadeIn(g2, shift=0.2 * DOWN), run_time=0.9)
    scene.say("練習 17 的公式直接算：", "$720/144=5$", wait=SLOW * 0.7)
    scene.play(FadeIn(g3, shift=0.2 * DOWN), run_time=0.9)
    scene.say("$Gr(3,6)$", "：", "$3\\times3$", " 方框，", "$f^{(3,3,3)}=42$", wait=SLOW * 0.8)
    scene.say("不只 ", "$\\sigma_1$", "：任兩個 Schubert 類相乘，就是 Schur 函數相乘", wait=SLOW * 0.2)
    scene.play(Write(lr), run_time=1.6)
    scene.wait(SLOW * 0.4)
    scene.play(*[p.animate.set_opacity(0.35) for p in (pieces[k] for k in LR_OUT)], ShowCreation(strikes),
               run_time=1.0)
    scene.say("在 ", "$Gr(3,6)$", " 裡，放不進 ", "$3\\times3$", " 方框的四項全部丟掉", wait=SLOW * 0.8)
    scene.play(FadeIn(res, shift=0.2 * DOWN), run_time=0.9)
    scene.play(FadeIn(note, shift=0.2 * UP), run_time=0.8)
    scene.say("$\\sigma_{21}^2=\\sigma_{33}+2\\sigma_{321}+\\sigma_{222}$", wait=SLOW * 0.7)
    scene.say("Schubert 計算 ＝ Schur 函數的乘法，只留方框裡的項", wait=SLOW * 1.2)


class SceneF49FourLines(ChuScene):
    def construct(self):
        self.show_header("四條線問題：Schubert 計算")
        check_math()
        part_question(self)
        self.clear_stage()
        part_pieri(self)
        self.clear_stage()
        part_reveal(self)
        self.clear_stage()
        part_duality(self)
        self.clear_stage()
        part_general(self)
        self.wait(1.0)
