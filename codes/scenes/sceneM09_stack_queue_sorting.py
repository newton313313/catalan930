"""
Scene M09 —— 堆疊排序與「佇列＋插隊線」排序（MIT 18.212 第 3 講）

    堆疊（後進先出）：頂端正好是下一個要輸出的數就彈出，否則推入下一個輸入；輸入用完而頂端不對 -> 失敗
    佇列＋插隊線（先進先出）：佇列頭是下一個要輸出的就出列；否則下一個輸入正好是它就走插隊線，
                               不是就排到佇列尾；輸入用完而佇列頭不對 -> 失敗
    堆疊可排序 <=> 避開 231；佇列＋插隊線可排序 <=> 避開 321；兩者都有 C_n 個。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM09_stack_queue_sorting.py SceneM09StackQueueSorting
"""
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import avoiders, catalan, contains_pattern, queue_bypass_sort, sort_states, stack_sort
from utils.mit_draw import perm_row
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh

STACK_OK = "4213"        # 可以用堆疊排好（避開 231）
STACK_BAD = "231"        # 堆疊排不出來
QUEUE_OK = "231"         # 佇列＋插隊線排得出來
QUEUE_BAD = "321"        # 佇列＋插隊線排不出來

SIZE = 0.6               # 方塊邊長
PITCH = 0.7              # 相鄰方塊中心距離
BOX_COLOR = GREY_A

# 堆疊場景的位置
S_Y = 1.2                # 輸入／輸出那一排的高度
S_IN_X0 = 1.5            # 第一個輸入方塊
S_OUT_X0 = -4.6          # 第一個輸出格
S_TOP = 0.75             # 堆疊開口
S_BOTTOM = -2.15         # 堆疊底
S_HALF = 0.42            # 堆疊半寬
S_LEFT_X = -3.7          # 左側說明欄中心

# 佇列場景的位置
Q_Y = 0.9
Q_IN_X0 = 2.0
Q_OUT_X0 = -4.4
Q_X0 = -0.7              # 佇列頭那一格
Q_HALF_LEN = 1.15
Q_HALF_H = 0.4
BYPASS_X = 1.55
BYPASS_Y = 2.1
Q_LEFT_X = -3.7


# ----------------------------------------------------------------------- 位置
def row_pos(x0, k, y):
    return np.array([x0 + k * PITCH, y, 0.0])


def stack_pos(level):
    return np.array([0.0, S_BOTTOM + 0.05 + SIZE / 2 + level * PITCH, 0.0])


def queue_pos(k):
    return np.array([Q_X0 + k * PITCH, Q_Y, 0.0])


def polyline_point(pts, a):
    """折線上依長度比例 a 的點。"""
    lens = [get_norm(q - p) for p, q in zip(pts[:-1], pts[1:])]
    total = sum(lens)
    if total == 0:
        return pts[-1]
    d = a * total
    for p, q, L in zip(pts[:-1], pts[1:], lens):
        if d <= L and L > 0:
            return p + (q - p) * (d / L)
        d -= L
    return pts[-1]


def travel(box, pts, color=None, run_time=0.6):
    """方塊沿折線移動；給 color 時順便把方框換色。"""
    pts = [np.array(p, dtype=float) for p in pts]
    c0 = box.square.get_stroke_color()

    def upd(m, a):
        m.move_to(polyline_point(pts, a))
        if color is not None:
            c = interpolate_color(c0, color, a)
            m.square.set_stroke(c)
            m.square.set_fill(c, opacity=0.15 + 0.2 * a)

    return UpdateFromAlphaFunc(box, upd, run_time=run_time)


def recolor(box, color, opacity=0.35):
    box.square.set_stroke(color)
    box.square.set_fill(color, opacity=opacity)
    return box


# ----------------------------------------------------------------------- 小物件
def tick_mob(size=0.42, color=OK_COLOR):
    t = VMobject().set_points_as_corners([[-0.5, 0.0, 0.0], [-0.15, -0.38, 0.0], [0.5, 0.42, 0.0]])
    t.set_stroke(color, width=7).set_fill(opacity=0)
    return t.set_width(size)


