"""
Scene M14 —— 鉤上漫步：鉤長公式的機率證明（MIT 18.212 L4，Greene–Nijenhuis–Wilf）

    1. 鉤上漫步：均勻選起點（1/n），每步跳到鉤上的其他格（1/(h-1)），停在角落
    2. 主張 P(c) = (1/n) H(λ)/H(λ-c)；ΣP(c)=1 正是 M13 的化約 -> 鉤長公式（對 n 歸納）
    3. 一條漫步的機率；投影成列集合 A、行集合 B
    4. 關鍵恆等式 h(a,b)-1 = (h(a,β)-1)+(h(α,b)-1)；引理（對 |A|+|B| 歸納）
    5. 對起點與 A、B 加總 -> (1/n)∏h/(h-1) = (1/n)H(λ)/H(λ-c)；數值驗算 (3,2)

所有數字由 utils/counting.py 算出並 assert（格子 0 起算，畫面上 +1）。
輔助函式都是模組層級（連續播放會用別的場景物件呼叫 construct）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM14_hook_walk.py SceneM14HookWalk
"""
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import (corner_prob_formula, corner_prob_product, corners, hook_cells, hook_identity,
                            hook_lemma_rhs, hook_length, hook_lengths, hook_product, hook_walk_probs,
                            hook_walks, remove_corner, syt_count, walk_rows_cols, young_cells)
from utils.mit_draw import CORNER_COLOR, HOOK_COLOR, YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

LAM = (4, 3, 1)                       # 接 M13 的例子，n = 8
N = sum(LAM)
C = (1, 2)                            # 角落 c = (α, β)（0 起算；畫面上是 (2,3)）
WALK_R = ((0, 0), (0, 2), (1, 2))     # 示範漫步：先往右
WALK_D = ((0, 0), (1, 0), (1, 2))     # 投影相同（A、B 一樣）：先往下
SMALL = (3, 2)                        # 最後的數值驗算

WALK_COLOR = ORANGE
ROW_COLOR = TEAL                      # 列集合 A；c 上方的格子（x_i）
COL_COLOR = PINK                      # 行集合 B；c 左方的格子（y_j）
X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


# =============================================================================
# 小工具（模組層級）
# =============================================================================
def ftex(x) -> str:
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else rf"\frac{{{x.numerator}}}{{{x.denominator}}}"


def one(c) -> str:
    """0 起算的格子 -> 畫面上的 (列,行)。"""
    return f"({c[0] + 1},{c[1] + 1})"


def lam_tex(lam) -> str:
    return "(" + ",".join(str(r) for r in lam) + ")"


