"""
Scene F01 —— Young 圖、分割與共軛分割（Fulton《Young Tableaux》Notation，p.1–2）

    Young 圖：一列一列靠左的格子，列長由上往下不增加；列長依序寫下 = n 的分割
    λ = (6,4,4,2) ⊢ 16，|λ| = 16；結尾補 0 視為同一個；重複的數寫成次方 (6 4^2 2)
    共軛 λ̃：沿主對角線翻轉，λ̃ 的列長 = λ 的行長 → (4,4,3,3,1,1)；再翻一次回到 λ
    格子裡放正整數：可重複叫填數（filling），兩兩不同叫編號（numbering）；加上條件就是 Young 表（F02）

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF01_young_diagrams.py SceneF01YoungDiagrams
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    conjugate,
    is_partition,
    is_tableau,
    partitions,
    shape,
    young_boxes,
)

LAM = (6, 4, 4, 2)                         # 書 p.1 的例子
N = 16
PI_DIGITS = str(math.pi).replace(".", "")  # 3141592653589793：剛好 16 位，沒有 0
FILLING = ((3, 1, 4, 1, 5, 9), (2, 6, 5, 3), (5, 8, 9, 7), (9, 3))
NUMBERING = ((7, 12, 3, 16, 1, 9), (14, 5, 11, 2), (8, 15, 4, 13), (10, 6))
REPEAT_VALUE = 5

DIAG_COLOR = GREY_A
COL_COLORS = [BLUE_C, TEAL_C, GREEN_C, YELLOW_C, ORANGE, PINK]   # λ 的第 j 行 = λ̃ 的第 j 列
ROW_HL, COL_HL = YELLOW, TEAL

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def tuple_str(parts):
    return "(" + ",".join(str(p) for p in parts) + ")"


def power_str(lam):
    """(6,4,4,2) -> '(6\\,4^{2}\\,2)'：連續重複的數寫成次方（書 p.1 的 (d^a) 記號）。"""
    groups = []
    for d in lam:
        if groups and groups[-1][0] == d:
            groups[-1][1] += 1
        else:
            groups.append([d, 1])
    body = r"\,".join(str(d) if a == 1 else f"{d}^{{{a}}}" for d, a in groups)
    return "(" + body + ")"


def check_math():
    conj = conjugate(LAM)
    assert is_partition(LAM) and sum(LAM) == N == len(young_boxes(LAM))
    assert LAM in partitions(N) and len(partitions(N)) == 231
    assert conj == (4, 4, 3, 3, 1, 1) and sum(conj) == N and conjugate(conj) == LAM
    assert all(conj[j] == sum(1 for (i, jj) in young_boxes(LAM) if jj == j) for j in range(LAM[0]))
    assert LAM[1] == 4 and conj[2] == 3                       # 第 2 列有 4 格、第 3 行有 3 格
    assert power_str(LAM) == r"(6\,4^{2}\,2)"
    assert power_str(conj) == r"(4^{2}\,3^{2}\,1^{2})"
    # 填數：圓周率的前 16 位，有重複；編號：1..16 各一次。兩個都不是 Young 表（F02 才加條件）
    assert len(PI_DIGITS) == N and "0" not in PI_DIGITS
    assert "".join(str(v) for r in FILLING for v in r) == PI_DIGITS
    for T in (FILLING, NUMBERING):
        assert shape(T) == LAM and all(v > 0 for r in T for v in r) and not is_tableau(T)
    flat_fill = [v for r in FILLING for v in r]
    assert flat_fill.count(REPEAT_VALUE) == 3 and len(set(flat_fill)) < N
    assert sorted(v for r in NUMBERING for v in r) == list(range(1, N + 1))
    return conj


# =============================================================================
def part_diagram(scene):
    cs = 0.6
    tl = np.array([-6.2, 2.6, 0.0])
    lam_mob = YoungDiagramMob(LAM, cell_size=cs, top_left=tl, fill_color=BLUE_C, fill_opacity=0.25)
    row_labels = VGroup()
    for i, r in enumerate(LAM):
        lab = Tex(str(r), font_size=32, fill_color=YELLOW)
        lab.next_to(lam_mob.cell(i, r - 1), RIGHT, buff=0.22)
        row_labels.add(lab)

    cx = 2.6
    lam_tex = Tex(r"\lambda=" + tuple_str(LAM), font_size=46).move_to(np.array([cx, 2.3, 0.0]))
    sum_tex = Tex("+".join(str(r) for r in LAM) + f"={N}", font_size=40).move_to(np.array([cx, 1.55, 0.0]))
    vdash = mixed("$\\lambda\\vdash 16$", "：", "$\\lambda$", " 是 16 的分割", font_size=28)
    size = mixed("$|\\lambda|=16$", "：被分割的數（格子總數）", font_size=28)
    vdash.move_to(np.array([cx, 0.8, 0.0]))
    size.move_to(np.array([cx, 0.25, 0.0]))
    count = mixed("16 的分割共 ", "$231$", " 個，各對應一張 Young 圖", font_size=26, color=MUTED_COLOR)
    count.move_to(np.array([cx, -0.3, 0.0]))

    zeros = mixed("結尾補 0 不算新的分割：", "$" + tuple_str(LAM) + "=" + tuple_str(LAM + (0, 0)) + "$",
                  font_size=28)
    power = mixed("重複的數寫成次方：", "$" + tuple_str(LAM) + "=" + power_str(LAM) + "$",
                  "（4 出現 2 次）", font_size=28)
    VGroup(zeros, power).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([0.0, -1.35, 0.0]))

    row_rect = SurroundingRectangle(lam_mob.cell_group([(1, j) for j in range(LAM[1])]), buff=0.05,
                                    color=ROW_HL, stroke_width=5)
    col_cells = [(i, 2) for i in range(len(LAM)) if LAM[i] > 2]
    col_rect = SurroundingRectangle(lam_mob.cell_group(col_cells), buff=0.05, color=COL_HL, stroke_width=5)
    rc_text = VGroup(zh(f"第 2 列有 {LAM[1]} 格", font_size=28, color=ROW_HL),
                     zh(f"第 3 行有 {len(col_cells)} 格", font_size=28, color=COL_HL)).arrange(RIGHT, buff=0.9)
    rc_text.move_to(np.array([0.0, -2.55, 0.0]))
    assert len(col_cells) == conjugate(LAM)[2]

    assert_in_frame(lam_mob, row_labels, lam_tex, sum_tex, vdash, size, count, zeros, power, rc_text)
    assert_apart(VGroup(lam_mob, row_labels), VGroup(lam_tex, sum_tex, vdash, size, count))
    assert_apart(VGroup(lam_mob, row_labels, count), zeros)
    assert_apart(zeros, power)
    assert_apart(power, rc_text)
    for a, b in [(lam_tex, sum_tex), (sum_tex, vdash), (size, count)]:
        assert_apart(a, b)

    scene.say("Young 圖：格子一列列靠左排好，下面的列不會比上面長")
    for i, r in enumerate(LAM):
        row = VGroup(*[lam_mob.cell(i, j) for j in range(r)])
        scene.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in row], lag_ratio=0.12),
                   FadeIn(row_labels[i]), run_time=0.5)
    scene.wait(0.5)

    scene.say("由上往下記下每列的格數：", "$6,4,4,2$", "，加起來是 ", "$16$")
    scene.play(TransformFromCopy(row_labels, lam_tex), run_time=1.0)
    scene.play(FadeIn(sum_tex, shift=0.15 * DOWN), run_time=0.6)
    scene.wait(0.8)

    scene.say("這串由大到小的數就是 16 的一個分割")
    scene.play(FadeIn(vdash, shift=0.15 * UP), run_time=0.6)
    scene.play(FadeIn(size, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.0)

    scene.say("反過來，每個分割都畫得出唯一一張 Young 圖")
    scene.play(FadeIn(count), run_time=0.6)
    scene.wait(1.2)

    scene.say("寫法上：尾巴多幾個 0 視為同一個；重複的數可用次方縮寫")
    scene.play(FadeIn(zeros, shift=0.15 * UP), run_time=0.7)
    scene.wait(0.8)
    scene.play(FadeIn(power, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.2)

    scene.say("分割和圖看成同一件事，就能說「", "$\\lambda$", " 的第 2 列」「", "$\\lambda$", " 的第 3 行」")
    scene.play(ShowCreation(row_rect), FadeIn(rc_text[0]), run_time=0.8)
    scene.play(ShowCreation(col_rect), FadeIn(rc_text[1]), run_time=0.8)
    scene.wait(1.6)


def part_conjugate(scene, conj):
    cs = 0.5
    tl1 = np.array([-6.3, 2.6, 0.0])
    tl2 = np.array([-1.5, 2.6, 0.0])
    lam_mob = YoungDiagramMob(LAM, cell_size=cs, top_left=tl1, stroke_width=3)
    for i, j in young_boxes(LAM):
        lam_mob.cell(i, j).set_fill(COL_COLORS[j], opacity=0.5)
    base_y = tl1[1] - len(LAM) * cs - 0.32
    col_labels = VGroup()
    for j in range(LAM[0]):
        lab = Tex(str(conj[j]), font_size=30, fill_color=COL_COLORS[j])
        lab.move_to(np.array([lam_mob.cell_center(0, j)[0], base_y, 0.0]))
        col_labels.add(lab)
    lam_name = Tex(r"\lambda", font_size=40).next_to(lam_mob, LEFT, buff=0.2)
    lam_name.align_to(lam_mob, UP)
    col_note = zh("各行的長度", font_size=24, color=MUTED_COLOR).next_to(col_labels, DOWN, buff=0.2)

    diag_len = 4.2 * cs
    diag1 = DashedLine(tl1 + 0.3 * cs * (UL), tl1 + diag_len * (DR), stroke_color=DIAG_COLOR, stroke_width=3)
    diag2 = diag1.copy().shift(tl2 - tl1)

    # 翻轉：繞著過左上角、方向 (1,-1,0) 的軸轉 180°，就是沿主對角線鏡射
    axis = np.array([1.0, -1.0, 0.0])
    moved = lam_mob.copy()
    moved.shift(tl2 - tl1)
    flipped = moved.copy().rotate(PI, axis=axis, about_point=tl2)
    conj_ref = YoungDiagramMob(conj, cell_size=cs, top_left=tl2)
    for i, j in young_boxes(LAM):
        assert np.allclose(flipped.cell(i, j).get_center(), conj_ref.cell_center(j, i), atol=1e-6)
    assert sorted(young_boxes(conj)) == sorted((j, i) for i, j in young_boxes(LAM))

    row_labels = VGroup()
    for i, r in enumerate(conj):
        lab = Tex(str(r), font_size=30, fill_color=COL_COLORS[i])
        lab.next_to(conj_ref.cell(i, r - 1), RIGHT, buff=0.2)
        row_labels.add(lab)
    conj_name = Tex(r"\tilde{\lambda}", font_size=40).next_to(conj_ref, LEFT, buff=0.2).align_to(conj_ref, UP)

    cx = 4.15
    conj_tex = Tex(r"\tilde{\lambda}=" + tuple_str(conj), font_size=42).move_to(np.array([cx, 2.3, 0.0]))
    conj_pow = Tex("=" + power_str(conj), font_size=40).move_to(np.array([cx, 1.6, 0.0]))
    conj_size = Tex(r"|\tilde{\lambda}|=|\lambda|=16", font_size=40).move_to(np.array([cx, 0.9, 0.0]))
    rule = mixed("$\\tilde{\\lambda}$", " 的第 ", "$j$", " 列 ＝ ", "$\\lambda$", " 的第 ", "$j$", " 行",
                 font_size=30)
    back = mixed("再翻一次就回到原圖：", "$\\tilde{\\tilde{\\lambda}}=\\lambda$", font_size=28)
    rule_box = SurroundingRectangle(rule, buff=0.2, color=YELLOW, stroke_width=3)
    VGroup(VGroup(rule_box, rule), back).arrange(DOWN, buff=0.35).move_to(np.array([2.6, -1.75, 0.0]))

    assert_in_frame(lam_mob, lam_name, col_labels, col_note, diag1, diag2, conj_ref, row_labels, conj_name,
                    conj_tex, conj_pow, conj_size, rule_box, back)
    left_grp = VGroup(lam_mob, lam_name, col_labels, col_note, diag1)
    right_grp = VGroup(conj_ref, row_labels, conj_name, diag2)
    assert_apart(left_grp, right_grp, gap=0.3)
    assert_apart(right_grp, VGroup(conj_tex, conj_pow, conj_size), gap=0.3)
    assert_apart(right_grp, rule_box)
    assert_apart(left_grp, VGroup(rule_box, back))
    assert_apart(conj_size, rule_box)
    for a, b in [(conj_tex, conj_pow), (conj_pow, conj_size), (rule_box, back)]:
        assert_apart(a, b)

    scene.say("給 ", "$\\lambda$", " 的每一行一個顏色，底下寫出各行的長度")
    scene.play(FadeIn(lam_mob), FadeIn(lam_name), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.1 * DOWN) for c in col_labels], lag_ratio=0.12),
               FadeIn(col_note), run_time=1.0)
    scene.wait(0.6)

    scene.say("沿著主對角線（左上到右下）把整張圖翻過去")
    scene.play(ShowCreation(diag1), run_time=0.6)
    copy_mob = lam_mob.copy()
    scene.play(copy_mob.animate.shift(tl2 - tl1), TransformFromCopy(diag1, diag2), run_time=1.0)
    scene.play(Rotate(copy_mob, PI, axis=axis, about_point=tl2), run_time=2.0)
    scene.play(FadeOut(diag2), FadeIn(conj_name), run_time=0.5)
    for i, j in young_boxes(LAM):
        assert np.allclose(copy_mob.cell(i, j).get_center(), conj_ref.cell_center(j, i), atol=1e-6)

    scene.say("翻過來的圖叫共軛 ", "$\\tilde{\\lambda}$", "：原來第 ", "$j$", " 行變成了第 ", "$j$", " 列")
    scene.play(TransformFromCopy(col_labels, row_labels), run_time=1.2)
    scene.play(FadeIn(conj_tex), run_time=0.7)
    scene.wait(1.0)

    scene.say("所以 ", "$\\tilde{\\lambda}$", " 記錄的是 ", "$\\lambda$", " 每一行的長度，格子總數不變")
    scene.play(FadeIn(conj_pow, shift=0.15 * DOWN), run_time=0.6)
    scene.play(FadeIn(conj_size, shift=0.15 * DOWN), run_time=0.6)
    scene.wait(0.8)
    scene.play(ShowCreation(rule_box), FadeIn(rule), run_time=0.8)
    scene.wait(0.6)

    scene.say("沿同一條對角線再翻一次，又回到 ", "$\\lambda$")
    scene.play(FadeIn(back, shift=0.15 * UP), run_time=0.7)
    scene.wait(1.6)


def part_filling(scene):
    cs = 0.55
    lam_w = LAM[0] * cs
    left = YoungDiagramMob(LAM, cell_size=cs, top_left=np.array([-3.4 - lam_w / 2, 2.25, 0.0]))
    right = YoungDiagramMob(LAM, cell_size=cs, top_left=np.array([3.4 - lam_w / 2, 2.25, 0.0]))
    title = zh("在每一格放一個正整數", font_size=30).move_to(np.array([0.0, 2.75, 0.0]))

    fs = 28
    left.set_entries(FILLING, font_size=fs)
    right.set_entries(NUMBERING, font_size=fs)
    left_lab = mixed("填數（filling）：數字可以重複", font_size=26)
    left_lab.next_to(left, DOWN, buff=0.3)
    right_lab = mixed("編號（numbering）：數字兩兩不同", font_size=26)
    right_lab.next_to(right, DOWN, buff=0.3)
    right_lab.align_to(left_lab, UP)
    pi_note = zh("（剛好是圓周率的前 16 位數字）", font_size=22, color=MUTED_COLOR)
    pi_note.next_to(left_lab, DOWN, buff=0.18)
    rep_cells = [(i, j) for i, r in enumerate(FILLING) for j, v in enumerate(r) if v == REPEAT_VALUE]
    assert len(rep_cells) == 3
    rep_hl = VGroup(*[Square(side_length=cs * 0.86, stroke_width=0).set_fill(YELLOW, opacity=0.45)
                      .move_to(left.cell_center(i, j)) for i, j in rep_cells])
    rep_note = mixed("$5$", " 出現了 ", "$3$", " 次", font_size=24, color=YELLOW)
    rep_note.next_to(left, RIGHT, buff=0.3).align_to(left, DOWN)

    teaser = mixed("再要求「每列", "$\\rightarrow$", "弱遞增、每行", "$\\downarrow$", "嚴格遞增」",
                   "$\\Longrightarrow$", "Young 表（下一幕）", font_size=28)
    teaser_box = SurroundingRectangle(teaser, buff=0.22, color=YELLOW, stroke_width=3)
    VGroup(teaser_box, teaser).move_to(np.array([0.0, -2.3, 0.0]))

    assert_in_frame(title, left, right, left_lab, right_lab, pi_note, rep_note, teaser_box)
    assert_apart(VGroup(left, left_lab, pi_note, rep_note), VGroup(right, right_lab), gap=0.3)
    assert_apart(title, VGroup(left, right))
    assert_apart(VGroup(left_lab, pi_note, right_lab), teaser_box)
    assert all(m.get_width() < cs * 0.85 for m in VGroup(*left.entries, *right.entries))

    scene.say("畫 Young 圖的目的，是要在格子裡放東西")
    scene.play(FadeIn(title), ShowCreation(left.cells), ShowCreation(right.cells), run_time=0.9)

    scene.say("每格放一個正整數，叫做填數（filling），數字可以重複")
    scene.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in left.entries], lag_ratio=0.06), run_time=1.3)
    scene.play(FadeIn(left_lab), FadeIn(pi_note), run_time=0.6)
    scene.play(FadeIn(rep_hl), FadeIn(rep_note), run_time=0.6)
    scene.wait(0.8)

    scene.say("若放進去的數字兩兩不同，通常改叫編號（numbering）")
    scene.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in right.entries], lag_ratio=0.06), run_time=1.3)
    scene.play(FadeIn(right_lab), run_time=0.6)
    scene.wait(1.0)

    scene.say("這裡的數還可以亂放；下一幕加上大小順序的規定")
    scene.play(ShowCreation(teaser_box), FadeIn(teaser), run_time=0.9)
    scene.wait(2.0)


class SceneF01YoungDiagrams(ChuScene):
    def construct(self):
        self.show_header("Young 圖、分割與共軛")
        conj = check_math()
        part_diagram(self)
        self.clear_stage()
        part_conjugate(self, conj)
        self.clear_stage()
        part_filling(self)
        self.wait(1.0)
