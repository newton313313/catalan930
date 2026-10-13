r"""
make_mit_figs.py —— 一次重新產生附錄 A（MIT 補充）四段的 TikZ 圖

在 notes/ 資料夾內執行：
    python make_mit_figs.py
依序執行 mit/make_figs_part1.py … part4.py；每一段會先檢查自己寫到的數字，再寫出 mit/figs_partK.tex。
任何一段失敗就停下來。之後照常編譯講義（xelatex 兩次）。
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

for k in (1, 2, 3, 4):
    script = HERE / "mit" / f"make_figs_part{k}.py"
    print(f"--- {script.name}")
    result = subprocess.run([sys.executable, str(script)], cwd=HERE)
    if result.returncode != 0:
        sys.exit(f"{script.name} 失敗")
print("附錄 A 的圖全部重新產生完畢")