def cross_mob(size=0.36, color=CROSSING_COLOR):
    h = size / 2
    return VGroup(Line([-h, -h, 0], [h, h, 0]), Line([-h, h, 0], [h, -h, 0])).set_stroke(color, width=7)


def slots(n, x0, y):
    return VGroup(*[DashedVMobject(Square(side_length=SIZE), num_dashes=16).set_stroke(GREY_C, width=2)
                    .move_to(row_pos(x0, k, y)) for k in range(n)])


def input_boxes(perm, x0, y):
    row = perm_row([int(c) for c in perm], size=SIZE, buff=PITCH - SIZE, color=BOX_COLOR, font_size=34)
    row.shift(row_pos(x0, 0, y) - row[0].get_center())
    return row


def need_mob(need, n, pos):
    if need > n:
        mob = zh("全部輸出完畢", font_size=26, color=OK_COLOR)
    else:
        mob = mixed("下一個要輸出：", Tex(str(need), font_size=36, fill_color=YELLOW), font_size=26)
    return mob.move_to(pos)


def action_mob(kind, op, x, need, head, pos):
    """說明這一步為什麼這樣做（kind = 'stack' / 'queue'）。"""
    arrow = "$\\Rightarrow$"
    fs = 24
    if kind == "stack":
        if op == "push":
            if head is None:
                mob = mixed("堆疊是空的", arrow, f"推入 {x}", font_size=fs)
            else:
                mob = mixed("頂端", f"${head}\\neq {need}$", arrow, f"推入 {x}", font_size=fs)
        else:
            mob = mixed("頂端", f"$={need}$", arrow, "彈出", font_size=fs)
    else:
        if op == "push":
            mob = mixed("下一個輸入", f"${x}\\neq {need}$", arrow, "排到佇列尾", font_size=fs)
        elif op == "bypass":
            mob = mixed("下一個輸入", f"${x}={need}$", arrow, "走插隊線", font_size=fs, color=YELLOW)
        else:
            mob = mixed("佇列頭", f"$={need}$", arrow, "出列", font_size=fs)
    return mob.move_to(pos)


def swap_mob(scene_anims, holder, key, new):
    old = holder.get(key)
    if old is not None:
        scene_anims.append(FadeOut(old))
    scene_anims.append(FadeIn(new))
    holder[key] = new


# ----------------------------------------------------------------------- 執行排序
def run_sort(scene, perm, kind, boxes, holder, step_time=0.65):
    """
    依 counting.py 的 ops 一步一步移動方塊，每一步都和 sort_states 比對。
    holder 放左側的「下一個要輸出」「這一步」兩個說明物件。回傳 (ok, 容器, 輸出)。
    """
    sorter = stack_sort if kind == "stack" else queue_bypass_sort
    ok, ops = sorter(perm)
    states = sort_states(perm, ops)
    n = len(perm)
    by_value = {b.value: b for b in boxes}
    if kind == "stack":
        y, out_x0, left_x = S_Y, S_OUT_X0, S_LEFT_X
        need_pos, act_pos = np.array([left_x, 0.35, 0]), np.array([left_x, -0.35, 0])
    else:
        y, out_x0, left_x = Q_Y, Q_OUT_X0, Q_LEFT_X
        need_pos, act_pos = np.array([left_x, 0.05, 0]), np.array([left_x, -0.6, 0])

    inp, box, out = [int(c) for c in perm], [], []
    for step, (op, x) in enumerate(ops):
        need = len(out) + 1
        b = by_value[x]
        anims = []
        if kind == "stack":
            head = box[-1] if box else None
        else:
            head = box[0] if box else None
        swap_mob(anims, holder, "act", action_mob(kind, op, x, need, head, act_pos))
        if op == "push":
            assert inp[0] == x and head != need
            if kind == "queue":
                assert x != need
            inp.pop(0)
            if kind == "stack":
                pts = [b.get_center(), [0.0, y, 0.0], stack_pos(len(box))]
            else:
                pts = [b.get_center(), queue_pos(len(box))]
            box.append(x)
            anims.append(travel(b, pts, run_time=step_time))
        elif op == "pop":
            assert head == x == need
            target = row_pos(out_x0, len(out), y)
            if kind == "stack":
                box.pop()
                pts = [b.get_center(), [0.0, y, 0.0], target]
            else:
                box.pop(0)
                pts = [b.get_center(), target]
                for k, v in enumerate(box):
                    anims.append(by_value[v].animate.move_to(queue_pos(k)))
            out.append(x)
            anims.append(travel(b, pts, color=OK_COLOR, run_time=step_time))
            swap_mob(anims, holder, "need", need_mob(len(out) + 1, n, need_pos))
        else:   # bypass
            assert kind == "queue" and inp[0] == x == need and head != need
            inp.pop(0)
            target = row_pos(out_x0, len(out), y)
            pts = [b.get_center(), [BYPASS_X, y, 0], [BYPASS_X, BYPASS_Y, 0], [-BYPASS_X, BYPASS_Y, 0],
                   [-BYPASS_X, y, 0], target]
            out.append(x)
            anims.append(travel(b, pts, color=OK_COLOR, run_time=step_time * 1.6))
            swap_mob(anims, holder, "need", need_mob(len(out) + 1, n, need_pos))
        scene.play(*anims, run_time=step_time * (1.6 if op == "bypass" else 1.0))
        assert (tuple(inp), tuple(box), tuple(out)) == states[step + 1]
    assert ok == (len(out) == n)
    if not ok:
        assert not inp and box
    return ok, box, out


