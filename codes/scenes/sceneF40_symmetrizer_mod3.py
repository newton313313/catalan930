"""
Scene F40 —— Young 對稱化子、多項式模型、模 3（Fulton §7.4 Lemma 5、Ex. 15–20，書 p.99–104；原大綱卡 F724、X703、X702）
執行（在 codes/ 內）：manimgl scenes/sceneF40_symmetrizer_mod3.py SceneF40SymmetrizerMod3

c_T = (1 − (13))(1 + (12))：16 個乘積按置換合併得 c² = 3c；c/3 才是冪等；n_λ = n!/f^λ = 鉤長乘積（(3,2)：24）。
F_T = 各行 (上 − 下) 之積：F_{12/3} = x1 − x3、F_{13/2} = x1 − x2、F_{21/3} = F_{12/3} − F_{13/2}。
模 3：c ≠ 0 但 c² = 0；S 有平凡線 v_a + v_b，S̃ 沒有 ⇒ 不同構；αβ = 3I。
"""
import sys
from collections import Counter
from math import factorial, prod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_data import act, compose, gr_mul, load, rep_matrix21, symmetrizers
from utils.rep_draw import (COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob, perm_tex,
                            signed_sum)
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

TA = ((1, 2), (3,))
TB = ((1, 3), (2,))
TN = ((2, 1), (3,))
ORDER = [(1, 2, 3), (2, 1, 3), (3, 2, 1), (2, 3, 1), (1, 3, 2), (3, 1, 2)]   # 1、(12)、(13)、(123)、(23)、(132)


# =============================================================================
# 純 Python 的小工具
# =============================================================================
def ptex(p):
    t = perm_tex(p)
    return "1" if t == "e" else t


def merge_table():
    """c·c 的 16 個乘積按結果置換合併：{置換: (乘積個數, 係數和)}。"""
    _, _, c = symmetrizers(TA)
    cnt, tot = Counter(), Counter()
    for p, x in c.items():
        for q, y in c.items():
            r = compose(p, q)
            cnt[r] += 1
            tot[r] += x * y
    return c, cnt, tot


def F(rows):
    """F_T = Π_行 Π_{上<下} (x_上 − x_下)；λ=(2,1) 時只有第一行兩格，是一次式 {變數: 係數}。"""
    top, bot = rows[0][0], rows[1][0]
    return {top: 1, bot: -1}


def poly_str(d):
    s = ""
    for v in sorted(d):
        c = d[v]
        if c:
            s += ("+" if c > 0 and s else "") + ("-" if c < 0 else "") + f"x{v}"
    return s


def lin(a, b, sa=1, sb=1):
    out = Counter()
    for k, v in a.items():
        out[k] += sa * v
    for k, v in b.items():
        out[k] += sb * v
    return {k: v for k, v in out.items() if v}


def mat_vec(m, v, mod=None):
    out = [sum(m[i][j] * v[j] for j in range(len(v))) for i in range(len(m))]
    return [x % mod for x in out] if mod else out


