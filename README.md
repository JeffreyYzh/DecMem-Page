# Project Page Template (Infinite-World style)

基于 [Infinite-World 项目页](https://rq-wu.github.io/projects/infinite-world/) 的静态学术主页模板，源码参考 [RQ-Wu/RQ-Wu.github.io](https://github.com/RQ-Wu/RQ-Wu.github.io/tree/main/projects/infinite-world)。

## 目录结构

```
opensource/projects/infinite-world/
├── index.html                      # 【主模板】带 [需替换] 注释，改成你的项目
├── index.infinite-world-demo.html  # Infinite-World 原文内容示例（需 assets）
├── css/style.css                   # 样式（可选改 --accent 主题色）
├── assets/                         # 图片与视频（需自行放入或脚本下载）
│   ├── framework.png
│   ├── logo.png
│   ├── title.png
│   └── videos/
├── scripts/download_assets.sh      # 从官方仓库拉取 Infinite-World 素材
├── scripts/pdf_to_png.sh           # 将 introv5.pdf / pipeline_v3.pdf 转为 PNG
└── README.md
```

## 快速开始

### 1. 本地预览

```bash
cd /m2v_intern/yangzhenhao/code/opensource/projects/infinite-world
python3 -m http.server 8080
# 浏览器打开 http://127.0.0.1:8080/
```

### 2. PDF 转 PNG（DecMem 图）

若更新了 `assets/*.pdf`，重新生成 PNG：

```bash
bash scripts/pdf_to_png.sh
```

页面使用 `assets/introv5.png`（Motivation）与 `assets/pipeline_v3.png`（Method）。

### 3. 下载 Infinite-World 官方素材（可选）

网络可访问 GitHub 时：

```bash
bash scripts/download_assets.sh
# 预览官方还原版：
# 将 index.infinite-world-demo.html 复制为 index.html，或单独打开该文件
```

### 4. 改成你自己的项目

在 **`index.html`** 中搜索 **`[需替换]`**，按注释逐项修改：

| 区块 | 需替换内容 |
|------|------------|
| `<head>` | 标题、meta description、favicon |
| `#intro` | 背景视频、主副标题、作者、机构、按钮链接 |
| `#abstract` | 摘要段落 |
| `#method` | `framework.png` 与图注 (a)(b)(c) |
| `#gallery` | 每个 demo 的 mp4 路径与 caption |
| `#comparison` | 表头、基线行、你们的方法行与 best/second 样式 |
| `#bibtex` | BibTeX |
| `footer` | 版权与致谢 |

样式主题色：编辑 `css/style.css` 顶部 `:root { --accent: ... }`。

### 5. 部署到 GitHub Pages

将本目录放到你的 `username.github.io` 仓库下，例如：

```
projects/your-project-name/index.html
projects/your-project-name/css/...
projects/your-project-name/assets/...
```

访问地址：`https://<username>.github.io/projects/your-project-name/`

> 视频文件较大，建议使用 Git LFS，或将 demo 托管到 CDN 后只改 `index.html` 里的 `src` URL。

## 文件说明

- **`index.html`**：空白占位 + 中文 `<!-- [需替换] -->` 注释，作为你的主编辑文件。
- **`index.infinite-world-demo.html`**：已填好 Infinite-World 论文内容的完整示例，便于对照原版。
- **`scripts/download_assets.sh`**：一键下载官方 `assets/`（约 200MB+ 视频）。

## 参考链接

- 项目页：https://rq-wu.github.io/projects/infinite-world/
- 论文代码：https://github.com/MeiGen-AI/Infinite-World
- arXiv：https://arxiv.org/abs/2602.02393
