"""
Scene F31 —— tabloid、零和平面、polytabloid（Fulton §7.2，書 p.85–87；原大綱卡 F705、F706、F707）
執行（在 codes/ 內）：manimgl scenes/sceneF31_tabloids_plane.py SceneF31TabloidsPlane

6 個編號按第二列分成 3 對、壓成 3 張 tabloid t1,t2,t3；(12)、(23) 怎麼搬卡；dim M^λ = n!/∏λ_i!（3、10）；
x = 平均·z + 零和部分；正交座標 q1,q2 下 t_i - z/3 是等邊三角形；v_a = t3 - t1、v_b = t2 - t1 是兩條邊差；
v_T = b_T{T}；其餘 4 個 v_T 也在平面上 ⇒ S^(2,1) = W、M^(2,1) = Cz ⊕ W；σ v_T = v_{σT}。
"""
import sys
from math import factorial, isclose, prod, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import Y_MIN, assert_apart, assert_in_frame, tableau_mob
from utils.rep_data import act, act_vec, load, polytabloid, specht21, t21, tabloid_key
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, TabloidMob, perm_tex, signed_sum
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

SH = load("shape21")
SH32 = load("shape32")
PL = load("plane21")
TA = tuple(map(tuple, SH["Ta"]))
TB = tuple(map(tuple, SH["Tb"]))
NUMS = [tuple(map(tuple, r["rows"])) for r in SH["all_numberings"]]
COORDS = [tuple(r["specht_coordinates"]) for r in SH["all_numberings"]]
S12, S23, S13 = (2, 1, 3), (1, 3, 2), (3, 2, 1)
Z_COLOR, W_COLOR = TEAL, PURPLE_B
ORIG = np.array([-3.0, -0.25, 0.0])
SCALE = 1.9


def num(s):
    return eval(s, {"__builtins__": {}}, {"sqrt": sqrt})


Q1 = np.array([-1, 1, 0]) / sqrt(2)
Q2 = np.array([-1, -1, 2]) / sqrt(6)
PROJ = {i: np.array([Q1[i - 1], Q2[i - 1]]) for i in (1, 2, 3)}       # t_i - z/3 在 (q1, q2) 下的座標


def plane_pt(xy):
    return ORIG + SCALE * np.array([xy[0], xy[1], 0.0])


def vec_xy(a, b):
    """a·v_a + b·v_b 在 (q1, q2) 下的座標；v_a = t3 - t1、v_b = t2 - t1。"""
    return a * (PROJ[3] - PROJ[1]) + b * (PROJ[2] - PROJ[1])


def tindex(key):
    return next(i for i in (1, 2, 3) if t21(i) == key)


def action_map(p):
    return {i: tindex(tabloid_key(act(p, t21(i)))) for i in (1, 2, 3)}


def check_math():
    for i in (1, 2, 3):
        assert tuple(map(tuple, SH["tabloids"][f"t{i}"])) == t21(i)
        assert np.allclose(PROJ[i], [num(s) for s in PL[f"projected_t{i}"]])
    assert [len([T for T in NUMS if tabloid_key(T) == t21(i)]) for i in (1, 2, 3)] == [2, 2, 2]
    assert action_map(S12) == {1: 2, 2: 1, 3: 3} and action_map(S23) == {1: 1, 2: 3, 3: 2}
    assert factorial(3) // (factorial(2) * factorial(1)) == 3
    assert factorial(5) // prod(factorial(x) for x in SH32["lambda"]) == SH32["dim_M"] == 10
    d = [np.linalg.norm(PROJ[i] - PROJ[j]) for i, j in ((1, 2), (2, 3), (1, 3))]
    assert isclose(d[0], d[1]) and isclose(d[1], d[2])                        # 等邊三角形
    assert np.allclose(sum(PROJ.values()), 0)
    assert polytabloid(TA) == {t21(3): 1, t21(1): -1} and polytabloid(TB) == {t21(2): 1, t21(1): -1}
    assert tuple(SH["va"]) == (-1, 0, 1) and tuple(SH["vb"]) == (-1, 1, 0)
    for T, c in zip(NUMS, COORDS):
        assert specht21(polytabloid(T)) == c                                  # 六個 v_T 都在 W（零和）裡
    assert COORDS[:2] == [(1, 0), (0, 1)]
    assert act(S23, TA) == TB and act_vec(S23, polytabloid(TA)) == polytabloid(TB)
    m, rest = 2, (2, -1, -1)
    assert sum(rest) == 0 and tuple(m + r for r in rest) == (4, 1, 1)


