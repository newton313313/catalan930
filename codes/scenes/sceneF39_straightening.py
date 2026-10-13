"""
Scene F39 —— 兩輪 straightening 與 kernel（Fulton §7.4 Lemma 6、Prop. 4，書 p.99–101；原大綱卡 F722、F723）
執行（在 codes/ 內）：manimgl scenes/sceneF39_straightening.py SceneF39Straightening

[125/43] 第一輪 (j,k)=(1,2) 修好下列、弄壞上列；第二輪 (1,1) 得 [125/34] − [135/24]，座標 (0,0,1,0,−1)。
停止的理由是 Fulton 的序（最右不同行、最低不同格、數字大者大），不是「下降數變少」。
Q ⊆ ker α（Garnir 碰撞相消、k=2 的包含排除係數 −1, 0, +1）＋ dim 商 ≤ f ＋ α 滿射 ⇒ ker α = Q^λ。
"""
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_data import load, polytabloid, specht21
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, ColumnTabloidMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

T0 = ((1, 2, 5), (4, 3))
T1 = ((2, 1, 5), (3, 4))
TA = ((1, 2, 5), (3, 4))
TB_RAW = ((2, 3, 5), (1, 4))
TB = ((1, 3, 5), (2, 4))


# =============================================================================
# 小工具（純 Python：行、排序、交換、Fulton 的序）
# =============================================================================
def columns(rows):
    return [tuple(r[j] for r in rows if len(r) > j) for j in range(len(rows[0]))]


def from_columns(cols, lam):
    return tuple(tuple(cols[j][i] for j in range(li)) for i, li in enumerate(lam))


def sort_columns(rows):
    """把每一行由上到下排好；回傳 (符號, rows)。行 tabloid 換順序要乘上置換的符號。"""
    lam = [len(r) for r in rows]
    s, new = 1, []
    for c in columns(rows):
        s *= (-1) ** sum(c[a] > c[b] for a in range(len(c)) for b in range(a + 1, len(c)))
        new.append(tuple(sorted(c)))
    return s, from_columns(new, lam)


def exchange(rows, j, k):
    """π_{j,k}：第 j+1 行最上面 k 個數，與第 j 行任選 k 個交換（保持上下順序）；j 由 1 起算。"""
    lam = [len(r) for r in rows]
    cols = [list(c) for c in columns(rows)]
    left, right = cols[j - 1], cols[j]
    out = []
    for pos in combinations(range(len(left)), k):
        L, R = left[:], right[:]
        for a, p in enumerate(pos):
            L[p], R[a] = right[a], left[p]
        new = [tuple(c) for c in cols]
        new[j - 1], new[j] = tuple(L), tuple(R)
        out.append(sort_columns(from_columns(new, lam)))
    return out


def fulton_less(s, t):
    """s ≺ t：最右邊不同的行裡，最低的不同格，t 的數字較大。回傳 (真假, (列, 行, s 的數, t 的數))。"""
    cs, ct = columns(s), columns(t)
    for j in reversed(range(len(cs))):
        if cs[j] != ct[j]:
            for i in reversed(range(len(cs[j]))):
                if cs[j][i] != ct[j][i]:
                    return cs[j][i] < ct[j][i], (i, j, cs[j][i], ct[j][i])
    return False, None


def row_descents(rows):
    return sum(r[j] > r[j + 1] for r in rows for j in range(len(r) - 1))


def ie_coefficient(z, w):
    """Σ_{∅≠Y⊆W} (−1)^{|Y|} γ_Y 裡，交換集合 Z 那一項的係數（γ_Y 內部交換 Z ⊆ Y 帶 (−1)^{|Z|}）。"""
    tot = 0
    for r in range(1, len(w) + 1):
        for y in combinations(w, r):
            if set(z) <= set(y):
                tot += (-1) ** len(y) * (-1) ** len(z)
    return tot


