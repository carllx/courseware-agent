#!/usr/bin/env bash

# 参数校验
if [ "$#" -ne 3 ]; then
    echo "用法: $0 <输入文件.docx> <目标格式:pdf|md> <输出路径>"
    exit 1
fi

INPUT_FILE="$1"
FORMAT="$2"
OUTPUT_FILE="$3"

# 验证输入文件
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 找不到输入文件 '$INPUT_FILE'"
    exit 1
fi

# 验证目标格式
if [[ "$FORMAT" != "pdf" && "$FORMAT" != "md" ]]; then
    echo "错误: 目标格式必须是 pdf 或 md"
    exit 1
fi

# 验证工具依赖
if ! command -v pandoc >/dev/null 2>&1; then
    echo "错误: 必须安装 pandoc 才能执行此脚本。"
    exit 1
fi

echo "正在将 $INPUT_FILE 转换为 $FORMAT..."

# 执行转换
if [ "$FORMAT" == "md" ]; then
    # 转换为 Markdown
    pandoc "$INPUT_FILE" -f docx -t markdown -o "$OUTPUT_FILE"
elif [ "$FORMAT" == "pdf" ]; then
    # 转换为 PDF (通常需要配置相应的 pdf-engine)
    pandoc "$INPUT_FILE" -f docx -o "$OUTPUT_FILE"
fi

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "转换成功: $OUTPUT_FILE"
    exit 0
else
    echo "转换失败。如果是 PDF 转换失败，请检查是否已正确配置相关依赖引擎 (如 xelatex、basictex 等)。"
    exit 1
fi
