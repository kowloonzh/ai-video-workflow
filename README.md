# ai-video-workflow

一个 Claude Code / Codex skill：让 AI 当总导演，带你把一个想法做成一支 AI 短片。

流程是：剧情 → 分镜与配色 → 画风与设定图 → 首尾帧 → 视频提示词与提交前审核 → 生成 → 代码后期 → 打分评审与修改 → 交付。

核心原则是**把错误挡在花钱之前**：改提示词几乎免费，重画一张图很便宜，重新生成视频却按秒收钱。所以文字里能发现的错不留到图上，图上能发现的错不留到视频上。每道关卡都有独立的审核 agent 把关，关键节点会停下来和你讨论确认。

和工具无关：生图可以用 Codex 等，视频可以用 Seedance、可灵、即梦、Runway 等，后期用 ffmpeg + Python。

## 安装

把整个目录放进 skill 目录即可：

```bash
# Claude Code（个人全局）
git clone https://github.com/kowloonzh/ai-video-workflow ~/.claude/skills/ai-video-workflow
# 或只给某个项目用：<项目>/.claude/skills/ai-video-workflow
# Codex：<项目>/.agents/skills/ai-video-workflow
```

然后对 AI 说"我想做一支 AI 短片……"，或者直接调用 `/ai-video-workflow`。

依赖：ffmpeg；Python 3 + Pillow、numpy（用于 `scripts/check_keyframes.py`）。

## 目录

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 总导演规则、铁规矩、阶段与关卡、交互节点 |
| `references/story.md` | 剧情标准、剧情提示词、审故事提示词 |
| `references/storyboard.md` | 分镜规则、配色与色表、色块草图和黑白检查 |
| `references/keyframes.md` | 画风、风格特征清单、设定图、首尾帧画法和检查清单 |
| `references/video-prompt.md` | 七段式视频提示词、易错点对照表、提交前审核、生成与省钱技巧 |
| `references/post.md` | 代码后期、打分评审与修改循环、交付 |
| `references/multi-agent.md` | 四线程协作模式（主做 / 审核 / 监督 / 代理） |
| `references/tools.md` | 生图和视频工具接入（Codex、Seedance 及其他） |
| `references/model-quirks.md` | 各模型的已知怪癖和对策，可持续追加 |
| `scripts/check_keyframes.py` | 首尾帧尺寸和画幅检查，输出叠加图、差异热图、黑白图 |
| `scripts/extract_frames.sh` | 视频抽帧并读取视频信息 |

## 来源与致谢

- 主体流程、创作标准、各阶段提示词、易错点对照表、Seedance 相关经验和四线程模式，改编自 **Eian** 的文章《Claude code/Codex+Seedance AI视频：从一个想法到成片的全流程》（[原文](https://x.com/EianLu/article/2118317430665613741)）。其中不少提示词基本沿用原文。版权归原作者所有。
- 打分评审与"评审 → 修改"循环、可检验的风格特征清单，借鉴了 [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)（MIT）的 `rubric.md` 和 `template.md`，并按 AI 视频的情况改写。
- 交互节点、工具无关的适配、项目目录与日志规范、辅助脚本等是本仓库新增的内容。其中部分后期参数（锐化、码率等）是经验值，尚未经过系统验证。

如果你是原作者，并且希望调整引用方式或撤下相关内容，请提 issue。