def check_math():
    y = load("young_symmetrizer21")
    c, cnt, tot = merge_table()
    assert {tuple(t["perm"]): t["coef"] for t in y["c_terms"]} == c
    assert sum(cnt.values()) == 16 and set(cnt) == set(ORDER)
    assert all(tot[p] == 3 * c.get(p, 0) for p in ORDER)
    assert dict(gr_mul(c, c)) == {p: 3 * v for p, v in c.items()}
    assert compose((2, 1, 3), (2, 1, 3)) == (1, 2, 3)                      # 代表乘積 (12)(12) = 1
    assert y["n_lambda"] == 3 and y["n_factorial"] // y["f"] == 3
    h = load("hooks")
    for key, n, f, sc in (("21", 3, 2, 3), ("32", 5, 5, 24)):
        assert h[key]["f"] == f and h[key]["scale"] == sc
        assert factorial(n) // f == sc == prod(x for r in h[key]["hooks"] for x in r)
    sp = load("specht_polynomial21")
    assert poly_str(F(TA)) == sp["Fa"] == "x1-x3" and poly_str(F(TB)) == sp["Fb"] == "x1-x2"
    assert poly_str(F(TN)) == sp["nonstandard"] == "x2-x3"
    assert lin(F(TA), F(TB), 1, -1) == F(TN)                                 # F_{21/3} = F_a − F_b
    s12 = (2, 1, 3)
    assert act(s12, TA) == TN and {s12[v - 1]: k for v, k in F(TA).items()} == F(TN)   # σF_T = F_{σT}
    m = load("mod3")
    assert m["field"] == 3 and m["c_mod3_is_nonzero"] and m["c_squared_mod3"] == "0"
    assert all(v % 3 for v in c.values()) and all(tot[p] % 3 == 0 for p in ORDER)
    A, B = m["rho12_S"], m["rho23_S"]
    assert A == rep_matrix21((2, 1, 3)) and B == rep_matrix21((1, 3, 2))
    assert mat_vec(A, [1, 1]) == [1, -2] and mat_vec(A, [1, 1], 3) == [1, 1] == mat_vec(B, [1, 1], 3)
    At, Bt = m["rho12_tildeS"], m["rho23_tildeS"]
    assert At == [[1, -1], [0, -1]] and Bt == B
    for x in range(3):                                                        # B̃ 固定 (x,x)；Ã(x,x) = (0,−x)
        assert mat_vec(Bt, [x, x], 3) == [x, x] and mat_vec(At, [x, x], 3) == [0, (-x) % 3]
        assert (mat_vec(At, [x, x], 3) == [x, x]) == (x == 0)
    al, be = m["alpha_on_tildeS"], m["beta_on_S"]
    assert al == [[2, -1], [-1, 2]] and be == [[2, 1], [1, 2]] and m["alpha_det"] == 3
    ab = [[sum(al[i][k] * be[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert ab == [[3, 0], [0, 3]] and al[0][0] * al[1][1] - al[0][1] * al[1][0] == 3


# =============================================================================
# 畫圖小工具
# =============================================================================
def tx(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def button(active=True):
    t = mixed("normalized：", r"$c_T/3$", font_size=24, color=WHITE if active else GREY_C)
    r = RoundedRectangle(width=t.get_width() + 0.5, height=t.get_height() + 0.35, corner_radius=0.18,
                         stroke_color=POS_COLOR if active else GREY_C, stroke_width=3)
    r.set_fill(POS_COLOR if active else GREY_E, opacity=0.25)
    return VGroup(r, t.move_to(r))


# =============================================================================
# 第一段：c² = 3c
# =============================================================================
def part_square(scene):
    tab = tableau_mob(TA, cs=0.6, center=np.array([-5.7, 1.9, 0]))
    rrow = SurroundingRectangle(VGroup(tab.cell(0, 0), tab.cell(0, 1)), buff=0.06, color=ROW_COLOR)
    rcol = SurroundingRectangle(VGroup(tab.cell(0, 0), tab.cell(1, 0)), buff=0.12, color=COL_COLOR)
    a_t = tx(r"a_T=1+(1\,2)", 34, ROW_COLOR)
    b_t = tx(r"b_T=1-(1\,3)", 34, COL_COLOR)
    ab = VGroup(a_t, b_t).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.5)
    c, cnt, tot = merge_table()
    terms = [(c[p], tx(ptex(p), 34)) for p in ORDER if p in c]
    c_line = VGroup(tx(r"c_T=b_Ta_T=", 34), signed_sum(terms, font_size=34, buff=0.15)).arrange(RIGHT, buff=0.15)
    c_line.move_to(np.array([-3.3, 0.5, 0]))
    assert_in_frame(tab, ab, c_line)
    scene.play(FadeIn(tab), ShowCreation(rrow), ShowCreation(rcol))
    scene.play(FadeIn(ab, lag_ratio=0.3))
    scene.say("$T_a=12/3$", "：列給 ", "$a_T$", "（藍），行給 ", "$b_T$", "（橙）", wait=2.3)
    scene.play(Write(c_line), run_time=1.5)
    scene.say("$c_T=b_Ta_T$", " 展開成四項，係數都是 ", "$\\pm1$", wait=2.8)
    scene.say("乘法順序固定：", "$b_T$", " 在左、", "$a_T$", " 在右", wait=2.5)

    rep = VGroup(zh("16 個乘積之一：", font_size=24, color=MUTED_COLOR),
                 tx(r"(1\,2)\cdot(1\,2)=1", 34, OP_COLOR)).arrange(RIGHT, buff=0.2)
    rep.move_to(np.array([-3.3, -0.6, 0]))
    scene.play(FadeIn(rep))
    scene.say("把 ", "$c_T$", " 乘自己：4 × 4 = 16 個乘積，只看一個代表", wait=2.8)

    heads = ["置換", "乘積數", "c² 係數", "c 係數"]
    xs = [1.4, 2.85, 4.3, 5.75]
    table = VGroup()
    hrow = VGroup(*[zh(h, font_size=22, color=MUTED_COLOR).move_to(np.array([x, 2.3, 0])) for h, x in zip(heads, xs)])
    table.add(hrow)
    body = VGroup()
    for k, p in enumerate(ORDER):
        yk = 1.75 - 0.5 * k
        cc, ct = tot[p], c.get(p, 0)
        col = lambda v: POS_COLOR if v > 0 else (NEG_COLOR if v < 0 else MUTED_COLOR)
        body.add(VGroup(tx(ptex(p), 30).move_to(np.array([xs[0], yk, 0])),
                        tx(str(cnt[p]), 30, MUTED_COLOR).move_to(np.array([xs[1], yk, 0])),
                        tx(str(cc), 30, col(cc)).move_to(np.array([xs[2], yk, 0])),
                        tx(str(ct), 30, col(ct)).move_to(np.array([xs[3], yk, 0]))))
    table.add(body)
    line = Line(np.array([0.7, 2.03, 0]), np.array([6.5, 2.03, 0]), stroke_color=GREY_B, stroke_width=1.5)
    total = mixed("合計 ", "$16$", " 個乘積", font_size=22, color=MUTED_COLOR).move_to(np.array([3.6, -1.5, 0]))
    assert_in_frame(table, total)
    assert_apart(table, c_line)
    assert_apart(table, rep)
    scene.play(FadeIn(hrow), ShowCreation(line))
    scene.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2])) for r in body], lag_ratio=0.15), FadeIn(total),
               run_time=2.0)
    scene.say("按結果的置換合併：同一格的係數加起來", wait=2.8)
    scene.play(*[FadeIn(r[3]) for r in body])
    hi = VGroup(SurroundingRectangle(VGroup(*[r[2] for r in body]), buff=0.1, color=OP_COLOR),
                SurroundingRectangle(VGroup(*[r[3] for r in body]), buff=0.1, color=OP_COLOR))
    scene.play(ShowCreation(hi))
    scene.say("每一格都剛好是 ", "$c_T$", " 的 3 倍；(23)、(132) 的正負抵消成 0", wait=3.3)
    res = tx(r"c_T^2=3\,c_T", 48, OP_COLOR)
    rbox = SurroundingRectangle(res, buff=0.2, color=OP_COLOR, stroke_width=3)
    rg = VGroup(rbox, res).move_to(np.array([-3.3, -2.0, 0]))
    assert_in_frame(rg)
    assert_apart(rg, rep)
    scene.play(FadeIn(rg, scale=1.1))
    scene.say("做兩次不是原樣，而是放大三倍", wait=2.8)