def show_failure(scene, kind, boxes, box, out, holder):
    """卡住了：把擋路的方塊標紅、要的方塊框黃（數字要看得到，不蓋叉）。"""
    by_value = {b.value: b for b in boxes}
    need = len(out) + 1
    head = box[-1] if kind == "stack" else box[0]
    assert head != need and need in box
    blocker, wanted = by_value[head], by_value[need]
    left_x = S_LEFT_X if kind == "stack" else Q_LEFT_X
    act_y = -0.35 if kind == "stack" else -0.6
    word = "頂端" if kind == "stack" else "佇列頭"
    act = mixed("輸入用完，" + word, f"${head}\\neq {need}$", "$\\Rightarrow$", "失敗",
                font_size=24, color=CROSSING_COLOR).move_to(np.array([left_x, act_y, 0]))
    anims = []
    swap_mob(anims, holder, "act", act)
    wanted_ring = SurroundingRectangle(wanted.square, buff=0.06, color=YELLOW, stroke_width=4)
    scene.play(*anims, blocker.square.animate.set_stroke(CROSSING_COLOR).set_fill(CROSSING_COLOR, opacity=0.35),
               ShowCreation(wanted_ring), run_time=0.8)
    return wanted_ring, head, need


def status_mob(perm, ok, pos):
    if ok:
        mob = zh(f"{perm}：可以排序", font_size=30, color=OK_COLOR)
        mob = VGroup(mob, tick_mob(0.4).next_to(mob, RIGHT, buff=0.2))
    else:
        mob = zh(f"{perm}：排不出來", font_size=30, color=CROSSING_COLOR)
        mob = VGroup(mob, cross_mob(0.32).next_to(mob, RIGHT, buff=0.2))
    return mob.move_to(pos)


def rules_panel(lines, top_right):
    body = VGroup(*lines).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    rect = SurroundingRectangle(body, buff=0.2, color=GREY_C, stroke_width=2)
    panel = VGroup(rect, body)
    panel.shift(top_right - panel.get_corner(UR))
    return panel


def in_frame(mob, xmax=6.8, ymin=-3.0, ymax=3.2):
    return (mob.get_left()[0] >= -xmax and mob.get_right()[0] <= xmax
            and mob.get_bottom()[1] >= ymin and mob.get_top()[1] <= ymax)


def disjoint(a, b, gap=0.02):
    return (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
            or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])


