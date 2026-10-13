"""
Scene F32 —— 不可約與標準基底（Fulton §7.2 Prop. 1、Prop. 2；原大綱卡 F708、F709）
執行（在 codes/ 內）：manimgl scenes/sceneF32_irreducible_basis.py SceneF32IrreducibleBasis

1. 零和平面沒有共同的特徵直線：(12) 與 (23) 兩個反射的特徵線不同（正交座標，只為畫圖）。
2. 一般證明：b_T M^λ = C v_T（一條線）⇒ S^λ 不可分解；Maschke ⇒ 不可約；Sagan 的二分一句。
3. 三種形狀 ↔ 三個共軛類。
4. 標準 v_T 獨立（首項三角形）＋ Σ(f^λ)² = n! ⇒ 標準 v_T 是基底，dim S^λ = f^λ。
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import X_MIN, assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import act, load, polytabloid, rep_matrix21, specht21, tabloid_key
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import character_table, standard_tableaux

PLANE_O = np.array([-3.6, -0.1, 0.0])
SC = 2.5                                   # 正交座標放大倍數
TAU13 = (3, 2, 1)                          # (13) 的一行記法


# ----------------------------------------------------------------------------- 資料
def num(s: str) -> float:
    return float(eval(s, {"sqrt": math.sqrt}))


def orth(key):
    return np.array([[num(x) for x in r] for r in load("plane21")[key]])


def projected():
    p = load("plane21")
    return [np.array([num(x) for x in p[f"projected_t{i}"]]) for i in (1, 2, 3)]


def t_index(key) -> int:
    """λ=(2,1) 的 tabloid：t_i = 第二列是 i。"""
    return key[1][0]


def b_t_images():
    """b_{T_a} = 1 − (13) 作用在 t_1, t_2, t_3：回傳 [(i, {tabloid: 係數})]。"""
    tabs = load("shape21")["tabloids"]
    out = []
    for i in (1, 2, 3):
        rows = tabs[f"t{i}"]
        vec = {}
        for c, key in ((1, tabloid_key(rows)), (-1, tabloid_key(act(TAU13, rows)))):
            vec[key] = vec.get(key, 0) + c
        out.append((i, {k: c for k, c in vec.items() if c}))
    return out


def vab_tex(c) -> str:
    a, b = c
    parts = []
    for coef, name in ((a, "v_a"), (b, "v_b")):
        if coef:
            s = "-" if coef < 0 else ("+" if parts else "")
            parts.append(s + ("" if abs(coef) == 1 else str(abs(coef))) + name)
    return "".join(parts) or "0"


def check_math():
    m = load("matrices21")
    assert [list(r) for r in rep_matrix21((2, 1, 3))] == m["rho12"] == [[1, 0], [-1, -1]]
    assert [list(r) for r in rep_matrix21((1, 3, 2))] == m["rho23"] == [[0, 1], [1, 0]]
    r12, r23 = orth("rho12_orthonormal"), orth("rho23_orthonormal")
    assert np.allclose(r12 @ r12, np.eye(2)) and np.allclose(r23 @ r23, np.eye(2))
    for k in range(2):                       # (12) 的特徵線 e_1, e_2 都不是 (23) 的特徵線
        e = np.eye(2)[:, k]
        w = r23 @ e
        assert abs(e[0] * w[1] - e[1] * w[0]) > 0.5
    pts = projected()
    sides = [np.linalg.norm(pts[i] - pts[(i + 1) % 3]) for i in range(3)]
    assert max(sides) - min(sides) < 1e-9    # 等邊三角形
    imgs = {i: specht21(v) for i, v in b_t_images()}
    assert imgs == {1: (-1, 0), 2: (0, 0), 3: (1, 0)}          # b_T M = C v_a
    sh = load("shape21")
    for item in sh["all_numberings"]:
        assert list(specht21(polytabloid(item["rows"]))) == item["specht_coordinates"]
    assert polytabloid(sh["Ta"]) == {((1, 2), (3,)): 1, ((2, 3), (1,)): -1}
    assert polytabloid(sh["Tb"]) == {((1, 3), (2,)): 1, ((2, 3), (1,)): -1}
    s32 = load("shape32")
    assert s32["f"] == 5 == len(standard_tableaux((3, 2))) and s32["dim_M"] == 10
    cs3 = load("character_S3")
    lams, _ = character_table(3)
    fs = [len(standard_tableaux(l)) for l in lams]
    assert sorted(fs) == sorted(cs3["regular_dimensions"]) == [1, 1, 2]
    assert sum(f * f for f in fs) == cs3["squared_dimension_sum"] == 6 == math.factorial(3)
    assert len(lams) == len(cs3["types"]) == 3


# ----------------------------------------------------------------------------- 小工具
def pp(v):
    return PLANE_O + SC * np.array([v[0], v[1], 0.0])


def eig_line(vec, color, dashed=False, length=2.4):
    d = np.array([vec[0], vec[1], 0.0])
    d = d / np.linalg.norm(d)
    if d[1] < -1e-9 or (abs(d[1]) < 1e-9 and d[0] < 0):
        d = -d                               # get_end() 一律在上方（或右方）
    a, b = PLANE_O - length * d, PLANE_O + length * d
    ln = DashedLine(a, b, dash_length=0.14) if dashed else Line(a, b)
    return ln.set_stroke(color, width=4)


def eigs(M):
    vals, vecs = np.linalg.eigh(M)
    return {int(round(v)): vecs[:, k] for k, v in enumerate(vals)}


def triangle_group():
    pts = projected()
    tri = Polygon(*[pp(v) for v in pts]).set_stroke(GREY_B, width=2.5)
    labels = VGroup()
    for i, v in enumerate(pts):
        d = v / np.linalg.norm(v)
        labels.add(Tex(f"t_{i + 1}", font_size=34).move_to(pp(v) + 0.38 * np.array([d[0], d[1], 0])))
    dot = Dot(PLANE_O, radius=0.05, fill_color=GREY_B)
    return VGroup(tri, labels, dot)


def col_tex(col) -> str:
    cells = [x.replace("sqrt(3)", "\\sqrt{3}") for x in col]
    return "\\begin{pmatrix}" + "\\\\".join(cells) + "\\end{pmatrix}"


# ----------------------------------------------------------------------------- 1. 平面
def part_plane(scene):
    scene.say("零和平面 ", "$W$", " 還能再拆成兩條「所有排列都保持」的直線嗎？")
    tri = triangle_group()
    tag = mixed("$W$", "（正交座標，只為畫圖）", font_size=24, color=MUTED_COLOR)
    tag.next_to(np.array([X_MIN, 2.85, 0]), RIGHT, buff=0)
    scene.play(ShowCreation(tri[0]), FadeIn(tri[1]), FadeIn(tri[2]), FadeIn(tag), run_time=1.2)
    scene.wait(5.0)

    e12 = eigs(orth("rho12_orthonormal"))
    l12p, l12m = eig_line(e12[1], POS_COLOR), eig_line(e12[-1], NEG_COLOR)
    lab12 = VGroup(Tex("(12):+1", font_size=28, fill_color=POS_COLOR).next_to(l12p.get_end(), LEFT, buff=0.15),
                   Tex("(12):-1", font_size=28, fill_color=NEG_COLOR).next_to(l12m.get_end(), DOWN, buff=0.1))
    scene.say("$(12)$", " 是鏡射：鏡面上的線乘 ", "$+1$", "，垂直的線乘 ", "$-1$")
    scene.play(ShowCreation(l12p), ShowCreation(l12m), FadeIn(lab12), run_time=1.0)
    flip = tri[0].copy().set_stroke(OP_COLOR, width=3)
    scene.play(flip.animate.stretch(-1, 0, about_point=PLANE_O), run_time=1.0)
    scene.play(FadeOut(flip), run_time=0.4)
    scene.wait(5.0)

    e23 = eigs(orth("rho23_orthonormal"))
    l23p, l23m = eig_line(e23[1], POS_COLOR, dashed=True), eig_line(e23[-1], NEG_COLOR, dashed=True)
    lab23 = VGroup(Tex("(23):+1", font_size=28, fill_color=POS_COLOR).next_to(l23p.get_end(), UR, buff=0.05),
                   Tex("(23):-1", font_size=28, fill_color=NEG_COLOR).next_to(l23m.get_start(), DR, buff=0.05))
    scene.say("$(23)$", " 也是鏡射，但它的兩條特徵線（虛線）轉了方向")
    scene.play(ShowCreation(l23p), ShowCreation(l23m), FadeIn(lab23), run_time=1.0)
    scene.wait(6.0)

    r23 = load("plane21")["rho23_orthonormal"]
    head = zh("共同的穩定直線必須同時是兩者的特徵線", font_size=26)
    cand = mixed("$(12)$", " 只有兩條候選：", "$e_1,\\ e_2$", font_size=26)
    eq1 = Tex("\\rho(23)e_1=" + col_tex([r23[0][0], r23[1][0]]) + "\\not\\parallel e_1", font_size=34)
    eq2 = Tex("\\rho(23)e_2=" + col_tex([r23[0][1], r23[1][1]]) + "\\not\\parallel e_2", font_size=34)
    concl = mixed("⇒ ", "$W$", " 沒有共同的特徵直線", font_size=28, color=POS_COLOR)
    right = VGroup(head, cand, eq1, eq2, concl).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    right.move_to(np.array([3.3, 0.2, 0]))
    scene.say("用矩陣核對：", "$(12)$", " 的特徵線就是座標軸 ", "$e_1,e_2$")
    scene.play(FadeIn(head), FadeIn(cand), run_time=0.8)
    scene.play(Write(eq1), run_time=1.0)
    scene.play(Write(eq2), run_time=1.0)
    scene.wait(3.0)
    scene.play(FadeIn(concl, shift=0.1 * UP), run_time=0.7)
    assert_in_frame(tri, right, tag, lab12, lab23)
    assert_apart(VGroup(tri, l12p, l12m, l23p, l23m), right)
    scene.say("所以 ", "$S^{(2,1)}=W$", " 不可約——不過這只是 ", "$\\lambda=(2,1)$", " 這一例", wait=6.0)


# ----------------------------------------------------------------------------- 2. 一般證明
def part_general(scene):
    scene.say("一般的 ", "$\\lambda$", " 不能靠畫圖，關鍵是 ", "$b_T$", " 把整個 ", "$M^\\lambda$", " 壓成一條線")
    T = tableau_mob(load("shape21")["Ta"], cs=0.55)
    T.cell_group([(0, 0), (1, 0)]).set_stroke(COL_COLOR, width=5)
    bt = Tex("b_T=1-(13)", font_size=40, fill_color=COL_COLOR)
    top = VGroup(T, bt).arrange(RIGHT, buff=0.5).move_to(np.array([-3.6, 2.2, 0]))
    scene.play(FadeIn(T), Write(bt), run_time=1.0)

    lines = VGroup()
    for i, vec in b_t_images():
        lines.add(Tex(f"b_T\\,t_{i}=" + vab_tex(specht21(vec)), font_size=38,
                      t2c={"v_a": POS_COLOR}))
    lines.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(top, DOWN, buff=0.5)
    scene.play(LaggedStartMap(FadeIn, lines, shift=0.1 * RIGHT, lag_ratio=0.4), run_time=1.6)
    rank = Tex("b_TM^\\lambda=\\mathbb{C}v_T", font_size=44).next_to(lines, DOWN, buff=0.45)
    rank_box = SurroundingRectangle(rank, buff=0.15).set_stroke(OP_COLOR, width=2.5)
    scene.say("三個像全落在 ", "$\\mathbb{C}v_a$", " 上；一般地 ", "$b_TM^\\lambda=\\mathbb{C}v_T$", "（F30 的碰撞相消）")
    scene.play(Write(rank), ShowCreation(rank_box), run_time=1.0)
    scene.wait(6.0)

    # 右邊：S^λ = V ⊕ W 的兩盒
    boxV = RoundedRectangle(width=2.0, height=1.6, corner_radius=0.15).set_stroke(ROW_COLOR, width=3)
    boxW = boxV.copy().set_stroke(MUTED_COLOR, width=3)
    boxes = VGroup(boxV, boxW).arrange(RIGHT, buff=0.6).move_to(np.array([3.2, 1.3, 0]))
    labV, labW = Tex("V", font_size=40).move_to(boxV), Tex("W", font_size=40).move_to(boxW)
    oplus = Tex("\\oplus", font_size=40).move_to(boxes)
    head = Tex("S^\\lambda=V\\oplus W", font_size=40).next_to(boxes, UP, buff=0.3)
    scene.say("假設 ", "$S^\\lambda=V\\oplus W$", "：", "$b_T$", " 把兩盒各自送回自己")
    scene.play(FadeIn(head), ShowCreation(boxes), FadeIn(labV), FadeIn(labW), FadeIn(oplus), run_time=1.0)
    eq = Tex("\\mathbb{C}v_T=b_TV\\oplus b_TW", font_size=38).next_to(boxes, DOWN, buff=0.4)
    scene.play(Write(eq), run_time=1.0)
    scene.wait(5.0)
    vt = Tex("v_T", font_size=36, fill_color=POS_COLOR).move_to(boxV.get_center() + 0.45 * DOWN)
    scene.say("一條線只能整條落在一盒：比方 ", "$v_T\\in V$")
    scene.play(labV.animate.shift(0.3 * UP), FadeIn(vt, scale=1.4), run_time=0.8)
    span = Tex("V\\supseteq \\mathbb{C}[S_n]\\,v_T=S^\\lambda", font_size=38).next_to(eq, DOWN, buff=0.3)
    wzero = Tex("W=0", font_size=40, fill_color=NEG_COLOR).next_to(span, DOWN, buff=0.3)
    scene.say("$v_T$", " 的軌道張成整個 ", "$S^\\lambda$", "，另一盒只能是 0")
    scene.play(Write(span), run_time=1.0)
    scene.play(FadeIn(wzero), boxW.animate.set_stroke(NEG_COLOR, opacity=0.5), run_time=0.8)
    assert_in_frame(top, lines, rank_box, head, boxes, eq, span, wzero)
    assert_apart(VGroup(top, lines, rank_box), VGroup(head, boxes, eq, span, wzero))
    scene.wait(5.0)
    scene.say("這證的是「不可分解」；複數上有 Maschke（完全可約），所以就是不可約", wait=6.0)

    sagan = VGroup(mixed("Sagan 的二分：子模組 ", "$U\\subseteq M^\\lambda$", font_size=24, color=MUTED_COLOR),
                   mixed("$U\\supseteq S^\\lambda$", "  或  ", "$U\\subseteq(S^\\lambda)^\\perp$", font_size=26))
    sagan.arrange(DOWN, buff=0.18)
    sbox = SurroundingRectangle(sagan, buff=0.2).set_stroke(MUTED_COLOR, width=2)
    side = VGroup(sbox, sagan).move_to(np.array([-3.6, -2.3, 0]))
    scene.play(FadeOut(rank_box), rank.animate.shift(0.2 * UP), FadeIn(side), run_time=0.8)
    assert_in_frame(side)
    assert_apart(side, rank)
    scene.say("另一種說法：看有沒有某個 ", "$b_Tu\\neq0$", "——有就整個含 ", "$S^\\lambda$", wait=8.0)


# ----------------------------------------------------------------------------- 3. 形狀與類
def part_classes(scene):
    lams, _ = character_table(3)
    sizes = load("character_S3")["sizes"]
    shapes = VGroup(*[YoungDiagramMob(l, cell_size=0.42) for l in lams]).arrange(RIGHT, buff=1.6)
    shapes.move_to(np.array([0, 1.4, 0]))
    reps = {(3,): "e", (2, 1): "(12)", (1, 1, 1): "(123)"}
    cls = VGroup(*[Tex(reps[tuple(lam)], font_size=40) for lam in lams])
    cls.arrange(RIGHT, buff=2.2).move_to(np.array([0, -1.2, 0]))
    for c, sh in zip(cls, shapes):
        c.set_x(sh.get_x())
    size_labs = VGroup()
    types = [tuple(t) for t in load("character_S3")["types"]]
    for lam, c in zip(lams, cls):
        ct = {"e": (1, 1, 1), "(12)": (2, 1), "(123)": (3,)}[reps[tuple(lam)]]
        size_labs.add(zh(f"{sizes[types.index(ct)]} 個", font_size=24, color=MUTED_COLOR).next_to(c, DOWN, buff=0.2))
    links = VGroup(*[DashedLine(sh.get_bottom() + 0.1 * DOWN, c.get_top() + 0.1 * UP).set_stroke(GREY_B, 2)
                     for sh, c in zip(shapes, cls)])
    scene.say("不同形狀給出不同構的 ", "$S^\\lambda$", "；而形狀數＝共軛類數")
    scene.play(LaggedStartMap(FadeIn, shapes, lag_ratio=0.3), run_time=1.0)
    scene.play(LaggedStartMap(FadeIn, cls, lag_ratio=0.3), FadeIn(size_labs), run_time=1.0)
    scene.play(ShowCreation(links), run_time=0.8)
    assert_in_frame(shapes, cls, size_labs)
    scene.say("不可約表示的個數＝共軛類數，所以這份清單已經完整", wait=8.0)


# ----------------------------------------------------------------------------- 4. 標準基底
def part_basis(scene):
    sh = load("shape21")
    cards = VGroup()
    for item in sh["all_numberings"]:
        T = tableau_mob(item["rows"], cs=0.42)
        coords = specht21(polytabloid(item["rows"]))
        lab = Tex(vab_tex(coords), font_size=30).next_to(T, DOWN, buff=0.18)
        cards.add(VGroup(T, lab))
    cards.arrange(RIGHT, buff=0.55).move_to(np.array([0, 1.9, 0]))
    std = [k for k, it in enumerate(sh["all_numberings"]) if it["rows"] in (sh["Ta"], sh["Tb"])]
    for k in std:
        cards[k][1].set_fill(POS_COLOR)
    marks = VGroup(*[SurroundingRectangle(cards[k], buff=0.1).set_stroke(POS_COLOR, 3) for k in std])
    scene.say("$(2,1)$", " 的 6 種編號：兩張標準表給 ", "$v_a,v_b$", "，其餘都是它們的組合")
    scene.play(LaggedStartMap(FadeIn, cards, lag_ratio=0.15), run_time=1.5)
    scene.play(ShowCreation(marks), run_time=0.8)
    scene.wait(6.0)

    rows_t = [3, 2, 1]
    cols = []
    for key in ("Ta", "Tb"):
        vec = polytabloid(sh[key])
        cols.append([sum(c for k, c in vec.items() if t_index(k) == i) for i in rows_t])
    mat_rows = [[cols[0][r], cols[1][r]] for r in range(3)]
    mat = MatrixMob(mat_rows, font_size=34, h_buff=0.9, v_buff=0.55,
                    colors={(0, 0): POS_COLOR, (1, 1): POS_COLOR, (2, 0): NEG_COLOR, (2, 1): NEG_COLOR})
    rlab = VGroup(*[Tex(f"t_{i}", font_size=30) for i in rows_t])
    for r, lab in enumerate(rlab):
        lab.next_to(mat, LEFT, buff=0.25).set_y(mat.row(r).get_y())
    clab = VGroup(Tex("v_a", font_size=30), Tex("v_b", font_size=30))
    for j, lab in enumerate(clab):
        lab.next_to(mat, UP, buff=0.15).set_x(mat.col(j).get_x())
    tri = VGroup(rlab, mat, clab).move_to(np.array([-3.8, -1.2, 0]))
    note = VGroup(zh("依 Fulton 的全序排 tabloid：", font_size=24),
                  mixed("每個 ", "$v_T$", " 的首項是自己的 ", "$\\{T\\}$", font_size=24),
                  zh("⇒ 三角形 ⇒ 線性獨立", font_size=24, color=POS_COLOR)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    note.next_to(tri, RIGHT, buff=0.5)
    scene.say("獨立性看首項：", "$v_a=t_3-t_1$", "、", "$v_b=t_2-t_1$", "，係數排成三角形")
    scene.play(FadeIn(tri), run_time=1.0)
    scene.play(FadeIn(note, shift=0.1 * RIGHT), run_time=0.8)
    assert_in_frame(cards, marks, tri, note)
    assert_apart(cards, VGroup(tri, note))
    scene.wait(8.0)
    scene.play(FadeOut(VGroup(cards, marks, tri, note)), run_time=0.6)

    s32 = load("shape32")
    big = VGroup(*[tableau_mob(T, cs=0.42) for T in s32["standard"]])
    for b in big:
        b.cells.set_stroke(POS_COLOR, width=3)
    big.arrange(RIGHT, buff=0.45).move_to(np.array([0, 2.1, 0]))
    blabs = VGroup(*[Tex(f"v_{{T_{k + 1}}}", font_size=28, fill_color=POS_COLOR).next_to(b, DOWN, buff=0.15)
                     for k, b in enumerate(big)])
    info = Tex(f"f^{{(3,2)}}={s32['f']},\\quad \\dim M^{{(3,2)}}={s32['dim_M']}", font_size=34)
    info.next_to(blabs, DOWN, buff=0.3)
    scene.say("$(3,2)$", " 有 5 張標準表：5 個獨立的 ", "$v_T$", "（", "$M$", " 本身是 10 維）")
    scene.play(LaggedStartMap(FadeIn, big, lag_ratio=0.2), FadeIn(blabs), run_time=1.4)
    scene.play(FadeIn(info), run_time=0.6)
    scene.wait(5.0)

    lams, _ = character_table(3)
    fs = [len(standard_tableaux(l)) for l in lams]
    sq = VGroup()
    for f in fs:
        g = VGroup(*[Square(side_length=0.36).set_stroke(GREY_A, 2).set_fill(POS_COLOR, 0.35)
                     for _ in range(f * f)])
        g.arrange_in_grid(f, f, buff=0)
        sq.add(g)
    sq.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
    plus = VGroup(*[Tex("+", font_size=34).move_to((sq[k].get_right() + sq[k + 1].get_left()) / 2)
                    for k in range(len(sq) - 1)])
    total = Tex(f"=6=3!", font_size=36).next_to(sq, RIGHT, buff=0.3)
    area = VGroup(sq, plus, total).move_to(np.array([-3.3, -1.4, 0]))
    squeeze = VGroup(Tex("\\dim S^\\lambda\\ge f^\\lambda", font_size=34),
                     Tex("n!=\\sum_\\lambda(\\dim S^\\lambda)^2\\ge\\sum_\\lambda(f^\\lambda)^2=n!", font_size=34),
                     Tex("\\dim S^\\lambda=f^\\lambda", font_size=40, fill_color=POS_COLOR))
    squeeze.arrange(DOWN, buff=0.3).move_to(np.array([3.0, -1.2, 0]))
    scene.say("維數上下夾：獨立給 ", "$\\dim S^\\lambda\\ge f^\\lambda$", "；兩邊平方和都是 ", "$n!$", "（見 F16）")
    scene.play(FadeIn(squeeze[0]), run_time=0.6)
    scene.play(LaggedStartMap(FadeIn, sq, lag_ratio=0.3), FadeIn(plus), FadeIn(total), run_time=1.2)
    scene.play(Write(squeeze[1]), run_time=1.2)
    scene.wait(3.0)
    scene.play(FadeIn(squeeze[2], scale=1.2), run_time=0.7)
    assert_in_frame(big, blabs, info, area, squeeze)
    assert_apart(area, squeeze)
    assert_apart(info, VGroup(area, squeeze))
    scene.say("$n=3$", "：", "$1^2+2^2+1^2=6$", "，沒有空間再多出任何一維", wait=6.0)
    scene.say("所以標準 ", "$v_T$", " 也張成；另一條路是 Garnir 關係，F38–F39 會真的算", wait=8.0)


class SceneF32IrreducibleBasis(ChuScene):
    def construct(self):
        self.show_header("不可約與標準基底")
        check_math()
        part_plane(self)
        self.clear_stage()
        part_general(self)
        self.clear_stage()
        part_classes(self)
        self.clear_stage()
        part_basis(self)
        self.wait(1.0)
