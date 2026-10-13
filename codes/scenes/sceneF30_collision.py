"""
Scene F30 —— 碰撞相消與支配序（Fulton §7.1 Lemma 1、§7.2 Lemma 2，書 p.84–86；原大綱卡 F704）
執行（在 codes/ 內）：manimgl scenes/sceneF30_collision.py SceneF30Collision

T = 12/3 與 T' = 123 共用 {1,3}：b_T τ = -b_T、τ{T'} = {T'} ⇒ b_T{T'} = 0（正負兩項配對消失）；
(3,2) 對 (4,1)：第一列 4 個數塞不進 3 行 ⇒ 一定碰撞；無碰撞 ⇒ 支配（前綴容量圖）；同形狀無碰撞 T' = (13)T；
(3,3) 與 (4,1,1) 不可比（同 F12，一句帶過）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_data import act, act_vec, columns, gr_mul, load, sign, tabloid_key
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, TabloidMob, perm_tex, signed_sum
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import dominates, shape

CO = load("collision")
T = tuple(map(tuple, CO["T"]))
TP = tuple(map(tuple, CO["Tprime"]))
TAU = tuple(CO["tau"])
E3 = (1, 2, 3)
WIDE_T = tuple(map(tuple, CO["wide_shape"]["T"]))
WIDE_TP = tuple(map(tuple, CO["wide_shape"]["Tprime"]))
SAME = tuple(map(tuple, CO["same_shape_no_collision"]))
INC = [tuple(p) for p in CO["incomparable"]]


def prefix(lam, k):
    lam = tuple(lam) + (0,) * (k - len(lam))
    return [sum(lam[:r + 1]) for r in range(k)]


def collisions(T, Tp):
    """同在 T' 的一列、又在 T 的一行的數對。"""
    col_of = {v: j for j, c in enumerate(columns(T)) for v in c}
    out = []
    for r in Tp:
        for a in r:
            for b in r:
                if a < b and col_of[a] == col_of[b]:
                    out.append((a, b))
    return out


def check_math():
    assert collisions(T, TP) == [tuple(CO["pair"])] == [(1, 3)]
    assert perm_tex(TAU) == r"(1\,3)" and sign(TAU) == -1
    assert tabloid_key(act(TAU, TP)) == tabloid_key(TP)                       # τ{T'} = {T'}
    b = {E3: 1, TAU: -1}
    assert gr_mul(b, {TAU: 1}) == {TAU: 1, E3: -1} == {k: -v for k, v in b.items()}   # b_T τ = -b_T
    total = {}
    for q, c in b.items():
        for key, x in act_vec(q, {tabloid_key(TP): 1}).items():
            total[key] = total.get(key, 0) + c * x
    assert all(v == 0 for v in total.values())                               # b_T{T'} = 0
    lam, lamp = shape(WIDE_T), shape(WIDE_TP)
    assert (lam, lamp) == ((3, 2), (4, 1)) and len(WIDE_TP[0]) > len(WIDE_T[0])
    assert tuple(CO["wide_shape"]["pair"]) in collisions(WIDE_T, WIDE_TP) and (1, 4) in collisions(WIDE_T, WIDE_TP)
    assert prefix(lam, 2) == [3, 5] and prefix(lamp, 2) == [4, 5] and not dominates(lam, lamp)
    assert collisions(T, SAME) == [] and act(TAU, T) == SAME and shape(SAME) == shape(T)
    a, c = INC
    assert [prefix(a, 3), prefix(c, 3)] == CO["partial_sums"] == [[3, 6, 6], [4, 5, 6]]
    assert not dominates(a, c) and not dominates(c, a) and c > a                 # 字典序 (4,1,1) > (3,3)


def pos_of(T, v):
    return next((i, j) for i, r in enumerate(T) for j, x in enumerate(r) if x == v)


def tabloid_pos(tm, v):
    return next((i, j) for i, r in enumerate(tm.key) for j, x in enumerate(r) if x == v)


def link(a, b, color=OP_COLOR):
    return DashedLine(a.get_center(), b.get_center(), dash_length=0.12, stroke_color=color, stroke_width=3)