# ----------------------------------------------------------------------- 場景
class SceneM09StackQueueSorting(ChuScene):
    def construct(self):
        self.show_header("用堆疊、佇列排序")

        # ---------------------------------------------------------- 數學檢查
        assert stack_sort(STACK_OK)[0] and not stack_sort(STACK_BAD)[0]
        assert queue_bypass_sort(QUEUE_OK)[0] and not queue_bypass_sort(QUEUE_BAD)[0]
        assert contains_pattern(STACK_OK, "231") is None and contains_pattern(STACK_BAD, "231") is not None
        assert contains_pattern(QUEUE_OK, "321") is None and contains_pattern(QUEUE_BAD, "321") is not None
        counts = {}
        for n in (3, 4):
            perms = list(permutations(range(1, n + 1)))
            ss = {p for p in perms if stack_sort(p)[0]}
            qs = {p for p in perms if queue_bypass_sort(p)[0]}
            assert ss == set(avoiders(n, "231")) and qs == set(avoiders(n, "321"))
            assert len(ss) == len(qs) == catalan(n)
            counts[n] = len(ss)
        assert counts == {3: 5, 4: 14}

        # ========================================================== 1. 堆疊
        walls = VGroup(
            Line([-S_HALF, S_TOP, 0], [-S_HALF, S_BOTTOM, 0]),
            Line([-S_HALF, S_BOTTOM, 0], [S_HALF, S_BOTTOM, 0]),
            Line([S_HALF, S_BOTTOM, 0], [S_HALF, S_TOP, 0]),
        ).set_stroke(GREY_B, width=4)
        stack_lab = mixed("堆疊（後進先出）", font_size=24).next_to(walls, DOWN, buff=0.15)
        push_arrow = Arrow([0.78, 0.6, 0], [0.78, -0.2, 0], buff=0, stroke_width=4, fill_color=GREY_B)
        pop_arrow = Arrow([-0.78, -0.2, 0], [-0.78, 0.6, 0], buff=0, stroke_width=4, fill_color=GREY_B)
        push_lab = zh("推入", font_size=22, color=GREY_B).next_to(push_arrow, RIGHT, buff=0.1)
        pop_lab = zh("彈出", font_size=22, color=GREY_B).next_to(pop_arrow, LEFT, buff=0.1)
        n = len(STACK_OK)
        inbox = input_boxes(STACK_OK, S_IN_X0, S_Y)
        outslots = slots(n, S_OUT_X0, S_Y)
        in_lab = zh("輸入", font_size=26, color=MUTED_COLOR).next_to(inbox, UP, buff=0.2)
        out_lab = zh("輸出", font_size=26, color=MUTED_COLOR).next_to(outslots, UP, buff=0.2)
        apparatus = VGroup(walls, stack_lab, push_arrow, pop_arrow, push_lab, pop_lab)

        self.say("堆疊：後放進去的先拿出來，只能從頂端放、從頂端拿")
        self.play(ShowCreation(walls), FadeIn(stack_lab), run_time=0.8)
        self.play(FadeIn(inbox, shift=0.2 * LEFT), FadeIn(in_lab), ShowCreation(outslots), FadeIn(out_lab),
                  GrowArrow(push_arrow), GrowArrow(pop_arrow), FadeIn(push_lab), FadeIn(pop_lab), run_time=1.0)
        self.wait(0.8)

        rules = rules_panel([
            zh("每一步：", font_size=24, color=MUTED_COLOR),
            mixed("頂端是下一個要輸出的數", "$\\Rightarrow$", "彈出", font_size=24),
            mixed("否則", "$\\Rightarrow$", "推入下一個輸入", font_size=24),
            mixed("輸入用完而頂端不對", "$\\Rightarrow$", "失敗", font_size=24),
        ], np.array([6.6, -0.25, 0]))
        holder = {}
        need0 = need_mob(1, n, np.array([S_LEFT_X, 0.35, 0]))
        holder["need"] = need0
        goal = ", ".join(str(k) for k in range(1, n + 1))
        self.say(f"目標：依序輸出 {goal}")
        self.play(FadeIn(rules), FadeIn(need0), run_time=0.8)
        self.wait(1.0)

        # 版面檢查
        for m in (walls, stack_lab, push_lab, pop_lab, inbox, outslots, in_lab, out_lab, rules, need0):
            assert in_frame(m), m
        for a, b in ((rules, push_lab), (rules, inbox), (rules, walls), (rules, stack_lab), (need0, pop_lab),
                     (need0, outslots), (push_lab, inbox)):
            assert disjoint(a, b)

        self.say(f"例：{STACK_OK}，照規則一步一步做")
        ok, box, out = run_sort(self, STACK_OK, "stack", inbox, holder)
        assert ok and out == list(range(1, n + 1))
        status = status_mob(STACK_OK, True, np.array([S_LEFT_X, -1.3, 0]))
        self.play(FadeIn(status, shift=0.2 * UP), run_time=0.6)
        self.say(f"{STACK_OK} 可以用一個堆疊排好", wait=1.2)
        for m in (holder["act"], status):
            assert in_frame(m) and disjoint(m, pop_lab) and disjoint(m, walls)

        # ---------------------------------------------------------- 231 失敗
        n2 = len(STACK_BAD)
        inbox2 = input_boxes(STACK_BAD, S_IN_X0, S_Y)
        outslots2 = slots(n2, S_OUT_X0, S_Y)
        in_lab2 = zh("輸入", font_size=26, color=MUTED_COLOR).next_to(inbox2, UP, buff=0.2)
        out_lab2 = zh("輸出", font_size=26, color=MUTED_COLOR).next_to(outslots2, UP, buff=0.2)
        new_need = need_mob(1, n2, np.array([S_LEFT_X, 0.35, 0]))
        self.say(f"再試 {STACK_BAD}")
        self.play(FadeOut(inbox), FadeOut(outslots), FadeOut(in_lab), FadeOut(out_lab), FadeOut(status),
                  FadeOut(holder.pop("act")), FadeOut(holder["need"]), run_time=0.6)
        holder["need"] = new_need
        self.play(FadeIn(inbox2, shift=0.2 * LEFT), ShowCreation(outslots2), FadeIn(in_lab2), FadeIn(out_lab2),
                  FadeIn(new_need), run_time=0.8)
        ok, box, out = run_sort(self, STACK_BAD, "stack", inbox2, holder)
        assert not ok
        marks, head, need = show_failure(self, "stack", inbox2, box, out, holder)
        assert (head, need) == (3, 2)
        assert in_frame(holder["act"]) and disjoint(holder["act"], pop_lab, gap=0.1) and disjoint(holder["act"], walls)
        status2 = status_mob(STACK_BAD, False, np.array([S_LEFT_X, -1.3, 0]))
        self.play(FadeIn(status2, shift=0.2 * UP), run_time=0.5)
        self.say(f"要輸出 {need}，可是 {need} 被 {head} 壓在下面 ", "$\\Rightarrow$", " 卡住了", wait=2.0)
        self.say("只要出現「中、大、小」（231 模式），大的就一定壓住中的", wait=2.4)

        # ========================================================== 2. 佇列＋插隊線
        self.clear_stage()
        tube = VGroup(
            Line([-Q_HALF_LEN, Q_Y + Q_HALF_H, 0], [Q_HALF_LEN, Q_Y + Q_HALF_H, 0]),
            Line([-Q_HALF_LEN, Q_Y - Q_HALF_H, 0], [Q_HALF_LEN, Q_Y - Q_HALF_H, 0]),
        ).set_stroke(GREY_B, width=4)
        q_lab = zh("佇列（先進先出）", font_size=24).next_to(tube, DOWN, buff=0.2)
        head_lab = zh("頭", font_size=20, color=MUTED_COLOR).next_to(tube[0].get_left(), UP, buff=0.12).shift(0.25 * RIGHT)
        tail_lab = zh("尾", font_size=20, color=MUTED_COLOR).next_to(tube[0].get_right(), UP, buff=0.12).shift(0.25 * LEFT)
        bypass = VMobject().set_points_as_corners([
            [BYPASS_X, Q_Y, 0], [BYPASS_X, BYPASS_Y, 0], [-BYPASS_X, BYPASS_Y, 0], [-BYPASS_X, Q_Y, 0]])
        bypass = DashedVMobject(bypass, num_dashes=40).set_stroke(YELLOW, width=3)
        bypass_lab = zh("插隊線", font_size=24, color=YELLOW).move_to([0, BYPASS_Y + 0.35, 0])
        n3 = len(QUEUE_OK)
        inbox3 = input_boxes(QUEUE_OK, Q_IN_X0, Q_Y)
        outslots3 = slots(n3, Q_OUT_X0, Q_Y)
        in_lab3 = zh("輸入", font_size=26, color=MUTED_COLOR).next_to(inbox3, UP, buff=0.2)
        out_lab3 = zh("輸出", font_size=26, color=MUTED_COLOR).next_to(outslots3, UP, buff=0.2)

        self.say("佇列：先排隊的先出去；另外有一條插隊線")
        self.play(ShowCreation(tube), FadeIn(q_lab), FadeIn(head_lab), FadeIn(tail_lab), run_time=0.8)
        self.play(ShowCreation(bypass), FadeIn(bypass_lab), FadeIn(inbox3, shift=0.2 * LEFT), FadeIn(in_lab3),
                  ShowCreation(outslots3), FadeIn(out_lab3), run_time=1.0)
        q_rules = rules_panel([
            zh("每一步：", font_size=23, color=MUTED_COLOR),
            mixed("佇列頭是下一個要輸出的數", "$\\Rightarrow$", "出列", font_size=23),
            mixed("否則，下一個輸入正好是它", "$\\Rightarrow$", "走插隊線", font_size=23),
            mixed("否則", "$\\Rightarrow$", "下一個輸入排到佇列尾", font_size=23),
            mixed("輸入用完而佇列頭不對", "$\\Rightarrow$", "失敗", font_size=23),
        ], np.array([6.6, -0.3, 0]))
        note = zh("註：佇列排序有幾種版本，本片採用「佇列＋插隊線」", font_size=19, color=MUTED_COLOR)
        note.move_to(np.array([Q_LEFT_X, -2.55, 0]))
        holder = {"need": need_mob(1, n3, np.array([Q_LEFT_X, 0.05, 0]))}
        self.say("正好輪到的數可以走插隊線直接輸出，其他的排隊")
        self.play(FadeIn(q_rules), FadeIn(note), FadeIn(holder["need"]), run_time=0.8)
        self.wait(1.4)

        for m in (tube, q_lab, head_lab, tail_lab, bypass, bypass_lab, inbox3, outslots3, in_lab3, out_lab3,
                  q_rules, note, holder["need"]):
            assert in_frame(m), m
        for a, b in ((q_rules, inbox3), (q_rules, q_lab), (q_rules, note), (bypass_lab, in_lab3),
                     (bypass_lab, out_lab3), (holder["need"], q_lab), (head_lab, tail_lab)):
            assert disjoint(a, b)
        assert inbox3[0].get_left()[0] > BYPASS_X + 0.05 and outslots3[-1].get_right()[0] < -BYPASS_X - 0.05

        self.say(f"用同樣的 {QUEUE_OK} 試試看")
        ok, box, out = run_sort(self, QUEUE_OK, "queue", inbox3, holder)
        assert ok and out == list(range(1, n3 + 1))
        status3 = status_mob(QUEUE_OK, True, np.array([Q_LEFT_X, -1.45, 0]))
        self.play(FadeIn(status3, shift=0.2 * UP), run_time=0.6)
        self.say(f"{QUEUE_OK} 用佇列＋插隊線就排得出來", wait=1.2)
        for m in (holder["act"], status3):
            assert in_frame(m) and disjoint(m, q_lab) and disjoint(m, note) and disjoint(m, tube)

        # ---------------------------------------------------------- 321 失敗
        n4 = len(QUEUE_BAD)
        inbox4 = input_boxes(QUEUE_BAD, Q_IN_X0, Q_Y)
        new_need = need_mob(1, n4, np.array([Q_LEFT_X, 0.05, 0]))
        self.say(f"換成 {QUEUE_BAD}")
        self.play(FadeOut(inbox3), FadeOut(status3), FadeOut(holder.pop("act")), FadeOut(holder["need"]),
                  run_time=0.6)
        holder["need"] = new_need
        self.play(FadeIn(inbox4, shift=0.2 * LEFT), FadeIn(new_need), run_time=0.7)
        ok, box, out = run_sort(self, QUEUE_BAD, "queue", inbox4, holder)
        assert not ok
        marks, head, need = show_failure(self, "queue", inbox4, box, out, holder)
        assert (head, need) == (3, 2)
        assert in_frame(holder["act"]) and disjoint(holder["act"], q_lab) and disjoint(holder["act"], bypass)
        status4 = status_mob(QUEUE_BAD, False, np.array([Q_LEFT_X, -1.45, 0]))
        self.play(FadeIn(status4, shift=0.2 * UP), run_time=0.5)
        self.say(f"要輸出 {need}，可是 {head} 先排隊，擋在 {need} 前面 ", "$\\Rightarrow$", " 卡住了", wait=2.0)
        self.say("只要出現「大、中、小」（321 模式），大的就一定擋在中的前面", wait=2.2)

        # ========================================================== 3. 結論
        self.clear_stage()
        perms3 = list(permutations((1, 2, 3)))
        xs = [-2.4 + 1.25 * k for k in range(len(perms3))]
        title = mixed("$n=3$", f"的 {len(perms3)} 個排列", font_size=28, color=MUTED_COLOR).move_to([0.7, 2.55, 0])
        ptexts = VGroup(*[Tex("".join(map(str, p)), font_size=44).move_to([x, 1.85, 0]) for x, p in zip(xs, perms3)])
        row_y = (1.05, 0.25)
        row_labs = VGroup(
            zh("堆疊", font_size=26),
            zh("佇列＋插隊線", font_size=26),
        )
        for lab, yy in zip(row_labs, row_y):
            lab.move_to([0, yy, 0]).align_to(np.array([xs[0] - 0.75, 0, 0]), RIGHT)
        marks = VGroup()
        fails = {}
        for r, sorter in enumerate((stack_sort, queue_bypass_sort)):
            for x, p in zip(xs, perms3):
                ok = sorter(p)[0]
                if not ok:
                    fails.setdefault(r, []).append(p)
                marks.add((tick_mob(0.42) if ok else cross_mob(0.34)).move_to([x, row_y[r], 0]))
        assert fails == {0: [(2, 3, 1)], 1: [(3, 2, 1)]}
        self.say("$n=3$", f"的 {len(perms3)} 個排列，兩種方法各試一次")
        self.play(FadeIn(title), LaggedStart(*[FadeIn(t, shift=0.15 * DOWN) for t in ptexts], lag_ratio=0.12),
                  FadeIn(row_labs), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in marks], lag_ratio=0.06), run_time=1.6)
        # 只框住打叉的那一格（321 那一行的堆疊是打勾，不能一起框進去）
        bad_cols = VGroup(*[
            SurroundingRectangle(marks[r * len(perms3) + perms3.index(fails[r][0])],
                                 buff=0.12, color=CROSSING_COLOR, stroke_width=3)
            for r in (0, 1)])
        bad_heads = VGroup(*[ptexts[perms3.index(fails[r][0])] for r in (0, 1)])
        self.say("堆疊只排不了 231，佇列＋插隊線只排不了 321")
        self.play(ShowCreation(bad_cols), bad_heads.animate.set_color(YELLOW), run_time=0.8)
        self.wait(1.4)

        thm = VGroup(
            mixed("堆疊可排序", "$\\Longleftrightarrow$", "避開 231", font_size=28),
            mixed("佇列＋插隊線可排序", "$\\Longleftrightarrow$", "避開 321", font_size=28),
            mixed("可排序的個數都是", "$C_n$", "：", "$n=3$", f"有 {counts[3]} 個，", "$n=4$", f"有 {counts[4]} 個",
                  font_size=26, t2c={"C_n": BLUE}),
        ).arrange(DOWN, buff=0.25)
        thm_box = SurroundingRectangle(thm, buff=0.25, color=YELLOW, stroke_width=3)
        thm_all = VGroup(thm_box, thm).move_to([0.3, -1.45, 0])
        for m in (title, ptexts, row_labs, marks, bad_cols, thm_all):
            assert in_frame(m), m
        assert disjoint(thm_all, marks) and disjoint(thm_all, row_labs) and disjoint(row_labs, marks)
        assert disjoint(title, ptexts)
        self.say("定理：長度", "$n$", "的排列中，兩種方法可排序的都恰好有", "$C_n$", "個")
        self.play(FadeIn(thm[0]), FadeIn(thm[1]), ShowCreation(thm_box), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(thm[2], shift=0.15 * UP), run_time=0.7)
        self.wait(2.5)