def fit_width(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def tlabel(i, fs=36):
    return Tex(f"t_{i}", font_size=fs, fill_color=OP_COLOR)


# =============================================================================
def part_tabloids(scene):
    tabs = VGroup(*[tableau_mob(T, cs=0.55) for T in NUMS]).arrange(RIGHT, buff=0.7).move_to(1.1 * UP)
    scene.play(LaggedStartMap(FadeIn, tabs, lag_ratio=0.2), run_time=1.5)
    scene.say("形狀 ", "$(2,1)$", " 的 6 個編號", wait=3.5)
    xs = {1: -4.2, 2: 0.0, 3: 4.2}
    targets = []
    for i in (1, 2, 3):
        members = [k for k, T in enumerate(NUMS) if tabloid_key(T) == t21(i)]
        pair = VGroup(*[tabs[k].copy() for k in members]).arrange(RIGHT, buff=0.35).move_to(np.array([xs[i], 1.1, 0]))
        targets += list(zip(members, pair))
    scene.play(*[tabs[k].animate.move_to(m.get_center()) for k, m in targets], run_time=1.5)
    frames = VGroup(*[SurroundingRectangle(VGroup(*[tabs[k] for k, T in enumerate(NUMS) if tabloid_key(T) == t21(i)]),
                                           buff=0.15, color=GREY_B, stroke_width=2) for i in (1, 2, 3)])
    scene.play(ShowCreation(frames), run_time=0.8)
    scene.say("按第二列的數分成三對：每對只差第一列裡的先後", wait=5.5)

    cards = VGroup(*[TabloidMob(t21(i), cs=0.6, center=np.array([xs[i], 1.1, 0])) for i in (1, 2, 3)])
    labs = VGroup(*[tlabel(i, 40).next_to(cards[i - 1], DOWN, buff=0.4) for i in (1, 2, 3)])
    groups = [VGroup(*[tabs[k] for k, T in enumerate(NUMS) if tabloid_key(T) == t21(i)]) for i in (1, 2, 3)]
    scene.play(*[ReplacementTransform(VGroup(g, f), c) for g, f, c in zip(groups, frames, cards)], run_time=1.5)
    scene.play(FadeIn(labs), run_time=0.6)
    scene.say("忘掉列裡的順序，只記得每一列有哪些數：這叫列 tabloid ", "$\\{T\\}$", wait=5.5)
    scene.say("第二列是 ", "$i$", " 的那一張，叫做 ", "$t_i$", "；不同列的數不能合併", wait=5.5)
    return cards, labs


def part_action(scene, cards, labs):
    arcs = VGroup()
    for p, (i, j), side in ((S12, (1, 2), UP), (S23, (2, 3), DOWN)):
        amap = action_map(p)
        assert amap[i] == j and amap[j] == i
        a = cards[i - 1].get_top() if side is UP else labs[i - 1].get_bottom()
        b = cards[j - 1].get_top() if side is UP else labs[j - 1].get_bottom()
        sh = 0.1 * side
        arc = CurvedDoubleArrow(a + sh, b + sh, angle=-PI / 4 if side is UP else PI / 4, stroke_color=OP_COLOR, stroke_width=4)
        lab = Tex(perm_tex(p), font_size=38, fill_color=OP_COLOR).next_to(arc, side, buff=0.1)
        fixed = next(k for k in (1, 2, 3) if amap[k] == k)
        still = zh("不動", font_size=24, color=MUTED_COLOR).next_to(cards[fixed - 1], RIGHT if fixed == 3 else LEFT, buff=0.25)
        g = VGroup(arc, lab, still)
        assert_in_frame(g)
        scene.play(ShowCreation(arc), FadeIn(lab), run_time=1.0)
        scene.play(FadeIn(still), Indicate(cards[fixed - 1], color=GREY_A), run_time=0.8)
        scene.wait(1.0)
        k = fixed
        others = [x for x in (1, 2, 3) if x != k]
        scene.say("$" + perm_tex(p) + "$", " 把 ", f"$t_{others[0]}$", " 和 ", f"$t_{others[1]}$", " 對調，", f"$t_{k}$", " 不動", wait=4.5)
        arcs.add(g)
        if side is UP:
            scene.play(g.animate.set_opacity(0.3), run_time=0.4)
    span = Tex(r"M^{(2,1)}=\mathbb{C}t_1\oplus\mathbb{C}t_2\oplus\mathbb{C}t_3", font_size=44).move_to(2.55 * DOWN)
    assert_in_frame(span)
    assert_apart(span, arcs)
    scene.play(Write(span), run_time=1.2)
    scene.say("三張 tabloid 當基底：排列只是在搬這三張卡", wait=5.5)


def part_dimension(scene):
    gen = Tex(r"\dim M^\lambda=\frac{n!}{\lambda_1!\,\lambda_2!\cdots}", font_size=48).move_to(1.4 * UP)
    ex1 = Tex(r"(2,1):\ \frac{3!}{2!\,1!}=3", font_size=44, fill_color=ROW_COLOR)
    ex2 = Tex(r"(3,2):\ \frac{5!}{3!\,2!}=10", font_size=44, fill_color=ROW_COLOR)
    exs = VGroup(ex1, ex2).arrange(RIGHT, buff=1.5).move_to(0.6 * DOWN)
    assert_in_frame(gen, exs)
    scene.play(Write(gen), run_time=1.2)
    scene.say("數 tabloid：", "$n!$", " 種編號，每一列裡的排列都算同一張", wait=5.5)
    scene.play(FadeIn(ex1), run_time=0.8)
    scene.play(FadeIn(ex2), run_time=0.8)
    scene.say("所以 ", "$\\dim M^{(2,1)}=3$", "、", "$\\dim M^{(3,2)}=10$", wait=5.5)
    coset = Tex(r"M^\lambda\cong\operatorname{Ind}_{R(T)}^{S_n}\mathbb{I}", font_size=40, fill_color=MUTED_COLOR)
    coset.move_to(2.2 * DOWN)
    assert_in_frame(coset)
    assert_apart(coset, exs)
    scene.play(FadeIn(coset), run_time=0.8)
    scene.say("每張 tabloid 對應列群 ", "$R(T)$", " 的一個陪集：", "$M^\\lambda$", " 由平凡表示誘導而來（F35 再談）", wait=4.5)


def part_plane(scene):
    axes = VGroup(Arrow(plane_pt((-1.75, 0)), plane_pt((1.75, 0)), buff=0, thickness=2, fill_color=GREY_C),
                  Arrow(plane_pt((0, -0.45)), plane_pt((0, 1.3)), buff=0, thickness=2, fill_color=GREY_C))
    axl = VGroup(Tex("q_1", font_size=34, fill_color=GREY_B).next_to(axes[0].get_end(), DOWN, buff=0.1),
                 Tex("q_2", font_size=34, fill_color=GREY_B).next_to(axes[1].get_end(), LEFT, buff=0.1))
    split = Tex(r"x=\bar{x}\,z+(x-\bar{x}\,z)", font_size=40).move_to(np.array([3.6, 2.5, 0]))
    ex = Tex(r"(4,1,1)=2(1,1,1)+(2,-1,-1)", font_size=36)
    fit_width(ex, 5.4)
    ex.next_to(split, DOWN, buff=0.3)
    side = VGroup(Tex(r"z=t_1+t_2+t_3", font_size=34, fill_color=Z_COLOR),
                  zh("共同方向：放到旁窗，沒有消失", font_size=22, color=MUTED_COLOR)).arrange(DOWN, buff=0.15)
    side_box = SurroundingRectangle(side, buff=0.2, color=Z_COLOR, stroke_width=2)
    sidewin = VGroup(side_box, side).next_to(ex, DOWN, buff=0.4)
    scene.play(Write(split), run_time=1.0)
    scene.play(FadeIn(ex), run_time=0.8)
    scene.say("每個向量 = 平均值乘 ", "$z$", "，加上座標和為 0 的部分", wait=4.5)
    scene.play(FadeIn(sidewin), run_time=0.8)
    scene.say("共同方向 ", "$z$", " 收到旁窗；主畫面只看零和平面 ", "$W$", wait=4.5)

    basis = VGroup(Tex(r"q_1=\tfrac{1}{\sqrt2}(-1,1,0)", font_size=34),
                   Tex(r"q_2=\tfrac{1}{\sqrt6}(-1,-1,2)", font_size=34)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    basis.next_to(sidewin, DOWN, buff=0.35)
    scene.play(GrowArrow(axes[0]), GrowArrow(axes[1]), FadeIn(axl), FadeIn(basis), run_time=1.2)
    scene.say("在 ", "$W$", " 裡取兩個互相垂直的單位向量 ", "$q_1,q_2$", " 當座標", wait=4.5)

    dots = VGroup(*[Dot(plane_pt(PROJ[i]), radius=0.08, fill_color=OP_COLOR) for i in (1, 2, 3)])
    dirs = {1: DL, 2: DR, 3: UR}
    dlabs = VGroup(*[Tex(r"\bar t_" + str(i), font_size=36, fill_color=OP_COLOR).next_to(dots[i - 1], dirs[i], buff=0.12)
                     for i in (1, 2, 3)])
    tri = Polygon(*[plane_pt(PROJ[i]) for i in (1, 2, 3)], stroke_color=W_COLOR, stroke_width=3,
                  fill_color=W_COLOR, fill_opacity=0.15)
    bar_def = Tex(r"\bar t_i=t_i-\tfrac13 z", font_size=36, fill_color=OP_COLOR).next_to(basis, DOWN, buff=0.35)
    assert_in_frame(axes, axl, split, ex, sidewin, basis, dots, dlabs, tri, bar_def)
    assert_apart(VGroup(axes, dlabs), VGroup(split, ex, sidewin, basis, bar_def))
    scene.play(FadeIn(dots), FadeIn(dlabs), FadeIn(bar_def), run_time=1.0)
    scene.play(ShowCreation(tri), run_time=1.0)
    scene.wait(1.0)
    scene.say("三個 ", "$\\bar t_i=t_i-\\tfrac13 z$", " 排成等邊三角形；它們不是原來的 ", "$t_i$", wait=5.5)

    va = Arrow(plane_pt(PROJ[1]), plane_pt(PROJ[3]), buff=0.08, thickness=3, fill_color=POS_COLOR)
    vb = Arrow(plane_pt(PROJ[1]), plane_pt(PROJ[2]), buff=0.08, thickness=3, fill_color=POS_COLOR)
    la = Tex(r"v_a=t_3-t_1", font_size=34, fill_color=POS_COLOR).next_to(va.get_center(), LEFT, buff=0.25)
    lb = Tex(r"v_b=t_2-t_1", font_size=34, fill_color=POS_COLOR).next_to(vb, DOWN, buff=0.15)
    assert_in_frame(la, lb)
    scene.play(GrowArrow(va), FadeIn(la), run_time=1.0)
    scene.play(GrowArrow(vb), FadeIn(lb), run_time=1.0)
    scene.say("兩條邊差 ", "$v_a=t_3-t_1$", "、", "$v_b=t_2-t_1$", "：不平行，張出整個二維的 ", "$W$", wait=5.5)
    keep = VGroup(axes, axl, dots, dlabs, tri, va, vb, la, lb)
    scene.play(FadeOut(VGroup(split, ex, sidewin, basis, bar_def)), run_time=0.6)
    return keep


def part_polytabloid(scene, keep):
    d = tableau_mob(TA, cs=0.45)
    cbox = SurroundingRectangle(d.cell_group([(0, 0), (1, 0)]), buff=0.04, color=COL_COLOR, stroke_width=4)
    vdef = Tex(r"v_T=b_T\{T\}", font_size=40)
    top = VGroup(VGroup(d, cbox), vdef).arrange(RIGHT, buff=0.6).move_to(np.array([3.7, 2.6, 0]))
    terms = [(c, TabloidMob(k, cs=0.4)) for k, c in sorted(polytabloid(TA).items(), key=lambda kv: -kv[1])]
    s = signed_sum(terms, font_size=38)
    eq = VGroup(Tex(r"v_{T_a}=", font_size=36), s, Tex(r"=t_3-t_1", font_size=36, fill_color=POS_COLOR))
    eq.arrange(RIGHT, buff=0.2)
    fit_width(eq, 5.5)
    eq.move_to(np.array([3.7, 1.45, 0]))
    eq_b = Tex(r"v_{T_b}=t_2-t_1", font_size=36, fill_color=POS_COLOR).next_to(eq, DOWN, buff=0.25).align_to(eq, LEFT)
    assert_in_frame(top, eq, eq_b)
    assert_apart(VGroup(top, eq, eq_b), keep)
    assert_apart(top, eq)
    scene.play(FadeIn(top), run_time=0.8)
    scene.say("polytabloid：", "$v_T=b_T\\{T\\}$", "，用行的交錯和把 tabloid 組起來", wait=4.5)
    scene.play(FadeIn(eq), run_time=1.0)
    scene.say("正項是 ", "$\\{T_a\\}=t_3$", "，負項是 ", "$\\{(1\\,3)T_a\\}=t_1$", "：正好是 ", "$v_a$", wait=5.5)
    scene.play(FadeIn(eq_b), run_time=0.8)
    scene.say("同樣 ", "$v_{T_b}=t_2-t_1=v_b$", wait=4.0)

    rows = VGroup()
    for T, (a, b) in list(zip(NUMS, COORDS))[2:]:
        terms = [(c, Tex(n, font_size=30)) for c, n in ((a, "v_a"), (b, "v_b")) if c]
        rows.add(VGroup(tableau_mob(T, cs=0.32), Tex(r"\mapsto", font_size=30), signed_sum(terms, font_size=30))
                 .arrange(RIGHT, buff=0.18))
    rows.arrange_in_grid(2, 2, h_buff=0.5, v_buff=0.2, aligned_edge=LEFT).next_to(eq_b, DOWN, buff=0.3)
    fit_width(rows, 5.5)
    rows.next_to(eq_b, DOWN, buff=0.3).set_x(3.7)
    hexa = VGroup()
    for (a, b) in COORDS:
        hexa.add(Arrow(ORIG, plane_pt(vec_xy(a, b)), buff=0, thickness=2.5,
                       fill_color=POS_COLOR if (a, b) in ((1, 0), (0, 1)) else W_COLOR))
    assert_in_frame(rows, hexa)
    assert_apart(rows, VGroup(keep, hexa))
    assert_apart(rows, eq_b)
    scene.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.3), run_time=1.6)
    scene.say("另外四個編號也送進去：只記座標，都是 ", "$v_a,v_b$", " 的組合", wait=5.5)
    scene.play(keep[5:].animate.set_opacity(0.25), LaggedStartMap(GrowArrow, hexa, lag_ratio=0.15), run_time=1.8)
    scene.say("從原點畫出六個 ", "$v_T$", "：全部落在零和平面上，而且彼此有相依關係", wait=5.5)

    res = VGroup(Tex(r"S^{(2,1)}=\operatorname{span}\{v_T\}=W", font_size=34, fill_color=POS_COLOR),
                 Tex(r"M^{(2,1)}=\mathbb{C}z\oplus S^{(2,1)}", font_size=34)).arrange(DOWN, buff=0.18)
    res.next_to(rows, DOWN, buff=0.25).set_x(3.7)
    avail = rows.get_bottom()[1] - 0.25 - (Y_MIN + 0.15)
    if res.get_height() > avail:
        res.set_height(avail)
        res.next_to(rows, DOWN, buff=0.25).set_x(3.7)
    box = SurroundingRectangle(res, buff=0.12, color=POS_COLOR, stroke_width=2)
    assert_in_frame(res, box)
    assert_apart(box, rows)
    assert_apart(box, VGroup(keep, hexa))
    scene.play(Write(res), ShowCreation(box), run_time=1.5)
    scene.wait(1.0)
    scene.say("所以本例 ", "$S^{(2,1)}=W$", "，三維的 ", "$M^{(2,1)}$", " 拆成 ", "$\\mathbb{C}z\\oplus W$", wait=6.0)


