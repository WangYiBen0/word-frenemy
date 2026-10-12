#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — 从 data/{words,phrases}/<letter>/*.json 构建 Markdown 和 PDF

用法:
    python build.py
    python build.py --font /path/to/font.ttf

输出:
    dist/word-frenemy.md
    dist/word-frenemy.pdf

顺序: 先 words/ 再 phrases/，各自按目录内字母序，全局连续编号。
"""

import json
import os
import sys
import argparse
from pathlib import Path
import subprocess

DATA = Path('data')
DIST = Path('dist')


# ---------- 读取 ----------

def load_entries():
    entries = []
    for kind in ('words', 'phrases'):
        d = DATA / kind
        if not d.exists():
            print(f'警告: 目录不存在 {d}', file=sys.stderr)
            continue
        for f in sorted(d.rglob('*.json')):
            try:
                e = json.loads(f.read_text(encoding='utf-8'))
            except json.JSONDecodeError as ex:
                print(f'警告: 解析失败 {f}: {ex}', file=sys.stderr)
                continue
            entries.append(e)
    return entries


def renumber(entries):
    for i, e in enumerate(entries, 1):
        e['id'] = i
    return entries


# ---------- Markdown ----------

def write_markdown(entries, path):
    lines = []
    for e in entries:
        lines.append(f"{e['id']}. {e['term']}")
        for s in e.get('senses', []):
            pos = s.get('pos', '')
            meaning = s.get('meaning', '')
            lines.append(f"   - {pos} {meaning}".rstrip())
            for ex in s.get('examples', []):
                lines.append(f"     - {ex}")
        lines.append('')
    path.write_text('\n'.join(lines), encoding='utf-8')


# ---------- PDF ----------

def find_font():
    """优先用 fontconfig 找中文衬线字体，再回退到硬编码路径。"""
    # 1) 环境变量最高优先级
    env = os.environ.get('FONT_PATH')
    if env and os.path.exists(env):
        return env

    # 2) fontconfig
    queries = [
        'serif:lang=zh-cn',
        'serif:lang=zh',
        'Noto Serif CJK SC',
        'Source Han Serif SC',
        'Songti SC',
        'SimSun',
        'serif',
    ]
    for q in queries:
        try:
            out = subprocess.run(
                ['fc-match', '-f', '%{file}', q],
                capture_output=True, text=True, timeout=3,
            )
            path = out.stdout.strip()
            if path and os.path.exists(path):
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            break  # 没装 fontconfig，跳出直接回退

    # 3) 硬编码回退
    candidates = [
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSerifCJKsc-Regular.otf',
        '/usr/share/fonts/opentype/source-han-serif/SourceHanSerifSC-Regular.otf',
        '/usr/share/fonts/truetype/arphic/uming.ttc',
        '/System/Library/Fonts/Supplemental/Songti.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/simfang.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def escape_pdf_text(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

def write_pdf(entries, path, font_path=None):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        print('警告: 未安装 reportlab，跳过 PDF。安装: pip install reportlab',
              file=sys.stderr)
        return False

    if not font_path:
        font_path = find_font()
    if font_path and os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('Serif', font_path))
            font_name = 'Serif'
        except Exception as e:
            print(f'字体注册失败: {e}，用默认字体', file=sys.stderr)
            font_name = 'Times-Roman'
    else:
        print('警告: 未找到中文衬线字体，PDF 中文可能乱码。设置 FONT_PATH。',
              file=sys.stderr)
        font_name = 'Times-Roman'

    # A4 = 595 x 842 pt
    # 上下 25mm 边距 -> 可用高度 700pt
    # leading 14pt -> 正好 50 行/页
    LEADING = 14
    PAGE_MARGIN_V = 25 * mm
    PAGE_MARGIN_H = 18 * mm

    term_style = ParagraphStyle(
        'Term',
        fontName=font_name,
        fontSize=10,
        leading=LEADING,
        spaceBefore=4,
        spaceAfter=1,
    )
    sense_style = ParagraphStyle(
        'Sense',
        fontName=font_name,
        fontSize=9,
        leading=LEADING,
        leftIndent=10,
        spaceBefore=0,
        spaceAfter=0,
    )
    example_style = ParagraphStyle(
        'Example',
        fontName=font_name,
        fontSize=8.5,
        leading=LEADING,
        leftIndent=20,
        textColor='#444444',
        spaceBefore=0,
        spaceAfter=0,
    )

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        topMargin=PAGE_MARGIN_V,
        bottomMargin=PAGE_MARGIN_V,
        leftMargin=PAGE_MARGIN_H,
        rightMargin=PAGE_MARGIN_H,
        title='Word Frenemy',
    )

    story = []
    for e in entries:
        term = escape_pdf_text(e['term'])
        story.append(Paragraph(f"{e['id']}. {term}", term_style))
        for s in e.get('senses', []):
            pos = escape_pdf_text(s.get('pos', ''))
            meaning = escape_pdf_text(s.get('meaning', ''))
            story.append(Paragraph(f"- {pos} {meaning}".rstrip(), sense_style))
            for ex in s.get('examples', []):
                ex_clean = escape_pdf_text(ex.replace('**', ''))
                story.append(Paragraph(f"- {ex_clean}", example_style))
    doc.build(story)
    return True


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description='Build Word Frenemy markdown & pdf')
    ap.add_argument('--font', default=None, help='中文字体路径 (PDF)')
    ap.add_argument('--data', default='data', help='输入数据目录 (默认 data)')
    ap.add_argument('--dist', default='dist', help='输出目录 (默认 dist)')
    args = ap.parse_args()

    global DATA, DIST
    DATA = Path(args.data)
    DIST = Path(args.dist)

    entries = load_entries()
    if not entries:
        sys.exit('没有读到任何条目，检查 data/ 目录')

    renumber(entries)
    print(f'共 {len(entries)} 条')

    DIST.mkdir(parents=True, exist_ok=True)

    md_path = DIST / 'word-frenemy.md'
    write_markdown(entries, md_path)
    print(f'Markdown -> {md_path}')

    pdf_path = DIST / 'word-frenemy.pdf'
    if write_pdf(entries, pdf_path, args.font):
        print(f'PDF      -> {pdf_path}')


if __name__ == '__main__':
    main()
