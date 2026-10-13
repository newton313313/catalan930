"""
Scene F33 —— 矩陣與特徵標（Fulton §7.2；原大綱卡 F710、F711）
執行（在 codes/ 內）：manimgl scenes/sceneF33_matrices_characters.py SceneF33MatricesCharacters

1. 逐欄算 ρ(12)：(12)T_b = 23/1 排行帶負號 → −v_b；(12)T_a = 21/3 用 tabloid 差 → v_a − v_b。
2. ρ(23) 交換兩欄；A² = B² = I、ABA = BAB；AB = 先 (23) 後 (12)。
3. 換到正交座標（只為畫圖）：兩個反射、AB 是 120° 旋轉。
4. 按類取跡 2, 0, −1；平凡、sign 兩列；內積 (4+0+2)/6 = 1；M^(2,1) 的 3, 1, 0 減平凡列。
"""
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_data import act, compose, cycle_type, load, polytabloid, rep_matrix21, sign, specht21, tabloid_key
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob, perm_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import character_table

E, P12, P23, P13 = (1, 2, 3), (2, 1, 3), (1, 3, 2), (3, 2, 1)
P123, P132 = (2, 3, 1), (3, 1, 2)
CLASSES = [[E], [P12, P13, P23], [P123, P132]]          # 依 character_S3["types"] 的順序
PLANE_O = np.array([-3.4, -0.2, 0.0])
SC = 2.4
DOT_COLORS = [TEAL_C, GOLD_C, PURPLE_B]


# ----------------------------------------------------------------------------- 資料
def M(p):
    return np.array(rep_matrix21(p))


def num(s: str) -> float:
    return float(eval(s, {"sqrt": math.sqrt}))


def orth(key):
    return np.array([[num(x) for x in r] for r in load("plane21")[key]])


def projected():
    p = load("plane21")
    return [np.array([num(x) for x in p[f"projected_t{i}"]]) for i in (1, 2, 3)]


def vab_tex(c) -> str:
    parts = []
    for coef, name in zip(c, ("v_a", "v_b")):
        if coef:
            parts.append(("-" if coef < 0 else ("+" if parts else "")) + ("" if abs(coef) == 1 else str(abs(coef))) + name)
    return "".join(parts) or "0"


def fixed_tabloids(p) -> int:
    tabs = load("shape21")["tabloids"].values()
    return sum(tabloid_key(act(p, t)) == tabloid_key(t) for t in tabs)