def check_math():
    d = load("straightening32")
    std = [tuple(map(tuple, t)) for t in load("shape32")["standard"]]
    assert tuple(map(tuple, d["input"])) == T0 and tuple(map(tuple, d["intermediate"])) == T1
    assert (d["first_exchange"]["j"], d["first_exchange"]["k"]) == (1, 2)
    assert (d["second_exchange"]["j"], d["second_exchange"]["k"]) == (1, 1)
    assert exchange(T0, 1, 2) == [(1, T1)]                               # 第一輪只有一項
    assert exchange(T1, 1, 1) == [(1, TA), (-1, TB)]                     # 第二輪兩項，第二項排行得 −1
    assert sort_columns(TB_RAW) == (-1, TB)
    assert [tuple(map(tuple, t["rows"])) for t in d["sorted_terms"]] == [TA, TB]
    assert [t["coefficient"] for t in d["sorted_terms"]] == [1, -1]
    coords = [1 if t == TA else (-1 if t == TB else 0) for t in std]
    assert coords == d["standard_coordinates"] == [0, 0, 1, 0, -1]
    assert row_descents(T0) == row_descents(T1) == 1                     # 下降數沒有變少
    assert fulton_less(T0, T1) == (True, (1, 1, 3, 4))
    assert fulton_less(T1, TA) == (True, (0, 1, 1, 2))
    assert fulton_less(T1, TB) == (True, (0, 1, 1, 3))
    # α 把關係送到 0：v_{125/43} = v_{125/34} − v_{135/24}
    v0, va, vb = polytabloid(T0), polytabloid(TA), polytabloid(TB)
    assert all(v0.get(k, 0) == va.get(k, 0) - vb.get(k, 0) for k in set(v0) | set(va) | set(vb))
    s21 = load("straightening21")
    assert [t["coefficient"] for t in s21["sorted_terms"]] == [1, -1]
    assert tuple(specht21(polytabloid(((2, 1), (3,))))) == (1, -1)
    assert tuple(specht21(polytabloid(((1, 2), (3,))))) == (1, 0)
    assert tuple(specht21(polytabloid(((1, 3), (2,))))) == (0, 1)
    w = ("w1", "w2")                                                     # k = 2 的包含排除
    assert ie_coefficient((), w) == -1 and ie_coefficient(("w1",), w) == 0
    assert ie_coefficient(("w2",), w) == 0 and ie_coefficient(w, w) == 1
    assert load("shape32")["f"] == 5 and load("hooks")["21"]["f"] == 2


