# Word Frenemy

> 熟词生义 · 熟悉的词，陌生的义  
> Familiar words, unfamiliar meanings.

![License](https://img.shields.io/github/license/WangYiBen0/word-frenemy)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Data](https://img.shields.io/badge/data-JSON%20%7C%20Markdown-blue)

**Word Frenemy** 是一个专注于「熟词生义」的开源项目。

你认识 `address`，但可能不知道它还能表示「处理、应对」；  
你认识 `company`，但可能不知道它还能表示「陪伴」；  
你认识 `fine`，但可能不知道它还能表示「罚款」和「细微的」。

这些词就像你的 **frenemy**：看起来是朋友，实际可能让你在阅读、考试、翻译中翻车。

---

## 简介

**Word Frenemy** 收集英语中常见的「熟词生义」，并提供：

- 常见义 vs 生义对比
- 真实例句与翻译
- 词性、难度、考试标签
- JSON / Markdown 双格式数据
- 可持续扩展的词条模板

目标：帮助英语学习者更系统地掌握那些「以为自己认识」的单词。

---

## 为什么叫 Word Frenemy？

**Frenemy = Friend + Enemy**

熟词像朋友，让你觉得熟悉；  
生义像敌人，在你最放松的时候给你一刀。

所以这个项目叫 **Word Frenemy**。

---

## 快速开始

```bash
git clone https://github.com/WangYiBen0/word-frenemy.git
cd word-frenemy
```

浏览 JSON 词库：

```bash
cat data/words.json
```

---

## 数据格式

JSON 示例

```json
[
  {
    "word": "address",
    "common": ["n. 地址；住址"],
    "uncommon": [
      {
        "pos": "v.",
        "meaning": "处理；应对；解决",
        "example": "The government must address the housing crisis.",
        "translation": "政府必须解决住房危机。",
        "tags": ["CET6", "考研", "雅思"],
        "level": "B2"
      }
    ],
    "notes": "address 作动词时，常考“处理、应对”，而不是“写地址”。"
  }
]
```

---

## 目录结构

```text
word-frenemy/
├── README.md
├── LICENSE
├── data
│   ├── phrases
│   │   └── a
│   │       └── a_host_of.json
│   └── words/
│       └── a/
│           └── address.json
└── build.py
```

---

## 如何贡献

欢迎 PR！你可以添加新词条、修正释义、补充例句或改进工具。

### 添加一个新词条（示例：address）

1. Fork 本仓库
2. 创建分支：

```bash
git checkout -b add/address
```

3. 在 `data/words.json` 中添加词条
4. 提交：

```bash
git add .
git commit -m "feat: add word `address`"
git push origin add/address
```

5. 提交 Pull Request

### 收录标准

- 常见义与生义差异明显
- 生义在真实语料、考试或日常阅读中有实用价值
- 至少提供一个真实例句和中文翻译
- 标注词性、难度、标签
- 尽量注明来源
- 不收录拼写错误、纯专有名词、过于生僻且无实用价值的义项

---

## License

MIT © Word Frenemy Contributors

---

如果这个项目对你有帮助，欢迎 Star ⭐、Fork、PR。

**Familiar words, unfamiliar meanings.**
