#!/usr/bin/env bash
# 从 Infinite-World 官方 Pages 仓库拉取静态资源（可选，网络需可访问 GitHub）
# 用法: bash scripts/download_assets.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="https://raw.githubusercontent.com/RQ-Wu/RQ-Wu.github.io/main/projects/infinite-world"
ASSETS="${ROOT}/assets"

mkdir -p "${ASSETS}/videos"

echo "Downloading images..."
for f in framework.png logo.png logo_white.png title.png; do
  curl -fsSL "${BASE}/assets/${f}" -o "${ASSETS}/${f}"
done

echo "Downloading videos (large files, may take a while)..."
for f in \
  teaser.mp4 \
  "82_A_street_in_a_fantasy_city_whe_button.mp4" \
  "03_A_serene_indoor_Zen_pool_room,_button.mp4" \
  "65_Looking_across_a_vast_salt_fla_button.mp4" \
  "05_A_cozy_attic_workshop_with_exp_button.mp4" \
  "52_Looking_out_at_a_calm_glacial__button.mp4" \
  "73_A_wide_view_of_a_turquoise_cor_button.mp4"
do
  encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${f}'))")
  curl -fsSL "${BASE}/assets/videos/${encoded}" -o "${ASSETS}/videos/${f}"
done

echo "Done. Assets saved under ${ASSETS}"