# =============================================================================
# 畫圖小工具
# =============================================================================
def tx(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def ct_entry(ct, i, j):
    """ColumnTabloidMob 第 i 列第 j 行的數字（0 起算）。"""
    k = sum(sum(1 for r in ct.rows if len(r) > jj) + 2 for jj in range(j))
    return ct.body[k + i]


def hl(mobs, color, buff=0.07):
    return SurroundingRectangle(VGroup(*mobs), buff=buff, color=color, stroke_width=3)


# =============================================================================
# 第一段：兩輪 straightening
# =============================================================================
def part_rounds(scene):
    qlabel = mixed("以下等式都在商空間 ", r"$\widetilde M^\lambda/Q^\lambda$", " 裡", font_size=24)
    qbox = SurroundingRectangle(qlabel, buff=0.12, color=MUTED_COLOR, stroke_width=2)
    q = VGroup(qbox, qlabel).move_to(np.array([3.7, 2.85, 0]))
    c0 = ColumnTabloidMob(T0, cs=0.65, center=np.array([-4.6, 1.0, 0]))
    assert_in_frame(q, c0)
    scene.play(FadeIn(q), FadeIn(c0, shift=0.2 * RIGHT))
    scene.say("起點 ", "$[125/43]$", "：三行由上到下都遞增", wait=3.1)
    bad = hl([ct_entry(c0, 1, 0), ct_entry(c0, 1, 1)], NEG_COLOR)
    bad_t = tx("4>3", 32, NEG_COLOR).next_to(bad, DOWN, buff=0.15)
    scene.play(ShowCreation(bad), FadeIn(bad_t))
    scene.say("但第二列 ", "$4>3$", "：不是標準表，要拉直", wait=3.6)

    r1 = mixed("第 1 輪：", "$j=1,\\ k=2$", font_size=26, color=OP_COLOR).next_to(c0, UP, buff=0.45)
    left = hl([ct_entry(c0, 0, 0), ct_entry(c0, 1, 0)], COL_COLOR)
    right = hl([ct_entry(c0, 0, 1), ct_entry(c0, 1, 1)], OP_COLOR, buff=0.12)
    scene.play(FadeIn(r1), FadeOut(bad), FadeOut(bad_t), ShowCreation(left), ShowCreation(right))
    scene.say(r"$\pi_{j,k}$", "：右行最上面 ", "$k$", " 個，和左行任選 ", "$k$", " 個交換，上下順序不變", wait=3.0)
    scene.say("右行上面 ", "$k=2$", " 個數 2、3，和左行的 1、4 整批交換", wait=4.1)
    eq1 = tx("=", 44).move_to(np.array([-2.75, 1.0, 0]))
    c1 = ColumnTabloidMob(T1, cs=0.65, center=np.array([-0.9, 1.0, 0]))
    scene.play(Write(eq1), TransformFromCopy(c0, c1), run_time=1.4)
    scene.play(FadeOut(left), FadeOut(right))
    good = hl([ct_entry(c1, 1, 0), ct_entry(c1, 1, 1)], POS_COLOR)
    new_bad = hl([ct_entry(c1, 0, 0), ct_entry(c1, 0, 1)], NEG_COLOR)
    nb_t = tx("2>1", 32, NEG_COLOR).next_to(new_bad, UP, buff=0.12)
    assert_apart(nb_t, q)
    scene.play(ShowCreation(good), ShowCreation(new_bad), FadeIn(nb_t))
    scene.say("下列 3、4 修好了，上列卻冒出 ", "$2>1$", "。失敗了嗎？", wait=4.1)
    scene.say("沒有失敗：再做一輪就好", wait=2.6)

    r2 = mixed("第 2 輪：", "$j=1,\\ k=1$", font_size=26, color=OP_COLOR).next_to(c1, DOWN, buff=0.25)
    pick = hl([ct_entry(c1, 0, 1)], OP_COLOR, buff=0.1)
    lcol = hl([ct_entry(c1, 0, 0), ct_entry(c1, 1, 0)], COL_COLOR)
    scene.play(FadeOut(good), FadeOut(new_bad), FadeOut(nb_t), FadeIn(r2), ShowCreation(pick), ShowCreation(lcol))
    scene.say("右行最上面的 1，輪流和左行的 2、3 交換：兩項", wait=3.6)
    ca = ColumnTabloidMob(TA, cs=0.55, center=np.array([-2.6, -1.75, 0]))
    plus = tx("+", 40, POS_COLOR).move_to(np.array([-1.15, -1.75, 0]))
    cr = ColumnTabloidMob(TB_RAW, cs=0.55, center=np.array([0.3, -1.75, 0]))
    arr_a = Arrow(r2.get_bottom() + 0.3 * LEFT, ca.get_top(), buff=0.1, thickness=2, fill_color=GREY_B)
    arr_b = Arrow(r2.get_bottom() + 0.3 * RIGHT, cr.get_top(), buff=0.1, thickness=2, fill_color=GREY_B)
    scene.play(GrowArrow(arr_a), GrowArrow(arr_b), FadeIn(ca), FadeIn(plus), FadeIn(cr), run_time=1.3)
    cb = ColumnTabloidMob(TB, sign_=-1, cs=0.55, center=np.array([3.6, -1.75, 0]))
    sort_arr = Arrow(cr.get_right(), cb.get_left(), buff=0.15, thickness=2, fill_color=NEG_COLOR)
    sort_t = mixed("第一行排好：", "$(-1)$", font_size=22, color=NEG_COLOR).next_to(sort_arr, UP, buff=0.1)
    assert_in_frame(ca, cr, cb, sort_t, r1, r2)
    assert_apart(sort_t, c1)
    scene.play(GrowArrow(sort_arr), FadeIn(sort_t), FadeIn(cb, shift=0.2 * RIGHT))
    scene.say("第二項第一行是 2 在 1 上面，換回來要乘 ", "$-1$", wait=4.1)
    scene.play(Indicate(ca, color=POS_COLOR), Indicate(cb, color=POS_COLOR))
    scene.say("兩項都是標準表，拉直結束", wait=3.1)
    scene.clear_stage()

    e0 = ColumnTabloidMob(T0, cs=0.6)
    ea = ColumnTabloidMob(TA, cs=0.6)
    eb = ColumnTabloidMob(TB, sign_=-1, cs=0.6)
    eq = VGroup(e0, tx("=", 44), ea, eb).arrange(RIGHT, buff=0.4).move_to(np.array([0, 1.5, 0]))
    std = load("shape32")["standard"]
    coords = load("straightening32")["standard_coordinates"]
    cols = VGroup()
    for t, c in zip(std, coords):
        tab = tableau_mob(tuple(map(tuple, t)), cs=0.4)
        color = POS_COLOR if c > 0 else (NEG_COLOR if c < 0 else MUTED_COLOR)
        num = tx(str(c), 40, color).next_to(tab, DOWN, buff=0.3)
        cols.add(VGroup(tab, num))
    cols.arrange(RIGHT, buff=0.8).move_to(np.array([0.6, -1.3, 0]))
    lab = zh("座標", font_size=28, color=MUTED_COLOR).next_to(cols, LEFT, buff=0.6).align_to(cols[0][1], DOWN)
    assert_in_frame(eq, cols, lab)
    scene.play(FadeIn(eq, lag_ratio=0.2), run_time=1.4)
    scene.say("$[125/43]=[125/34]-[135/24]$", wait=3.6)
    scene.play(FadeIn(cols, lag_ratio=0.1), FadeIn(lab), run_time=1.4)
    scene.play(*[FlashAround(cols[k], color=OP_COLOR) for k in (2, 4)])
    scene.say("在五個標準表上的座標是 ", "$(0,0,1,0,-1)$", wait=4.6)


# =============================================================================
# 第二段：為什麼會停——Fulton 的序
# =============================================================================
def part_order(scene):
    k0 = ColumnTabloidMob(T0, cs=0.45, center=np.array([-5.6, 0.2, 0]))
    k1 = ColumnTabloidMob(T1, cs=0.45, center=np.array([-3.4, 0.2, 0]))
    ka = ColumnTabloidMob(TA, cs=0.45, center=np.array([-1.0, 1.0, 0]))
    kb = ColumnTabloidMob(TB, cs=0.45, center=np.array([-1.0, -0.6, 0]))
    p1 = tx(r"\prec", 40, OP_COLOR).move_to(np.array([-4.5, 0.2, 0]))
    pa = tx(r"\prec", 40, OP_COLOR).move_to(np.array([-2.2, 0.85, 0])).rotate(-0.3)
    pb = tx(r"\prec", 40, OP_COLOR).move_to(np.array([-2.2, -0.45, 0])).rotate(0.3)
    d0 = mixed("下降 ", "$1$", font_size=22, color=MUTED_COLOR).next_to(k0, DOWN, buff=0.3)
    d1 = mixed("下降 ", "$1$", font_size=22, color=MUTED_COLOR).next_to(k1, DOWN, buff=0.3)
    scene.play(FadeIn(VGroup(k0, k1)), FadeIn(d0), FadeIn(d1))
    scene.say("第一輪前後各有 1 個下降：下降數沒有變少", wait=3.6)
    no = zh("不能拿下降數證明會停", font_size=24, color=NEG_COLOR).next_to(VGroup(d0, d1), DOWN, buff=0.3)
    assert_in_frame(no)
    scene.play(FadeIn(no))
    scene.say("要換一把尺：Fulton 給表排的序", wait=3.1)

    rule = VGroup(
        zh("1. 找最右邊不同的那一行", font_size=24),
        zh("2. 在這行找最低的不同格", font_size=24),
        zh("3. 那格數字大的，整張表較大", font_size=24),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    rbox = SurroundingRectangle(rule, buff=0.2, color=OP_COLOR, stroke_width=2)
    rg = VGroup(rbox, rule).move_to(np.array([3.6, 2.2, 0]))
    notes = VGroup(
        mixed("第 1 輪：第 2 行最低格 ", "$3<4$", font_size=22),
        mixed("第 2 輪第一項：第 2 行第 1 格 ", "$1<2$", font_size=22),
        mixed("第 2 輪第二項：第 2 行第 1 格 ", "$1<3$", font_size=22),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([3.6, -0.4, 0]))
    assert_in_frame(rg, notes, ka, kb)
    assert_apart(rg, notes)
    scene.play(FadeIn(rg, shift=0.2 * LEFT))
    scene.say("比較時先看最右邊不同的行，再看最低的不同格", wait=3.6)
    b0 = hl([ct_entry(k0, 1, 1)], OP_COLOR, 0.05)
    b1 = hl([ct_entry(k1, 1, 1)], OP_COLOR, 0.05)
    scene.play(ShowCreation(b0), ShowCreation(b1), Write(p1), FadeIn(notes[0]))
    scene.say("第 1 輪：第 2 行最低格由 3 變 4，表變大", wait=3.6)
    c1 = hl([ct_entry(k1, 0, 1)], OP_COLOR, 0.05)
    ca_ = hl([ct_entry(ka, 0, 1)], OP_COLOR, 0.05)
    cb_ = hl([ct_entry(kb, 0, 1)], OP_COLOR, 0.05)
    scene.play(FadeOut(b0), FadeOut(b1), FadeIn(ka), FadeIn(kb), Write(pa), Write(pb),
               ShowCreation(c1), ShowCreation(ca_), ShowCreation(cb_), FadeIn(notes[1:]))
    scene.say("第 2 輪兩個分枝：1 變 2、1 變 3，每一枝都嚴格變大", wait=4.1)
    scene.say("提醒：這個序不是 §7.1 讀字的全序，是專為拉直設計的", wait=3.0)
    concl = tx(r"\dim\big(\widetilde M^\lambda/Q^\lambda\big)\le f^\lambda", 40)
    cbox = SurroundingRectangle(concl, buff=0.15, color=POS_COLOR, stroke_width=3)
    cg = VGroup(cbox, concl).move_to(np.array([2.8, -2.3, 0]))
    assert_in_frame(cg)
    assert_apart(cg, notes)
    scene.say("同大小的表只有有限多張，每步嚴格變大 ", "$\\Rightarrow$", " 一定會停", wait=3.6)
    scene.play(FadeIn(cg, shift=0.2 * UP))
    scene.say("所以標準的 ", "$[T]$", " 張成商空間，維度最多 ", "$f^\\lambda$", wait=4.1)


# =============================================================================
# 第三段：Q ⊆ ker α，再用維度夾住
# =============================================================================
def part_kernel(scene):
    mt = tx(r"\widetilde M^\lambda", 48).move_to(np.array([-3.6, 2.3, 0]))
    sl = tx(r"S^\lambda", 48).move_to(np.array([3.0, 2.3, 0]))
    arr = Arrow(mt.get_right(), sl.get_left(), buff=0.3, thickness=3, fill_color=WHITE)
    a_lab = tx(r"\alpha:\ [T]\mapsto v_T", 32).next_to(arr, UP, buff=0.1)
    onto = zh("滿射", font_size=22, color=MUTED_COLOR).next_to(arr, DOWN, buff=0.1)
    stack = VGroup(*[RoundedRectangle(width=2.2, height=0.5, corner_radius=0.08, stroke_color=COL_COLOR,
                                      stroke_width=2).set_fill(BLACK, 1).shift(0.1 * k * (UP + RIGHT))
                     for k in range(3)])
    stack.next_to(mt, DOWN, buff=0.35)
    q_lab = tx(r"Q^\lambda", 32, COL_COLOR).move_to(stack[-1])
    zero = tx("0", 44).move_to(np.array([sl.get_x(), stack.get_y(), 0]))
    q_arr = DashedLine(stack.get_right(), zero.get_left(), buff=0.25, stroke_color=OP_COLOR)
    q_q = mixed("先要證明", font_size=22, color=OP_COLOR).next_to(q_arr, DOWN, buff=0.08)
    top = VGroup(mt, sl, arr, a_lab, onto, stack, q_lab, zero, q_arr, q_q)
    assert_in_frame(top)
    scene.play(FadeIn(VGroup(mt, sl)), GrowArrow(arr), FadeIn(a_lab), FadeIn(onto))
    scene.say("$\\alpha$", " 把行 tabloid ", "$[T]$", " 送到 ", "$v_T$", "，而且是滿射", wait=3.6)
    scene.play(FadeIn(stack, lag_ratio=0.3), FadeIn(q_lab))
    scene.say("$Q^\\lambda$", "：所有交換關係 ", "$[T]-\\pi_{j,k}(T)$", " 疊成一疊", wait=3.6)
    scene.play(ShowCreation(q_arr), FadeIn(zero), FadeIn(q_q))
    scene.say("第一步要證明：每條關係都被 ", "$\\alpha$", " 送到 0，這不是定義送的", wait=4.1)

    tab = tableau_mob(T0, cs=0.6, center=np.array([-5.0, -1.5, 0]))
    tab.fill_cells([(0, 0), (1, 0)], COL_COLOR, 0.45)
    tab.fill_cells([(0, 1), (1, 1)], OP_COLOR, 0.35)
    gl = VGroup(
        mixed("$X=\\{1,4\\}$", "：左行全部", font_size=22),
        mixed("$\\varnothing\\ne Y\\subseteq W=\\{2,3\\}$", font_size=22),
        mixed("$|X|+|Y|\\ge 3>2$", " 列 ", "$\\Rightarrow$", " 有兩數同列", font_size=22),
        zh("交錯和的正負項成對相消", font_size=22, color=POS_COLOR),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(tab, RIGHT, buff=0.35)
    garnir = VGroup(tab, gl)
    assert_in_frame(garnir)
    assert_apart(garnir, top)
    scene.play(FadeIn(tab), FadeIn(gl[:2]))
    scene.say("Garnir：左行全部 ", "$X$", "，加上右行上方的非空 ", "$Y$", wait=3.6)
    scene.play(FadeIn(gl[2:]))
    scene.say("數比列多，鴿籠：每個行 tabloid 都碰撞，正負兩兩抵消", wait=4.1)

    head = VGroup(tx("Z", 30), zh("係數", font_size=22))
    rows = [(r"\varnothing", -1), (r"\{w_1\},\ \{w_2\}", 0), ("W", 1)]
    table = VGroup(head)
    for z, c in rows:
        color = POS_COLOR if c > 0 else (NEG_COLOR if c < 0 else MUTED_COLOR)
        table.add(VGroup(tx(z, 30), tx(("+" if c > 0 else "") + str(c), 30, color)))
    for k, r in enumerate(table):
        y = -0.3 - 0.55 * k
        r[0].move_to(np.array([1.5, y, 0]), aligned_edge=LEFT)
        r[1].move_to(np.array([4.8, y, 0]))
    rule_l = Line(np.array([1.4, -0.58, 0]), np.array([5.3, -0.58, 0]), stroke_color=GREY_B, stroke_width=1.5)
    res = tx(r"=\pi_{j,k}(T)-[T]", 32).next_to(table, DOWN, buff=0.25)
    ie = VGroup(table, rule_l, res)
    assert_in_frame(ie)
    assert_apart(ie, garnir)
    assert_apart(ie, top)
    scene.play(FadeIn(table, lag_ratio=0.2), ShowCreation(rule_l))
    scene.say("每個 ", r"$\gamma_Y$", " 內部的帶號交換也包含「什麼都不換」那一項", wait=3.0)
    scene.say("$k=2$", "：把各個 ", "$\\gamma_Y$", " 用 ", "$(-1)^{|Y|}$", " 加起來，交換集合 ", "$Z$", " 的係數", wait=4.1)
    scene.play(FadeIn(res))
    scene.say("只剩 ", "$\\pi_{j,k}(T)-[T]$", "：每條關係都在 ", "$\\ker\\alpha$", " 裡", wait=3.6)
    ok = tx(r"Q^\lambda\subseteq\ker\alpha", 34, POS_COLOR).move_to(q_q)
    scene.play(q_arr.animate.set_stroke(POS_COLOR), FadeTransform(q_q, ok))
    scene.wait(1.0)
    scene.clear_stage()

    rel = VGroup(ColumnTabloidMob(((2, 1), (3,)), cs=0.5), tx("-", 40, NEG_COLOR),
                 ColumnTabloidMob(((1, 2), (3,)), cs=0.5), tx("+", 40, POS_COLOR),
                 ColumnTabloidMob(((1, 3), (2,)), cs=0.5)).arrange(RIGHT, buff=0.25)
    img = tx(r"\overset{\alpha}{\longmapsto}\ (v_a-v_b)-v_a+v_b=0", 36)
    chk = VGroup(rel, img).arrange(RIGHT, buff=0.3).move_to(np.array([0, 2.0, 0]))
    assert_in_frame(chk)
    scene.play(FadeIn(rel), run_time=0.8)
    scene.play(Write(img), run_time=1.4)
    scene.say("小例子對一次：", "$(2,1)$", " 的那條關係確實送到 0", wait=3.6)
    sq = VGroup(tx(r"f^\lambda=\dim S^\lambda", 40), tx(r"\le", 40, OP_COLOR),
                tx(r"\dim\big(\widetilde M^\lambda/Q^\lambda\big)", 40), tx(r"\le", 40, OP_COLOR),
                tx(r"f^\lambda", 40)).arrange(RIGHT, buff=0.25).move_to(np.array([0, 0.3, 0]))
    why1 = mixed(r"$\alpha$", " 滿射且 ", r"$Q^\lambda\subseteq\ker\alpha$", font_size=20, color=MUTED_COLOR).next_to(sq[1], DOWN, buff=0.35)
    why2 = zh("straightening", font_size=20, color=MUTED_COLOR).next_to(sq[3], DOWN, buff=0.35)
    fin = tx(r"\ker\alpha=Q^\lambda,\qquad S^\lambda\cong\widetilde M^\lambda/Q^\lambda", 44)
    fbox = SurroundingRectangle(fin, buff=0.2, color=POS_COLOR, stroke_width=3)
    fg = VGroup(fbox, fin).move_to(np.array([0, -1.9, 0]))
    assert_in_frame(sq, why1, why2, fg)
    assert_apart(why1, why2)
    assert_apart(why1, fg)
    scene.play(FadeIn(sq[:3]), FadeIn(why1))
    scene.say("$\\alpha$", " 誘導出商空間到 ", "$S^\\lambda$", " 的滿射：商的維度至少 ", "$f^\\lambda$", wait=3.6)
    scene.play(FadeIn(sq[3:]), FadeIn(why2))
    scene.say("straightening 又說它至多 ", "$f^\\lambda$", "：兩邊夾住", wait=3.6)
    scene.play(FadeIn(fg, shift=0.2 * UP))
    scene.say("所以沒有藏起來的關係：", "$\\ker\\alpha$", " 恰好就是 ", "$Q^\\lambda$", wait=4.1)
    scene.say("不是試了幾次都成功就算數，是維度把它夾住", wait=3.0)
    scene.say("第 8 章把編號換成向量，沿用同一種交換", wait=3.6)


class SceneF39Straightening(ChuScene):
    def construct(self):
        self.show_header("F39　兩輪 straightening 與 kernel")
        check_math()
        part_rounds(self)
        self.clear_stage()
        part_order(self)
        self.clear_stage()
        part_kernel(self)
        self.wait(1.0)