def part_equivariant(scene):
    nodes = {
        "TA": Tex("T_a", font_size=44), "TB": Tex("T_b", font_size=44),
        "VA": Tex("v_a", font_size=44, fill_color=POS_COLOR), "VB": Tex("v_b", font_size=44, fill_color=POS_COLOR),
    }
    pos = {"TA": (-2.2, 1.3), "TB": (2.2, 1.3), "VA": (-2.2, -1.2), "VB": (2.2, -1.2)}
    for k, m in nodes.items():
        m.move_to(np.array([*pos[k], 0]))
    arr = VGroup(
        Arrow(nodes["TA"].get_right(), nodes["TB"].get_left(), buff=0.3, thickness=2.5, fill_color=OP_COLOR),
        Arrow(nodes["VA"].get_right(), nodes["VB"].get_left(), buff=0.3, thickness=2.5, fill_color=OP_COLOR),
        Arrow(nodes["TA"].get_bottom(), nodes["VA"].get_top(), buff=0.3, thickness=2.5, fill_color=COL_COLOR),
        Arrow(nodes["TB"].get_bottom(), nodes["VB"].get_top(), buff=0.3, thickness=2.5, fill_color=COL_COLOR),
    )
    labs = VGroup(Tex(r"\sigma=(2\,3)", font_size=34, fill_color=OP_COLOR).next_to(arr[0], UP, buff=0.12),
                  Tex(r"\sigma", font_size=34, fill_color=OP_COLOR).next_to(arr[1], DOWN, buff=0.12),
                  Tex(r"b_{T_a}", font_size=34, fill_color=COL_COLOR).next_to(arr[2], LEFT, buff=0.12),
                  Tex(r"b_{T_b}", font_size=34, fill_color=COL_COLOR).next_to(arr[3], RIGHT, buff=0.12))
    law = Tex(r"\sigma\,v_T=v_{\sigma T}", font_size=48, fill_color=POS_COLOR).move_to(np.array([0, -2.45, 0]))
    assert_in_frame(*nodes.values(), arr, labs, law)
    scene.play(FadeIn(nodes["TA"]), run_time=0.6)
    scene.play(GrowArrow(arr[0]), FadeIn(labs[0]), FadeIn(nodes["TB"]), run_time=1.0)
    scene.say("先換標號：", "$(2\\,3)T_a=T_b$", "，再交錯化得到 ", "$v_b$", wait=4.0)
    scene.play(GrowArrow(arr[2]), FadeIn(labs[2]), FadeIn(nodes["VA"]), run_time=1.0)
    scene.play(GrowArrow(arr[1]), FadeIn(labs[1]), FadeIn(nodes["VB"]), GrowArrow(arr[3]), FadeIn(labs[3]), run_time=1.2)
    scene.say("或先交錯化得到 ", "$v_a$", "，再作用 ", "$\\sigma$", "：兩條路走到同一個 ", "$v_b$", wait=5.5)
    scene.play(Write(law), run_time=1.0)
    scene.say("換標號和交錯化可以交換順序，所以 ", "$S^\\lambda$", " 是穩定子空間", wait=5.5)


class SceneF31TabloidsPlane(ChuScene):
    def construct(self):
        self.show_header("tabloid、零和平面、polytabloid")
        check_math()
        cards, labs = part_tabloids(self)
        part_action(self, cards, labs)
        self.clear_stage()
        part_dimension(self)
        self.clear_stage()
        keep = part_plane(self)
        part_polytabloid(self, keep)
        self.clear_stage()
        part_equivariant(self)
        self.wait(1.0)
