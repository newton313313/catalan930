"""
Scene F23 —— LR 規則：數 LR 斜表就是算係數（Fulton《Young Tableaux》§5.2–5.3，書 p.63–67）

    鉤子「計數機器」：餵進斜形狀 ν/λ，機器找出所有 LR 斜表（是斜表、字是反格字），再依內容 μ 分堆
        ν/λ = (5,4,3,2)/(3,3,1)：15 個 LR 斜表，堆的大小是 1、2、3
        → s_{ν/λ} = s(5,2)+s(5,1,1)+s(4,1,1,1)+s(2,2,2,1)+2[s(4,3)+s(3,3,1)+s(3,2,2)+s(3,2,1,1)]+3 s(4,2,1)
          （另用 4 個變數把斜 Schur 多項式整個展開驗算）
    s(2,1)·s(2,1)：對每個含 (2,1) 的 6 格 ν，在 ν/(2,1) 上數內容 (2,1) 的 LR 斜表
        → s(4,2)+s(4,1,1)+s(3,3)+2 s(3,2,1)+s(3,1,1,1)+s(2,2,2)+s(2,2,1,1)；(5,1)、(2,1,1,1,1) 是 0
    練習 2：ν = λ+μ 時 c = 1（例 λ=(3,1)、μ=(2,2,1)、ν=(5,3,1)：第 i 列只能全填 i）

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF23_lr_rule.py SceneF23LRRule
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import MU_COLOR, SkewMob, WordMob, assert_apart, assert_in_frame, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH5_DECOMP,
    CH5_LAM,
    CH5_NU,
    CH5_S21_SQUARED,
    contains,
    is_reverse_lattice,
    is_skew_tableau,
    lr_coefficient,
    lr_product,
    lr_tableaux,
    partitions,
    poly_mul,
    poly_sum,
    schur_poly,
    skew_boxes,
    skew_decomposition,
    skew_shape,
    skew_tableaux,
    tableau_word,
    young_boxes,
)

NU, LAM = CH5_NU, CH5_LAM
LR15 = tuple(lr_tableaux(NU, LAM))
EX_S = ((None, None, None, 1, 1), (None, None, None, 2), (None, 1, 1), (2, 3))
EX_WORD = (2, 3, 1, 1, 2, 1, 1)
EX_MU = (4, 2, 1)
TIERS = ((1, ((5, 2), (5, 1, 1), (4, 1, 1, 1), (2, 2, 2, 1))),
         (2, ((4, 3), (3, 3, 1), (3, 2, 2), (3, 2, 1, 1))),
         (3, ((4, 2, 1),)))
TIER_COLORS = {1: BLUE_C, 2: GREEN_C, 3: GOLD}
M_VARS = 4                                   # 驗算多項式用的變數個數
L21 = (2, 1)
SQ_NUS = ((4, 2), (4, 1, 1), (3, 3), (3, 2, 1), (3, 1, 1, 1), (2, 2, 2), (2, 2, 1, 1))
SQ_ZERO = ((5, 1), (2, 1, 1, 1, 1))          # 含 (2,1) 的 6 格 ν，但一個 LR 斜表也沒有
EX2_LAM, EX2_MU, EX2_NU = (3, 1), (2, 2, 1), (5, 3, 1)
EX2_S = ((None, None, None, 1, 1), (None, 2, 2), (3,))
NUM_COLORS = {1: BLUE_C, 2: GREEN_C, 3: GOLD, 4: RED_C}
GRID_CS, GRID_FS = 0.25, 18
PILE_X = (-4.0, -0.95, 2.1, 5.15)
TIER_Y = {1: 1.45, 2: -0.25, 3: -1.95}


def skew_content(S):
    c = Counter(v for r in S for v in r if v is not None)
    return tuple(c[i] for i in range(1, max(c) + 1))


def piles():
    out = {}
    for S in LR15:
        out.setdefault(skew_content(S), []).append(S)
    return out


def skew_poly(nu, lam, m):
    """斜 Schur 多項式 s_{ν/λ}(x1..xm)：每個斜表貢獻一個單項式。"""
    f = Counter()
    for S in skew_tableaux(nu, lam, m):
        c = Counter(v for r in S for v in r if v is not None)
        f[tuple(c[i] for i in range(1, m + 1))] += 1
    return dict(f)


def combo(coeffs, m):
    return poly_sum({e: c * k for e, k in schur_poly(mu, m).items()} for mu, c in coeffs.items())


def tallies(w):
    """從字尾往前讀，每讀一個字母後 1、2、3 各有幾個。"""
    cnt, out = Counter(), []
    for a in reversed(w):
        cnt[a] += 1
        out.append((cnt[1], cnt[2], cnt[3]))
    return out


def check_math():
    P = piles()
    assert len(LR15) == 15 == sum(CH5_DECOMP.values())
    assert {mu: len(v) for mu, v in P.items()} == CH5_DECOMP == skew_decomposition(NU, LAM)
    assert sorted(mu for _, mus in TIERS for mu in mus) == sorted(CH5_DECOMP)
    for c, mus in TIERS:
        assert all(CH5_DECOMP[mu] == c for mu in mus)
    for S in LR15:
        assert is_skew_tableau(S) and is_reverse_lattice(tableau_word(S)) and skew_shape(S) == (NU, LAM)
        assert sorted((i, j) for i, r in enumerate(S) for j, v in enumerate(r) if v) == skew_boxes(NU, LAM)
    assert EX_S in LR15 and tableau_word(EX_S) == EX_WORD and skew_content(EX_S) == EX_MU
    assert all(a >= b >= c for a, b, c in tallies(EX_WORD))
    assert skew_poly(NU, LAM, M_VARS) == combo(CH5_DECOMP, M_VARS)
    # s(2,1)²
    assert lr_product(L21, L21) == CH5_S21_SQUARED and tuple(CH5_S21_SQUARED) == SQ_NUS
    for nu in SQ_NUS:
        assert len(lr_tableaux(nu, L21, L21)) == CH5_S21_SQUARED[nu] == lr_coefficient(L21, L21, nu)
    s21 = schur_poly(L21, M_VARS)
    assert poly_mul(s21, s21) == combo(CH5_S21_SQUARED, M_VARS)
    assert tuple(nu for nu in partitions(6) if contains(nu, L21) and nu not in CH5_S21_SQUARED) == SQ_ZERO
    assert all(lr_coefficient(L21, L21, nu) == 0 for nu in SQ_ZERO)
    # 練習 2
    assert tuple(a + b for a, b in zip(EX2_LAM + (0,), EX2_MU)) == EX2_NU
    assert lr_tableaux(EX2_NU, EX2_LAM, EX2_MU) == [EX2_S]
    assert all(v == i + 1 for i, r in enumerate(EX2_S) for v in r if v)
    assert lr_coefficient(L21, L21, (4, 2)) == 1
    for n1 in range(1, 4):
        for n2 in range(1, 4):
            for lam in partitions(n1):
                for mu in partitions(n2):
                    k = max(len(lam), len(mu))
                    nu = tuple(a + b for a, b in zip(lam + (0,) * k, mu + (0,) * k) if a + b)
                    assert lr_coefficient(lam, mu, nu) == 1


def s_tex(mu):
    return "s_{" + tuple_str(mu) + "}"


def colored_skew(S, cs, fs, stroke=None, **kw):
    """SkewMob，數字依大小上色；stroke 給定時把格線改細（小格子時字比較清楚）。"""
    t = SkewMob(S, cs=cs, fs=fs, **kw)
    for i, r in enumerate(S):
        for j, v in enumerate(r):
            if v:
                t.entry(i, j).set_fill(NUM_COLORS[v])
    if stroke:
        t.cells.set_stroke(width=stroke)
    return t


# =============================================================================
# 機器的樣子
# =============================================================================
def make_gear(r, color=GREY_B, teeth=8):
    body = Circle(radius=r).set_stroke(color, width=3).set_fill(color, opacity=0.25)
    hub = Circle(radius=0.3 * r).set_stroke(color, width=2).set_fill(BLACK, opacity=1)
    tt = VGroup()
    for a in np.linspace(0, TAU, teeth, endpoint=False):
        tooth = Square(side_length=0.3 * r).set_stroke(width=0).set_fill(color, opacity=1)
        tooth.rotate(a).move_to(1.1 * r * np.array([np.cos(a), np.sin(a), 0]))
        tt.add(tooth)
    return VGroup(tt, body, hub)


def make_machine(center, scale=1.0):
    box = RoundedRectangle(width=3.0, height=2.1, corner_radius=0.2).set_stroke(TEAL, width=3)
    box.set_fill(TEAL, opacity=0.08)
    title = zh("LR 計數機", font_size=26, color=TEAL_A).move_to(box.get_top() + 0.35 * DOWN)
    g1 = make_gear(0.38).move_to(0.45 * LEFT + 0.3 * DOWN)
    g2 = make_gear(0.26, GREY_A, 6).move_to(0.42 * RIGHT + 0.12 * DOWN)
    return VGroup(box, title, g1, g2).scale(scale).move_to(center)


def spin(machine, run_time, turns=0.5):
    return [Rotate(machine[2], -turns * TAU, run_time=run_time),
            Rotate(machine[3], 1.45 * turns * TAU, run_time=run_time)]


# =============================================================================
# 第 1 段：計數機器與一個 LR 斜表
# =============================================================================
def part_machine(scene):
    shape_ = YoungDiagramMob(NU, cell_size=0.5, top_left=np.array([-6.5, 2.4, 0]))
    shape_.fill_cells(young_boxes(LAM), MU_COLOR, opacity=0.35)
    in_lab = Tex(r"\nu/\lambda=" + tuple_str(NU) + "/" + tuple_str(LAM), font_size=24)
    in_lab.next_to(shape_, DOWN, buff=0.18, aligned_edge=LEFT)
    machine = make_machine([-0.3, 1.4, 0])
    out = Tex(r"s_{\nu/\lambda}=\,?", font_size=40).move_to([3.7, 1.4, 0])
    a1 = Arrow([-3.85, 1.4, 0], machine.get_left() + 0.08 * LEFT, buff=0)
    a2 = Arrow(machine.get_right() + 0.08 * RIGHT, out.get_left() + 0.15 * LEFT, buff=0)
    r1 = zh("① 是斜表：每列由左到右不減、每行由上到下遞增", font_size=24)
    r2 = zh("② 字是反格字（字：由下往上逐列、每列由左往右讀）", font_size=24)
    rules = VGroup(r1, r2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-2.3, -0.55, 0], aligned_edge=LEFT)
    fill = colored_skew(EX_S, 0.5, 28, top_left=(-6.5, 2.4, 0), show_mu=False)
    word = WordMob(EX_WORD, size=0.38, colors=[NUM_COLORS[a] for a in EX_WORD])
    word.move_to([-6.5, -0.75, 0], aligned_edge=LEFT)
    order = [(i, j) for i in reversed(range(len(EX_S))) for j, v in enumerate(EX_S[i]) if v]
    states = [Tex(rf"{a}\ge {b}\ge {c}", font_size=32) for a, b, c in tallies(EX_WORD)]
    tally_lab = zh("1、2、3 的個數：", font_size=22, color=MUTED_COLOR)
    tally_lab.move_to([-6.5, -1.5, 0], aligned_edge=LEFT)
    for s in states:
        s.next_to(tally_lab, RIGHT, buff=0.15)
    badge = mixed("LR 斜表，內容 ", "$\\mu=" + tuple_str(EX_MU) + "$", font_size=26, color=OK_COLOR)
    badge.move_to([-6.3, -2.35, 0], aligned_edge=LEFT)
    badge_box = SurroundingRectangle(badge, buff=0.12, color=OK_COLOR, stroke_width=3)
    assert_in_frame(shape_, in_lab, machine, out, rules, word, tally_lab, *states, badge_box)
    for a, b in [(shape_, machine), (machine, out), (in_lab, rules), (word, rules), (states[-1], rules),
                 (machine, rules), (word, tally_lab), (tally_lab, badge_box), (states[-1], badge_box),
                 (in_lab, word), (rules, badge_box)]:
        assert_apart(a, b, gap=0.12)

    scene.say("想像一台計數機器：餵進斜形狀 ", "$\\nu/\\lambda$", "，吐出 ", "$s_{\\nu/\\lambda}$", " 的展開")
    scene.play(FadeIn(shape_), FadeIn(in_lab), run_time=0.7)
    scene.play(GrowArrow(a1), FadeIn(machine), *spin(machine, 1.2), run_time=1.2)
    scene.play(GrowArrow(a2), FadeIn(out, shift=0.2 * RIGHT), run_time=0.7)
    scene.wait(0.8)
    scene.say("它只認兩條規則")
    scene.play(FadeIn(r1, shift=0.1 * UP), run_time=0.6)
    scene.play(FadeIn(r2, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    scene.say("先試一個填法：每列不減、每行遞增，是斜表")
    scene.play(LaggedStart(*[FadeIn(e, scale=1.4) for e in fill.entries], lag_ratio=0.12), run_time=1.2)
    scene.wait(0.8)
    scene.say("由下往上逐列讀出它的字 ", "$" + "".join(map(str, EX_WORD)) + "$")
    srcs = VGroup(*[fill.entry(i, j).copy() for i, j in order])
    scene.play(*[FadeIn(t.square) for t in word.tiles], run_time=0.4)
    scene.play(*[Transform(s, t.label) for s, t in zip(srcs, word.tiles)], run_time=1.2)
    scene.remove(*srcs)
    scene.add(*[t.label for t in word.tiles])
    scene.wait(0.5)
    scene.say("從字尾往前數：1 的個數 ", "$\\ge$", " 2 的個數 ", "$\\ge$", " 3 的個數，一路成立")
    hl = SurroundingRectangle(word.tiles[-1], buff=0.04, color=YELLOW, stroke_width=3)
    scene.play(FadeIn(tally_lab), ShowCreation(hl), FadeIn(states[0]), run_time=0.5)
    cur = states[0]
    for k in range(1, len(states)):
        scene.play(hl.animate.move_to(word.tiles[len(EX_WORD) - 1 - k]), FadeOut(cur), FadeIn(states[k]),
                   run_time=0.35)
        cur = states[k]
    scene.play(FadeOut(hl), run_time=0.3)
    scene.wait(0.6)
    scene.say("兩條都過：這是一個 LR 斜表，內容 ", "$\\mu=" + tuple_str(EX_MU) + "$", "（四個 1、兩個 2、一個 3）")
    scene.play(FadeIn(badge), ShowCreation(badge_box), *spin(machine, 1.0, 0.25), run_time=1.0)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：15 個 LR 斜表依內容分堆 → s_{ν/λ} 的展開
# =============================================================================
def part_run(scene):
    P = piles()
    machine = make_machine([-0.3, 2.45, 0], scale=0.55)
    count_lab = zh("找到的 LR 斜表：", font_size=26, color=MUTED_COLOR).move_to([1.6, 2.45, 0], aligned_edge=LEFT)
    counter = Integer(0, font_size=44).next_to(count_lab, RIGHT, buff=0.2)
    tabs = {}
    grid = VGroup()
    for k, S in enumerate(LR15):
        t = colored_skew(S, GRID_CS, GRID_FS, stroke=1.6)
        r, c = divmod(k, 5)
        t.move_to([(c - 2) * 2.5, 0.75 - 1.5 * r, 0])
        tabs[S] = t
        grid.add(t)
    # 分堆後的位置
    frames, plabs, tier_labs = VGroup(), {}, VGroup()
    step = 5 * GRID_CS + 0.12
    frame_of = {}
    for c, mus in TIERS:
        col = TIER_COLORS[c]
        tier_labs.add(Tex(f"c={c}", font_size=30, fill_color=col).move_to([-6.2, TIER_Y[c], 0]))
        for p, mu in enumerate(mus):
            x0 = PILE_X[p] if c < 3 else (PILE_X[1] + PILE_X[2]) / 2
            for q, S in enumerate(P[mu]):
                t = tabs[S]
                t.generate_target()
                t.target.move_to([x0 + (q - (c - 1) / 2) * step, TIER_Y[c], 0])
            fr = SurroundingRectangle(VGroup(*[tabs[S].target for S in P[mu]]), buff=0.06, color=col,
                                      stroke_width=2)
            frames.add(fr)
            frame_of[mu] = fr
            plabs[mu] = Tex(s_tex(mu), font_size=26, fill_color=col).next_to(fr, DOWN, buff=0.08)
    targets = VGroup(*[t.target for t in grid])
    assert_in_frame(machine, count_lab, counter, grid, targets, frames, tier_labs, *plabs.values())
    assert_apart(VGroup(machine, count_lab), grid, gap=0.2)
    assert_apart(tier_labs, VGroup(targets, frames), gap=0.15)
    for (_, mus), (_, nxt) in zip(TIERS, TIERS[1:]):
        for mu in mus:
            for mu2 in nxt:
                assert_apart(plabs[mu], frame_of[mu2], gap=0.08)
    for k in range(len(frames) - 1):
        assert_apart(frames[k], frames[k + 1], gap=0.1)
    # 輸出的公式
    terms = {mu: Tex(s_tex(mu), font_size=40, fill_color=TIER_COLORS[CH5_DECOMP[mu]]) for mu in CH5_DECOMP}
    plus = lambda: Tex("+", font_size=40)
    line1 = [Tex(r"s_{\nu/\lambda}", font_size=40), Tex("=", font_size=40)]
    for k, mu in enumerate(TIERS[0][1]):
        line1 += ([plus()] if k else []) + [terms[mu]]
    c2 = Tex(str(TIERS[1][0]), font_size=40, fill_color=TIER_COLORS[2])
    c3 = Tex(str(TIERS[2][0]), font_size=40, fill_color=TIER_COLORS[3])
    line2 = [plus(), c2, Tex(r"\big(", font_size=40)]
    for k, mu in enumerate(TIERS[1][1]):
        line2 += ([plus()] if k else []) + [terms[mu]]
    line2 += [Tex(r"\big)", font_size=40), plus(), c3, terms[TIERS[2][1][0]]]
    L1, L2 = VGroup(*line1).arrange(RIGHT, buff=0.14), VGroup(*line2).arrange(RIGHT, buff=0.14)
    formula = VGroup(L1, L2).arrange(DOWN, buff=0.4).move_to(0.9 * UP)
    meaning = mixed("係數 ", "$c^{\\nu}_{\\lambda\\mu}$", "＝內容 ", "$\\mu$", " 的 LR 斜表有幾個（命題 3）",
                    font_size=28)
    meaning.move_to(1.1 * DOWN)
    mbox = SurroundingRectangle(meaning, buff=0.15, color=OK_COLOR, stroke_width=3)
    assert_in_frame(formula, mbox)
    assert_apart(formula, mbox, gap=0.3)

    scene.say("開機！機器把所有 LR 斜表一個一個找出來")
    scene.play(FadeIn(machine), FadeIn(count_lab), FadeIn(counter), run_time=0.6)
    mc = machine.get_center()
    scene.play(LaggedStart(*[GrowFromPoint(t, mc) for t in grid], lag_ratio=0.18),
               ChangeDecimalToValue(counter, len(LR15)), *spin(machine, 4.0, 1.5), run_time=4.0)
    scene.wait(0.6)
    scene.say("共 ", f"${len(LR15)}$", " 個。接著依內容 ", "$\\mu$", " 分堆：同一堆的表內容相同")
    scene.play(FadeOut(machine), FadeOut(count_lab), FadeOut(counter), run_time=0.4)
    scene.play(*[MoveToTarget(t, path_arc=0.4) for t in grid], run_time=1.8)
    scene.play(FadeIn(frames), FadeIn(tier_labs), *[FadeIn(l) for l in plabs.values()], run_time=0.8)
    scene.wait(0.8)
    sizes = "、".join(str(c) for c, _ in TIERS)
    scene.say(f"堆的大小只有 {sizes} 三種；最大的一堆是 ", "$\\mu=" + tuple_str(TIERS[2][1][0]) + "$")
    big = frames[-1]
    scene.play(Indicate(VGroup(big, plabs[TIERS[2][1][0]]), color=GOLD, scale_factor=1.05), run_time=1.2)
    scene.wait(1.2)
    scene.say("每一堆的大小，就是 ", "$s_\\mu$", " 的係數")
    scene.play(FadeOut(grid), FadeOut(frames), FadeOut(tier_labs),
               *[ReplacementTransform(plabs[mu], terms[mu]) for mu in CH5_DECOMP], run_time=1.4)
    rest = [m for m in line1 + line2 if all(m is not t for t in terms.values())]
    scene.play(*[FadeIn(m) for m in rest], run_time=0.8)
    scene.wait(1.0)
    scene.say("這就是 LR 規則：算係數＝數表")
    scene.play(FadeIn(meaning, shift=0.15 * UP), ShowCreation(mbox), run_time=0.9)
    scene.wait(1.6)
    scene.say("用 ", f"${M_VARS}$", " 個變數把兩邊整個展開比對，每一項都相同")
    scene.wait(2.0)


# =============================================================================
# 第 3 段：s(2,1)·s(2,1)
# =============================================================================
def part_square(scene):
    top = Tex(r"s_{(2,1)}\cdot s_{(2,1)}=\sum_{\nu}c^{\nu}_{(2,1),(2,1)}\,s_{\nu}", font_size=34).move_to(2.6 * UP)
    cols = []
    for k, nu in enumerate(SQ_NUS):
        x = -5.7 + 1.9 * k
        name = Tex(tuple_str(nu), font_size=24, fill_color=MUTED_COLOR).move_to([x, 1.75, 0])
        ts = VGroup(*[colored_skew(S, 0.42, 25, stroke=2.2) for S in lr_tableaux(nu, L21, L21)])
        ts.arrange(DOWN, buff=0.25).move_to([x, 1.45, 0], aligned_edge=UP)
        n = CH5_S21_SQUARED[nu]
        cl = Tex(f"c={n}", font_size=28, fill_color=YELLOW if n > 1 else WHITE).move_to([x, -1.62, 0])
        cols.append((nu, name, ts, cl))
    hi = next(c for c in cols if CH5_S21_SQUARED[c[0]] > 1)
    hi_box = SurroundingRectangle(VGroup(hi[1], hi[2], hi[3]), buff=0.12, color=YELLOW, stroke_width=3)
    parts = [Tex(r"s_{(2,1)}^2", font_size=32), Tex("=", font_size=32)]
    coef = None
    for k, nu in enumerate(SQ_NUS):
        if k:
            parts.append(Tex("+", font_size=32))
        term = Tex(s_tex(nu), font_size=32)
        if CH5_S21_SQUARED[nu] > 1:
            coef = Tex(str(CH5_S21_SQUARED[nu]), font_size=32, fill_color=YELLOW)
            term = VGroup(coef, term).arrange(RIGHT, buff=0.05)
        parts.append(term)
    result = VGroup(*parts).arrange(RIGHT, buff=0.12).move_to(2.45 * DOWN)
    assert_in_frame(top, *[VGroup(*c[1:]) for c in cols], hi_box, result)
    for k in range(len(cols) - 1):
        assert_apart(VGroup(*cols[k][1:]), VGroup(*cols[k + 1][1:]), gap=0.15)
    for c in cols:
        assert_apart(top, c[1], gap=0.15)
        assert_apart(c[1], c[2], gap=0.08)
        assert_apart(c[2], c[3], gap=0.15)
        assert_apart(c[3], result, gap=0.25)
    assert_apart(hi_box, result, gap=0.1)

    scene.say("同一台機器也能算乘積：", "$s_{(2,1)}\\cdot s_{(2,1)}$")
    scene.play(FadeIn(top), run_time=0.8)
    scene.wait(0.6)
    scene.say("對每個 6 格的 ", "$\\nu$", "：在 ", "$\\nu/(2,1)$", " 上只數內容 ", "$(2,1)$", " 的 LR 斜表")
    scene.play(LaggedStart(*[AnimationGroup(FadeIn(c[1]), FadeIn(c[2], shift=0.15 * DOWN)) for c in cols],
                           lag_ratio=0.2), run_time=2.4)
    scene.play(LaggedStart(*[FadeIn(c[3]) for c in cols], lag_ratio=0.1), run_time=0.8)
    scene.wait(0.8)
    scene.say("$\\nu=" + tuple_str(hi[0]) + "$", " 有兩種填法（2 放在第 2 列或第 3 列）：係數是 ",
              f"${CH5_S21_SQUARED[hi[0]]}$")
    scene.play(ShowCreation(hi_box), Indicate(hi[2], color=YELLOW, scale_factor=1.06), run_time=1.2)
    scene.wait(1.4)
    scene.say("$" + tuple_str(SQ_ZERO[0]) + "$", " 與 ", "$" + tuple_str(SQ_ZERO[1]) + "$",
              " 雖然也含 ", "$(2,1)$", "，卻一個也填不出來：係數 0")
    scene.wait(2.0)
    scene.say("收集起來就是展開式（用 ", f"${M_VARS}$", " 個變數乘開驗算，也對）")
    scene.play(FadeIn(result, shift=0.15 * UP), run_time=0.9)
    scene.play(Indicate(coef, color=YELLOW, scale_factor=1.4), run_time=0.8)
    scene.wait(1.6)


# =============================================================================
# 第 4 段：練習 2，ν = λ+μ 時 c = 1
# =============================================================================
def part_ex2(scene):
    title = mixed("練習 2：", "$\\nu_i=\\lambda_i+\\mu_i$", " 時 ", "$c^{\\nu}_{\\lambda\\mu}=1$", font_size=30)
    title.move_to(2.6 * UP)
    ex = mixed("例：", "$\\lambda=" + tuple_str(EX2_LAM) + "$", "、", "$\\mu=" + tuple_str(EX2_MU) + "$", "、",
               "$\\nu=" + tuple_str(EX2_NU) + "$", font_size=26, color=MUTED_COLOR).move_to(1.85 * UP)
    d = YoungDiagramMob(EX2_NU, cell_size=0.7, center=np.array([-3.9, -0.2, 0]))
    d.fill_cells(young_boxes(EX2_LAM), MU_COLOR, opacity=0.35)
    rows = []
    for i, r in enumerate(EX2_S):
        row = VGroup(*[Tex(str(v), font_size=40, fill_color=NUM_COLORS[v]).move_to(d.cell_center(i, j))
                       for j, v in reversed(list(enumerate(r))) if v])
        rows.append(row)
    reasons = VGroup(
        zh("從右往左讀，第 1 列最先被讀到：只能全是 1", font_size=26),
        mixed("1 剛好 ", "$\\mu_1$", " 個，全在第 1 列用完：第 2 列只能全是 2", font_size=26),
        zh("依此類推：第 i 列全是 i，只有這一種填法", font_size=26),
    ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-1.3, -0.2, 0], aligned_edge=LEFT)
    res = Tex(r"c^{" + tuple_str(EX2_NU) + "}_{" + tuple_str(EX2_LAM) + "," + tuple_str(EX2_MU) + "}=" +
              str(lr_coefficient(EX2_LAM, EX2_MU, EX2_NU)), font_size=40, fill_color=OK_COLOR)
    res.move_to([-3.9, -2.2, 0])
    res_box = SurroundingRectangle(res, buff=0.12, color=OK_COLOR, stroke_width=3)
    assert_in_frame(title, ex, d, reasons, res_box)
    for a, b in [(title, ex), (ex, d), (ex, reasons), (d, reasons), (d, res_box), (reasons, res_box)]:
        assert_apart(a, b, gap=0.12)

    scene.say("最後一個小練習：", "$\\nu$", " 恰好是 ", "$\\lambda$", " 與 ", "$\\mu$", " 逐列相加")
    scene.play(FadeIn(title), run_time=0.7)
    scene.play(FadeIn(ex), FadeIn(d), run_time=0.8)
    scene.wait(0.6)
    for k, (row, reason) in enumerate(zip(rows, reasons)):
        if k == 0:
            scene.say("反格字的最後一個字母一定是 1；第 1 列不減，所以全是 1")
        elif k == 1:
            scene.say("1 已經用光，第 2 列最右邊只能是 2，於是整列都是 2")
        else:
            scene.say("每一列都被逼成唯一的樣子")
        scene.play(FadeIn(reason, shift=0.1 * LEFT), LaggedStart(*[FadeIn(e, scale=1.5) for e in row],
                                                                  lag_ratio=0.25), run_time=1.0)
        scene.wait(1.3)
    scene.say("所以 ", "$c^{\\nu}_{\\lambda\\mu}=1$", "；前面的 ", "$(4,2)=(2,1)+(2,1)$", " 係數也正是 1")
    scene.play(FadeIn(res), ShowCreation(res_box), run_time=0.8)
    scene.wait(2.6)


class SceneF23LRRule(ChuScene):
    def construct(self):
        self.show_header("LR 規則：數表就是算係數")
        check_math()
        part_machine(self)
        self.clear_stage()
        part_run(self)
        self.clear_stage()
        part_square(self)
        self.clear_stage()
        part_ex2(self)
        self.wait(1.0)
