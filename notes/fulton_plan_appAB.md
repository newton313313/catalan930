# Fulton《Young Tableaux》附錄 A–B → Manim：大綱、檢討與定稿（2026-10-16）

> 本檔的相對路徑以 `C:\mypython\manim\projects\catalan930\` 為基準。來源：`../ref/fulton/md/A_combinatorial-variations.md`（書 p.183–210）、
> `../ref/fulton/md/B_on-the-topology-of-algebraic-varieties.md`（p.211–225）；例子圖從 `../ref/fulton/combinatorial-variations.pdf` 讀出。
> 場景 F56–F65，獨立連續播放 `FultonDemo7`；舊影片不動。流程同 `notes/fulton_plan_ch9-10.md`：§1 草稿 → §2 生動度 → §3 例子 → §4 程式 → §5 省 token → §6 定稿（代理人只讀 §6–§8）。

## 1. 草稿大綱（11 幕）
| 草稿 | 主題 | Fulton |
|---|---|---|
| D1 | 對偶字母、evacuation、對偶定理 | §A.1 |
| D2 | 行插入（column bumping） | §A.2 |
| D3 | 形狀改變定理與 LR 對應 | §A.3 |
| D4 | Burge 對應 | §A.4.1 |
| D5 | 矩陣的四個角 | §A.4.2 |
| D6 | 0-1 矩陣、對偶 Cauchy、Gale–Ryser | §A.4.3 |
| D7 | 左右鑰匙 | §A.5 |
| D8 | 奇異同調與 Borel–Moore 同調 | §B.1–B.2 |
| D9 | 子簇的類、胞腔給出基底 | §B.3 |
| D10 | Chern 類 | §B.4 |
| D11 | 全書回顧 | — |

## 2. 生動度檢討
- **D3（形狀改變定理）與 D8（同調的定義）太抽象**，畫面只能堆定義。→ D3 縮成 F56 的一個段落（「對偶給出 $c^\nu_{\lambda\mu}=c^\nu_{\mu\lambda}$ 的一一對應；§A.3 把它推廣成 LR 對應」）；D8 不單獨做，只在 F62 用一句話交代「同調＝數洞」。
- **D1 evacuation**：做成「拆積木」：一次拿走左上角、其餘滑過來、空格填上 $x^*$；書上 15 格的例子快轉，先用 4 格的小例子慢慢做。
- **D2 行插入**：和第 1 章的列插入左右並排「打擂台」，最後兩邊得到同一個 $P$。
- **D5 四個角**：「同一個矩陣從四個角看」——四個角各放一個觀察者，各自得到一對表，揭曉它們之間只差 $^*$。
- **D6 Gale–Ryser**：當成填格子遊戲：「列和 $(3,2,1)$、行和 $(2,2,2)$ 填得出來嗎？$(3,3)$ 與 $(3,1,1,1)$ 呢？」先讓觀眾猜。
- **D7 鑰匙**：用「把行重新排隊」的動畫：同一張表的行換順序（frank 斜表），最左邊那一行只跟它的長度有關。
- **D9–D10**：用「數格子＝數洞」「交點＝乘法」把拓撲講成計數；結尾回收第 10 章：Whitney 公式 $\prod(1-x_i)=1$ 一次解釋為什麼 $e_k=0$。
- **加 D11 全書回顧**：一張地圖把 F01–F64 串起來，當整個系列的結尾。

## 3. 例子檢討（每幕一個小例子算到底＋一個書上的例子）
| 幕 | 小例子 | 書上／較大的例子 |
|---|---|---|
| F56 | $T=\yts{12,3}$（$N=3$）逐步 evacuation；字 $3121$ 的 $w^*=3231$ | 書 p.184：$T=1223/2355/446/56$，$T^*=1123/2235/445/56$（$=6^*6^*5^*4^*/\cdots$） |
| F57 | 行插入 $1$、$2$ 到 $\yts{13,2}$ | 字 $24135$：列插入與逆序行插入得同一個 $P$；$P(w^{\rm rev})=P(w)^T$ |
| F58 | — | 書 p.199 的矩陣 $A=\begin{pmatrix}1&2&0\\0&1&1\\1&1&1\end{pmatrix}$：反字典序陣列、$(R,S)$ |
| F59 | 同一個 $A$：四個角的四對表 | 用所有 $2\times2$ 矩陣核對過（程式） |
| F60 | $\begin{pmatrix}0&1&1\\1&0&1\\1&0&1\end{pmatrix}$ → $P=112/333$、$Q=11/22/33$（共軛形狀） | Gale–Ryser：$(3,2,1)$/$(2,2,2)$ 有 3 個；$(3,3)$/$(3,1,1,1)$ 沒有 |
| F61 | $\yts{12,3}$ 的鑰匙 | 書 p.209–210：$T=1122/233/4$，frank 斜表 $(2,3,2,1)$，$K_-=1111/222/4$、$K_+=2222/333/4$ |
| F62 | $\mathbb P^2$：胞腔 $1,1,1$ → Betti $1,0,1,0,1$，$\chi=3$ | $Gr(2,4)$：$1,0,1,0,2,0,1,0,1$，$\chi=6$；$Fl(3)$：$\chi=6$ |
| F63 | $\mathbb P^2$ 裡直線與圓錐交 2 點（Bézout） | $Gr(2,4)\subset\mathbb P^5$ 的次數 $=\sigma_1^4=2$（二次超曲面）；$Gr(2,5)$：5；$\mathbb P^1\times\mathbb P^1\subset\mathbb P^3$：$(h_1+h_2)^2=2h_1h_2$ |
| F64 | $c(T\mathbb P^2)=(1+h)^3=1+3h+3h^2$，$c_2=3=\chi$ | $Fl(m)$：$\prod(1-x_i)=1$ ⇒ $e_k(x)=0$（第 10 章命題 3）；射影叢公式 |
| F65 | — | 全書地圖 |

## 4. 程式大綱（已完成）
- `codes/utils/fulton_appendix.py`（純 Python，`python utils/fulton_appendix.py` 自我測試；書上 p.184 的 $T^*$、p.209 的 frank 斜表、p.210 的鑰匙逐格重現；
  定理 1 的四個角用所有 $2\times2$ 矩陣核對；0-1 對應在 $3\times3$ 全部 511 個矩陣上一一對應；練習 19、20 在 $n\le5$ 全部核對）：
  `dual_word`、`evacuation`、`evacuation_steps`、`column_insert`、`column_insert_word`、`matrix_to_pairs`、`lex_sort`、`antilex_sort`、`rsk_array`、`burge`、`corners`、
  `dual_rsk`、`zero_one_matrices`、`gale_ryser`、`compact_skew`、`frank_tableau`、`keys`、`betti_from_cells`、`chern_projective`、`plucker_degree`。
- 既有可用：`utils.tableaux`（`insert_word`、`row_insert`、`rsk`、`rectify`、`transpose`、`kostka`、`conjugate`、`standard_tableaux`）、`utils.schubert`（`gaussian_binomial`、`q_factorial`、
  `box_product`、`grass_cell_pattern`）、`utils.fulton_draw`（`tableau_mob`、`SkewMob`、`TwoRowArray`、`BallMatrixMob`、`assert_in_frame`）、`utils.rep_draw.MatrixMob`、
  `utils.schubert_draw`（`CellMatrixMob`、`BoxDiagramMob`）。不新增畫圖模組。

## 5. 省 token 檢討
- 11 幕 → **10 幕**：D3 併入 F56、D8 併入 F62；保留 D11 回顧當全系列結尾。
- 不另做畫圖模組、不新增資料檔；數學都在 `fulton_appendix.py`，代理人不讀 Fulton 原文。
- 2 個代理人平行（A：F56–F60，B：F61–F65）；每幕最多 2 次 render_check；我只看 `--tile 480` 總覽圖；全部回報後才逐支輸出 1080p。
- 講義（附錄 A–B 兩節）由我在代理人工作時同步撰寫，數字用同一個模組核對。

## 6. 定稿場景卡（代理人讀這裡）
共同：每幕 2–3 分鐘；開頭一個問題、結尾一句收束；字幕繁中；Fulton 記號（$T^*$、$w^*$、$P,Q$、$R,S$、$K_\pm(T)$、$[V]$、$c_i$）。
表的對偶：在 $[N]$ 上 $x^*=N+1-x$；畫面可寫成 $6^*$ 或直接寫數字（兩者都要說明一次）。

**F56 拆積木：對偶字母與 evacuation**（§A.1，p.183–186；§A.3 一句）
1. 問：把一個字倒過來讀、每個字母換成「對面」的字母，它的表會變成什麼？
2. $w^*$：倒著讀＋$x\mapsto x^*$；Knuth 關係保持（$xzy\equiv zxy$ 對應到 $y^*z^*x^*\equiv y^*x^*z^*$）。例：$w=3121$（$N=3$）→ $w^*=3231$。
3. evacuation：拿走左上角 $x$、剩下的斜表滑成一般表 $\Delta T$、空出的格子填 $x^*$；重複到拿完。小例子 $T=\yts{12,3}$ 逐步做（`evacuation_steps`）。
4. 書上的例子（p.184）：$T=1223/2355/446/56$，第一步 $\Delta T=2223/3455/466/5$、$1^*$ 放在第 4 列第 2 格；快轉到 $T^*=6^*6^*5^*4^*/5^*5^*4^*2^*/3^*3^*2^*/2^*1^*$（$=1123/2235/445/56$）。
5. 對偶定理：(1) 形狀不變 (2) $(T^*)^*=T$ (3) $P(w^*)=P(w)^*$（例：$P(3121)=11/2/3$，$P(3231)=13/2/3=P(3121)^*$）(4) 陣列 $\omega\leftrightarrow(P,Q)$ 則 $\omega^*\leftrightarrow(P^*,Q^*)$。
   應用：$[T,U]\mapsto[U^*,T^*]$ 給出 $c^\nu_{\lambda\mu}=c^\nu_{\mu\lambda}$ 的一一對應；§A.3 把這種對應推廣成「LR 對應」（形狀改變定理）。
收束：evacuation＝把字母表倒過來看同一張表。

**F57 打擂台：行插入**（§A.2，p.186–189）
1. 問：第 1 章的列插入換成「一行一行地擠」，會得到不同的表嗎？
2. 行插入規則：$x$ 在第一行擠掉最上面的 $\ge x$ 的數，被擠的數去下一行；沒有就放在該行底部。例：$1\to\yts{13,2}$ 得 $\yts{113,2}$；$2\to\yts{13,2}$ 得 $\yts{123,2}$（`column_insert`，路徑上色）。
3. 擂台：字 $w=24135$，左邊列插入 $2,4,1,3,5$，右邊行插入 $5,3,1,4,2$（倒著），兩邊都得到 $P=135/24$（命題 1；`column_insert_word`）。
4. 字母相異時 $P(w^{\rm rev})=P(w)^T$：$P(53142)=12/34/5$ 是 $135/24$ 的轉置。
5. 一句：命題 1 的 $Q$ 用「滑進來」得到，和 R-S-K 一樣；練習 6：$Q(w^{\rm rev})$ 與 $Q(w^*)$ 互為轉置。
收束：列插入與行插入是同一個對應的兩種寫法。

**F58 反著排：Burge 對應**（§A.4.1，p.197–201）
1. 問：R-S-K 用字典序；把陣列換成「上列由大到小」會發生什麼？
2. 書上的矩陣 $A=\begin{pmatrix}1&2&0\\0&1&1\\1&1&1\end{pmatrix}$ → 成對 $(1,1),(1,2),(1,2),(2,2),(2,3),(3,1),(3,2),(3,3)$。
3. 反字典序（上列遞減、同上列時下列遞增）：$\binom{3\,3\,3\,2\,2\,1\,1\,1}{1\,2\,3\,2\,3\,1\,2\,2}$。作法 (1b)：依序行插入 $v_8,\dots,v_1$，把 $u_8,\dots,u_1$ 放進新格子（`burge`）。
4. 結果 $R=11222/23/3$、$S=11133/22/3$，同形狀 $(5,2,1)$；對照 R-S-K 的 $P=112223/23$、$Q=111223/33$（形狀 $(6,2)$）——同一個矩陣，兩種不同的表對。
5. 一句：命題 2，作法 (2b)（列插入＋滑動）與 (3b)（矩陣球，NW 序）也得到同一對 $(R,S)$。
收束：換一個排序，就換一個對應。

**F59 從四個角看矩陣**（§A.4.2 定理 1，p.201–203）
1. 問：R-S-K 的矩陣球是從左上角開始編號；如果從另外三個角開始呢？
2. 同一個 $A$，四個角各一個觀察者（箭頭）；用 `corners(A)` 得到四對：
   nw $(P,Q)$、se $(P^*,Q^*)$、sw $(R,S^*)$、ne $(R^*,S)$。數值：$P=112223/23$、$Q=111223/33$；$Q^*=111333/22$；$S^*=11123/23/3$；$R^*=11223/22/3$。
3. 揭曉關係：對角的兩個只差 $^*$（evacuation）；左下、右上用的是 Burge 的 $(R,S)$。
4. 程式用所有 $2\times2$（元素 $0..2$）的矩陣核對過定理 1。
收束：四個角，兩個對應，再加上 $^*$。

**F60 填格子遊戲：0-1 矩陣與 Gale–Ryser**（§A.4.3，p.203–208）
1. 問：列和 $(3,2,1)$、行和 $(2,2,2)$ 的 0-1 矩陣填得出來嗎？$(3,3)$ 與 $(3,1,1,1)$ 呢？（先讓觀眾猜）
2. Knuth 的對應：沒有重複的陣列（0-1 矩陣），依序行插入 $v_1..v_r$、把 $u_i$ 放在新格子的共軛位置 → 一對\textbf{形狀互為共軛}的表 $\{P,Q\}$。
   例：$\begin{pmatrix}0&1&1\\1&0&1\\1&0&1\end{pmatrix}$ → $P=112/333$、$Q=11/22/33$（`dual_rsk`）。$3\times3$ 的 511 個非零 0-1 矩陣一一對應（程式核對）。
3. 對偶 Cauchy（Littlewood）：$\prod_{i,j}(1+x_iy_j)=\sum_\lambda s_\lambda(x)s_{\tilde\lambda}(y)$。練習 19：個數 $=\sum_\nu K_{\tilde\nu\lambda}K_{\nu\mu}$。
4. 揭曉：$(3,2,1)/(2,2,2)$ 有 3 個（畫出來）；$(3,3)/(3,1,1,1)$ 一個都沒有。Gale–Ryser（練習 20）：存在 $\iff$ $\mu\trianglelefteq\tilde\lambda$
   （$(2,2,2)\trianglelefteq(3,2,1)$：$2\le3,4\le5,6\le6$；$(3,1,1,1)$ 對 $(2,2,2)$：$3>2$）。
收束：能不能填，看支配序。

**F61 把行重新排隊：鑰匙**（§A.5，p.208–210）
1. 問：一張表的各行換個順序排，還能保持「rectify 回原來的表」嗎？
2. 命題 7：給定各行長度的任一排列，恰有一個斜表（緊湊形式）rectify 成 $T$——叫 frank 斜表。書上 $T=1122/233/4$、行長排成 $(2,3,2,1)$：各行 $12$、$134$、$23$、$2$（`frank_tableau`，形狀 `compact_skew`）。
3. 推論 1：最左（最右）那一行只跟它的長度有關 → 長度 $c$ 的集合 $\mathcal L_c$（$\mathcal R_c$）；推論 2：$c<d$ 時 $\mathcal L_c\subset\mathcal L_d$。
4. 把它們排成表：$K_-(T)=1111/222/4$、$K_+(T)=2222/333/4$（`keys`）；小例子 $\yts{12,3}$：$K_-=\yts{11,3}$、$K_+=\yts{22,3}$。
5. 一句：鑰匙用在旗流形的標準單項式（§10.5 末，Lascoux–Schützenberger）。
收束：鑰匙是一張表「最靠左／最靠右」的影子。

**F62 數格子就是數洞：胞腔給出同調**（附錄 B，§B.1–B.3 Lemma 6，p.211–222）
1. 問：怎麼知道 $Gr(2,4)$ 有幾個「洞」？
2. 一句話的同調：$H_i$ 量 $i$ 維的洞；$\mathbb C^k$ 只貢獻在 $H_{2k}$（Lemma 6 證明的開頭）。
3. Lemma 6：空間切成 $\mathbb C^{n_{ij}}$ 的胞腔 ⇒ 胞腔的閉包給出同調的基底。$\mathbb P^2$：胞腔維數 $0,1,2$ → Betti $1,0,1,0,1$，$\chi=3$。
4. $Gr(2,4)$：胞腔 $1,1,2,1,1$（第 9 章的星號）→ Betti $1,0,1,0,2,0,1,0,1$，$\chi=6$＝不動點個數；$Fl(3)$：$1,2,2,1$ → $\chi=6$；Poincaré 對偶：左右對稱。
5. 對照 $\mathbb F_q$ 的點數：把 $q$ 換成 $t^2$ 就是 Poincaré 多項式（$1+q+2q^2+q^3+q^4$ ↔ $1+t^2+2t^4+t^6+t^8$）。
收束：星號數決定一切。

**F63 交點就是乘法：子簇的類**（§B.3，p.219–222；§B.1 的性質）
1. 問：直線和圓錐曲線交幾點？平面裡兩條曲線呢？
2. 子簇 $V$ 給出類 $[V]$；橫截相交時 $[V]\cdot[W]$＝交點的類（性質 (9)）。$\mathbb P^2$：$[\text{直線}]=h$，$[\text{圓錐}]=2h$，$h\cdot2h=2h^2=2$ 點（Bézout）；$d$ 次與 $e$ 次曲線：$de$ 點。
3. 次數：$V\subset\mathbb P^N$ 維數 $k$ 的次數＝$[V]\cdot h^k$。$Gr(2,4)\subset\mathbb P^5$：$h$ 拉回成 $\sigma_1$，次數 $\sigma_1^4=2$——正是二次超曲面（F46 的 Plücker 關係）。$Gr(2,5)$：5；$Gr(3,6)$：42（`plucker_degree`）。
4. 練習 8（Segre）：$\mathbb P^1\times\mathbb P^1\subset\mathbb P^3$，$h\mapsto h_1+h_2$，$(h_1+h_2)^2=2h_1h_2$ ⇒ 次數 2（又是二次曲面）。
收束：拓撲把「數交點」變成多項式乘法。

**F64 Chern 類：為什麼 $e_k=0$**（§B.4，p.222–225；接第 10 章命題 3、Lemma 9）
1. 問：第 10 章說 $H^*(Fl(m))$ 裡所有 $e_k(x)$ 都是 0——為什麼？
2. 線叢的 $c_1$；Whitney 公式 $c(E\oplus F)=c(E)c(F)$（(14)）；分裂原理（Lemma 7）。
3. 例：$c(T\mathbb P^n)=(1+h)^{n+1}$，$\mathbb P^2$：$1+3h+3h^2$，$c_2=3=\chi(\mathbb P^2)$；$\mathbb P^3$：$c_3=4$（`chern_projective`）。
4. 旗流形：$\mathbb C^m$ 這個平凡叢被 $U_1\subset U_2\subset\cdots$ 一層層切成線叢 $L_i=U_i/U_{i-1}$，$x_i=-c_1(L_i)$；Whitney：$\prod_i(1-x_i)=c(\text{平凡})=1$，展開就是 $e_1=e_2=\cdots=e_m=0$。
5. 射影叢公式（(33)）：$H^*(\mathbb P(E))=H^*(X)[\zeta]/(\zeta^e+c_1\zeta^{e-1}+\cdots+c_e)$；$Fl(m)$ 是一串 $\mathbb P$ 叢，所以命題 3 的基底 $x^I$（$i_j\le m-j$）；Lemma 9：$p_*(x^{e-1})=1$——正是差商 $\partial_i$ 的幾何。
收束：一條 Whitney 公式解釋了整個 Borel 表示。

**F65 全書回顧：一張地圖**（無對應頁）
1. 問：從第 1 章的「擠數字」走到第 10 章的「旗流形」，中間發生了什麼？
2. 地圖（三排）：組合（插入、字、R-S-K、LR、對稱函數；F01–F27）→ 表示（$S_n$、$GL$；F28–F45）→ 幾何（旗流形、Schubert；F46–F55）→ 附錄（F56–F64）。每站一個代表畫面或公式。
3. 三條貫穿的線：同一條交換關係（Specht／Schur 模／Plücker）；同一個 LR 係數（表的乘法／表示的分解／Schubert 計算）；同一個「2」（四條線、$c^{321}_{21,21}$、pipe dream）。
4. 收束：Young 表是組合、表示與幾何共用的語言。全系列完。

## 7. 製作規則（同 `notes/fulton_plan_ch9-10.md` §7）
- ManimGL，繼承 `ChuScene`；`construct` 只呼叫模組層級函式；開頭 `show_header`＋`check_math()`，結尾 `self.wait(1.0)`；骨架照 `notes/fulton_plan_ch7.md` §5。
- 每個畫面上的數字都由 `utils.fulton_appendix`／`utils.tableaux`／`utils.schubert` 算出並在 `check_math()` assert；版面用 `assert_in_frame`／`assert_apart`。
- `Tex(..., color=)` 無效（用 `.set_color()`）；同一個 `play` 不要同時動畫父物件與子物件；Tex 開頭結尾不放 `\,` `\;`；Tex 不放中文；`\iff` 會失敗，用 `\Leftrightarrow`。
- 只建立自己的場景檔；共用檔不改。每幕 250–450 行。自查：在 `C:\mypython\manim\projects\combkit` 執行
  `python tools/render_check.py ../catalan930/codes/scenes/<檔名> <類別> --config ../catalan930/codes/custom_config.yml --tile 480`；每幕最多 2 次。
- 回報 ≤ 8 行：檔名、長度、STATUS、偏離本檔之處。

## 8. 檔名與分工（`codes/scenes/`）
| 代號 | 檔名 | 類別 | 代理人 |
|---|---|---|---|
| F56 | `sceneF56_evacuation.py` | `SceneF56Evacuation` | A |
| F57 | `sceneF57_column_bumping.py` | `SceneF57ColumnBumping` | A |
| F58 | `sceneF58_burge.py` | `SceneF58Burge` | A |
| F59 | `sceneF59_four_corners.py` | `SceneF59FourCorners` | A |
| F60 | `sceneF60_zero_one.py` | `SceneF60ZeroOne` | A |
| F61 | `sceneF61_keys.py` | `SceneF61Keys` | B |
| F62 | `sceneF62_cells_homology.py` | `SceneF62CellsHomology` | B |
| F63 | `sceneF63_classes_degrees.py` | `SceneF63ClassesDegrees` | B |
| F64 | `sceneF64_chern_classes.py` | `SceneF64ChernClasses` | B |
| F65 | `sceneF65_book_map.py` | `SceneF65BookMap` | B |

> 完成（2026-10-16）：F56–F65 與 `FultonDemo7`（20 分 48 秒）。講義附錄 A、B：`notes/fulton/part9.tex`、`part10.tex`（數字由 `fulton/make_figs.py` 的 `check_numbers_appAB()` 核對）。
