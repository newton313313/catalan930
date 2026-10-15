# Fulton《Young Tableaux》第 9–10 章 → Manim：大綱、檢討與定稿（2026-10-15）

> 本檔的相對路徑以 `C:\mypython\manim\projects\catalan930\` 為基準。來源：`../ref/fulton/md/09_flag-varieties.md`（書 p.131–153）、
> `../ref/fulton/md/10_schubert-varieties-and-polynomials.md`（p.154–182）。場景 F46–F55，獨立連續播放 `FultonDemo6`；舊影片不動。
> 依使用者要求的順序：§1 草稿大綱 → §2 生動度檢討 → §3 例子檢討 → §4 程式大綱 → §5 省 token 檢討 → §6 定稿（代理人只讀 §6–§8）。

## 1. 草稿大綱（12 幕）
| 草稿 | 主題 | Fulton |
|---|---|---|
| D1 | Plücker 嵌入與二次關係 | §9.1 Lemma 1 |
| D2 | 關聯簇 $Fl_{p,q}$、旗流形的方程 | §9.1 Lemma 2、命題 1 |
| D3 | 不變量理論：$\mathbb C[Z]^{SL_n}$ 由最大子式生成 | §9.2 命題 2 |
| D4 | 表示與線叢（Borel–Weil） | §9.3 |
| D5 | Grassmannian 的 Schubert 胞腔 | §9.4 |
| D6 | 對偶、Pieri、Giambelli、LR | §9.4 |
| D7 | 環面不動點 | §10.1 |
| D8 | 旗流形的 Schubert 胞腔、上同調環 | §10.2 |
| D9 | 差商與 Schubert 類的關係 | §10.3 |
| D10 | Schubert 多項式 | §10.4 |
| D11 | Bruhat 序 | §10.5 |
| D12 | 應用到 Grassmannian | §10.6 |

## 2. 生動度檢討（哪裡太乾 → 怎麼改）
- **D3、D4 全是抽象定義**（不變量、線叢），畫面只能堆公式。→ 併進 D2 成為「旗流形的座標環」一幕，改成**數維數的遊戲**：雙次數 $(a,b)$ 的單項式個數減掉關係的倍數，剛好等於 $\dim E^{(a+b,b)}$（$9-1=8$，接回第 8 章）。不變量、Borel–Weil 各留一句話。
- **D5 只是列梯形矩陣**。→ 「數星星」：星號＝自由座標，星號個數＝胞腔維數；再加一個驚喜——在 $\mathbb F_2$ 上暴力數出 $35$ 個平面，正好是 $1+2+2\cdot4+8+16$。
- **D6 規則太多**。→ 用經典謎題開場：「空間中四條直線，有幾條直線和四條都相交？」答案 2 留到最後揭曉＝$2\times2$ 方框裡 Young 格的路徑數。
- **D9 差商像純代數**。→ 「吃多項式的機器」：對調 → 相減 → 除以 $x_i-x_{i+1}$，問「一定除得盡嗎？」，再玩幾個輸入。
- **D10 公式很長**。→ 從 $S_3$ 的 Hasse 圖頂端 $x_1^2x_2$ 一路「流下來」；書上的 $41352$ 例子當「長途旅行」。
- **加一幕 pipe dream**（書 p.172 只提一句「係數都非負，見 Billey–Jockusch–Stanley」）：把練習 5 的係數 2 變成「兩張水管圖」，是全章最好玩的畫面；標明是延伸。
- **D11 是比大小**。→ 「排序遊戲」：前綴排好序逐項比較；書上 9 位數的下降鏈當「下樓梯」。
- **每幕開頭一個問題、結尾一句收束**；貫穿的主角：$Gr(2,4)$（四條線）、$Fl(3)$（點在線上）、$S_3$ 的六角形。

## 3. 例子檢討（每幕至少一個小例子算到底＋一個書上的例子）
| 幕 | 小例子（逐步算） | 書上／較大的例子 |
|---|---|---|
| F46 | $A=\begin{pmatrix}1&2&0&1\\0&1&3&2\end{pmatrix}$ 的 6 個子式；換基底 $g$ 後全部 ×2 | 練習 2：由 $1,2,1,1,2,3$ 還原矩陣 |
| F47 | 點 $(1:2:3)$ 在線上：$1\cdot(-1)-2\cdot1+3\cdot1=0$ | 維數表 $(a,b)\le(2,2)$：$3,3,6,8,6,15,15,27$ |
| F48 | $Gr(2,4)$ 六個胞腔全部畫出 | 書上 $r=5,n=7,\lambda=(5,3,2,2,1)$ 的星號 $2,4,5,5,6$；$\mathbb F_2$ 上 35 個 |
| F49 | $\sigma_1^4=2\sigma_{22}$ 的兩條路徑 | $Gr(2,5)$：5；$Gr(3,6)$：$\sigma_{21}^2=\sigma_{33}+2\sigma_{321}+\sigma_{222}$ |
| F50 | $Fl(3)$ 的 6 個不動點與 6 個胞腔 | 書上 $w=426135$ 的 7 顆星；$\mathbb F_2$ 上 21、315 |
| F51 | $\partial_1(x_1^2)$、$\partial_1(x_1x_2)$、$\partial_1(x_2)$、$\partial_1(x_1^3)$ | 辮關係在 $x_1^2x_2$ 上兩邊都得 1 |
| F52 | $S_3$ 的 6 個 Schubert 多項式 | 書上 $54321\to\cdots\to41352$ 的五步 |
| F53 | $\mathfrak S_{132}=x_1+x_2$ 的兩張圖 | 練習 5：$\mathfrak S_{21543}$ 的係數 2 |
| F54 | $132\le312$（秩矩陣與前綴）、$1423$ 與 $3124$ 不可比 | 書上 $679251834$ 下降到 $428361795$ 的 8 步、失敗的例子 |
| F55 | $2413\mapsto s_{21}(x_1,x_2)$、$1342\mapsto e_2(x_1,x_2,x_3)$ | 四條線在 $Fl(4)$ 重算：$(x_1+x_2)^4=s_4+3s_{31}+2s_{22}$ |

## 4. 程式大綱（已完成，代理人直接用）
- `codes/utils/schubert.py`（純 Python，`python utils/schubert.py` 自我測試）：置換（`length`、`descents`、`act_right`、`w0`、`perms`、`perm_str`）、
  秩矩陣與 Bruhat（`rank_matrix`、`bruhat_leq`、`bruhat_leq_tableau`、`bruhat_chain`、`bruhat_levels`、`bruhat_covers`）、
  胞腔（`flag_cell_pattern`、`grass_cell_pattern`、`gaussian_binomial`、`q_factorial`、`count_subspaces_F2`、`count_flags_F2`）、
  Plücker（`plucker`、`plucker_from_coords`、`flag_ring_dim`）、Schubert 計算（`box_product`、`rectangle_count`）、
  多項式（`swap_vars`、`divided_difference`、`schubert_poly`、`schubert_path`、`pipe_dreams`、`pipe_exits`、`pipe_weight`、
  `grassmannian_partition`、`grassmannian_perm`、`staircase_monomials`、`poly_str`）。另用 `utils.tableaux` 的 `schur_poly`、`schur_expand`、`poly_mul`、`standard_tableaux`、`hook_content_count`。
- `codes/utils/schubert_draw.py`（ManimGL）：`CellMatrixMob`（1／*／0 矩陣，`.stars()`、`.ones()`、`.cell(i,j)`）、`BoxDiagramMob`（方框裡的 Young 圖）、
  `HasseMob`（Hasse 圖，`.node[w]`、`.edge[(u,v)]`，`label=` 可換成多項式字串）、`PipeDreamMob`（`.cross[(i,j)]`）、`poly_tex`、`word_tex`。
- 既有：`fulton_draw`（`tableau_mob`、`assert_in_frame`、`assert_apart`）、`rep_draw.MatrixMob`、`scene_base.ChuScene`、`styles`（`zh`、`mixed`、`MUTED_COLOR`）。

## 5. 省 token 檢討（改了什麼）
- 12 幕 → **10 幕**：D2+D3+D4 併成 F47；D7+D8 併成 F50；D8 的上同調環移到 F51 開頭；加 pipe dream 一幕。
- 不做 3D：四條線用 2D 示意圖（標「示意」）。不新增 JSON：所有數字由 `schubert.py` 現算並在 `check_math()` assert。
- 共用元件與數學我先寫好並測過（含 combkit 範例 ex12），代理人**不讀 Fulton 原文**，只讀本檔 §6–§8 與兩個模組開頭的說明。
- 2 個代理人平行（各 5 幕）；`render_check.py` 已改成每次試渲染用自己的 TEMP，可以同時跑；每幕最多 2 次 render_check；我只看 `--tile 480` 總覽圖。
- 所有代理人回報完才輸出 1080p（一次一支）；文件、接線、combkit、git 由我用腳本一次做完。

## 6. 定稿場景卡（代理人讀這裡）
共同：每幕 2–3 分鐘；開頭一個問題（字幕），結尾一句收束；字幕繁中；Fulton 記號（$\sigma_\lambda$、$\Omega_\lambda$、$X_w$、$\mathfrak S_w$、$\partial_i$、$\ell(w)$、$r_w(p,q)$）。
Fulton 慣例：$Gr$ 的子空間 $V=\ker A$（$A$ 是 $d\times m$ 矩陣），Plücker 座標＝$A$ 的最大子式；方框 $r\times n$，$n=m-r$；$\Omega_\lambda$ 的餘維數是 $|\lambda|$；$\sigma_w=[\Omega_w]=[X_{w_0w}]$ 的餘維數是 $\ell(w)$。

**F46 六個數認出一個平面：Plücker 座標**（§9.1，p.131–134）
1. 問：$\mathbb C^4$ 裡的 2 維子空間能不能用一串數字當身分證？
2. $A=\begin{pmatrix}1&2&0&1\\0&1&3&2\end{pmatrix}$，逐一框出第 $i,j$ 行算 $2\times2$ 子式：$p_{12},\dots,p_{34}=1,3,2,6,3,-3$。
3. 換一組列：$g=\begin{pmatrix}1&1\\0&2\end{pmatrix}$，$gA=\begin{pmatrix}1&3&3&3\\0&2&6&4\end{pmatrix}$，子式 $2,6,4,12,6,-6$ 全部 ×$\det g=2$ → 是 $\mathbb P^5$ 的一個點。
4. 不是每 6 個數都行：$p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0$（接 F45）；$Gr(2,4)$ 是 $\mathbb P^5$ 裡的二次超曲面（維數 4）。Lemma 1：一般的 $Gr$ 由二次方程切出。
5. 倒過來（練習 2）：給 $x_{12},\dots,x_{34}=1,2,1,1,2,3$，先驗 $3-4+1=0$；用式 (2)（$a_{s,t}$＝把 $I=(1,2)$ 的第 $s$ 個換成 $t$ 的座標）還原 $B=\begin{pmatrix}1&0&-1&-2\\0&1&2&1\end{pmatrix}$，再驗它的 6 個子式正是 $1,2,1,1,2,3$。子空間 $\ker B$ 由 $(1,-2,1,0)$、$(2,-1,0,1)$ 張成。
收束：子空間 ↔ 滿足二次關係的一點。

**F47 點在線上：旗流形與它的座標環**（§9.1 Lemma 2、命題 1；§9.2；§9.3；p.134–145）
1. 問：「一個點落在一條線上」要幾條方程？
2. $\mathbb P^2$ 裡的旗＝(點 ⊂ 線)。點 $v_1=(1,2,3)$、線由 $v_1$ 與 $v_2=(0,1,1)$ 張成：線的 Plücker 座標（$2\times2$ 子式）$y_{12},y_{13},y_{23}=1,1,-1$；關聯方程 $x_1y_{23}-x_2y_{13}+x_3y_{12}=-1-2+3=0$（Lemma 2，又是二次關係）。換一個不在線上的點（例如 $(1,0,0)$）就不等於 0。
3. 命題 1：$Fl(\mathbb C^3)\subset\mathbb P^2\times\mathbb P^2$ 由這種二次方程切出；座標環 $S(3;1,2)=\operatorname{Sym}(E\oplus\bigwedge^2E)/(\text{關係})$。
4. 數維數遊戲：雙次數 $(a,b)$ 的部分 $=\binom{a+2}2\binom{b+2}2-\binom{a+1}2\binom{b+1}2=\dim E^{(a+b,b)}$：表 $(1,0)=3$、$(0,1)=3$、$(2,0)=6$、$(1,1)=9-1=8$、$(0,2)=6$、$(2,1)=15$、$(1,2)=15$、$(2,2)=27$。
5. 一句不變量（§9.2 命題 2）：$SL_n$ 不變的多項式＝最大子式的多項式（$SL$ 不改變行列式）。一句 Borel–Weil（§9.3）：$E^\lambda$＝旗流形上一個線叢的截面；旗流形＝最高權重向量 $[e_{U(\lambda)}]$ 在 $\mathbb P(E^\lambda)$ 裡的軌道。
收束：一個環把 $GL_3$ 的不可約表示一個不漏地裝進來（每個一次）。

**F48 數星星：Grassmannian 的 Schubert 胞腔**（§9.4，p.145–148）
1. 問：4 維的 $Gr(2,4)$ 能不能切成一塊塊「平地」$\mathbb C^k$？
2. 固定旗 $F_1\subset F_2\subset F_3\subset\mathbb C^4$；每個 $V$ 有唯一的列梯形矩陣：第 $i$ 列的 1 在第 $n+i-\lambda_i$ 行（$n=2$），右邊與下方是 0，其餘是星號——$\lambda$ 落在 $2\times2$ 方框裡。
3. 六個胞腔並排（`grass_cell_pattern`，每個配 `BoxDiagramMob`）：星號數 $4-|\lambda|$＝$4,3,2,2,1,0$。
4. 數胞腔：$\binom42_q=1+q+2q^2+q^3+q^4$；$q=1$ 得 6；$q=2$ 得 $35$——在 $\mathbb F_2^4$ 裡暴力數平面也是 35（`count_subspaces_F2(4,2)`）。
5. Schubert 簇 $\Omega_\lambda=\{V:\dim(V\cap F_{n+i-\lambda_i})\ge i\}$ 是胞腔的閉包，餘維數 $|\lambda|$，包含所有 $\mu\supseteq\lambda$ 的胞腔（練習 13）。書上大例子 $r=5,n=7,\lambda=(5,3,2,2,1)$：各列星號 $2,4,5,5,6$，共 $22=35-13$（只閃過圖樣）。
收束：星號＝自由度，方框裡的 Young 圖＝胞腔。

**F49 四條線問題：Schubert 計算**（§9.4，p.146–153）
1. 問：空間中四條一般的直線，有幾條直線和它們四條都相交？（答案留到最後）
2. $\mathbb P^3$ 的直線 ＝ $Gr(2,4)$；「和一條給定的線相交」＝$\Omega_1$（餘維 1）。四個條件 → $\sigma_1^4\in H^8=\mathbb Z\sigma_{22}$。2D 示意圖：三條線、一個被直線掃出的曲面、第四條線穿過它兩次。
3. Pieri 在 $2\times2$ 方框裡：$\sigma_1\sigma_1=\sigma_2+\sigma_{11}$，$\sigma_1\sigma_2=\sigma_1\sigma_{11}=\sigma_{21}$，$\sigma_1\sigma_{21}=\sigma_{22}$ ⇒ $\sigma_1^4=2\sigma_{22}$：方框裡 Young 格從 $\emptyset$ 到 $(2,2)$ 的兩條路徑＝$(2,2)$ 的兩個標準表。揭曉：**2 條**。
4. 對偶（Lemma 3、式 (11)）：$\sigma_\lambda\sigma_\mu=\sigma_{22}$ 恰好當 $\mu$ 轉 180° 後與 $\lambda$ 拼滿方框（例 $\sigma_{21}\sigma_1=\sigma_{22}$）。
5. 推廣：$Gr(2,5)$ 六個條件 → $f^{(3,3)}=5$；練習 17 公式 $\frac{6!\cdot1!}{4!\cdot3!}=5$；$Gr(3,6)$ → 42。LR 在方框裡：$Gr(3,6)$ 中 $\sigma_{21}^2=\sigma_{33}+2\sigma_{321}+\sigma_{222}$（係數 2 就是第 5 章的 $c^{321}_{21,21}$；超出方框的 $s_{42},s_{411},s_{3111},s_{2211}$ 被丟掉）。
收束：Schubert 計算＝Schur 函數的乘法、只留方框裡的項。

**F50 旗流形：m! 個不動點與星號**（§10.1–10.2，p.154–162）
1. 問：$Fl(3)$（點在線上）裡，有幾個旗不會被對角矩陣移動？
2. 座標三角形（頂點 $e_1,e_2,e_3$）：不動的旗＝(頂點, 過它的邊)，$3\times2=6=3!$，標成置換 $w$（點 $e_{w(1)}$、線 $\langle e_{w(1)},e_{w(2)}\rangle$）。Lemma 2。
3. 胞腔 $X^\circ_w$：第 $p$ 列在第 $w(p)$ 行放 1，右邊與下方是 0，其餘星號；星號數＝$\ell(w)$（逆序數）。$S_3$ 六個：$0,1,1,2,2,3$。書上 $w=426135$：7 顆星。
4. 數旗：$[3]_q!=1+2q+2q^2+q^3$，$q=2$ → 21（$\mathbb F_2^3$ 的 7 個點 × 每點 3 條線，暴力也是 21）；$S_4$ 的層數 $1,3,5,6,5,3,1$，$q=2$ → 315。
5. 類 $\sigma_w=[\Omega_w]=[X_{w_0w}]$，餘維 $\ell(w)$；對偶 $\langle\sigma_u,\sigma_{w_0v}\rangle=\delta_{uv}$（式 (2)）。
收束：$m!$ 個點，$m!$ 個胞腔，$m!$ 個類。

**F51 吃多項式的機器：上同調環與差商**（§10.2 命題 3、§10.3，p.161–170）
1. 問：把 $x_i,x_{i+1}$ 對調、相減、除以 $x_i-x_{i+1}$——一定除得盡嗎？
2. 命題 3：$H^*(Fl(m))=\mathbb Z[x_1,\dots,x_m]/(e_1,\dots,e_m)$；$m=3$ 的基底 $1,x_1,x_2,x_1^2,x_1x_2,x_1^2x_2$（$i_j\le m-j$），6 個、次數分布 $1,2,2,1$＝F50 的胞腔數。
3. $\partial_if=\dfrac{f-s_if}{x_i-x_{i+1}}$：分子對 $x_i,x_{i+1}$ 反對稱 → 一定整除。輸入輸出：$\partial_1(x_1^2)=x_1+x_2$、$\partial_1(x_1x_2)=0$（對稱的被吃掉）、$\partial_1(x_2)=-1$、$\partial_1(x_1^3)=x_1^2+x_1x_2+x_2^2$。
4. 規則：$\partial_i^2=0$；辮關係 $\partial_1\partial_2\partial_1=\partial_2\partial_1\partial_2$（在 $x_1^2x_2$ 上：$x_1^2x_2\to x_1x_2\to x_1\to1$ 與 $x_1^2x_2\to x_1^2\to x_1+x_2\to1$）；Leibniz $\partial_i(fg)=\partial_if\cdot g+s_if\cdot\partial_ig$。
5. 幾何（Lemma 9、命題 4）：$\partial_i$＝沿 $\mathbb P^1$ 叢先拉回再推出；$w(i)>w(i+1)$ 時 $\partial_i\sigma_w=\sigma_{ws_i}$。
收束：一台機器把 Schubert 類一個個降下來。

**F52 從最頂端流下來：Schubert 多項式**（§10.4，p.170–173）
1. 問：知道最頂端的一個多項式，其他的能不能全部推出來？
2. Lemma 10：$\mathfrak S_{w_0}=x_1^{m-1}x_2^{m-2}\cdots x_{m-1}$；$m=3$：$x_1^2x_2$。
3. $S_3$ 的 Hasse 圖（`HasseMob`，節點標多項式）由上往下：$321:x_1^2x_2$；$231:x_1x_2$（$\partial_1$）、$312:x_1^2$（$\partial_2$）；$213:x_1$、$132:x_1+x_2$；$123:1$。兩條路到同一處，結果一樣。
4. 長途旅行（書 p.172）：$54321\xrightarrow{\partial_1}45321\xrightarrow{\partial_4}45312\xrightarrow{\partial_3}45132\xrightarrow{\partial_2}41532\xrightarrow{\partial_3}41352$，多項式依序 $x_1^4x_2^3x_3^2x_4\to x_1^3x_2^3x_3^2x_4\to x_1^3x_2^3x_3^2\to x_1^3x_2^3x_3+x_1^3x_2^3x_4\to$（5 項）$\to x_1^3(x_2x_3+x_2x_4+x_3x_4)$（用 `schubert_path(5,[1,4,3,2,3])`；長的只顯示項數或前幾項）。
5. 性質：$\mathfrak S_{s_i}=x_1+\cdots+x_i$；命題 6：$\mathfrak S_w$ 是 $\mathbb Z[x_1,\dots,x_k]$ 的基底；不隨 $m$ 改變（穩定）。
收束：Schubert 多項式＝把 $\sigma_w$ 寫成 $x$ 的多項式的「標準答案」。

**F53 係數 2 是兩張水管圖：pipe dream**（§10.4 p.172 的註、練習 5；延伸）
1. 問：練習 5 說 $\mathfrak S_{21543}$ 中 $x_1^2x_2x_3$ 的係數是 2——這個 2 數的是什麼？
2. 秀出 $\mathfrak S_{21543}$（13 項），框出 $2x_1^2x_2x_3$；書上說係數都是非負的（Macdonald；Billey–Jockusch–Stanley 1993 給組合公式）。
3. 規則：階梯格子裡放十字或彎管；第 $i$ 條水管從左邊第 $i$ 列流進、從頂端第 $w(i)$ 行流出（`pipe_exits`），任兩條最多交叉一次；權重 $x^D$＝每列十字數。
4. 小例子：$\mathfrak S_{132}=x_1+x_2$ 的兩張圖（十字在 $(1,2)$ → $x_1$；在 $(2,1)$ → $x_2$）；$\mathfrak S_{321}$ 只有一張（三個十字）。
5. 練習 5 的兩張圖（`[D for D in pipe_dreams((2,1,5,4,3)) if pipe_weight(D,5)==(2,1,1,0,0)]`），水管上色、出口標 $2,1,5,4,3$。$\mathfrak S_w=\sum_Dx^D$（標明是書外的延伸）。
收束：係數＝圖的張數，所以一定是非負整數。

**F54 排序遊戲：Bruhat 序**（§10.5，p.173–177）
1. 問：胞腔 $X^\circ_u$ 什麼時候落在 $X_v$ 的邊界上？
2. 秩矩陣 $r_w(p,q)=\#\{i\le p:w(i)\le q\}$；$u\le v\iff r_u\ge r_v$（逐格）。例：$r_{132}=\begin{pmatrix}1&1&1\\1&1&2\\1&2&3\end{pmatrix}$、$r_{312}=\begin{pmatrix}0&0&1\\1&1&2\\1&2&3\end{pmatrix}$ ⇒ $132\le312$。
3. 排序遊戲（練習 8）：每個前綴排好序逐項比較。$2143\le4231$：$\{2\}\le\{4\}$、$\{1,2\}\le\{2,4\}$、$\{1,2,4\}\le\{2,3,4\}$ ✓；$1423$ 與 $3124$ 互不可比（$1<3$ 但 $\{1,4\}$ 對 $\{1,3\}$ 第二項 $4>3$）。
4. $S_3$ 的 Hasse 圖（8 條邊）；$S_4$ 各層 $1,3,5,6,5,3,1$。下樓梯（Lemma 11、書 p.175）：$679251834\to579261834\to479261835\to429761835\to428761935\to428671935\to428371965\to428361975\to428361795$，每步長度減 1；換成 $428671953$ 時走到第二行就卡住 ⇒ 不可比。
5. 命題 7：$u\le v\iff X_u\subset X_v\iff\Omega_u\supset\Omega_v$；$X_w=\{E_\bullet:\dim(E_p\cap F_q)\ge r_w(p,q)\}$。
收束：比大小只要排序。

**F55 回到 Grassmannian：Schubert 多項式變 Schur 多項式**（§10.6，p.178–182）＋第 9–10 章總結
1. 問：第 9 章的四條線，能不能在旗流形裡再算一次？
2. Grassmann 置換（只在 $r$ 下降）$\leftrightarrow$ 方框裡的 $\lambda=(w(r)-r,\dots,w(1)-1)$（命題 8）：$2413\mapsto(2,1)$，$\mathfrak S_{2413}=x_1^2x_2+x_1x_2^2=s_{21}(x_1,x_2)$；$1342\mapsto(1,1)$，$\mathfrak S_{1342}=e_2(x_1,x_2,x_3)$；$1324\mapsto(1)$，$x_1+x_2$。
3. 投影 $p:Fl(4)\to Gr(2,4)$，$E_\bullet\mapsto E_2$；$p^*\sigma_\lambda=\sigma_w$（命題 9）。
4. 四條線重算：$\sigma_1\mapsto x_1+x_2=s_1(x_1,x_2)$，$(x_1+x_2)^4=s_4+3s_{31}+2s_{22}$；$s_4,s_{31}$ 放不進 $2\times2$ 方框 → $2\sigma_{22}$，而 $\mathfrak S_{3412}=x_1^2x_2^2$。又是 2。
5. 總結（快問快答）：三個「2」各數什麼？四條線（標準表）、$c^{321}_{21,21}$（LR 表）、$\mathfrak S_{21543}$ 的係數（pipe dream）。再一頁回顧：星號＝維數、二次關係、Schubert 計算＝LR、Schubert 多項式推廣 Schur。
收束：第 9–10 章完。

## 7. 製作規則（沿用 `notes/fulton_plan_ch7.md` 第 4–5 節，這裡只列差異與重點）
- ManimGL（`from manimlib import *`），繼承 `ChuScene`；`construct` 只呼叫模組層級函式；開頭 `show_header`＋`check_math()`，結尾 `self.wait(1.0)`。骨架照 ch7 §5。
- 每個畫面上的數字都由 `utils.schubert`／`utils.tableaux` 算出並在 `check_math()` assert；版面用 `assert_in_frame`／`assert_apart`。
- `Tex(..., color=...)` 在這版無效，用 `.set_color()`；同一個 `play` 不要同時動畫父物件與它的子物件（見 `schubert_draw` 說明）；Tex 開頭結尾不放 `\,` `\;`；Tex 不放中文；長多項式最多一行、超過就只顯示前幾項＋「…（共 N 項）」。
- 只建立自己的場景檔；共用檔不改（缺什麼寫成場景檔的模組層級函式，回報時說明）。每幕 250–450 行。
- 自查：在 `C:\mypython\manim\projects\combkit` 執行
  `python tools/render_check.py ../catalan930/codes/scenes/<檔名> <類別> --config ../catalan930/codes/custom_config.yml --tile 480`，看 `runs/<類別>/sheet.png`；每幕最多 2 次。
- 回報 ≤ 8 行：檔名、長度、STATUS、偏離本檔之處。

## 8. 檔名與分工（`codes/scenes/`）
| 代號 | 檔名 | 類別 | 代理人 |
|---|---|---|---|
| F46 | `sceneF46_plucker.py` | `SceneF46Plucker` | A |
| F47 | `sceneF47_flag_ring.py` | `SceneF47FlagRing` | A |
| F48 | `sceneF48_grass_cells.py` | `SceneF48GrassCells` | A |
| F49 | `sceneF49_four_lines.py` | `SceneF49FourLines` | A |
| F50 | `sceneF50_flag_cells.py` | `SceneF50FlagCells` | A |
| F51 | `sceneF51_divided_differences.py` | `SceneF51DividedDifferences` | B |
| F52 | `sceneF52_schubert_polys.py` | `SceneF52SchubertPolys` | B |
| F53 | `sceneF53_pipe_dreams.py` | `SceneF53PipeDreams` | B |
| F54 | `sceneF54_bruhat.py` | `SceneF54Bruhat` | B |
| F55 | `sceneF55_grassmannian_schur.py` | `SceneF55GrassmannianSchur` | B |