def inside(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, ("x out", m.get_left(), m.get_right())
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, ("y out", m.get_bottom(), m.get_top())


def apart(*mobs, gap=0.04):
    """外框兩兩不重疊。"""
    for k, a in enumerate(mobs):
        for b in mobs[k + 1:]:
            ok = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
                  or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
            assert ok, ("overlap", a.get_center(), b.get_center())


def at_left(mob, x, y):
    """左緣放在 x、垂直置中於 y。"""
    mob.move_to(np.array([x + mob.get_width() / 2, y, 0.0]))
    return mob


def frame_box(mob, color=YELLOW, buff=0.18):
    return SurroundingRectangle(mob, buff=buff, color=color, stroke_width=3)


def young(lam, cs, top_left=None, center=ORIGIN, hooks=True, font_size=None, color=WHITE):
    if top_left is not None:
        top_left = np.array([top_left[0], top_left[1], 0.0])
    yd = YoungDiagramMob(lam, cell_size=cs, top_left=top_left, center=center)
    if hooks:
        yd.set_entries(hook_lengths(lam), font_size=font_size, color=color)
    return yd


def marker(yd, c, color=WALK_COLOR, width=6):
    sq = Square(side_length=yd.cell_size * 0.84, stroke_color=color, stroke_width=width)
    sq.set_fill(color, opacity=0)
    return sq.move_to(yd.cell_center(*c)).set_z_index(2)


def fills(yd, cells, color, opacity=0.45):
    out = VGroup()
    for c in cells:
        sq = Square(side_length=yd.cell_size * 0.86, stroke_width=0).set_fill(color, opacity=opacity)
        out.add(sq.move_to(yd.cell_center(*c)))
    return out


def jump_arrow(yd, p, q, color=WALK_COLOR, thickness=3.5):
    """同列往右：在格子上半部向上拱；同行往下：在格子左半部向左拱（不壓到中間的數字）。"""
    cs = yd.cell_size
    if p[0] == q[0]:
        off, arc = 0.26 * cs * UP, -PI / 3
    else:
        off, arc = 0.26 * cs * LEFT, PI / 3
    arr = Arrow(yd.cell_center(*p) + off, yd.cell_center(*q) + off, buff=0.04, path_arc=arc,
                thickness=thickness, fill_color=color)
    return arr.set_z_index(3)


def walk_arrows(yd, walk, color=WALK_COLOR, thickness=3.5):
    return VGroup(*[jump_arrow(yd, p, q, color, thickness) for p, q in zip(walk, walk[1:])])


def walk_weight(lam, walk) -> Fraction:
    """∏ 1/(h(a_k)-1)（不含選起點的 1/n），並確認它是 counting.hook_walks 裡的一條。"""
    w = Fraction(1)
    for c in walk[:-1]:
        w /= hook_length(lam, *c) - 1
    assert (tuple(walk), w) in hook_walks(lam, walk[0])
    return w


def axis_labels(yd, font_size=26):
    """列號（左邊）與行號（上面），1 起算。"""
    lam = yd.lam
    rows = VGroup(*[Tex(str(i + 1), font_size=font_size, fill_color=GREY_B).next_to(yd.cell(i, 0), LEFT, buff=0.14)
                    for i in range(len(lam))])
    cols = VGroup(*[Tex(str(j + 1), font_size=font_size, fill_color=GREY_B).next_to(yd.cell(0, j), UP, buff=0.1)
                    for j in range(lam[0])])
    return rows, cols


def arm_leg(lam, c):
    hc = hook_cells(lam, *c)[1:]
    arm = sum(1 for (i, _) in hc if i == c[0])
    return arm, len(hc) - arm


def corner_labels(yd, cells, values, font_size=26, buff=0.14):
    """角落右邊的機率標籤；確認標籤完全落在該列的高度內（不碰到上一列的格子）。"""
    labs = VGroup()
    for c, v in zip(cells, values):
        lab = Tex(ftex(v), font_size=font_size, fill_color=CORNER_COLOR).next_to(yd.cell(*c), RIGHT, buff=buff)
        cell = yd.cell(*c)
        assert lab.get_top()[1] <= cell.get_top()[1] - 0.06 and lab.get_bottom()[1] >= cell.get_bottom()[1] + 0.06
        labs.add(lab)
    return labs


def say_clear(scene, mobs, *parts):
    """字幕含分式會變高：先量字幕的上緣，確認畫面上的物件都在它上方，再顯示。"""
    cap = scene.make_caption(*parts)
    for m in mobs:
        assert m.get_bottom()[1] >= cap.get_top()[1] + 0.08, ("caption overlap", m.get_bottom(), cap.get_top())
    return scene.say(*parts)


def show_walk(scene, g):
    yd, rl, cl, arrs, mks, prob, proj = g
    scene.play(FadeIn(yd), FadeIn(rl), FadeIn(cl), FadeIn(mks[0]), run_time=0.7)
    for arr in arrs:
        scene.play(GrowArrow(arr), run_time=0.6)
    scene.play(FadeIn(mks[1]), FadeIn(prob, shift=0.15 * UP), run_time=0.7)


def project_walk(scene, g, A, B):
    yd, rl, cl, arrs, mks, prob, proj = g
    anims = [rl[i].animate.set_fill(ROW_COLOR).scale(1.35) for i in A]
    anims += [cl[j].animate.set_fill(COL_COLOR).scale(1.35) for j in B]
    scene.play(*anims, FadeIn(proj, shift=0.15 * UP), run_time=0.8)


# =============================================================================
# 1. 鉤上漫步
# =============================================================================
def part1_walk(scene):
    hl = hook_lengths(LAM)
    assert hl == [(6, 4, 3, 1), (4, 2, 1), (1,)] and N == 8
    assert corners(LAM) == [(0, 3), (1, 2), (2, 0)] and C in corners(LAM)
    hs = [hook_length(LAM, *c) for c in WALK_R]
    assert hs == [6, 3, 1]
    assert WALK_R[1] in hook_cells(LAM, *WALK_R[0]) and WALK_R[2] in hook_cells(LAM, *WALK_R[1])
    w = walk_weight(LAM, WALK_R)
    prob = w / N
    assert w == Fraction(1, 10) and prob == Fraction(1, 80)

    cs = 0.85
    yd = young(LAM, cs, top_left=(-6.3, 2.0), font_size=34, color=GREY_A)
    scene.say("鉤上漫步：在 Young 圖上隨機往右、往下跳，直到停住")
    scene.play(ShowCreation(yd.cells, lag_ratio=0.15), run_time=1.0)
    scene.say("每格先寫上它的鉤長 ", "$h$", "（M13：自己＋右邊＋下面的格數）")
    scene.play(FadeIn(yd.entries, lag_ratio=0.1), run_time=0.8)
    scene.wait(1.0)

    x0, fs = -1.9, 28
    lines = [
        mixed("① 起點：", f"$n={N}$", " 格中均勻選一格，機率 ", f"$\\frac{{1}}{{{N}}}$", font_size=fs),
        mixed("② ", f"$h={hs[0]}$", "：跳到鉤上其他 ", f"${hs[0] - 1}$", " 格之一，各 ",
              f"$\\frac{{1}}{{{hs[0] - 1}}}$", font_size=fs),
        mixed("③ ", f"$h={hs[1]}$", "：跳到其他 ", f"${hs[1] - 1}$", " 格之一，各 ",
              f"$\\frac{{1}}{{{hs[1] - 1}}}$", font_size=fs),
        mixed("④ ", f"$h={hs[2]}$", "：鉤上只剩自己，停在角落", font_size=fs),
    ]
    for k, ln in enumerate(lines):
        at_left(ln, x0, 1.75 - 0.8 * k)

    # ① 起點
    mk = marker(yd, WALK_R[0])
    scene.say("從 ", f"$n={N}$", " 格中均勻隨機選一格當起點，每格機率 ", f"$\\frac{{1}}{{{N}}}$")
    scene.play(FadeIn(mk, scale=1.4), FadeIn(lines[0], shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(1.2)

    # ② 鉤上跳
    hk = yd.hook_highlight(*WALK_R[0], cell_color=WALK_COLOR, cell_opacity=0.3)
    scene.say("每一步：跳到目前格子鉤上的其他格，每格機率 ", "$\\frac{1}{h-1}$")
    scene.play(FadeIn(hk), FadeIn(lines[1], shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(1.5)
    arrows = walk_arrows(yd, WALK_R)
    scene.say("這次跳到 ", f"${one(WALK_R[1])}$", "（第 1 列第 3 行）")
    scene.play(GrowArrow(arrows[0]), mk.animate.move_to(yd.cell_center(*WALK_R[1])), FadeOut(hk), run_time=0.9)
    scene.wait(0.8)

    # ③
    hk2 = yd.hook_highlight(*WALK_R[1], cell_color=WALK_COLOR, cell_opacity=0.3)
    scene.say("在 ", f"${one(WALK_R[1])}$", "：鉤長 ", f"${hs[1]}$", "，往右或往下各 ",
              f"$\\frac{{1}}{{{hs[1] - 1}}}$")
    scene.play(FadeIn(hk2), FadeIn(lines[2], shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(1.2)
    scene.play(GrowArrow(arrows[1]), mk.animate.move_to(yd.cell_center(*WALK_R[2])), FadeOut(hk2), run_time=0.9)

    # ④ 停
    stop = fills(yd, [WALK_R[2]], CORNER_COLOR, 0.55)
    scene.say("到了 ", f"${one(WALK_R[2])}$", "：鉤長 1，鉤上沒有別的格，漫步停止")
    scene.play(FadeIn(stop), FadeIn(lines[3], shift=0.2 * RIGHT), run_time=0.8)
    scene.wait(1.0)

    res = mixed("這條漫步的機率 ", f"$=\\frac{{1}}{{{N}}}\\cdot\\frac{{1}}{{{hs[0] - 1}}}\\cdot"
                f"\\frac{{1}}{{{hs[1] - 1}}}={ftex(prob)}$", font_size=30)
    at_left(res, x0 + 0.2, -1.55)
    res_box = frame_box(res)
    scene.say("把每一步的機率乘起來")
    scene.play(FadeIn(res), ShowCreation(res_box), run_time=0.9)
    scene.wait(1.5)

    others = [c for c in corners(LAM) if c != WALK_R[2]]
    more = fills(yd, others, CORNER_COLOR, 0.55)
    legend = zh("綠色：角落（鉤長 1）", font_size=24, color=CORNER_COLOR)
    legend.next_to(yd.cells, DOWN, buff=0.3).align_to(yd.cells, LEFT)
    inside(yd, *lines, res_box, legend)
    apart(VGroup(yd, legend), *lines, res_box)
    scene.say("鉤長 1 的格子就是角落；只往右、往下跳，一定會停在某個角落")
    scene.play(FadeIn(more), FadeIn(legend), run_time=0.8)
    scene.wait(2.5)
    scene.clear_stage()


# =============================================================================
# 2. 主張與化約
# =============================================================================
def part2_claim(scene):
    H = hook_product(LAM)
    assert H == 576
    cs_ = corners(LAM)
    data = []
    for c in cs_:
        sub = remove_corner(LAM, c)
        hsub = hook_product(sub)
        p = corner_prob_formula(LAM, c)
        assert p == Fraction(H, N * hsub) == hook_walk_probs(LAM)[c]
        data.append((c, sub, hsub, p))
    assert [(d[1], d[2], d[3]) for d in data] == [((3, 3, 1), 240, Fraction(3, 10)), ((4, 2, 1), 144, Fraction(1, 2)),
                                                  ((4, 3), 360, Fraction(1, 5))]
    assert sum(d[3] for d in data) == 1

    claim = mixed("主張：停在角落 ", "$c$", " 的機率 ", "$P(c)=\\frac{1}{n}\\cdot\\frac{H(\\lambda)}{H(\\lambda-c)}$",
                  "，其中 ", "$H(\\lambda)=\\prod_{x\\in\\lambda}h(x)$", font_size=28)
    claim.move_to(np.array([0.3, 2.55, 0.0]))
    scene.say("主張：停在每個角落的機率，可以用鉤長的乘積寫出來")
    scene.play(FadeIn(claim, shift=0.2 * DOWN), run_time=0.9)
    scene.wait(1.5)

    yd = young(LAM, 0.85, top_left=(-6.3, 1.65), font_size=32, color=GREY_A)
    cf = fills(yd, cs_, CORNER_COLOR, 0.55)
    plabs = corner_labels(yd, [d[0] for d in data], [d[3] for d in data], font_size=30)
    lam_lab = Tex(f"\\lambda={lam_tex(LAM)},\\ n={N}", font_size=32).next_to(yd.cells, DOWN, buff=0.3)
    lam_lab.align_to(yd.cells, LEFT)
    rows = VGroup()
    for k, (c, sub, hsub, p) in enumerate(data):
        t = Tex(rf"P{one(c)}=\frac{{1}}{{{N}}}\cdot\frac{{H{lam_tex(LAM)}}}{{H{lam_tex(sub)}}}"
                rf"=\frac{{{H}}}{{{N}\cdot {hsub}}}={ftex(p)}", font_size=32)
        rows.add(at_left(t, -1.9, 1.15 - 0.95 * k))
    total = Tex("+".join(ftex(d[3]) for d in data) + "=1", font_size=36, fill_color=YELLOW)
    at_left(total, -1.9, -1.75)
    inside(claim, yd, plabs, lam_lab, rows, total)
    apart(claim, VGroup(yd, plabs, lam_lab), *rows, total)

    scene.say("例 ", f"$\\lambda={lam_tex(LAM)}$", "：三個角落（綠色），用公式算出三個機率")
    scene.play(FadeIn(yd), FadeIn(cf), FadeIn(lam_lab), run_time=0.8)
    for t, pl in zip(rows, plabs):
        scene.play(FadeIn(t, shift=0.2 * RIGHT), FadeIn(pl), run_time=0.8)
        scene.wait(1.0)
    scene.say("漫步一定停在某個角落，所以這些機率加起來必須是 1")
    scene.play(Write(total), run_time=0.9)
    scene.wait(2.0)

    # ---- 一般情形：ΣP(c)=1 就是 M13 的化約
    scene.play(FadeOut(VGroup(yd, cf, plabs, lam_lab, rows, total)), run_time=0.6)
    g1 = Tex(r"\sum_{c}\frac{1}{n}\cdot\frac{H(\lambda)}{H(\lambda-c)}=1", font_size=40)
    g1_note = zh("＝ M13 最後的化約", font_size=26, color=MUTED_COLOR)
    VGroup(g1, g1_note).arrange(RIGHT, buff=0.5).move_to(np.array([0, 1.25, 0.0]))
    g1_box = frame_box(g1)
    g2 = mixed("兩邊乘 ", "$\\frac{n!}{H(\\lambda)}$", "：", "$\\sum_{c}\\frac{(n-1)!}{H(\\lambda-c)}=\\frac{n!}{H(\\lambda)}$",
               font_size=28)
    g3 = mixed("歸納假設 ", "$f^{\\lambda-c}=\\frac{(n-1)!}{H(\\lambda-c)}$", "，角落遞迴 ",
               "$f^{\\lambda}=\\sum_{c}f^{\\lambda-c}$", font_size=28)
    g4 = mixed("$\\Longrightarrow$", "$f^{\\lambda}=\\frac{n!}{H(\\lambda)}$", "（鉤長公式）", font_size=30)
    g2.move_to(np.array([0, 0.0, 0.0]))
    g3.move_to(np.array([0, -1.05, 0.0]))
    g4.move_to(np.array([0, -2.2, 0.0]))
    g4_box = frame_box(g4, color=CORNER_COLOR)
    inside(claim, g1_box, g1_note, g2, g3, g4_box)
    apart(claim, VGroup(g1_box, g1_note), g2, g3, g4_box)
    scene.say("對所有角落加總：正是 M13 最後要證的式子")
    scene.play(FadeIn(g1), ShowCreation(g1_box), FadeIn(g1_note), run_time=0.9)
    scene.wait(1.5)
    scene.say("兩邊乘 ", "$\\frac{n!}{H(\\lambda)}$", "，再用歸納假設（", "$n-1$", " 格的圖已成立）與角落遞迴")
    scene.play(FadeIn(g2, shift=0.2 * DOWN), run_time=0.8)
    scene.wait(1.5)
    scene.play(FadeIn(g3, shift=0.2 * DOWN), run_time=0.8)
    scene.wait(1.8)
    say_clear(scene, [g4_box], "所以只要證明主張，鉤長公式就對 ", "$n$", " 歸納成立")
    scene.play(FadeIn(g4), ShowCreation(g4_box), run_time=0.9)
    scene.wait(2.5)
    scene.clear_stage()


# =============================================================================
# 3. 一條漫步的機率與投影
# =============================================================================
def part3_projection(scene):
    wr, wd = walk_weight(LAM, WALK_R), walk_weight(LAM, WALK_D)
    pr, pd = wr / N, wd / N
    assert (wr, wd, pr, pd) == (Fraction(1, 10), Fraction(1, 15), Fraction(1, 80), Fraction(1, 120))
    A, B = walk_rows_cols(WALK_R)
    assert (A, B) == walk_rows_cols(WALK_D) == ((0, 1), (0, 2))
    assert WALK_R[0] == WALK_D[0] == (min(A), min(B)) and WALK_R[-1] == WALK_D[-1] == C == (max(A), max(B))

    top = mixed("一條漫步 ", "$a_1\\to a_2\\to\\cdots\\to a_m$", " 的機率 ",
                "$=\\frac{1}{n}\\prod_{k<m}\\frac{1}{h(a_k)-1}$", font_size=28)
    top.move_to(np.array([0.2, 2.6, 0.0]))
    scene.say("一條漫步的機率：選起點的 ", "$\\frac{1}{n}$", "，乘上每一跳的 ", "$\\frac{1}{h-1}$")
    scene.play(FadeIn(top, shift=0.2 * DOWN), run_time=0.9)
    scene.wait(1.2)

    cs = 0.75
    groups = []
    a_tex = "A=\\{" + ",".join(str(i + 1) for i in A) + "\\}"
    b_tex = "B=\\{" + ",".join(str(j + 1) for j in B) + "\\}"
    for walk, w, x_left in ((WALK_R, wr, -5.3), (WALK_D, wd, 1.3)):
        yd = young(LAM, cs, top_left=(x_left, 1.45), font_size=30, color=GREY_A)
        rl, cl = axis_labels(yd)
        arrs = walk_arrows(yd, walk)
        mks = VGroup(marker(yd, walk[0]), fills(yd, [walk[-1]], CORNER_COLOR, 0.55))
        hs = [hook_length(LAM, *c) for c in walk[:-1]]
        prob = Tex(rf"\frac{{1}}{{{N}}}" + "".join(rf"\cdot\frac{{1}}{{{h - 1}}}" for h in hs) + f"={ftex(w / N)}",
                   font_size=34)
        prob.next_to(yd.cells, DOWN, buff=0.4)
        proj = VGroup(Tex(a_tex, font_size=34, fill_color=ROW_COLOR), Tex(b_tex, font_size=34, fill_color=COL_COLOR))
        proj.arrange(RIGHT, buff=0.6).next_to(prob, DOWN, buff=0.35)
        groups.append((yd, rl, cl, arrs, mks, prob, proj))
    for g in groups:
        inside(*g)
    inside(top)
    apart(top, VGroup(*groups[0][:5]), groups[0][5], groups[0][6])
    apart(VGroup(*groups[0]), VGroup(*groups[1]))

    scene.say("例：示範的那條漫步，機率 ", f"${ftex(pr)}$")
    show_walk(scene, groups[0])
    scene.wait(1.0)
    scene.say("投影：經過的列組成集合 ", "$A$", "，經過的行組成集合 ", "$B$")
    project_walk(scene, groups[0], A, B)
    scene.wait(1.5)
    scene.say("另一條漫步：先往下，投影也是同一組 ", "$A$", "、", "$B$")
    show_walk(scene, groups[1])
    project_walk(scene, groups[1], A, B)
    scene.wait(1.5)
    scene.say("起點一定是 ", "$(\\min A,\\min B)$", "，終點 ", "$c=(\\max A,\\max B)$", "；同一組 ", "$A,B$",
              " 的漫步放在一起加總")
    scene.wait(3.0)
    scene.clear_stage()


# =============================================================================
# 4. 關鍵恆等式與引理
# =============================================================================
def part4_lemma(scene):
    ab = (0, 0)
    al, be = C
    a_beta, alpha_b = (ab[0], be), (al, ab[1])
    vals = hook_identity(LAM, ab, C)
    assert vals == (5, 2, 3)
    assert len(hook_cells(LAM, *ab)) - 1 == 5 and len(hook_cells(LAM, *a_beta)) - 1 == 2
    assert len(hook_cells(LAM, *alpha_b)) - 1 == 3
    arm_ab, leg_ab = arm_leg(LAM, ab)
    arm_aB, leg_aB = arm_leg(LAM, a_beta)
    arm_Ab, leg_Ab = arm_leg(LAM, alpha_b)
    assert arm_ab == (be - ab[1]) + arm_aB and leg_ab == (al - ab[0]) + leg_Ab
    assert be - ab[1] == arm_Ab and al - ab[0] == leg_aB

    head = mixed("關鍵恆等式：", "$c=(\\alpha,\\beta)$", " 是角落，", "$(a,b)$", " 在它的左上方", font_size=28)
    head.move_to(np.array([0.3, 2.8, 0.0]))
    cs = 0.55
    specs = [(ab, HOOK_COLOR, "h(a,b)-1"), (a_beta, ROW_COLOR, "h(a,\\beta)-1"), (alpha_b, COL_COLOR, "h(\\alpha,b)-1")]
    panels = VGroup()
    for (cell, col, lab), x in zip(specs, (-4.4, 0.0, 4.4)):
        yd = young(LAM, cs, center=np.array([x, 0.85, 0.0]), hooks=False)
        hk = fills(yd, hook_cells(LAM, *cell)[1:], col, 0.6)
        base = marker(yd, cell, WALK_COLOR, 5)
        cor = marker(yd, C, CORNER_COLOR, 5)
        title = Tex(lab, font_size=36, fill_color=col).next_to(yd.cells, UP, buff=0.3)
        num = Tex(str(len(hook_cells(LAM, *cell)) - 1), font_size=52, fill_color=col).next_to(yd.cells, DOWN, buff=0.3)
        panels.add(VGroup(yd, hk, base, cor, title, num))
    signs = VGroup(Tex("=", font_size=60), Tex("+", font_size=60))
    signs[0].move_to(np.array([-2.2, 0.85, 0.0]))
    signs[1].move_to(np.array([2.2, 0.85, 0.0]))
    ident = Tex(r"h(a,b)-1=\big(h(a,\beta)-1\big)+\big(h(\alpha,b)-1\big)", font_size=38)
    ident.move_to(np.array([0, -1.2, 0.0]))
    ident_box = frame_box(ident)
    e1 = mixed("$(a,b)$", " 的臂 ", "$=(\\beta-b)+\\mathrm{arm}(a,\\beta)$", "，腿 ",
               "$=(\\alpha-a)+\\mathrm{leg}(\\alpha,b)$", font_size=24, color=GREY_A)
    e2 = mixed("因為 ", "$c$", " 是角落：", "$\\beta-b=\\mathrm{arm}(\\alpha,b)$", "，",
               "$\\alpha-a=\\mathrm{leg}(a,\\beta)$", font_size=24, color=GREY_A)
    e1.move_to(np.array([0, -2.05, 0.0]))
    e2.move_to(np.array([0, -2.65, 0.0]))
    inside(head, panels, signs, ident_box, e1, e2)
    apart(head, *[VGroup(p[0], p[4], p[5]) for p in panels])
    apart(VGroup(panels, signs), ident_box, e1, e2)

    scene.say("證明的關鍵：一個鉤長的恆等式（例 ", f"$(a,b)={one(ab)}$", "、", f"$c={one(C)}$", "）")
    scene.play(FadeIn(head, shift=0.2 * DOWN), run_time=0.8)
    for k, p in enumerate(panels):
        if k:
            scene.play(FadeIn(signs[k - 1]), run_time=0.3)
        scene.play(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[3]), FadeIn(p[4]), run_time=0.6)
        scene.play(FadeIn(p[1], lag_ratio=0.15), FadeIn(p[5]), run_time=0.7)
        scene.wait(0.6)
    scene.say("數一數鉤上「自己以外」的格子：", f"${vals[0]}={vals[1]}+{vals[2]}$")
    scene.wait(1.5)
    scene.play(FadeIn(ident), ShowCreation(ident_box), run_time=0.9)
    scene.say("原因：", "$(a,b)$", " 的臂和腿各切成兩段，長度剛好對上")
    scene.play(FadeIn(e1, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.5)
    scene.play(FadeIn(e2, shift=0.15 * UP), run_time=0.7)
    scene.wait(2.5)
    scene.clear_stage()

    # ---- 引理
    A, B = walk_rows_cols(WALK_R)
    rhs = hook_lemma_rhs(LAM, C, A, B)
    group = [(p, w) for s in young_cells(LAM) for p, w in hook_walks(LAM, s)
             if p[-1] == C and walk_rows_cols(p) == (A, B)]
    assert sorted(p for p, _ in group) == sorted([WALK_R, WALK_D])
    wr, wd = walk_weight(LAM, WALK_R), walk_weight(LAM, WALK_D)
    assert wr + wd == sum(w for _, w in group) == rhs == Fraction(1, 6)
    x_fac = hook_length(LAM, A[0], be) - 1          # i ∈ A∖{α} = {0}
    y_fac = hook_length(LAM, al, B[0]) - 1          # j ∈ B∖{β} = {0}
    assert (x_fac, y_fac) == (2, 3) and rhs == Fraction(1, x_fac * y_fac)
    h_ab = hook_length(LAM, *ab) - 1
    down_rest = hook_lemma_rhs(LAM, C, A[1:], B)     # 先往下：剩下從 (1,0) 出發
    right_rest = hook_lemma_rhs(LAM, C, A, B[1:])    # 先往右：剩下從 (0,2) 出發
    assert (h_ab, down_rest, right_rest) == (5, Fraction(1, 3), Fraction(1, 2))
    assert down_rest == rhs * x_fac and right_rest == rhs * y_fac
    assert Fraction(1, h_ab) * (down_rest + right_rest) == rhs

    s1 = mixed("引理：從 ", "$(a,b)$", " 出發、列集合 ", "$A$", "、行集合 ", "$B$", "、停在 ", "$c$",
               " 的所有漫步，權重和", font_size=28)
    s1.move_to(np.array([0.3, 2.92, 0.0]))
    s2 = mixed("$R=\\prod_{i\\in A\\setminus\\{\\alpha\\}}\\frac{1}{h(i,\\beta)-1}"
               "\\prod_{j\\in B\\setminus\\{\\beta\\}}\\frac{1}{h(\\alpha,j)-1}$",
               "（權重不含選起點的 ", "$\\frac{1}{n}$", "）", font_size=28)
    s2[1:].shift(0.3 * RIGHT)
    s2.move_to(np.array([0.0, 1.82, 0.0]))
    s2_box = frame_box(s2[0])
    apart(s2_box, s2[1:])
    cs2 = 0.55
    minis = VGroup()
    for walk, w, x in ((WALK_R, wr, -4.9), (WALK_D, wd, -2.0)):
        yd = young(LAM, cs2, center=np.array([x, 0.1, 0.0]), hooks=False)
        arrs = walk_arrows(yd, walk, thickness=3)
        mk = VGroup(marker(yd, walk[0], WALK_COLOR, 4), fills(yd, [walk[-1]], CORNER_COLOR, 0.55))
        hs = [hook_length(LAM, *c) for c in walk[:-1]]
        wt = Tex(r"\cdot".join(rf"\frac{{1}}{{{h - 1}}}" for h in hs) + f"={ftex(w)}", font_size=32)
        wt.next_to(yd.cells, DOWN, buff=0.2)
        minis.add(VGroup(yd, arrs, mk, wt))
    a_tex = "A=\\{" + ",".join(str(i + 1) for i in A) + "\\}"
    b_tex = "B=\\{" + ",".join(str(j + 1) for j in B) + "\\}"
    r1 = mixed("例：", f"${a_tex}$", "，", f"${b_tex}$", "，", f"$c={one(C)}$", font_size=26)
    r2 = Tex(f"{ftex(wr)}+{ftex(wd)}={ftex(wr + wd)}", font_size=36)
    r3 = Tex(rf"R=\frac{{1}}{{h{one((A[0], be))}-1}}\cdot\frac{{1}}{{h{one((al, B[0]))}-1}}"
             rf"=\frac{{1}}{{{x_fac}}}\cdot\frac{{1}}{{{y_fac}}}={ftex(rhs)}", font_size=32)
    at_left(r1, 0.0, 0.75)
    at_left(r2, 0.0, -0.05)
    at_left(r3, 0.0, -0.95)
    check = Tex(r"\checkmark", font_size=44, fill_color=CORNER_COLOR).next_to(r3, RIGHT, buff=0.2)
    p1 = mixed("證明（對 ", "$|A|+|B|$", " 歸納）：第一步往下或往右，剩下的部分用歸納假設", font_size=26)
    p1.move_to(np.array([0, -1.95, 0.0]))
    p2 = Tex(r"\frac{R\cdot(h(a,\beta)-1)+R\cdot(h(\alpha,b)-1)}{h(a,b)-1}=R", font_size=34)
    p2n = Tex(rf"\frac{{1}}{{{h_ab}}}\left({ftex(down_rest)}+{ftex(right_rest)}\right)"
              rf"=\frac{{1}}{{{h_ab}}}\cdot{ftex(down_rest + right_rest)}={ftex(rhs)}", font_size=34)
    VGroup(p2, p2n).arrange(RIGHT, buff=1.0).move_to(np.array([0, -2.58, 0.0]))
    inside(s1, s2_box, minis, r1, r2, r3, check, p1, p2, p2n)
    apart(s1, VGroup(s2, s2_box), minis[0], minis[1], VGroup(r1, r2, r3, check))
    apart(VGroup(minis, r1, r2, r3, check), p1, VGroup(p2, p2n))
    apart(r1, r2, r3)

    scene.say("引理：把同一組 ", "$A,B$", " 的漫步權重加起來，會得到一個乘積")
    scene.play(FadeIn(s1, shift=0.2 * DOWN), run_time=0.8)
    scene.play(FadeIn(s2), ShowCreation(s2_box), run_time=0.9)
    scene.wait(2.0)
    scene.say("驗算剛才那兩條漫步：權重和 ", f"${ftex(wr + wd)}$")
    scene.play(FadeIn(minis[0]), FadeIn(minis[1]), FadeIn(r1), run_time=0.9)
    scene.play(FadeIn(r2, shift=0.15 * RIGHT), run_time=0.7)
    scene.wait(1.0)
    scene.say("右邊的乘積也是 ", f"${ftex(rhs)}$")
    scene.play(FadeIn(r3, shift=0.15 * RIGHT), run_time=0.8)
    scene.play(FadeIn(check, scale=1.5), run_time=0.4)
    scene.wait(1.5)
    say_clear(scene, [p2, p2n], "第一步往下或往右：剩下的權重和分別是 ", "$R\\cdot(h(a,\\beta)-1)$", " 與 ",
              "$R\\cdot(h(\\alpha,b)-1)$")
    scene.play(FadeIn(p1), run_time=0.6)
    scene.play(FadeIn(p2), run_time=0.8)
    scene.wait(2.0)
    say_clear(scene, [p2, p2n], "分子用關鍵恆等式就等於分母：", f"${h_ab}={x_fac}+{y_fac}$", "，所以總和正好是 ", "$R$")
    scene.play(FadeIn(p2n, shift=0.15 * LEFT), run_time=0.8)
    scene.wait(3.0)
    scene.clear_stage()


# =============================================================================
# 5. 加總與結論
# =============================================================================
def part5_conclusion(scene):
    al, be = C
    up_cells = [(i, be) for i in range(al)]          # c 上方：x_i
    left_cells = [(al, j) for j in range(be)]        # c 左方：y_j
    xs = [Fraction(1, hook_length(LAM, *c) - 1) for c in up_cells]
    ys = [Fraction(1, hook_length(LAM, *c) - 1) for c in left_cells]
    assert xs == [Fraction(1, 2)] and ys == [Fraction(1, 3), Fraction(1, 1)]
    prod = Fraction(1, N)
    for v in xs + ys:
        prod *= 1 + v
    assert prod == corner_prob_product(LAM, C) == corner_prob_formula(LAM, C) == hook_walk_probs(LAM)[C] == Fraction(1, 2)
    # 依 (A, B) 分組：每一組的權重和 = 引理的 R；共 2^(α+β) 組，總和 = 乘積
    groups = {}
    for s in young_cells(LAM):
        for p, w in hook_walks(LAM, s):
            if p[-1] == C:
                key = walk_rows_cols(p)
                groups[key] = groups.get(key, 0) + w
    assert len(groups) == 2 ** (al + be) == 8
    assert all(v == hook_lemma_rhs(LAM, C, *k) for k, v in groups.items())
    assert sum(groups.values()) / N == prod

    t1 = mixed("對所有起點與 ", "$A,B$", " 加總：", "$A$", " 一定含 ", "$\\alpha$", "，每個 ", "$i<\\alpha$",
               " 可選可不選；", "$B$", " 也一樣", font_size=26)
    t1.move_to(np.array([0.3, 2.8, 0.0]))
    t2 = Tex(r"P(c)=\frac{1}{n}\sum_{A,B}\prod_{i\in A\setminus\{\alpha\}}x_i\prod_{j\in B\setminus\{\beta\}}y_j"
             r"=\frac{1}{n}\prod_{i<\alpha}(1+x_i)\prod_{j<\beta}(1+y_j)", font_size=34)
    t2.move_to(np.array([0, 1.85, 0.0]))
    t3 = mixed("$x_i=\\frac{1}{h(i,\\beta)-1}$", "（", "$c$", " 上方的格）", "$y_j=\\frac{1}{h(\\alpha,j)-1}$", "（", "$c$",
               " 左方的格）", font_size=26)
    t3[4:].shift(0.5 * RIGHT)
    t3[0].set_fill(ROW_COLOR)
    t3[4].set_fill(COL_COLOR)
    t3.move_to(np.array([0, 0.85, 0.0]))
    t4 = mixed("$1+\\frac{1}{h-1}=\\frac{h}{h-1}$", "$\\Longrightarrow$",
               "$P(c)=\\frac{1}{n}\\prod_{x}\\frac{h(x)}{h(x)-1}$", "（", "$x$", " 跑過 ", "$c$", " 上方與左方的格子）",
               font_size=26)
    t4.move_to(np.array([0, -0.2, 0.0]))
    yd = young(LAM, 0.42, center=np.array([-5.95, -1.95, 0.0]), font_size=22, color=GREY_A)
    ex_fill = VGroup(fills(yd, up_cells, ROW_COLOR, 0.6), fills(yd, left_cells, COL_COLOR, 0.6),
                     fills(yd, [C], CORNER_COLOR, 0.6))
    factors = r"".join(rf"\left(1+{ftex(v)}\right)" for v in xs + ys)
    ratios = r"\cdot".join(ftex(1 + v) if (1 + v).denominator != 1 else rf"\frac{{{(1 + v).numerator}}}{{1}}"
                           for v in xs + ys)
    ex = Tex(rf"P{one(C)}=\frac{{1}}{{{N}}}{factors}=\frac{{1}}{{{N}}}\cdot{ratios}={ftex(prod)}", font_size=32)
    at_left(ex, -4.75, -1.95)
    assert ratios == r"\frac{3}{2}\cdot\frac{4}{3}\cdot\frac{2}{1}"
    inside(t1, t2, t3, t4, yd, ex)
    apart(t1, t2, t3, t4, VGroup(yd, ex))
    apart(yd, ex, gap=0.25)

    scene.say("最後把所有起點與 ", "$A,B$", " 加起來：每個引理的乘積再加總")
    scene.play(FadeIn(t1, shift=0.2 * DOWN), run_time=0.8)
    scene.play(FadeIn(t2), run_time=0.9)
    scene.wait(1.5)
    scene.say("每個 ", "$x_i$", " 選或不選，加總就分解成 ", "$(1+x_i)$", " 的乘積")
    scene.play(FadeIn(t3, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.8)
    scene.play(FadeIn(t4, shift=0.15 * UP), run_time=0.8)
    scene.wait(1.5)
    scene.say("例 ", f"$c={one(C)}$", "：展開共 ", f"${len(groups)}$", " 項，每一項就是一組 ", "$A,B$")
    scene.play(FadeIn(yd), FadeIn(ex_fill), run_time=0.7)
    scene.play(FadeIn(ex, shift=0.15 * RIGHT), run_time=0.9)
    scene.wait(2.0)
    term = xs[0] * ys[0]
    assert groups[walk_rows_cols(WALK_R)] == term == Fraction(1, 6)
    say_clear(scene, [VGroup(yd, ex)], "其中 ", f"${ftex(xs[0])}\\cdot{ftex(ys[0])}={ftex(term)}$",
              " 這一項，就是引理驗算過的那一組 ", "$A,B$")
    scene.wait(2.5)
    scene.clear_stage()

    # ---- 拿掉 c 只改變 c 上方與左方的鉤長
    sub = remove_corner(LAM, C)
    assert sub == (4, 2, 1)
    changed = sorted((i, j) for i, j in young_cells(sub) if hook_length(sub, i, j) != hook_length(LAM, i, j))
    assert changed == sorted(up_cells + left_cells)
    assert all(hook_length(LAM, *c) - hook_length(sub, *c) == 1 for c in changed)
    H, Hs = hook_product(LAM), hook_product(sub)
    ratio = Fraction(H, Hs)
    assert (H, Hs, ratio) == (576, 144, 4) and ratio == prod * N
    cs = 0.65
    yl = young(LAM, cs, center=np.array([-3.4, 1.15, 0.0]), font_size=30)
    yr = young(sub, cs, top_left=yl.cells[0].get_corner(UL) + 6.8 * RIGHT, font_size=30)
    fl = VGroup(fills(yl, up_cells, ROW_COLOR, 0.55), fills(yl, left_cells, COL_COLOR, 0.55),
                fills(yl, [C], CORNER_COLOR, 0.55))
    fr = VGroup(fills(yr, up_cells, ROW_COLOR, 0.55), fills(yr, left_cells, COL_COLOR, 0.55))
    ghost = DashedVMobject(Square(side_length=cs, stroke_color=GREY_B, stroke_width=2), num_dashes=16)
    ghost.move_to(yr.cell_center(0, 0) + C[0] * cs * DOWN + C[1] * cs * RIGHT)
    tl = Tex(rf"\lambda={lam_tex(LAM)}", font_size=34).next_to(yl.cells, UP, buff=0.3)
    tr = Tex(rf"\lambda-c={lam_tex(sub)}", font_size=34).next_to(yr.cells, UP, buff=0.3)
    tr.match_y(tl)
    hl_ = Tex(rf"H(\lambda)={H}", font_size=34).next_to(yl.cells, DOWN, buff=0.3)
    hr_ = Tex(rf"H(\lambda-c)={Hs}", font_size=34).next_to(yr.cells, DOWN, buff=0.3)
    hr_.match_y(hl_)
    arr = Arrow(np.array([-1.5, 1.15, 0.0]), np.array([1.5, 1.15, 0.0]), buff=0, thickness=3, fill_color=GREY_B)
    arr_lab = mixed("拿掉 ", "$c$", font_size=26).next_to(arr, UP, buff=0.15)
    ratio_parts = r"\cdot".join(rf"\frac{{{hook_length(LAM, *c)}}}{{{hook_length(sub, *c)}}}"
                                for c in up_cells + left_cells)
    assert ratio_parts == r"\frac{3}{2}\cdot\frac{4}{3}\cdot\frac{2}{1}"
    b1 = Tex(rf"\frac{{H(\lambda)}}{{H(\lambda-c)}}=\frac{{{H}}}{{{Hs}}}={ftex(ratio)}={ratio_parts}", font_size=36)
    b1.move_to(np.array([0, -1.1, 0.0]))
    b2 = mixed(f"$P{one(C)}=\\frac{{1}}{{{N}}}\\cdot {ftex(ratio)}={ftex(prod)}$", "，和列舉所有漫步得到的機率相同",
               font_size=28)
    b2.move_to(np.array([0, -2.2, 0.0]))
    b2_box = frame_box(b2, color=CORNER_COLOR)
    inside(yl, yr, tl, tr, hl_, hr_, arr_lab, b1, b2_box)
    apart(VGroup(yl, tl, hl_), arr, VGroup(yr, tr, hr_, ghost))
    apart(VGroup(yl, tl, hl_, yr, tr, hr_, arr_lab), b1, b2_box)

    scene.say("拿掉角落 ", "$c$", "：只有 ", "$c$", " 上方與左方的格子，鉤長各減 1")
    scene.play(FadeIn(yl), FadeIn(fl), FadeIn(tl), run_time=0.8)
    scene.play(GrowArrow(arr), FadeIn(arr_lab), run_time=0.6)
    scene.play(TransformFromCopy(yl, yr), FadeIn(fr), FadeIn(ghost), FadeIn(tr), run_time=1.2)
    scene.wait(2.0)
    say_clear(scene, [b1, b2_box], "所以 ", "$\\prod\\frac{h}{h-1}$", " 正好是 ", "$\\frac{H(\\lambda)}{H(\\lambda-c)}$",
              "，主張得證")
    scene.play(FadeIn(hl_), FadeIn(hr_), run_time=0.6)
    scene.play(FadeIn(b1, shift=0.15 * UP), run_time=0.9)
    scene.wait(1.8)
    scene.play(FadeIn(b2), ShowCreation(b2_box), run_time=0.9)
    scene.wait(2.5)
    scene.clear_stage()

    # ---- 數值驗算 (3,2) 與結論
    probs = hook_walk_probs(SMALL)
    n_walks = sum(len(hook_walks(SMALL, s)) for s in young_cells(SMALL))
    Hsm = hook_product(SMALL)
    cs_ = corners(SMALL)
    assert cs_ == [(0, 2), (1, 1)] and n_walks == 9 and Hsm == 24
    assert probs == {(0, 2): Fraction(2, 5), (1, 1): Fraction(3, 5)} and sum(probs.values()) == 1
    nsm = sum(SMALL)
    ysm = young(SMALL, 0.9, center=np.array([-4.6, 0.95, 0.0]), font_size=34, color=GREY_A)
    cfill = fills(ysm, cs_, CORNER_COLOR, 0.55)
    plabs = corner_labels(ysm, cs_, [probs[c] for c in cs_], font_size=34)
    tsm = Tex(rf"\lambda={lam_tex(SMALL)}", font_size=34).next_to(ysm.cells, UP, buff=0.3)
    c1 = mixed("列舉全部 ", f"${n_walks}$", " 條漫步（精確分數），再和公式比對：", font_size=26)
    at_left(c1, -1.9, 2.0)
    rows = VGroup()
    for k, c in enumerate(cs_):
        hsub = hook_product(remove_corner(SMALL, c))
        assert corner_prob_formula(SMALL, c) == probs[c] == Fraction(Hsm, nsm * hsub)
        rows.add(at_left(Tex(rf"P{one(c)}=\frac{{1}}{{{nsm}}}\cdot\frac{{{Hsm}}}{{{hsub}}}={ftex(probs[c])}",
                             font_size=34), -1.7, 1.1 - 0.95 * k))
    assert [hook_product(remove_corner(SMALL, c)) for c in cs_] == [12, 8]
    tot = Tex("+".join(ftex(probs[c]) for c in cs_) + "=1", font_size=36, fill_color=YELLOW)
    at_left(tot, -1.7, -0.8)
    fin = mixed("$\\sum_{c}P(c)=1$", "$\\Longrightarrow$", "$f^{\\lambda}=\\frac{n!}{\\prod_{x\\in\\lambda}h(x)}$",
                "鉤長公式得證", font_size=30, buff=0.3)
    fin.move_to(np.array([0, -2.15, 0.0]))
    fin_box = frame_box(fin, buff=0.22)
    assert syt_count(SMALL) == 5 == Fraction(120, Hsm)
    inside(ysm, plabs, tsm, c1, rows, tot, fin_box)
    apart(VGroup(ysm, plabs, tsm), c1, rows, tot)
    apart(c1, *rows, tot, fin_box)

    scene.say("數值驗算：", f"$\\lambda={lam_tex(SMALL)}$", "，列舉所有漫步算出每個角落的機率")
    scene.play(FadeIn(ysm), FadeIn(tsm), FadeIn(c1), run_time=0.8)
    scene.play(FadeIn(cfill), FadeIn(plabs), run_time=0.7)
    for r in rows:
        scene.play(FadeIn(r, shift=0.15 * RIGHT), run_time=0.7)
        scene.wait(0.8)
    scene.say("和公式完全一樣，而且加起來是 1（M13 的 ", "$\\frac{2}{5}+\\frac{3}{5}=1$", "）")
    scene.play(Write(tot), run_time=0.8)
    scene.wait(1.8)
    say_clear(scene, [fin_box, tot], "鉤上漫步一定停在某個角落，所以機率總和是 1，於是得到鉤長公式")
    scene.play(FadeIn(fin), ShowCreation(fin_box), run_time=1.0)
    scene.wait(3.5)


class SceneM14HookWalk(ChuScene):
    def construct(self):
        self.show_header("鉤上漫步：鉤長公式的證明")
        part1_walk(self)
        part2_claim(self)
        part3_projection(self)
        part4_lemma(self)
        part5_conclusion(self)