# =============================================================================
def part_setup(scene):
    d = tableau_mob(T, cs=0.85, center=np.array([-4.3, 1.4, 0]))
    cbox = SurroundingRectangle(d.cell_group([(0, 0), (1, 0)]), buff=0.06, color=COL_COLOR, stroke_width=5)
    tm = TabloidMob(TP, cs=0.85, center=np.array([2.6, 1.75, 0]))
    lab_t = Tex("T", font_size=44).next_to(d, LEFT, buff=0.4)
    lab_tp = Tex(r"\{T'\}", font_size=44).next_to(tm, UP, buff=0.25)
    scene.play(FadeIn(d), FadeIn(lab_t), run_time=0.8)
    scene.play(ShowCreation(cbox), run_time=0.6)
    scene.play(FadeIn(tm), FadeIn(lab_tp), run_time=0.8)
    scene.say("左邊 ", "$T=12/3$", "，橙框是它的一行；右邊是只有一列的 ", "$\\{T'\\}$", wait=3.5)
    a, b = CO["pair"]
    links = VGroup(*[link(d.entry(*pos_of(T, v)), tm.entry(*tabloid_pos(tm, v))) for v in (a, b)])
    hl = VGroup(*[m.copy().set_fill(OP_COLOR) for m in (d.entry(*pos_of(T, a)), d.entry(*pos_of(T, b)),
                                                      tm.entry(*tabloid_pos(tm, a)), tm.entry(*tabloid_pos(tm, b)))])
    assert_in_frame(d, cbox, tm, lab_t, lab_tp)
    assert_apart(VGroup(lab_t, d, cbox), VGroup(lab_tp, tm))
    scene.play(ShowCreation(links), FadeIn(hl), run_time=1.0)
    scene.say("1 和 3 在 ", "$T$", " 的同一行，又在 ", "$T'$", " 的同一列：這叫碰撞", wait=3.5)
    return d, tm, hl


def part_cancel(scene, d, tm, hl):
    tau = Tex(r"\tau=(1\,3)", font_size=42, fill_color=OP_COLOR).move_to(np.array([-4.3, -0.15, 0]))
    scene.play(FadeIn(tau), run_time=0.6)
    a, b = CO["pair"]
    ea, eb = tm.entry(*tabloid_pos(tm, a)), tm.entry(*tabloid_pos(tm, b))
    scene.play(FadeOut(hl[2:]), run_time=0.3)
    scene.play(Swap(ea, eb), run_time=1.0)
    scene.wait(0.5)
    scene.play(Swap(ea, eb), run_time=1.0)
    f_fix = Tex(r"\tau\{T'\}=\{T'\}", font_size=42, fill_color=ROW_COLOR).move_to(np.array([2.6, 0.45, 0]))
    scene.play(Write(f_fix), run_time=0.8)
    scene.say("同一列裡換位置，列 tabloid 不變：", "$\\tau\\{T'\\}=\\{T'\\}$", wait=3.5)

    f_b = VGroup(Tex(r"b_T\,\tau=(e-(1\,3))(1\,3)=(1\,3)-e", font_size=38, fill_color=COL_COLOR),
                 Tex(r"=-b_T", font_size=38, fill_color=NEG_COLOR)).arrange(RIGHT, buff=0.15)
    f_b.move_to(np.array([0.0, -0.75, 0]))
    scene.play(Write(f_b), run_time=1.2)
    scene.say("可是 ", "$b_T$", " 遇到同一行的交換會變號：", "$b_T\\tau=-b_T$", wait=3.5)

    pos_t = TabloidMob(TP, cs=0.5)
    neg_t = TabloidMob(act(TAU, TP), cs=0.5)
    s = signed_sum([(1, pos_t), (-1, neg_t)], font_size=40)
    lhs = Tex(r"b_T\{T'\}=", font_size=40)
    rowv = VGroup(lhs, s).arrange(RIGHT, buff=0.25).move_to(np.array([-2.2, -1.85, 0]))
    zero = Tex(r"=0", font_size=44, fill_color=POS_COLOR).next_to(rowv, RIGHT, buff=0.3)
    assert_in_frame(tau, f_fix, f_b, rowv, zero)
    assert_apart(f_b, rowv)
    assert_apart(VGroup(d, tm), f_b)
    scene.play(FadeIn(rowv), run_time=1.0)
    scene.say("直接展開：正項是 ", "$\\{T'\\}$", "，負項是 ", "$\\{\\tau T'\\}$", "，兩張其實是同一張", wait=3.5)
    arc = ArcBetweenPoints(s.terms[0].get_bottom() + 0.1 * DOWN, s.terms[1].get_bottom() + 0.1 * DOWN, angle=PI / 2,
                           stroke_color=OP_COLOR, stroke_width=3)
    scene.play(ShowCreation(arc), run_time=0.8)
    scene.play(s.animate.set_opacity(0.25), FadeOut(arc), Write(zero), run_time=1.0)
    scene.say("一正一負配成一對，抵消成 0", wait=3.0)

    chain = VGroup(Tex(r"b_T\{T'\}=b_T\,\tau\{T'\}=-b_T\{T'\}", font_size=40),
                   Tex(r"\Rightarrow\ b_T\{T'\}=0", font_size=40, fill_color=POS_COLOR)).arrange(RIGHT, buff=0.4)
    chain.move_to(np.array([0.0, -2.65, 0]))
    assert_in_frame(chain)
    assert_apart(chain, rowv)
    scene.play(Write(chain), run_time=1.4)
    scene.say("一般的說法：它等於自己的負數，所以是 0（特徵為 0，可以除以 2）", wait=4.0)


