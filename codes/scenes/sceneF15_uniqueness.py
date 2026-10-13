"""
Scene F15 —— 唯一性的證明：只用 L(w,k) 一格一格決定表（Fulton《Young Tableaux》§3.2，書 p.33–35）

    Lemma 3：w ≡ w′ ⇒ 兩邊各去掉最大的 p 個（或最小的 q 個）字母，仍然等價；相同的字母右邊的算比較大
        例（書 p.33）：1 3 4 2 3 1 3 去掉最大的 3 個 → 1 3 2 1
    唯一性的證明＝演算法（tableau_from_greene）：w = 1 3 4 2 3 4 1 2 2 3 3 2（CH3_WORD）
        w_p = w 去掉最大的 p 個字母，形狀 λ(w_p) = greene_numbers(w_p)
        (6,3,3) → (6,3,2) → (6,3,1) → (5,3,1) → … → ∅；每次少掉的格子放剛去掉的字母 → CH3_TABLEAU = P(w)
    → 第 2 章主定理成立（每個字恰與一個表的字等價），第 1 章的三個 Claim 也一起證完
    Exercise 1–2：嚴格遞減 ↔ 行；Erdős–Szekeres：w = 4 9 2 10 6 1 8 3 7 5，長 10 > 3²，
        P(w) 形狀 (3,3,3,1)：最長遞增 3（第 1 列）、最長嚴格遞減 4（列數）

數字全部由 utils/tableaux.py 算出並 assert（位置、格子 0 起算；字幕裡的列號 1 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF15_uniqueness.py SceneF15Uniqueness
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import WordMob, assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.mit_draw import CELL_STROKE, YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH3_TABLEAU,
    CH3_WORD,
    conjugate,
    greene_numbers,
    insert_word,
    max_increasing,
    remove_largest,
    shape,
    tableau_from_greene,
    young_boxes,
)

W = CH3_WORD                                       # 1 3 4 2 3 4 1 2 2 3 3 2（書 p.30）
T = CH3_TABLEAU                                    # P(w)
LAM = (6, 3, 3)
ORDER = [5, 2, 10, 9, 4, 1, 11, 8, 7, 3, 6, 0]    # 由大到小去掉的位置（相同時右邊先）
SHAPES = [(6, 3, 3), (6, 3, 2), (6, 3, 1), (5, 3, 1), (5, 2, 1), (5, 1, 1), (5, 1), (4, 1), (3, 1),
          (2, 1), (2,), (1,), ()]
CELLS = [(2, 2), (2, 1), (0, 5), (1, 2), (1, 1), (2, 0), (0, 4), (0, 3), (0, 2), (1, 0), (0, 1), (0, 0)]
N_SLOW = 3

L3_WORD = (1, 3, 4, 2, 3, 1, 3)                    # 書 p.33 的例子
L3_DROP = [2, 6, 4]                                # 4、最右邊的 3、再來的 3
L3_REST = (1, 3, 2, 1)

ES_WORD = (4, 9, 2, 10, 6, 1, 8, 3, 7, 5)          # Erdős–Szekeres 的例子
ES_P = ((1, 3, 5), (2, 6, 7), (4, 8, 10), (9,))
ES_N = 3
ES_INC = [0, 1, 3]                                 # 4 9 10
ES_DEC = [1, 6, 8, 9]                              # 9 8 7 5

FILL = BLUE_D
INC_COLOR, DEC_COLOR = TEAL, PINK


# =============================================================================
# 數學
# =============================================================================
def lost_box(lam, mu):
    """λ 比 μ 多出的那一格。"""
    boxes = set(young_boxes(lam)) - set(young_boxes(mu))
    assert len(boxes) == 1, (lam, mu)
    return boxes.pop()


def l_values(p):
    """w_p 的 L(w_p,1), L(w_p,2), …（直接用 max_increasing 算）。"""
    wp = remove_largest(W, p)
    lam = SHAPES[p]
    vals = [max_increasing(wp, k)[0] for k in range(1, len(lam) + 1)]
    assert vals == [sum(lam[:k]) for k in range(1, len(lam) + 1)]
    return vals


def check_math():
    assert insert_word(W) == T == tableau_from_greene(W) and shape(T) == LAM
    assert ORDER == sorted(range(len(W)), key=lambda i: (W[i], i))[::-1]
    for p in range(len(W) + 1):
        wp = remove_largest(W, p)
        assert wp == tuple(a for i, a in enumerate(W) if i not in ORDER[:p])
        assert (greene_numbers(wp) if wp else ()) == SHAPES[p]
        assert shape(insert_word(wp)) == SHAPES[p]
        if p:
            cell = lost_box(SHAPES[p - 1], SHAPES[p])
            assert cell == CELLS[p - 1] and T[cell[0]][cell[1]] == W[ORDER[p - 1]]
        l_values(p)
    # Lemma 3 的例子
    assert remove_largest(L3_WORD, 3) == L3_REST
    assert L3_DROP == sorted(range(len(L3_WORD)), key=lambda i: (L3_WORD[i], i))[::-1][:3]
    assert tuple(a for i, a in enumerate(L3_WORD) if i not in L3_DROP) == L3_REST
    # Erdős–Szekeres
    assert insert_word(ES_WORD) == ES_P and shape(ES_P) == (3, 3, 3, 1)
    assert len(ES_WORD) == 10 > ES_N ** 2 == 9
    assert max_increasing(ES_WORD, 1) == (3, [ES_INC]) and len(ES_P[0]) == 3 == ES_N
    assert max_increasing(ES_WORD, 1, decreasing=True) == (4, [ES_DEC]) and len(ES_P) == 4 == ES_N + 1
    assert all(ES_WORD[a] > ES_WORD[b] for a, b in zip(ES_DEC, ES_DEC[1:]))
    assert greene_numbers(ES_WORD, decreasing=True) == conjugate(shape(ES_P))
    assert greene_numbers(W, decreasing=True) == conjugate(LAM)


# =============================================================================
# 第 1 段：Lemma 3（去掉最大的字母）
# =============================================================================
def part_lemma3(scene):
    stmt = mixed("Lemma 3：", "$w\\equiv w'$", " 時，兩邊各去掉最大的 ", "$p$", " 個字母，仍然等價",
                 font_size=28)
    stmt.move_to(np.array([0.0, 2.55, 0.0]))
    word = WordMob(L3_WORD, size=0.75, center=np.array([0.0, 1.15, 0.0]))
    tags = VGroup(*[Tex(str(t + 1), font_size=30, fill_color=RED_B).next_to(word.tiles[p], UP, buff=0.12)
                    for t, p in enumerate(L3_DROP)])
    rest = WordMob(L3_REST, size=0.75, center=np.array([0.0, -0.55, 0.0]))
    arrow = Arrow(word.get_bottom() + 0.05 * DOWN, rest.get_top() + 0.05 * UP, buff=0.1, thickness=3,
                  fill_color=GREY_B)
    arrow_lab = zh(f"去掉最大的 {len(L3_DROP)} 個", font_size=22, color=MUTED_COLOR).next_to(arrow, RIGHT, buff=0.2)
    why = VGroup(
        mixed("去掉 ", "$z$", "：", "$y\\,x\\,z\\equiv y\\,z\\,x$", " 變成 ", "$y\\,x=y\\,x$", font_size=24),
        mixed("去掉 ", "$z$", "：", "$x\\,z\\,y\\equiv z\\,x\\,y$", " 變成 ", "$x\\,y=x\\,y$", font_size=24),
    ).arrange(RIGHT, buff=0.9).move_to(np.array([0.0, -2.05, 0.0]))
    assert_in_frame(stmt, word, tags, rest, arrow, arrow_lab, why)
    assert_apart(stmt, VGroup(word, tags), gap=0.2)
    assert_apart(rest, why, gap=0.3)
    assert_apart(arrow_lab, word, gap=0.1)
    assert_apart(arrow_lab, rest, gap=0.1)

    scene.say("Lemma 3：等價的字各自去掉最大的幾個字母，剩下的仍然等價")
    scene.play(FadeIn(stmt), run_time=0.7)
    scene.wait(0.8)
    scene.say(f"相同的字母，右邊的算比較大。例：去掉最大的 {len(L3_DROP)} 個字母")
    scene.play(FadeIn(word), run_time=0.6)
    for t, p in enumerate(L3_DROP):
        scene.play(*word.color_slots({p: RED}, opacity=0.45), FadeIn(tags[t], shift=0.1 * DOWN), run_time=0.45)
    keep = [k for k in range(len(L3_WORD)) if k not in L3_DROP]
    scene.play(GrowArrow(arrow), FadeIn(arrow_lab),
               *[TransformFromCopy(word.tiles[k], rest.tiles[t]) for t, k in enumerate(keep)], run_time=1.0)
    scene.wait(0.8)
    scene.say("理由：看一步基本變換就夠；去掉的若不是 ", "$x,y,z$", "，同一個變換照樣能做")
    scene.wait(2.0)
    scene.say("若去掉的是三者中最大的 ", "$z$", "，兩邊剩下的字根本一樣")
    scene.play(FadeIn(why, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：演算法（tableau_from_greene）
# =============================================================================
PANEL_POS = np.array([0.3, 0.45, 0.0])


def panel(p):
    name = "w" if p == 0 else f"w_{{{p}}}"
    vals = l_values(p)
    l1 = Tex(f"L({name},k):\\ " + ",\\ ".join(map(str, vals)) if vals else f"L({name},k)=0", font_size=40)
    l2 = Tex(f"\\lambda({name})=" + (tuple_str(SHAPES[p]) if SHAPES[p] else "\\varnothing"), font_size=40)
    return VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(PANEL_POS, aligned_edge=LEFT)


def step_caption(p):
    letter, (i, j) = W[ORDER[p - 1]], CELLS[p - 1]
    lam = tuple_str(SHAPES[p])
    if p == 1:
        return [f"去掉最右邊的 {letter}：剩下的字形狀是 ", f"${lam}$", f"，少了第 {i + 1} 列的一格"]
    if p == 2:
        return [f"再去掉另一個 {letter}：形狀 ", f"${lam}$", f"，這個 {letter} 放在第 {i + 1} 列第 {j + 1} 格"]
    return [f"接著是最右邊的 {letter}：形狀 ", f"${lam}$", f"，{letter} 放第 {i + 1} 列的最後"]


def part_algorithm(scene):
    word = WordMob(W, size=0.6, center=np.array([0.5, 2.5, 0.0]))
    wlab = Tex("w=", font_size=40).next_to(word, LEFT, buff=0.25)
    cs = 0.85
    tl = np.array([-6.3, 1.35, 0.0])
    diag = YoungDiagramMob(LAM, cell_size=cs, top_left=tl)
    final = tableau_mob(T, cs=cs, top_left=tl)
    note = mixed("$w_p$", "：", "$w$", " 去掉最大的 ", "$p$", " 個字母", font_size=24, color=MUTED_COLOR)
    note.move_to(PANEL_POS + 0.95 * UP, aligned_edge=LEFT)
    rule = zh("規則：形狀少掉的那一格，放剛去掉的字母", font_size=24, color=YELLOW)
    rule.move_to(PANEL_POS + 1.35 * DOWN, aligned_edge=LEFT)
    plab = Tex("P(w)", font_size=44, fill_color=OK_COLOR).next_to(diag, DOWN, buff=0.35).align_to(diag, LEFT)
    pan = panel(0)
    widest = VGroup(*[panel(p) for p in (0, 1, 12)])
    assert_in_frame(word, wlab, diag, note, rule, plab, widest)
    assert_apart(word, VGroup(diag, note), gap=0.25)
    assert_apart(diag, VGroup(note, widest, rule), gap=0.4)
    assert_apart(note, widest, gap=0.15)
    assert_apart(widest, rule, gap=0.2)

    scene.say("唯一性的證明其實是個演算法：只看 ", "$L(w,k)$", "，一格一格把表定出來")
    scene.play(FadeIn(wlab), FadeIn(word), run_time=0.7)
    scene.say("先由 ", "$L(w,k)$", " 得到形狀 ", f"${tuple_str(LAM)}$", "（上一幕的 Lemma 1、2）")
    scene.play(FadeIn(pan), ShowCreation(diag), run_time=1.0)
    scene.play(FadeIn(note), run_time=0.4)
    scene.wait(1.0)

    scale = cs / word.size
    placed = {}
    for p in range(1, len(W) + 1):
        slow = p <= N_SLOW
        pos, cell = ORDER[p - 1], CELLS[p - 1]
        tile, target = word.tiles[pos], diag.cell(*cell)
        assert tile.value == W[pos] == T[cell[0]][cell[1]]
        if slow:
            scene.say(*step_caption(p))
        elif p == N_SLOW + 1:
            scene.say("依此類推，一個一個去掉，表就從大的數開始填滿")
        mover = tile.label.copy()
        scene.add(mover)
        scene.play(tile.square.animate.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW),
                   run_time=0.4 if slow else 0.2)
        scene.play(Transform(pan, panel(p)), tile.animate.set_opacity(0.25),
                   target.animate.set_stroke(YELLOW, width=6), run_time=0.7 if slow else 0.3)
        if slow:
            scene.wait(0.7)
        scene.play(mover.animate.scale(scale).move_to(target.get_center()),
                   target.animate.set_fill(FILL, opacity=0.45).set_stroke(CELL_STROKE, width=3),
                   run_time=0.7 if slow else 0.35)
        placed[cell] = mover
        if slow:
            scene.wait(0.5)
            if p == 1:
                scene.play(FadeIn(rule, shift=0.1 * UP), run_time=0.5)
                scene.wait(0.6)
    assert set(placed) == set(young_boxes(LAM))
    assert all(np.allclose(placed[(i, j)].get_center(), final.entry(i, j).get_center())
               and final.entry(i, j).tab_value == T[i][j] for i, j in young_boxes(LAM))
    scene.say("全部填好，正是 ", "$P(w)$", "：與 ", "$w$", " 等價的表只能是這一個")
    scene.play(FadeIn(plab, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：主定理
# =============================================================================
def part_theorem(scene):
    t1 = zh("主定理：每個字恰好與一個表的字等價", font_size=34)
    t2 = mixed("存在：", "$P(w)=(\\cdots(x_1\\leftarrow x_2)\\leftarrow\\cdots)\\leftarrow x_r$", font_size=26,
               color=MUTED_COLOR)
    t3 = zh("唯一：剛才的演算法（對字的長度歸納）", font_size=26, color=MUTED_COLOR)
    block = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35)
    box = SurroundingRectangle(block, buff=0.3, color=YELLOW, stroke_width=3)
    VGroup(block, box).move_to(np.array([0.0, 0.9, 0.0]))
    claims = zh("第 1 章的三個 Claim，到這裡全部證完", font_size=30, color=OK_COLOR)
    claims.move_to(np.array([0.0, -1.3, 0.0]))
    assert_in_frame(box, block, claims)
    assert_apart(box, claims, gap=0.4)

    scene.say("歸納：少一個字母的表唯一；形狀由 ", "$L(w,k)$", " 決定，最後一格也就確定")
    scene.play(FadeIn(t1), ShowCreation(box), run_time=0.9)
    scene.play(FadeIn(t2), FadeIn(t3), run_time=0.7)
    scene.wait(1.6)
    scene.say("於是第 2 章的主定理成立，第 1 章留下的三個 Claim 也一起證完")
    scene.play(FadeIn(claims, shift=0.1 * UP), run_time=0.7)
    scene.wait(2.0)


# =============================================================================
# 第 4 段：習題 1–2、Erdős–Szekeres
# =============================================================================
def part_erdos(scene):
    word = WordMob(ES_WORD, size=0.62, center=np.array([0.9, 2.4, 0.0]))
    wlab = Tex("w=", font_size=40).next_to(word, LEFT, buff=0.25)
    cs = 0.72
    tl = np.array([-6.1, 1.3, 0.0])
    tab = tableau_mob(ES_P, cs=cs, top_left=tl)
    plab = Tex("P(w)", font_size=36).next_to(tab, DOWN, buff=0.25)
    box3 = DashedVMobject(Square(side_length=ES_N * cs), num_dashes=36).set_stroke(YELLOW, width=3)
    box3.move_to(tl + 0.5 * ES_N * cs * (RIGHT + DOWN))
    x0 = -3.0
    e2 = mixed("最長遞增子序列：", f"${len(ES_INC)}$", "（第 1 列的長度）", font_size=26)
    e3 = mixed("最長嚴格遞減子序列：", f"${len(ES_DEC)}$", "（列數）", font_size=26)
    e4 = mixed("長度 ", "$>n^2$", " 的字，必有長度 ", "$>n$", " 的遞增或嚴格遞減子序列", font_size=26)
    e4box = SurroundingRectangle(e4, buff=0.18, color=YELLOW, stroke_width=3)
    n2 = ES_N ** 2
    e1 = mixed(f"$|w|={len(ES_WORD)}>{ES_N}^2={n2}$", f"：{len(ES_WORD)} 格放不進 ", f"${ES_N}\\times {ES_N}$",
               " 的方格", font_size=26)
    for m, y in ((e2, 1.05), (e3, 0.35), (e4, -0.65), (e1, -1.65)):
        m.move_to(np.array([x0, y, 0.0]), aligned_edge=LEFT)
    e4box.move_to(e4)
    assert_in_frame(word, wlab, tab, plab, box3, e1, e2, e3, e4box)
    assert_apart(word, VGroup(tab, e2), gap=0.25)
    assert_apart(VGroup(tab, plab, box3), VGroup(e1, e2, e3, e4box), gap=0.3)
    for a, b in ((e2, e3), (e3, e4box), (e4box, e1)):
        assert_apart(a, b, gap=0.15)

    scene.say("習題 1：把「弱遞增」換成「嚴格遞減」，表的列就換成行")
    scene.play(FadeIn(wlab), FadeIn(word), FadeIn(tab), FadeIn(plab), run_time=0.8)
    scene.wait(0.8)
    scene.say("最長的遞增子序列有 ", f"${len(ES_INC)}$", " 個字母，正是 ", "$P(w)$", " 第 1 列的長度")
    scene.play(*word.color_slots({p: INC_COLOR for p in ES_INC}, opacity=0.5),
               *[tab.cell(0, j).animate.set_fill(INC_COLOR, opacity=0.45) for j in range(len(ES_P[0]))],
               FadeIn(e2), run_time=0.8)
    scene.wait(1.4)
    scene.say("最長的嚴格遞減子序列有 ", f"${len(ES_DEC)}$", " 個字母，正是 ", "$P(w)$", " 的列數")
    scene.play(*word.color_slots({p: GREY_A for p in ES_INC}, opacity=0.15),
               *[tab.cell(0, j).animate.set_fill(BLACK, opacity=0.0) for j in range(len(ES_P[0]))], run_time=0.4)
    scene.play(*word.color_slots({p: DEC_COLOR for p in ES_DEC}, opacity=0.5),
               *[tab.cell(i, 0).animate.set_fill(DEC_COLOR, opacity=0.45) for i in range(len(ES_P))],
               FadeIn(e3), run_time=0.8)
    scene.wait(1.4)
    scene.say("習題 2：Erdős 與 Szekeres 的定理")
    scene.play(FadeIn(e4), ShowCreation(e4box), run_time=0.8)
    scene.wait(1.6)
    scene.say("因為 ", "$P(w)$", " 的格子比 ", f"${ES_N}\\times {ES_N}$", " 多：第 1 列或列數一定超過 ",
              f"${ES_N}$")
    scene.play(ShowCreation(box3), FadeIn(e1), run_time=0.9)
    scene.play(Indicate(tab.cell(len(ES_P) - 1, 0), color=RED), run_time=0.8)
    scene.wait(2.0)


class SceneF15Uniqueness(ChuScene):
    def construct(self):
        self.show_header("唯一性：由 L(w,k) 重建表")
        check_math()
        part_lemma3(self)
        self.clear_stage()
        part_algorithm(self)
        self.clear_stage()
        part_theorem(self)
        self.clear_stage()
        part_erdos(self)
        self.wait(1.0)