# =============================================================================
# 第二段：c/3 才是冪等；n_λ = n!/f^λ = 鉤長乘積
# =============================================================================
def part_normalize(scene):
    btn = button(True).move_to(np.array([-3.6, 2.3, 0]))
    idem = tx(r"\Big(\frac{c_T}{3}\Big)^2=\frac{3\,c_T}{9}=\frac{c_T}{3}", 40).move_to(np.array([2.2, 2.3, 0]))
    assert_in_frame(btn, idem)
    scene.play(FadeIn(btn, scale=1.1))
    scene.say("按下 normalized：除以 3", wait=1.8)
    scene.play(Write(idem))
    scene.say("$c_T/3$", " 再做一次還是自己：這才是冪等元", wait=2.8)
    scene.say("冪等只是「做兩次等於做一次」，不自動是正交投影", wait=2.5)

    gen = tx(r"n_\lambda=\frac{n!}{f^\lambda}=\prod_{b\in\lambda}h(b)", 40).move_to(np.array([0, 0.9, 0]))
    h = load("hooks")
    h21 = tableau_mob(tuple(map(tuple, h["21"]["hooks"])), cs=0.5, center=np.array([-4.6, -1.0, 0]))
    h32 = tableau_mob(tuple(map(tuple, h["32"]["hooks"])), cs=0.5, center=np.array([1.0, -1.0, 0]))
    e21 = tx(r"\frac{3!}{2}=3=3\cdot1\cdot1", 36).next_to(h21, RIGHT, buff=0.4)
    e32 = tx(r"\frac{5!}{5}=24=4\cdot3\cdot1\cdot2\cdot1", 36).next_to(h32, RIGHT, buff=0.4)
    assert_in_frame(gen, h21, h32, e21, e32)
    assert_apart(e21, h32)
    scene.play(FadeIn(gen))
    scene.say("一般的放大倍數 ", "$n_\\lambda=n!/f^\\lambda$", "，正好是鉤長乘積", wait=2.8)
    scene.play(FadeIn(h21), FadeIn(e21))
    scene.say("$(2,1)$", "：", "$6/2=3$", "，鉤長 3、1、1", wait=2.3)
    scene.play(FadeIn(h32), FadeIn(e32))
    scene.say("$(3,2)$", "：", "$120/5=24$", "，和鉤長公式那一集的 24 對上", wait=2.8)
    note = VGroup(mixed("能除以 ", "$n_\\lambda$", "：要在特徵 0（例如 ", "$\\mathbb Q,\\mathbb C$", "）", font_size=22),
                  mixed("不同標準表的 ", "$c_T$", " 不一定互相正交", font_size=22, color=MUTED_COLOR)
                  ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(np.array([0, -2.45, 0]))
    assert_in_frame(note)
    scene.play(FadeIn(note))
    scene.say("除以 3 要求係數能除；換到模 3 就出事", wait=2.8)


# =============================================================================
# 第三段：多項式模型 F_T
# =============================================================================
def part_poly(scene):
    form = tx(r"F_T=\prod_{\text{columns }j}\ \prod_{i<k}\big(x_{T(i,j)}-x_{T(k,j)}\big)", 38)
    form.move_to(np.array([0, 2.3, 0]))
    scene.play(FadeIn(form))
    scene.say("每一行取「上減下」連乘：只有一格的行貢獻空積 1", wait=2.8)
    sp = load("specht_polynomial21")
    items = VGroup()
    for rows, name, poly, x in ((TA, "F_{12/3}", sp["Fa"], -4.2), (TB, "F_{13/2}", sp["Fb"], 0.0),
                                (TN, "F_{21/3}", sp["nonstandard"], 4.2)):
        tab = tableau_mob(rows, cs=0.55)
        tab.fill_cells([(0, 0), (1, 0)], COL_COLOR, 0.35)
        lab = tx(name + "=" + poly.replace("x1", "x_1").replace("x2", "x_2").replace("x3", "x_3"), 34)
        items.add(VGroup(tab, lab).arrange(DOWN, buff=0.3).move_to(np.array([x, 0.4, 0])))
    assert_in_frame(form, items)
    scene.play(LaggedStart(*[FadeIn(it) for it in items[:2]], lag_ratio=0.4))
    scene.say("$T_a$", " 第一行 1、3；", "$T_b$", " 第一行 1、2", wait=2.8)
    scene.play(FadeIn(items[2]))
    scene.say("非標準的 ", "$21/3$", "：第一行 2、3，得 ", "$x_2-x_3$", wait=2.3)
    rel = tx(r"F_{21/3}=F_{12/3}-F_{13/2}", 40, OP_COLOR).move_to(np.array([0, -1.4, 0]))
    same = tx(r"[21/3]=[12/3]-[13/2]", 34, MUTED_COLOR).next_to(rel, DOWN, buff=0.3)
    assert_in_frame(rel, same)
    scene.play(Write(rel))
    scene.say("$(x_1-x_3)-(x_1-x_2)=x_2-x_3$", wait=2.8)
    scene.play(FadeIn(same))
    scene.say("和行 tabloid 的交換關係一模一樣", wait=2.8)
    scene.play(FadeOut(VGroup(rel, same)))
    act_t = tx(r"(1\,2)\,F_{12/3}=x_2-x_3=F_{21/3}=F_{12/3}-F_{13/2}", 36).move_to(np.array([0, -1.5, 0]))
    assert_in_frame(act_t)
    scene.play(Write(act_t))
    scene.say("換編號就同時換變數：", "$\\sigma F_T=F_{\\sigma T}$", wait=2.8)
    scene.say("又一個同構的模型：同構，但不住在同一個空間", wait=2.8)


# =============================================================================
# 第四段：模 3
# =============================================================================
def part_mod3(scene):
    head = mixed("在 ", r"$\mathbb F_3$", " 裡 ", "$3=0$", "：", r"$c_T\ne0$", "，但 ", r"$c_T^2=3c_T=0$", font_size=26)
    head.move_to(np.array([-1.6, 2.6, 0]))
    dead = button(False).move_to(np.array([5.0, 2.6, 0]))
    slash = Line(dead.get_corner(DL), dead.get_corner(UR), stroke_color=NEG_COLOR, stroke_width=4)
    assert_in_frame(head, dead)
    assert_apart(head, dead)
    scene.play(FadeIn(head))
    scene.say("$c_T$", " 的四個係數是 ", "$\\pm1$", "，模 3 不是 0；但平方變成 0", wait=2.8)
    scene.play(FadeIn(dead), ShowCreation(slash))
    scene.say("normalized 按鈕不能用了：不能除以 3", wait=2.3)

    m = load("mod3")
    lt = mixed(r"$S^{(2,1)}$", "（", "$v_a,v_b$", " 座標）", font_size=24).move_to(np.array([-3.4, 1.7, 0]))
    rt = mixed(r"$\widetilde S^{(2,1)}$", "（行 tabloid 版）", font_size=24).move_to(np.array([3.4, 1.7, 0]))
    lA = VGroup(tx("A=", 32), MatrixMob(m["rho12_S"], 30, 0.6, 0.45))
    lB = VGroup(tx("B=", 32), MatrixMob(m["rho23_S"], 30, 0.6, 0.45))
    for g in (lA, lB):
        g.arrange(RIGHT, buff=0.12)
    lm = VGroup(lA, lB).arrange(RIGHT, buff=0.5).move_to(np.array([-3.4, 0.8, 0]))
    rA = VGroup(tx(r"\widetilde A=", 32), MatrixMob(m["rho12_tildeS"], 30, 0.6, 0.45))
    rB = VGroup(tx(r"\widetilde B=", 32), MatrixMob(m["rho23_tildeS"], 30, 0.6, 0.45))
    for g in (rA, rB):
        g.arrange(RIGHT, buff=0.12)
    rm = VGroup(rA, rB).arrange(RIGHT, buff=0.5).move_to(np.array([3.4, 0.8, 0]))
    sep = DashedLine(np.array([0, 2.0, 0]), np.array([0, -2.8, 0]), stroke_color=GREY_D)
    assert_in_frame(lt, rt, lm, rm)
    assert_apart(lm, rm)
    scene.play(FadeIn(VGroup(lt, lm)), ShowCreation(sep))
    scene.say("$S$", " 這邊：", "$A=\\rho(1\\,2)$", "、", "$B=\\rho(2\\,3)$", wait=2.3)
    l1 = tx(r"A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}1\\-2\end{pmatrix}\equiv\begin{pmatrix}1\\1\end{pmatrix}", 30)
    l2 = tx(r"B\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}", 30)
    lres = mixed("$v_a+v_b$", "：非零的平凡線", font_size=22, color=POS_COLOR)
    lcol = VGroup(l1, l2, lres).arrange(DOWN, buff=0.22).move_to(np.array([-3.4, -1.3, 0]))
    assert_in_frame(lcol)
    assert_apart(lcol, lm)
    scene.play(FadeIn(l1))
    scene.play(FadeIn(l2))
    scene.say("$(1,1)$", " 被 ", "$A$", "、", "$B$", " 都固定（模 3 時 ", "$-2\\equiv1$", "）", wait=2.3)
    scene.play(FadeIn(lres))
    scene.play(FadeIn(VGroup(rt, rm)))
    scene.say("$\\widetilde S$", " 這邊：", "$\\widetilde B=B$", "，但 ", "$\\widetilde A$", " 不同", wait=2.3)
    r1 = tx(r"\widetilde Bv=v\ \Rightarrow\ v=(x,x)", 30)
    r2 = tx(r"\widetilde A(x,x)=(0,-x)", 30)
    r3 = tx(r"(0,-x)=(x,x)\ \Rightarrow\ x=0", 30)
    rres = zh("沒有非零的平凡線", font_size=22, color=NEG_COLOR)
    rcol = VGroup(r1, r2, r3, rres).arrange(DOWN, buff=0.2).move_to(np.array([3.4, -1.35, 0]))
    assert_in_frame(rcol)
    assert_apart(rcol, rm)
    scene.play(FadeIn(r1))
    scene.say("要被 ", "$\\widetilde B$", " 固定，向量必須是 ", "$(x,x)$", wait=2.3)
    scene.play(FadeIn(r2), FadeIn(r3))
    scene.say("再被 ", "$\\widetilde A$", " 固定，只剩 ", "$x=0$", wait=2.3)
    scene.play(FadeIn(rres))
    scene.say("模 3 時一個有平凡線、一個沒有 ", "$\\Rightarrow$", " 不同構", wait=2.8)
    scene.clear_stage()

    al = VGroup(tx(r"\alpha=", 36), MatrixMob(m["alpha_on_tildeS"], 34, 0.7, 0.5)).arrange(RIGHT, buff=0.12)
    be = VGroup(tx(r"\beta=", 36), MatrixMob(m["beta_on_S"], 34, 0.7, 0.5)).arrange(RIGHT, buff=0.12)
    mats = VGroup(al, be).arrange(RIGHT, buff=1.0).move_to(np.array([0, 1.6, 0]))
    facts = tx(r"\alpha\beta=3I,\qquad \det\alpha=3", 40, OP_COLOR).move_to(np.array([0, 0.1, 0]))
    concl = VGroup(mixed("在 ", r"$\mathbb C$", " 上：", r"$\alpha/3$", " 可逆，兩個構造同構", font_size=24),
                   mixed("在 ", r"$\mathbb Z$", " 上：若同構，模 3 也同構——矛盾", font_size=24, color=NEG_COLOR)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([0, -1.6, 0]))
    assert_in_frame(mats, facts, concl)
    scene.play(FadeIn(mats))
    scene.say("$\\alpha:\\widetilde S\\to S$", " 與 ", "$\\beta:S\\to\\widetilde S$", " 的矩陣", wait=2.3)
    scene.play(Write(facts))
    scene.say("兩個方向接起來是 3 倍：又是那個 3", wait=2.8)
    scene.say("$\\det\\alpha=3$", "：在 ", "$\\mathbb Z$", " 上不可逆，模 3 時行列式變成 0", wait=2.5)
    scene.play(FadeIn(concl[0]))
    scene.play(FadeIn(concl[1]))
    scene.say("同一個公式，換了係數就有不同的命運", wait=3.3)


class SceneF40SymmetrizerMod3(ChuScene):
    def construct(self):
        self.show_header("F40　Young 對稱化子、多項式模型、模 3")
        check_math()
        part_square(self)
        self.clear_stage()
        part_normalize(self)
        self.clear_stage()
        part_poly(self)
        self.clear_stage()
        part_mod3(self)
        self.wait(1.0)