def part_wide(scene):
    d = tableau_mob(WIDE_T, cs=0.75, center=np.array([-4.0, 1.2, 0]))
    cboxes = VGroup(*[SurroundingRectangle(d.cell_group([(i, j) for i in range(len(WIDE_T)) if j < len(WIDE_T[i])]),
                                           buff=0.06, color=COL_COLOR, stroke_width=4) for j in range(len(WIDE_T[0]))])
    tm = TabloidMob(WIDE_TP, cs=0.75, center=np.array([2.6, 1.4, 0]))
    labs = VGroup(Tex(r"T:\ (3,2)", font_size=38).next_to(d, UP, buff=0.35),
                  Tex(r"\{T'\}:\ (4,1)", font_size=38).next_to(tm, UP, buff=0.35))
    scene.play(FadeIn(d), FadeIn(tm), FadeIn(labs), run_time=1.0)
    scene.play(ShowCreation(cboxes), run_time=0.8)
    scene.say("換成 ", "$(3,2)$", " 對 ", "$(4,1)$", "：", "$T'$", " 的第一列有 4 個數", wait=3.5)
    note = mixed("4 個數要放進 3 行，至少兩個擠在同一行", font_size=30, color=OP_COLOR).move_to(0.6 * DOWN)
    scene.play(FadeIn(note), run_time=0.6)
    scene.say("先自己找找看：哪兩個數撞在一起？", wait=3.5)
    a, b = CO["wide_shape"]["pair"]
    links = VGroup(*[link(d.entry(*pos_of(WIDE_T, v)), tm.entry(*tabloid_pos(tm, v))) for v in (a, b)])
    found = Tex(r"\{1,4\}", font_size=42, fill_color=OP_COLOR).next_to(note, DOWN, buff=0.45)
    assert_in_frame(d, cboxes, tm, labs, note, found)
    assert_apart(VGroup(d, cboxes, labs[0]), VGroup(tm, labs[1]))
    scene.play(ShowCreation(links), Indicate(cboxes[0], color=OP_COLOR), FadeIn(found), run_time=1.2)
    scene.say("1 和 4：在 ", "$T$", " 的第一行，也在 ", "$T'$", " 的第一列", wait=3.5)


