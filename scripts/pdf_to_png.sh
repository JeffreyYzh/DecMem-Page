#!/usr/bin/env bash
# 将 assets/*.pdf 转为同名 PNG（2x 分辨率）
set -euo pipefail

export http_proxy="${http_proxy:-http://oversea-squid2.ko.txyun:11080}"
export https_proxy="${https_proxy:-http://oversea-squid2.ko.txyun:11080}"
export no_proxy="${no_proxy:-localhost,127.0.0.1,localaddress,localdomain.com,internal,corp.kuaishou.com,test.gifshow.com,staging.kuaishou.com}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-/m2v_intern/yangzhenhao/miniconda3/bin/python}"
PIP="${PIP:-/m2v_intern/yangzhenhao/miniconda3/bin/pip}"

"$PIP" install pymupdf -q
"$PY" << PY
import fitz
from pathlib import Path

assets = Path("$ROOT/assets")
pairs = [
    ("introv5.pdf", "introv5.png"),
    ("pipeline_v3.pdf", "pipeline_v3.png"),
]
for pdf_name, png_name in pairs:
    pdf_path = assets / pdf_name
    if not pdf_path.exists():
        print(f"skip (missing): {pdf_path}")
        continue
    doc = fitz.open(pdf_path)
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    out = assets / png_name
    pix.save(str(out))
    print(f"OK {out.name}: {pix.width}x{pix.height}")
    doc.close()
PY

echo "Done."