def check_math():
    m, sh, cs = load("matrices21"), load("shape21"), load("character_S3")
    A, B = M(P12), M(P23)
    assert A.tolist() == m["rho12"] and B.tolist() == m["rho23"]
    assert A[:, 0].tolist() == m["rho12_va"] == [1, -1] and A[:, 1].tolist() == m["rho12_vb"] == [0, -1]
    tb12 = act(P12, sh["Tb"])
    assert tb12 == ((2, 3), (1,)) and specht21(polytabloid(tb12)) == (0, -1)
    ta12 = act(P12, sh["Ta"])
    assert ta12 == ((2, 1), (3,))
    assert polytabloid(ta12) == {((1, 2), (3,)): 1, ((1, 3), (2,)): -1} and specht21(polytabloid(ta12)) == (1, -1)
    assert [list(r) for r in act(P23, sh["Ta"])] == sh["Tb"] and [list(r) for r in act(P23, sh["Tb"])] == sh["Ta"]
    I2 = np.eye(2, dtype=int)
    assert (A @ A == I2).all() and (B @ B == I2).all()
    assert (A @ B @ A == B @ A @ B).all() and (A @ B @ A == M(P13)).all()
    assert compose(P12, P23) == P123 and (A @ B == M(P123)).all() and (A @ B).tolist() == m["rho123"]
    R12, R23, R123 = orth("rho12_orthonormal"), orth("rho23_orthonormal"), orth("rho123_orthonormal")
    assert np.allclose(R12 @ R23, R123)
    th = 2 * math.pi / 3
    assert np.allclose(R123, [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    types = [tuple(t) for t in cs["types"]]
    for k, cl in enumerate(CLASSES):
        assert len(cl) == cs["sizes"][k]
        for p in cl:
            assert tuple(cycle_type(p)) == types[k]
            assert int(np.trace(M(p))) == cs["specht"]["21"][k]
            assert sign(p) == cs["specht"]["111"][k]
            assert fixed_tabloids(p) == cs["permutation"]["21"][k]
    chi = cs["specht"]["21"]
    assert chi == [2, 0, -1] and cs["specht"]["3"] == [1, 1, 1]
    assert sum(Fraction(s * c * c, 6) for s, c in zip(cs["sizes"], chi)) == 1
    assert [a - b for a, b in zip(cs["permutation"]["21"], cs["specht"]["3"])] == chi
    lams, table = character_table(3)                 # 欄依 partitions(3)：(3),(2,1),(1,1,1)
    row = table[lams.index((2, 1))]
    assert [row[lams.index(t)] for t in types] == chi


# ----------------------------------------------------------------------------- 小工具
def pp(v):
    return PLANE_O + SC * np.array([v[0], v[1], 0.0])


def mirror_line(Rm, color):
    vals, vecs = np.linalg.eigh(Rm)
    d = vecs[:, int(np.argmax(vals))]
    d = np.array([d[0], d[1], 0.0])
    return DashedLine(PLANE_O - 2.4 * d, PLANE_O + 2.4 * d, dash_length=0.14).set_stroke(color, width=3)


def card(T, name, color=WHITE):
    t = tableau_mob(T, cs=0.42)
    lab = Tex(name, font_size=32, fill_color=color).next_to(t, DOWN, buff=0.15)
    return VGroup(t, lab)


def placeholder(mat):
    return VGroup(*[Tex("?", font_size=34, fill_color=MUTED_COLOR).move_to(mat.entry(i, j))
                    for i in range(2) for j in range(2)])


def headed_matrix(name, rows, center):
    mat = MatrixMob(rows, font_size=36, h_buff=0.8)
    lab = Tex(name + "=", font_size=38).next_to(mat, LEFT, buff=0.2)
    heads = VGroup(*[Tex(n, font_size=26, fill_color=MUTED_COLOR).next_to(mat, UP, buff=0.12).set_x(mat.col(j).get_x())
                     for j, n in enumerate(("v_a", "v_b"))])
    g = VGroup(lab, mat, heads).move_to(center)
    for e in mat.grid:
        e.set_opacity(0)
    return g, mat


def reveal_col(scene, mat, ph, j, run_time=0.8):
    olds = VGroup(ph[j], ph[2 + j])
    news = mat.col(j)
    scene.play(FadeOut(olds), news.animate.set_opacity(1), run_time=run_time)
    scene.play(Indicate(news, color=OP_COLOR), run_time=0.6)


# ----------------------------------------------------------------------------- 1. ρ(12)
def part_columns(scene):
    sh = load("shape21")
    ca, cb = card(sh["Ta"], "v_a", POS_COLOR), card(sh["Tb"], "v_b", POS_COLOR)
    cards = VGroup(ca, cb).arrange(DOWN, buff=0.5).move_to(np.array([-5.9, 0.9, 0]))
    gA, A = headed_matrix("\\rho(12)", load("matrices21")["rho12"], np.array([4.5, 1.7, 0]))
    phA = placeholder(A)
    scene.say("把 ", "$\\rho(12)$", " 一欄一欄算出來：第 ", "$j$", " 欄＝第 ", "$j$", " 個基底的像")
    scene.play(FadeIn(cards), FadeIn(gA), FadeIn(phA), run_time=1.0)
    scene.wait(5.0)

    # v_b 這一欄
    t1 = Tex("(12)T_b=", font_size=36)
    bad = tableau_mob(act(P12, sh["Tb"]), cs=0.42)
    bad.cell_group([(0, 0), (1, 0)]).set_stroke(COL_COLOR, width=5)
    arr = Arrow(LEFT, RIGHT, buff=0).set_width(0.8).set_color(OP_COLOR)
    minus = Tex("-", font_size=44, fill_color=NEG_COLOR)
    good = tableau_mob(sh["Tb"], cs=0.42)
    rowb = VGroup(t1, bad, arr, minus, good).arrange(RIGHT, buff=0.2).move_to(np.array([-1.4, 2.2, 0]))
    sort_lab = zh("第一行排好：換一次", font_size=22, color=COL_COLOR).next_to(rowb, UP, buff=0.12)
    sort_lab.set_x(arr.get_x())
    eqb = Tex("(12)v_b=v_{(12)T_b}=-v_b", font_size=36, t2c={"-v_b": NEG_COLOR}).next_to(rowb, DOWN, buff=0.35)
    scene.say("$(12)T_b$", " 的第一行是 2 在上、1 在下；排好要換一次，帶出負號")
    scene.play(FadeIn(t1), TransformFromCopy(cb[0], bad), run_time=1.0)
    scene.wait(3.0)
    scene.play(GrowArrow(arr), FadeIn(sort_lab), FadeIn(minus), FadeIn(good), run_time=1.0)
    scene.play(Write(eqb), run_time=1.0)
    scene.wait(4.0)
    scene.say("所以第二欄是 ", "$(0,-1)$")
    reveal_col(scene, A, phA, 1)
    scene.wait(4.0)

    # v_a 這一欄
    t2 = Tex("(12)T_a=", font_size=36)
    ta = tableau_mob(act(P12, sh["Ta"]), cs=0.42)
    rowa = VGroup(t2, ta).arrange(RIGHT, buff=0.2).next_to(eqb, DOWN, buff=0.55).set_x(-2.6)
    l1 = Tex("(12)v_a=t_3-t_2", font_size=36)
    l2 = Tex("=(t_3-t_1)-(t_2-t_1)=v_a-v_b", font_size=36, t2c={"v_a-v_b": OP_COLOR})
    lines = VGroup(l1, l2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(rowa, DOWN, buff=0.35).set_x(-1.4)
    scene.say("$(12)T_a$", " 不是標準表；直接看它的兩個 tabloid：", "$t_3-t_2$")
    scene.play(FadeIn(t2), TransformFromCopy(ca[0], ta), run_time=1.0)
    scene.play(Write(l1), run_time=1.0)
    scene.wait(4.0)
    scene.say("改寫成兩條邊差：", "$v_a-v_b$", "（F38 的交換關係會給同一個答案）")
    scene.play(Write(l2), run_time=1.2)
    scene.wait(4.0)
    reveal_col(scene, A, phA, 0)
    assert_in_frame(cards, gA, rowb, sort_lab, eqb, rowa, lines)
    assert_apart(VGroup(rowb, eqb, lines), gA)
    assert_apart(cards, VGroup(rowb, rowa, lines))
    scene.say("同一橫行的交換不見得讓 ", "$v_T$", " 不變：", "$(12)v_a\\neq v_a$", wait=6.0)

    # ρ(23)
    scene.play(FadeOut(VGroup(t1, bad, arr, sort_lab, minus, good, eqb, t2, ta, lines)), run_time=0.6)
    gB, B = headed_matrix("\\rho(23)", load("matrices21")["rho23"], np.array([4.5, -0.9, 0]))
    phB = placeholder(B)
    swap = Tex("(23)T_a=T_b,\\quad (23)T_b=T_a", font_size=38).move_to(np.array([-1.4, 1.7, 0]))
    scene.say("先猜猜看：", "$(23)$", " 把 ", "$T_a$", " 和 ", "$T_b$", " 互換，", "$\\rho(23)$", " 長什麼樣？")
    scene.play(FadeIn(gB), FadeIn(phB), Write(swap), run_time=1.0)
    scene.wait(6.0)
    reveal_col(scene, B, phB, 0, run_time=0.6)
    reveal_col(scene, B, phB, 1, run_time=0.6)
    scene.wait(3.0)

    rel1 = Tex("A^2=B^2=I", font_size=38)
    rel2 = Tex("ABA=BAB=\\rho(13)", font_size=38)
    rel3 = Tex("AB=\\rho(12)\\rho(23)=\\rho(123)", font_size=38)
    rels = VGroup(rel1, rel2, rel3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(swap, DOWN, buff=0.6)
    nameA = Tex("A", font_size=34, fill_color=OP_COLOR).next_to(gA, RIGHT, buff=0.2)
    nameB = Tex("B", font_size=34, fill_color=OP_COLOR).next_to(gB, RIGHT, buff=0.2)
    scene.say("記 ", "$A=\\rho(12)$", "、", "$B=\\rho(23)$", "：檢查 Coxeter 關係")
    scene.play(FadeIn(nameA), FadeIn(nameB), run_time=0.6)
    scene.play(Write(rel1), run_time=0.9)
    scene.play(Write(rel2), run_time=0.9)
    scene.wait(4.0)
    scene.say("矩陣乘 ", "$AB$", " 對應「先 ", "$(23)$", " 後 ", "$(12)$", "」，就是 3-循環 ", "$(123)$")
    scene.play(Write(rel3), run_time=1.0)
    assert_in_frame(gB, swap, rels, nameA, nameB)
    assert_apart(VGroup(swap, rels), VGroup(gA, gB))
    scene.wait(7.0)


# ----------------------------------------------------------------------------- 2. 正交座標
def part_geometry(scene):
    pts = projected()
    tri = Polygon(*[pp(v) for v in pts]).set_stroke(GREY_B, width=2.5)
    labs = VGroup(*[Tex(f"t_{i + 1}", font_size=32).move_to(pp(v) + 0.42 * np.append(v / np.linalg.norm(v), 0))
                    for i, v in enumerate(pts)])
    dots = VGroup(*[Dot(pp(v), radius=0.11, fill_color=c) for v, c in zip(pts, DOT_COLORS)])
    m12 = mirror_line(orth("rho12_orthonormal"), ROW_COLOR)
    m23 = mirror_line(orth("rho23_orthonormal"), COL_COLOR)
    note = zh("換成正交座標（同一個表示，只是換基底來畫圖）", font_size=24, color=MUTED_COLOR)
    note.move_to(np.array([0, 2.85, 0]))
    p = load("plane21")

    def mtex(key):
        return "\\begin{pmatrix}" + "\\\\".join("&".join(x.replace("sqrt(3)", "\\sqrt{3}") for x in r)
                                                 for r in p[key]) + "\\end{pmatrix}"

    f12 = Tex("\\rho(12)\\sim" + mtex("rho12_orthonormal"), font_size=32)
    f23 = Tex("\\rho(23)\\sim" + mtex("rho23_orthonormal"), font_size=32)
    f123 = Tex("AB\\sim" + mtex("rho123_orthonormal"), font_size=32)
    right = VGroup(f12, f23, f123).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(np.array([3.6, -0.2, 0]))
    scene.say("換一組正交座標畫圖：", "$S^{(2,1)}$", " 就是零和平面上的等邊三角形")
    scene.play(FadeIn(note), ShowCreation(tri), FadeIn(labs), FadeIn(dots), run_time=1.2)
    scene.wait(4.0)
    scene.say("$(12)$", " 與 ", "$(23)$", " 各是一面鏡子")
    scene.play(ShowCreation(m12), FadeIn(f12), run_time=0.9)
    scene.play(dots[0].animate.move_to(pp(pts[1])), dots[1].animate.move_to(pp(pts[0])), run_time=1.0)
    scene.play(dots[0].animate.move_to(pp(pts[0])), dots[1].animate.move_to(pp(pts[1])), run_time=0.8)
    scene.play(ShowCreation(m23), FadeIn(f23), run_time=0.9)
    scene.wait(4.0)
    scene.say("兩面鏡子夾 60°，連做兩次就是轉 120°：", "$AB$", " 是旋轉")
    scene.play(FadeIn(f123), run_time=0.7)
    scene.play(Rotate(dots, 2 * math.pi / 3, about_point=PLANE_O), run_time=1.6)
    scene.wait(2.0)
    scene.play(Rotate(dots, 2 * math.pi / 3, about_point=PLANE_O), run_time=1.2)
    scene.play(Rotate(dots, 2 * math.pi / 3, about_point=PLANE_O), run_time=1.2)
    assert_in_frame(note, tri, labs, m12, m23, right)
    assert_apart(VGroup(tri, labs, m12, m23), right)
    scene.say("只有正交座標的矩陣能當成歐氏反射來畫；跡不受換基底影響", wait=7.0)


# ----------------------------------------------------------------------------- 3. 特徵標
def part_characters(scene):
    cs = load("character_S3")
    xs = [-1.4, 1.4, 4.2]
    lab_x = -4.6
    heads = VGroup(*[Tex("\\ ".join(perm_tex(p) for p in cl), font_size=30) for cl in CLASSES])
    sizes = VGroup()
    for x, h, s in zip(xs, heads, cs["sizes"]):
        h.move_to(np.array([x, 2.55, 0]))
        sizes.add(zh(f"{s} 個", font_size=22, color=MUTED_COLOR).next_to(h, DOWN, buff=0.12))
    rule = Line(np.array([-5.6, 1.85, 0]), np.array([5.6, 1.85, 0])).set_stroke(GREY_C, 1.5)
    scene.say("六個排列依循環型分成三類：共軛的排列，矩陣的跡一定相同")
    scene.play(LaggedStartMap(FadeIn, heads, lag_ratio=0.3), FadeIn(sizes), ShowCreation(rule), run_time=1.4)
    scene.wait(5.0)

    def table_row(name, vals, y, color=WHITE):
        lab = Tex(name, font_size=34).move_to(np.array([lab_x, y, 0]))
        ents = VGroup(*[Tex(str(v), font_size=36, fill_color=color).move_to(np.array([x, y, 0])) for x, v in zip(xs, vals)])
        return VGroup(lab, ents)

    reps = [E, P12, P123]
    chi = [int(np.trace(M(p))) for p in reps]
    rS = table_row("\\chi^{(2,1)}", chi, 1.3, POS_COLOR)
    traces = VGroup(*[Tex(t, font_size=28).move_to(np.array([x, 0.65, 0]))
                      for x, t in zip(xs, ("\\mathrm{tr}\\,I", "\\mathrm{tr}\\,A", "\\mathrm{tr}\\,AB"))])
    geo = VGroup(zh("兩個方向都不動", font_size=22), mixed("$+1$", " 與 ", "$-1$", " 相消", font_size=22),
                 Tex("2\\cos 120^\\circ", font_size=28))
    for x, g in zip(xs, geo):
        g.move_to(np.array([x, 0.15, 0])).set_color(MUTED_COLOR)
    scene.say("取跡：", "$\\mathrm{tr}\\,I=2$", "、", "$\\mathrm{tr}\\,A=0$", "、", "$\\mathrm{tr}\\,AB=-1$")
    scene.play(FadeIn(rS[0]), FadeIn(traces), run_time=0.8)
    scene.play(LaggedStart(*[TransformFromCopy(t, e) for t, e in zip(traces, rS[1])], lag_ratio=0.3), run_time=1.4)
    scene.wait(3.0)
    scene.say("幾何上：恆等、鏡射（+1 與 −1）、轉 120°")
    scene.play(FadeIn(geo, shift=0.1 * DOWN), run_time=0.8)
    scene.wait(6.0)
    scene.play(FadeOut(traces), FadeOut(geo), run_time=0.5)

    rT = table_row("\\chi^{(3)}", cs["specht"]["3"], 0.6)
    rU = table_row("\\chi^{(1,1,1)}", cs["specht"]["111"], -0.1)
    scene.say("再補上平凡表示與 sign 表示兩列：一張完整的特徵標表")
    scene.play(FadeIn(rT, shift=0.1 * DOWN), run_time=0.7)
    scene.play(FadeIn(rU, shift=0.1 * DOWN), run_time=0.7)
    scene.wait(5.0)

    ip = Tex("\\langle\\chi,\\chi\\rangle=\\frac{1}{6}\\bigl(1\\cdot 2^2+3\\cdot 0^2+2\\cdot(-1)^2\\bigr)=1", font_size=36)
    ip.move_to(np.array([0.3, -1.1, 0]))
    scene.say("內積要按類的大小 1、3、2 加權（不是 ", "$z$", " 值）")
    scene.play(*[Indicate(s, color=OP_COLOR) for s in sizes], run_time=1.0)
    scene.play(Write(ip), run_time=1.4)
    scene.wait(4.0)
    scene.say("自己和自己的內積是 1：這正是不可約的特徵標檢驗", wait=6.0)

    rM = table_row("\\chi_{M^{(2,1)}}", cs["permutation"]["21"], -1.1, ROW_COLOR)
    scene.play(FadeOut(ip), run_time=0.5)
    scene.say("$M^{(2,1)}$", " 是置換表示：跡＝固定的 tabloid 數，得 ", "$3,1,0$")
    scene.play(FadeIn(rM, shift=0.1 * DOWN), run_time=0.8)
    scene.wait(5.0)
    diff = Tex("(3,1,0)-(1,1,1)=(2,0,-1)", font_size=38, t2c={"(2,0,-1)": POS_COLOR})
    diff.move_to(np.array([0.3, -2.1, 0]))
    scene.say("減掉平凡列，剩下的正是 ", "$\\chi^{(2,1)}$", "：", "$M^{(2,1)}=\\mathbb{C}z\\oplus S^{(2,1)}$")
    scene.play(Write(diff), run_time=1.2)
    scene.play(Indicate(rS[1], color=POS_COLOR), run_time=0.8)
    assert_in_frame(heads, sizes, rS, rT, rU, rM, diff)
    assert_apart(rM, diff)
    scene.wait(5.0)
    scene.say("注意：Specht 的矩陣不是置換矩陣，不能拿「固定的表」來數它的跡", wait=6.0)
    scene.say("複數、有限群、完全可約：特徵標只記跡，卻決定了表示的同構類", wait=7.0)


class SceneF33MatricesCharacters(ChuScene):
    def construct(self):
        self.show_header("矩陣與特徵標")
        check_math()
        part_columns(self)
        self.clear_stage()
        part_geometry(self)
        self.clear_stage()
        part_characters(self)
        self.wait(1.0)