def part_dominance(scene):
    defn = Tex(r"\lambda\trianglerighteq\mu\iff\lambda_1+\cdots+\lambda_r\ge\mu_1+\cdots+\mu_r\ \ (\forall r)",
               font_size=38).move_to(2.55 * UP)
    lemma = mixed("引理：", "$T$", " 與 ", "$T'$", " 沒有碰撞 ", "$\\Rightarrow$", "$\\lambda\\trianglerighteq\\lambda'$",
                  font_size=30).next_to(defn, DOWN, buff=0.35)
    scene.play(Write(defn), run_time=1.2)
    scene.say("支配序：每一個前綴和都要比較大", wait=3.0)
    scene.play(FadeIn(lemma), run_time=0.8)
    scene.say("理由是容量：", "$T'$", " 前 ", "$r$", " 列的數分在不同行，最多只塞得進 ", "$T$", " 的前 ", "$r$", " 列", wait=4.0)

    lam, lamp = shape(WIDE_T), shape(WIDE_TP)
    pl, pp = prefix(lam, 2), prefix(lamp, 2)
    u, bw = 0.33, 0.55
    base = np.array([-4.6, -2.4, 0])
    chart = VGroup()
    nums = VGroup()
    for r in range(2):
        for k, (vals, col) in enumerate(((pl, ROW_COLOR), (pp, OP_COLOR))):
            x = base + (r * 1.9 + k * (bw + 0.12)) * RIGHT
            bar = Rectangle(width=bw, height=vals[r] * u, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.45)
            bar.move_to(x + 0.5 * vals[r] * u * UP)
            chart.add(bar)
            nums.add(Tex(str(vals[r]), font_size=30, fill_color=col).next_to(bar, UP, buff=0.08))
        chart.add(Tex(f"r={r + 1}", font_size=28, fill_color=MUTED_COLOR).move_to(base + (r * 1.9 + 0.33) * RIGHT + 0.3 * DOWN))
    legend = VGroup(Tex(r"\lambda=(3,2)", font_size=30, fill_color=ROW_COLOR),
                    Tex(r"\lambda'=(4,1)", font_size=30, fill_color=OP_COLOR)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    legend.next_to(chart, RIGHT, buff=0.35).align_to(chart, UP)
    bad = Tex(r"3<4", font_size=36, fill_color=NEG_COLOR).next_to(legend, DOWN, buff=0.3).align_to(legend, LEFT)
    bad_box = SurroundingRectangle(VGroup(chart[0], chart[1], nums[0], nums[1]), buff=0.08, color=NEG_COLOR, stroke_width=3)
    assert_in_frame(defn, lemma, chart, nums, legend, bad, bad_box)
    assert_apart(lemma, VGroup(chart, nums, bad_box))
    scene.play(LaggedStartMap(GrowFromEdge, VGroup(*[m for m in chart if isinstance(m, Rectangle)]), edge=DOWN, lag_ratio=0.2),
               FadeIn(VGroup(*[m for m in chart if not isinstance(m, Rectangle)])), FadeIn(nums), FadeIn(legend), run_time=1.5)
    scene.say("前綴容量圖：藍是 ", "$T$", " 的容量，黃是 ", "$T'$", " 要放的數", wait=3.5)
    scene.play(ShowCreation(bad_box), FadeIn(bad), run_time=0.8)
    scene.say("第一列就超載：", "$(3,2)$", " 不支配 ", "$(4,1)$", "，所以碰撞躲不掉", wait=3.5)

    d1 = tableau_mob(T, cs=0.6)
    d2 = tableau_mob(SAME, cs=0.6)
    arr = Arrow(LEFT, RIGHT, buff=0, thickness=2.5, fill_color=COL_COLOR)
    ql = Tex(r"(1\,3)", font_size=34, fill_color=COL_COLOR)
    grp = VGroup(d1, arr, d2).arrange(RIGHT, buff=0.3)
    ql.next_to(arr, UP, buff=0.1)
    same = VGroup(grp, ql).move_to(np.array([3.6, -1.6, 0]))
    cap = zh("同形狀、無碰撞", font_size=26, color=MUTED_COLOR).next_to(same, DOWN, buff=0.25)
    assert_in_frame(same, cap)
    assert_apart(VGroup(chart, legend, bad, bad_box), VGroup(same, cap))
    scene.play(FadeIn(same), FadeIn(cap), run_time=1.0)
    scene.say("另一端：", "$T'=32/1$", " 和 ", "$T$", " 同形狀又沒碰撞，它正好是 ", "$(1\\,3)T$", "：只差一個行裡的重排", wait=4.0)


def part_incomparable(scene):
    a, c = INC
    pa, pc = prefix(a, 3), prefix(c, 3)
    rows = VGroup()
    for lam, ps, col in ((a, pa, ROW_COLOR), (c, pc, OP_COLOR)):
        lab = Tex("(" + ",".join(map(str, lam)) + ")", font_size=40, fill_color=col)
        rows.add(VGroup(lab, *[Tex(str(v), font_size=40) for v in ps]))
    for row in rows:
        row[0].move_to(np.array([-3.2, 0, 0]))
        for k in range(3):
            row[k + 1].move_to(np.array([-1.2 + 1.5 * k, 0, 0]))
    rows[0].shift(1.5 * UP)
    rows[1].shift(0.1 * UP)
    cmp = VGroup()
    for k in range(3):
        s = "<" if pa[k] < pc[k] else (">" if pa[k] > pc[k] else "=")
        col = NEG_COLOR if s == "<" else (POS_COLOR if s == ">" else MUTED_COLOR)
        cmp.add(Tex(s, font_size=40, fill_color=col).move_to(np.array([-1.2 + 1.5 * k, 0.8, 0])))
    head = zh("前綴和", font_size=26, color=MUTED_COLOR).next_to(rows[0][2], UP, buff=0.4)
    lex = mixed("字典序仍然排得出先後：", "$(4,1,1)>(3,3)$", font_size=28, color=MUTED_COLOR).move_to(1.6 * DOWN)
    assert_in_frame(rows, cmp, head, lex)
    scene.play(FadeIn(rows), FadeIn(head), run_time=1.0)
    scene.play(LaggedStartMap(FadeIn, cmp, lag_ratio=0.4), run_time=1.2)
    scene.say("支配序不是全序：", "$3<4$", " 但 ", "$6>5$", "，誰也不支配誰（同 F12）", wait=3.5)
    scene.play(FadeIn(lex), run_time=0.8)
    scene.say("所以證明裡用支配序講「碰撞」，排先後時再換成字典序", wait=3.5)


def same_shape_value():
    """沒碰撞、同形狀時 b_T{T'} = sgn(q) v_T：本例 T' = (13)T，得 -v_T。"""
    b = {E3: 1, TAU: -1}
    out = {}
    for q, c in b.items():
        for key, x in act_vec(q, {tabloid_key(SAME): 1}).items():
            out[key] = out.get(key, 0) + c * x
    return {k: v for k, v in out.items() if v}


def part_two_branches(scene):
    vt = {k: v for k, v in [(tabloid_key(T), 1), (tabloid_key(act(TAU, T)), -1)]}
    assert same_shape_value() == {k: -v for k, v in vt.items()}
    top = mixed("假設 ", "$\\lambda\\ntriangleright\\lambda'$", "（", "$\\lambda$", " 不嚴格支配 ", "$\\lambda'$", "）",
                font_size=30).move_to(2.35 * UP)
    left = VGroup(zh("有碰撞", font_size=30, color=NEG_COLOR),
                  Tex(r"b_T\{T'\}=0", font_size=42)).arrange(DOWN, buff=0.45)
    right = VGroup(zh("沒碰撞", font_size=30, color=POS_COLOR),
                   Tex(r"\lambda'=\lambda,\ \ p'T'=qT", font_size=40),
                   Tex(r"b_T\{T'\}=\operatorname{sgn}(q)\,v_T", font_size=42)).arrange(DOWN, buff=0.4)
    left.move_to(np.array([-3.4, -0.1, 0]))
    right.move_to(np.array([2.9, -0.35, 0]))
    arrows = VGroup(*[Arrow(top.get_bottom() + 0.1 * DOWN, g[0].get_top() + 0.1 * UP, buff=0.05, thickness=2.5,
                            fill_color=GREY_B) for g in (left, right)])
    ex = mixed("例：", "$T'=32/1=(1\\,3)T$", " ⇒ ", "$b_T\\{T'\\}=-v_T$", font_size=28, color=MUTED_COLOR)
    ex.next_to(right, DOWN, buff=0.35)
    assert_in_frame(top, left, right, arrows, ex)
    assert_apart(left, right)
    scene.play(FadeIn(top), run_time=0.8)
    scene.say("Fulton 的二分引理：先假設 ", "$\\lambda$", " 不嚴格支配 ", "$\\lambda'$", wait=3.5)
    scene.play(GrowArrow(arrows[0]), FadeIn(left), run_time=1.0)
    scene.say("有碰撞：剛才的配對相消，", "$b_T\\{T'\\}=0$", wait=3.5)
    scene.play(GrowArrow(arrows[1]), FadeIn(right), run_time=1.0)
    scene.say("沒碰撞：形狀相同，", "$T'$", " 和 ", "$T$", " 只差列裡、行裡的重排，結果是 ", "$\\pm v_T$", wait=3.5)
    scene.play(FadeIn(ex), run_time=0.8)
    scene.say("少了這個假設，「沒碰撞」並不保證同形狀", wait=3.5)


class SceneF30Collision(ChuScene):
    def construct(self):
        self.show_header("碰撞相消與支配序")
        check_math()
        d, tm, hl = part_setup(self)
        part_cancel(self, d, tm, hl)
        self.clear_stage()
        part_wide(self)
        self.clear_stage()
        part_dominance(self)
        self.clear_stage()
        part_incomparable(self)
        self.clear_stage()
        part_two_branches(self)
        self.wait(1.0)
