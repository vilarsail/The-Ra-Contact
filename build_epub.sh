#!/bin/bash
# 打包《一的法则》导读 + 正文为 EPUB
# 用法：在项目根目录执行 ./build_epub.sh

cd "$(dirname "$0")"

OUTPUT_FILE="output/The_Ra_Contact.epub"
TITLE="The Ra Contact (一的法则)"
AUTHOR="Ra / L/L Research"

# 按顺序生成文件列表：前言, guide_001, source_001, guide_002, source_002, ...
FILES=()
if [[ -f "output/0.md" ]]; then
  FILES+=("output/0.md")
fi
for i in $(seq -w 1 106); do
  guide="output/Ra_Session_${i}_guide.md"
  source="split/Ra_Session_${i}.md"
  if [[ -f "$guide" ]]; then
    FILES+=("$guide")
  fi
  if [[ -f "$source" ]]; then
    FILES+=("$source")
  fi
done

echo "共 ${#FILES[@]} 个文件，开始打包..."

pandoc "${FILES[@]}" \
  --from markdown \
  --to epub3 \
  --output "$OUTPUT_FILE" \
  --metadata title="$TITLE" \
  --metadata author="$AUTHOR" \
  --metadata lang="zh-CN" \
  --toc \
  --toc-depth=1 \
  --css=<(cat <<'EOF'
body { font-family: "Noto Serif CJK SC", "Songti SC", serif; }
h1, h2 { font-family: "Noto Sans CJK SC", "PingFang SC", sans-serif; }
EOF
  )

echo "完成：$OUTPUT_FILE"