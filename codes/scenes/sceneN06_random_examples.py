"""
Scene N06 —— 用循環引理製造例子：均勻隨機樹產生器（utils/raney_examples.py；Raney 導讀第 6.1 節的應用）
執行（在 codes/ 內）：manimgl scenes/sceneN06_random_examples.py SceneN06RandomExamples

1. 組成 (1; 0,2,1)（兩個二元、一個三元、五個引數）：把 8 個符號隨機打亂 → 轉到唯一的好讀法 → 一棵樹。
2. 再抽兩次；抽 2100 次，21 個字各出現約 100 次（均勻：每個字被 8 個（字串, 起點）讀到）。
3. 同樣的方法產生隨機的不交叉分法（Chu 的 n⃗ = (2,1)、v⃗ = (2,3)，經「固定一點」的一一對應）。
4. 例題集：python utils/raney_examples.py --md --seed 7。
所有隨機數用固定 seed，每次渲染相同。
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.polygon_groups import make_configuration
from utils.raney import L_formula, cyclic_variant, is_word, list_shifts, lists_with, partition_to_word, word_to_partition
from utils.raney_draw import WordTreeMob, word_tiles
from utils.raney_examples import random_list, random_string, word_to_expression
from utils.scene_base import ChuScene
from utils.styles import mixed, zh

A = (0, 2, 1)
SEED = 1960
N_SAMPLES = 2100


def demo_draws():
    """三次示範抽樣：(字串, 起點, 字)。"""
    rng = random.Random(SEED)
    out = []
    for _ in range(3):
        s = random_string(1, A, rng)
        k = list_shifts(s)[0]
        out.append((s, k, cyclic_variant(s, k)))
    return out


def histogram():
    rng = random.Random(SEED + 1)
    words = lists_with(1, A)
    cnt = {w: 0 for w in words}
    for _ in range(N_SAMPLES):
        cnt[random_list(1, A, rng)] += 1
    return [cnt[w] for w in words]


def random_partitions():
    rng = random.Random(SEED + 2)
    return [word_to_partition(random_list(1, (0, 2, 1), rng), 7) for _ in range(3)]


def check_math():
    assert L_formula(1, A) == 21 == len(lists_with(1, A))
    draws = demo_draws()
    assert all(is_word(w) for _, _, w in draws) and len({w for _, _, w in draws}) == 3
    h = histogram()
    assert sum(h) == N_SAMPLES and len(h) == 21 and min(h) >= 70 and max(h) <= 130
    import utils.counting as ct
    assert all(ct.is_noncrossing(p) and sorted(map(len, p)) == [2, 2, 3] for p in random_partitions())


def rotate_anim(tiles, k):
    """把方塊列轉 k 格：前 k 個沿弧線移到最後。"""
    m = len(tiles)
    slots = [t.get_center().copy() for t in tiles]
    anims = []
    for j, t in enumerate(tiles):
        target = slots[(j - k) % m]
        anims.append(t.animate(path_arc=-PI / 2 if j < k else 0).move_to(target))
    return anims


class SceneN06RandomExamples(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N06　用循環引理製造例子")
        draws = demo_draws()

        # 1. 一次抽樣，慢慢做
        self.say("想要一棵隨機的樹：兩個二元節點、一個三元節點（", "$21$", " 種之一，每種機率一樣）")
        s, k, w = draws[0]
        bag = word_tiles(sorted(s, reverse=True), size=0.55, font_size=30).move_to(2.3 * UP)
        lab_bag = zh("所有符號", font_size=24, color=GREY_A).next_to(bag, LEFT, buff=0.4)
        self.play(FadeIn(bag), FadeIn(lab_bag))
        row = word_tiles(s, size=0.55, font_size=30).move_to(1.0 * UP)
        lab_row = zh("隨機打亂", font_size=24, color=GREY_A).next_to(row, LEFT, buff=0.4)
        assert_in_frame(bag, row, lab_bag, lab_row)
        self.play(TransformFromCopy(bag, row), FadeIn(lab_row), run_time=1.5)
        self.say("循環引理：恰有一個起點讓它變成字（這裡從第 ", "$%d$" % k, " 項開始讀）")
        mark = SurroundingRectangle(row[k], color=YELLOW, buff=0.05)
        self.play(ShowCreation(mark))
        self.wait(1)
        self.play(FadeOut(mark), *rotate_anim(row, k), run_time=1.5)
        lab_word = zh("轉成字", font_size=24, color=GREY_A).next_to(row, LEFT, buff=0.4)
        self.play(Transform(lab_row, lab_word))
        tree = WordTreeMob(w, x_gap=0.5, y_gap=0.6, root_pos=np.array([0, -0.2, 0]))
        expr = Tex(word_to_expression(w)[1], font_size=34).next_to(tree, RIGHT, buff=0.8)
        assert_in_frame(tree, expr)
        self.play(FadeIn(tree), FadeIn(expr), run_time=1.2)
        self.say("這棵樹（運算式）就是一個均勻隨機的例子")
        self.wait(2.5)
        self.play(FadeOut(VGroup(bag, lab_bag, row, lab_row, tree, expr)))

        # 2. 再抽兩次 + 直方圖
        trees = VGroup()
        for s2, k2, w2 in draws:
            t = WordTreeMob(w2, x_gap=0.4, y_gap=0.48)
            lab = VGroup(word_tiles(s2, size=0.24, font_size=16, buff=0.02), Tex(r"\downarrow", font_size=26),
                         word_tiles(w2, size=0.24, font_size=16, buff=0.02)).arrange(DOWN, buff=0.1)
            trees.add(VGroup(lab, t).arrange(DOWN, buff=0.3))
        trees.arrange(RIGHT, buff=0.6).move_to(np.array([-2.9, 0.9, 0]))
        h = histogram()
        bars = VGroup(*[Rectangle(width=0.16, height=c / 100 * 1.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.8)
                        for c in h]).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        bars.move_to(np.array([4.0, 0.3, 0]), aligned_edge=DOWN)
        ref = DashedLine(bars.get_corner(DL) + 1.6 * UP + 0.1 * LEFT, bars.get_corner(DR) + 1.6 * UP + 0.1 * RIGHT,
                         stroke_color=YELLOW, stroke_width=2)
        hl = VGroup(mixed("抽 ", "$2100$", " 次：21 個字", font_size=24),
                    mixed("各 ", "$%d$" % min(h), "～", "$%d$" % max(h), " 次（期望 100）", font_size=24)).arrange(DOWN, buff=0.12)
        hl.next_to(bars, DOWN, buff=0.35)
        assert_in_frame(trees, bars, hl)
        assert_apart(trees, VGroup(bars, hl))
        self.say("每抽一次就是一個新例子")
        self.play(LaggedStartMap(FadeIn, trees, lag_ratio=0.4), run_time=2.5)
        self.wait(1)
        self.say("為什麼均勻？每個字恰好被 ", "$8$", " 個（字串, 起點）讀到——和定理 2.2 的雙重計數一樣")
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.05), ShowCreation(ref), run_time=2)
        self.play(FadeIn(hl))
        self.wait(3)
        self.play(FadeOut(VGroup(trees, bars, ref, hl)))

        # 3. 隨機不交叉分法
        parts = random_partitions()
        cfgs = VGroup(*[make_configuration(7, p, radius=1.0, root=0) for p in parts]).arrange(RIGHT, buff=1.3)
        cfgs.move_to(0.8 * UP)
        words = VGroup(*[word_tiles(partition_to_word(p, 7),
                                    size=0.3, font_size=18, buff=0.02).next_to(c, DOWN, buff=0.35) for p, c in zip(parts, cfgs)])
        note = mixed("均勻隨機的字 ", "$\\to$", " 「固定點 1」的一一對應 ", "$\\to$", " 均勻隨機的不交叉分法", font_size=26)
        note.next_to(words, DOWN, buff=0.5)
        assert_in_frame(cfgs, words, note)
        self.say("同樣的方法：7 個點分成兩條弦和一個三角形（21 種）的隨機分法")
        self.play(LaggedStartMap(FadeIn, cfgs, lag_ratio=0.3), LaggedStartMap(FadeIn, words, lag_ratio=0.3), run_time=2.5)
        self.play(FadeIn(note))
        self.wait(3)
        self.play(FadeOut(VGroup(cfgs, words, note)))

        # 4. 例題集
        cmd = Text("python utils/raney_examples.py --md --seed 7", font="Consolas", font_size=26, fill_color=YELLOW)
        lines = VGroup(
            zh("例題集（Markdown，附詳解；換 seed 就是新的一份）：", font_size=26),
            zh("運算式與字、循環引理、數字列、不交叉分法 ↔ 字、", font_size=24, color=GREY_A),
            zh("Lagrange 反演、卷積、整數序列的 Raney 引理、摸牌遊戲", font_size=24, color=GREY_A),
            zh("每一題的答案都由程式算出並核對", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        VGroup(cmd, lines).arrange(DOWN, buff=0.5).move_to(0.6 * UP)
        assert_in_frame(cmd, lines)
        self.say("程式：", "utils/raney_examples.py")
        self.play(Write(cmd), run_time=1.5)
        self.play(FadeIn(lines, shift=0.2 * UP), run_time=1.2)
        self.wait(3)
