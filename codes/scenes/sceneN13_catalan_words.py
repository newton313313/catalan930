"""
Scene N13 —— 只有 2 和 0 的字就是卡塔蘭數（Raney 導讀第 2.4 小節「從卡塔蘭到 Chu」）
執行（在 codes/ 內）：manimgl scenes/sceneN13_catalan_words.py SceneN13CatalanWords

1. a+(b+c) → 前序記法 +a+bc → 把 + 換成 2、字母換成 0：字 20200，畫成樹。
2. 「還要幾個東西」的計數器：從 1 開始，2 加 1、0 減 1，最後一格才變 0 ⇒ 0 比 2 多一個。
3. n = 3 的全部 5 個字、運算式、樹：C_3 = 5。
4. 為什麼是 C_n：3 個 2、4 個 0 共 C(7,3) = 35 種排法；每種排法轉一圈的 7 種讀法中恰有 1 種是字 ⇒ 35/7 = 5。
5. 倒過來讀、0 走 +1、2 走 −1：一直在 0 之上、終點 1 的路徑；拿掉最後一步就是 Dyck 路徑。
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import catalan
from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import chu_heights, cyclic_variant, head_ranks, is_word, lists_with
from utils.raney_draw import WordTreeMob, chu_walk, level_line, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

W1 = (2, 0, 2, 0, 0)                       # a+(b+c) = +a+bc
WORDS3 = sorted(lists_with(1, (0, 3)), reverse=True)
EXPR3 = ["((a+b)+c)+d", "(a+(b+c))+d", "(a+b)+(c+d)", "a+((b+c)+d)", "a+(b+(c+d))"]
ROT = (0, 0, 2, 0, 2, 2, 0)                # 3 個 2、4 個 0 的一種排法，只有 k = 2 是字
DYCK_W = (2, 0, 2, 2, 0, 0, 0)


def need_counts(w):
    """還要幾個東西：從 1 開始，讀到 2 加 1、讀到 0 減 1。"""
    return [h + 1 for h in head_ranks(w)]


def check_math():
    assert is_word(W1) and need_counts(W1) == [1, 2, 1, 2, 1, 0]
    assert len(WORDS3) == 5 == catalan(3) and WORDS3[0] == (2, 2, 2, 0, 0, 0, 0) and WORDS3[-1] == (2, 0, 2, 0, 2, 0, 0)
    assert comb(7, 3) == 35 and 35 // 7 == 5
    rots = [cyclic_variant(ROT, k) for k in range(7)]
    assert [is_word(r) for r in rots].count(True) == 1 and is_word(rots[2])
    assert [comb(2 * n + 1, n) // (2 * n + 1) for n in range(1, 6)] == [catalan(n) for n in range(1, 6)] == [1, 2, 5, 14, 42]
    assert chu_heights(DYCK_W) == [0, 1, 2, 3, 2, 1, 2, 1]


class SceneN13CatalanWords(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N13　只有 2 和 0 的字：卡塔蘭數")

        # 1. 運算式 → 前序記法 → 字 → 樹
        e0 = Tex("a+(b+c)", font_size=60).move_to(1.8 * UP + 3 * LEFT)
        self.say("一個運算式：", "$a+(b+c)$")
        self.play(Write(e0))
        self.wait(1)
        e1 = Tex("+\\,a\\,+\\,b\\,c", font_size=60).move_to(0.4 * UP + 3 * LEFT)
        self.say("把運算子寫在它的兩個東西前面（前序記法），就不需要括號")
        self.play(TransformFromCopy(e0, e1))
        self.wait(1.5)
        tiles = word_tiles(W1, size=0.75, font_size=44).move_to(1.1 * DOWN + 3 * LEFT)
        arrows = VGroup(*[Arrow(e1[k].get_bottom(), tiles[k].get_top(), buff=0.12, thickness=2, fill_color=GREY_B)
                          for k in range(5)])
        self.say("再把 ", "$+$", " 換成 2（它要 2 個東西），字母換成 0（它是一個數，不要東西）")
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.15))
        self.play(LaggedStartMap(FadeIn, tiles, lag_ratio=0.15))
        self.wait(1.5)
        tree = WordTreeMob(W1, x_gap=0.8, y_gap=0.95, labels=["+", "a", "+", "b", "c"],
                           node_size=0.28, font_size=30).move_to(3.3 * RIGHT + 0.4 * UP)
        tlab = zh("同一棵樹：2 是分兩叉的節點，0 是樹葉", font_size=26).next_to(tree, DOWN, buff=0.45)
        assert_in_frame(e0, e1, tiles, tree, tlab)
        assert_apart(VGroup(e0, e1, tiles), tree)
        self.say("這串數字 ", "$20200$", " 叫做一個「字」（word），它就是一棵樹")
        self.play(FadeIn(tree, lag_ratio=0.1), FadeIn(tlab))
        self.wait(2.5)
        self.play(FadeOut(VGroup(e0, e1, arrows, tree, tlab)), tiles.animate.move_to(1.9 * UP))

        # 2. 計數器：0 比 2 多一個
        cnt = need_counts(W1)
        badges = VGroup()
        for k in range(6):
            c = Circle(radius=0.3, stroke_color=GREEN_C if cnt[k] else RED_C, stroke_width=3,
                       fill_color=GREEN_C if cnt[k] else RED_C, fill_opacity=0.2)
            badges.add(VGroup(c, Tex(str(cnt[k]), font_size=34).move_to(c)))
        gap = tiles[1].get_center()[0] - tiles[0].get_center()[0]
        x0 = tiles[0].get_center()[0] - gap / 2
        for k, b in enumerate(badges):
            b.move_to(np.array([x0 + k * gap, 0.6, 0]))
        rule = VGroup(
            mixed("「還要幾個東西」：一開始要 1 個（整個式子）", font_size=28),
            mixed("讀到 2：用掉 1 個位置、多要 2 個 ", "$\\Rightarrow +1$", font_size=28),
            mixed("讀到 0：填掉 1 個位置 ", "$\\Rightarrow -1$", font_size=28),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(1.4 * DOWN)
        assert_in_frame(tiles, badges, rule)
        self.say("怎麼看出一串 2 和 0 是不是字？數「還要幾個東西」")
        self.play(FadeIn(rule[0]), FadeIn(badges[0]))
        self.wait(1)
        self.play(FadeIn(rule[1:]))
        for k in range(1, 6):
            self.play(Indicate(tiles[k - 1], scale_factor=1.15), FadeIn(badges[k], shift=0.2 * RIGHT), run_time=0.7)
        self.say("一直 ", "$\\geq 1$", "，讀完最後一個才變成 0：這就是字")
        self.wait(2)
        conc = boxed(mixed("每個 2 讓需求 ", "$+1$", "、每個 0 讓需求 ", "$-1$", "：", "$n$", " 個 2 的字一定有 ", "$n+1$", " 個 0",
                           font_size=30)).move_to(1.4 * DOWN)
        assert_in_frame(conc)
        self.play(FadeOut(rule), FadeIn(conc))
        self.say("所以 ", "$n$", " 個 2 的字長度是 ", "$2n+1$")
        self.wait(3)
        self.play(FadeOut(VGroup(tiles, badges, conc)))

        # 3. n = 3 的五個字
        rows = VGroup()
        for w, ex in zip(WORDS3, EXPR3):
            t = word_tiles(w, size=0.42, font_size=26)
            e = Tex(ex, font_size=32)
            tr = WordTreeMob(w, x_gap=0.3, y_gap=0.2, node_size=0.13, edge_width=2)
            rows.add(VGroup(t, e, tr))
        for r in rows:
            r[0].move_to(np.array([-4.2, 0, 0]))
            r[1].move_to(np.array([-0.4, 0, 0]))
            r[2].move_to(np.array([3.4, 0, 0]))
        heads = VGroup(zh("字", font_size=26), zh("運算式", font_size=26), zh("樹", font_size=26))
        for h, x in zip(heads, (-4.2, -0.4, 3.4)):
            h.move_to(np.array([x, 2.65, 0]))
        ys = [1.85, 0.85, -0.15, -1.15, -2.15]
        for r, y in zip(rows, ys):
            for part in r:
                part.set_y(y)
        assert_in_frame(rows, heads)
        self.say("3 個 2（3 個加號）的字有幾個？全部列出來")
        self.play(FadeIn(heads))
        for r in rows:
            self.play(FadeIn(r, lag_ratio=0.1), run_time=0.9)
        self.wait(1)
        self.say("共 5 個：4 個字母加括號的 5 種方法，也是 5 棵滿二元樹 ", "$=C_3$")
        self.wait(3.5)
        self.play(FadeOut(VGroup(rows, heads)))

        # 4. 為什麼是 C_n：轉一圈只有一種讀法是字
        self.say("為什麼是卡塔蘭數？先不管規則，把 3 個 2、4 個 0 隨便排")
        allc = mixed("排法共 ", "$\\binom{7}{3}=35$", " 種", font_size=34).move_to(2.6 * UP)
        self.play(FadeIn(allc))
        rot_rows = VGroup()
        for k in range(7):
            r = cyclic_variant(ROT, k)
            t = word_tiles(r, size=0.36, font_size=22)
            ok = is_word(r)
            tag = Tex(r"\checkmark" if ok else r"\times", font_size=36, fill_color=GREEN if ok else RED)
            lab = Tex("k=%d" % k, font_size=26, fill_color=GREY_A)
            row = VGroup(lab, t, tag).arrange(RIGHT, buff=0.35)
            rot_rows.add(row)
        rot_rows.arrange(DOWN, buff=0.13, aligned_edge=LEFT).move_to(0.15 * DOWN + 2.2 * LEFT)
        side = VGroup(
            zh("同一串排成一圈，", font_size=28),
            zh("從 7 個位置開始讀，", font_size=28),
            zh("恰好 1 種是字（循環引理）", font_size=28),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(3.3 * RIGHT + 0.6 * UP)
        assert_in_frame(allc, rot_rows, side)
        assert_apart(rot_rows, side)
        self.play(FadeIn(rot_rows[0]))
        self.say("拿其中一種，從第 ", "$k$", " 個位置開始繞一圈讀（", "$k=0,\\ldots,6$", "）")
        self.play(LaggedStartMap(FadeIn, rot_rows[1:], lag_ratio=0.2), run_time=2.2)
        self.play(FadeIn(side))
        self.play(Indicate(rot_rows[2], scale_factor=1.06))
        self.wait(2)
        fm = boxed(mixed("$C_n=\\dfrac{1}{2n+1}\\dbinom{2n+1}{n}$", font_size=34)).move_to(3.3 * RIGHT + 1.7 * DOWN)
        assert_in_frame(fm)
        assert_apart(fm, rot_rows)
        self.say("35 種排法分成 7 個一組，每組恰好 1 個字：", "$35/7=5$")
        self.wait(2.5)
        self.say("一般的 ", "$n$", "：長度 ", "$2n+1$", "，排法 ", "$\\binom{2n+1}{n}$", " 種，除以 ", "$2n+1$")
        self.play(FadeIn(fm))
        nums = Tex(r"1,\ 2,\ 5,\ 14,\ 42,\ \ldots", font_size=34).next_to(fm, UP, buff=0.35)
        assert_in_frame(nums)
        self.play(FadeIn(nums))
        self.wait(3)
        self.play(FadeOut(VGroup(allc, rot_rows, side, fm, nums)))

        # 5. 倒過來讀 = 走路
        t = word_tiles(DYCK_W, size=0.55, font_size=32).move_to(2.3 * UP)
        self.say("最後換一種看法：把字倒過來讀，0 走上一步、2 走下一步")
        self.play(FadeIn(t))
        rev = t.copy()
        self.play(*[m.animate.move_to(t[len(DYCK_W) - 1 - k].get_center() + 1.0 * DOWN) for k, m in enumerate(rev)],
                  t.animate.set_opacity(0.3), run_time=1.5)
        steps = VGroup(*[Tex("+1" if x == 0 else "-1", font_size=28, fill_color=GREY_B if x == 0 else BLUE_C)
                         .next_to(m, DOWN, buff=0.15) for x, m in zip(DYCK_W, rev)])
        self.play(FadeIn(steps, lag_ratio=0.1))
        walk = chu_walk(DYCK_W, unit=0.5, origin=np.array([-1.75, -2.9, 0]))
        base = level_line(walk, 0, 0, 7, color=MAROON_B)
        assert_in_frame(t, rev, steps, walk, base)
        assert_apart(steps, walk)
        self.play(FadeIn(VGroup(base, walk.dots[0])))
        self.play(ShowCreation(walk.steps, lag_ratio=1), FadeIn(walk.dots), run_time=2.5)
        self.say("出發後一直在 0 之上，終點高度 1；拿掉最後一步，就是 Dyck 路徑（場景 00g）")
        self.wait(3)
        self.say("記住這條路：下一段把 2 換成更多種符號，就是 Chu 的推廣")
        self.wait(2.5)
        self.play(FadeOut(VGroup(t, rev, steps, walk, base)))
        self.clear_caption()
