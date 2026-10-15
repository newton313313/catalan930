"""
check_env.py —— 檢查這台電腦能不能跑這個專案

在 codes/ 資料夾內執行：
    python check_env.py            檢查套件、外部程式、字型、數學驗證
    python check_env.py --render   另外實際渲染一張含 LaTeX 的圖，確認整條管線可用

每一項會顯示 OK / 缺少，最後列出要修的項目與建議指令。
"""
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
results = []


def report(name, ok, detail="", fix=""):
    results.append((name, ok, detail, fix))
    mark = "OK  " if ok else "缺少"
    print(f"[{mark}] {name}" + (f"  —  {detail}" if detail else ""))


def run(cmd):
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                             timeout=300, cwd=HERE, env=env)
        return out.returncode, ((out.stdout or "") + (out.stderr or "")).strip()
    except Exception as err:          # noqa: BLE001
        return -1, str(err)


def main():
    render = "--render" in sys.argv
    sys.argv = sys.argv[:1]     # manimlib 在 import 時會解析命令列，先清掉本程式自己的參數
    print(f"Python：{sys.version.split()[0]}  （{sys.executable}）\n")

    # 1. Python 版本
    report("Python 3.10 以上", sys.version_info >= (3, 10), sys.version.split()[0],
           "安裝 Python 3.10+（建議 Anaconda）")

    # 2. ManimGL
    try:
        import manimlib  # noqa: F401
        from importlib.metadata import version
        report("ManimGL（manimlib）", True, f"manimgl {version('manimgl')}，位置 {Path(manimlib.__file__).parent}")
    except Exception as err:          # noqa: BLE001
        report("ManimGL（manimlib）", False, str(err).splitlines()[-1],
               r"pip install -e ..\third_party\manim  再  pip install -r ..\third_party\manim\requirements.txt")

    # 3. 其他 Python 套件
    for mod in ["av", "manimpango", "numpy", "scipy", "sympy", "yaml"]:
        try:
            importlib.import_module(mod)
            report(f"Python 套件 {mod}", True)
        except Exception as err:      # noqa: BLE001
            report(f"Python 套件 {mod}", False, str(err),
                   r"pip install -r ..\third_party\manim\requirements.txt")

    # 4. 外部程式
    for exe, fix in [
        ("manimgl", "裝好 ManimGL 後應該會有；確認 Python 的 Scripts 資料夾在 PATH 上"),
        ("ffmpeg", "conda install -c conda-forge ffmpeg（或自行安裝並加入 PATH）"),
        ("latex", "安裝 MiKTeX：https://miktex.org/download"),
        ("xelatex", "安裝 MiKTeX（編譯講義用）"),
        ("dvisvgm", "安裝 MiKTeX（manim 把 LaTeX 轉成 SVG 用）"),
    ]:
        path = shutil.which(exe)
        report(f"外部程式 {exe}", path is not None, path or "", fix)

    # 5. cm-super 字型（沒有的話 LaTeX 場景會出現 "SVG has no content to measure"）
    if shutil.which("kpsewhich"):
        code, out = run(["kpsewhich", "sfrm1000.pfb"])     # cm-super 提供的 T1 字型外框
        found = [line for line in out.splitlines() if line.lower().endswith(".pfb")]
        report("MiKTeX 套件 cm-super", bool(found), found[0] if found else "",
               "miktex packages install cm-super，然後 manimgl --clear-cache")
    else:
        report("MiKTeX 套件 cm-super", False, "找不到 kpsewhich", "安裝 MiKTeX")

    # 6. 中文字型
    try:
        import manimpango
        fonts = manimpango.list_fonts()
        for font in ["Microsoft JhengHei", "DFKai-SB"]:
            report(f"字型 {font}", font in fonts, "",
                   "Windows 內建；其他系統請改 codes/utils/styles.py 的 CJK_FONT 與講義的字型設定")
    except Exception as err:          # noqa: BLE001
        report("字型檢查", False, str(err))

    # 7. 設定檔必須是純 ASCII
    cfg = HERE / "custom_config.yml"
    try:
        cfg.read_bytes().decode("ascii")
        report("custom_config.yml 為純 ASCII", True)
    except Exception:                 # noqa: BLE001
        report("custom_config.yml 為純 ASCII", False, "",
               "把檔案裡的中文刪掉（ManimGL 用 cp950 讀它）")

    # 8. 數學驗證
    code, out = run([sys.executable, str(HERE / "utils" / "counting.py")])
    ok = (code == 0 and "Raney 公式證明的每一步都通過" in out
          and "卡塔蘭基礎模組：所有物件的數目與一一對應都通過" in out
          and "MIT 補充模組：所有計數與一一對應都通過" in out)
    report("數學驗證 utils/counting.py", ok,
           "公式、暴力列舉、遞迴、Raney 證明、卡塔蘭物件、MIT 補充全部一致" if ok else out[-300:])

    # 9. Young 表（Fulton 第 1–4 章，場景 F01–F19）
    code, out = run([sys.executable, str(HERE / "utils" / "tableaux.py")])
    ok = (code == 0 and "Fulton 第 1 章：插入、乘積、jeu de taquin 全部驗證通過" in out
          and "Fulton 第 2–4 章：Knuth 等價、L(w,k)、R-S-K、矩陣球全部驗證通過" in out
          and "Fulton 第 5–6 章：Littlewood–Richardson 規則、對稱函數全部驗證通過" in out)
    report("數學驗證 utils/tableaux.py", ok,
           "列插入、乘積、jeu de taquin、Schur 多項式全部一致" if ok else out[-300:])

    # 9b. Schubert（Fulton 第 9–10 章，場景 F46–F55）
    code, out = run([sys.executable, str(HERE / "utils" / "schubert.py")])
    ok = code == 0 and "Fulton 第 9–10 章：Plücker、Schubert 胞腔與計算、Bruhat 序、差商、Schubert 多項式全部驗證通過" in out
    report("數學驗證 utils/schubert.py", ok,
           "Plücker、胞腔計數、Schubert 計算、Bruhat 序、Schubert 多項式＝pipe dream 全部一致" if ok else out[-300:])

    # 10. 實際渲染（選用）
    if render:
        # 只輸出 Scene04 的前兩個動畫（含 LaTeX 公式），存成一小段影片後刪掉。
        # 不用 -s 存 PNG：本專案開發機的 Pillow 9.4 在存 PNG 時會出錯（見交接說明）。
        print("\n渲染測試中（約 20 秒）……")
        code, out = run(["manimgl", "scenes/scene04_paper_example.py", "Scene04PaperExample",
                         "-w", "-l", "-n", "0,2", "--file_name", "_check_env_test"])
        video = HERE / "renders" / "_check_env_test.mp4"
        ok = code == 0 and video.exists() and video.stat().st_size > 0
        report("渲染測試（含 LaTeX 公式）", ok, "成功輸出測試影片" if ok else out[-400:],
               "看上面的錯誤；LaTeX 錯誤先試 manimgl --clear-cache")
        for leftover in (HERE / "renders").glob("_check_env_test*"):
            leftover.unlink()

    bad = [r for r in results if not r[1]]
    print("\n" + ("全部通過，可以開始使用。" if not bad else f"有 {len(bad)} 項需要處理："))
    for name, _, _, fix in bad:
        if fix:
            print(f"  - {name}：{fix}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
