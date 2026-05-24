#!/usr/bin/env python3
"""Claude UserPromptSubmit hook for Presentation Director requests."""

import json
import re
import sys


PRESENTATION_RE: re.Pattern[str] = re.compile(
    r"pptx?|"
    r"(?<![A-Za-z])(powerpoint|slides?|slide deck|presentation|deck)(?![A-Za-z])|"
    r"(präsentation|praesentation|folien)|"
    r"(幻灯片|演示文稿|做\s*PPT|生成\s*PPT|制作\s*PPT)",
    re.IGNORECASE,
)


def main() -> int:
    try:
        payload: dict[str, object] = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    prompt: object = payload.get("prompt", "")
    if not isinstance(prompt, str) or not PRESENTATION_RE.search(prompt):
        return 0

    additional_context: str = (
        "[Presentation Director hook] 检测到 PPT / slides / presentation 请求。"
        "全新 PPTX 必须使用 /Users/zengtao/Doc/My code/Presentation-Director 的 deck-builder / Presentation Director 流程；"
        "content_language 和 output_constraints 必须分开确认；"
        "init 时要传入最近用户请求作为 --conversation-text，让 Director HTML 页面 ui_language 自动跟随当前对话语言；"
        "生成前必须打开或呈现确认页/等价确认，并通过状态文件自动等待用户在 HTML 中点击确认；"
        "不要要求用户复制/粘贴，也不要要求用户回聊天里回复已确认；"
        "如果工作区可用 Presentation Director，生成前运行 "
        "`python3 scripts/presentation_director.py --base-dir . guard --task <task-slug>`；"
        "guard 失败时用 `presentation_director.py serve-wait --task <task-slug> --for confirmed` 打开页面并自动等待；不得生成 PPTX。"
    )

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": additional_context,
                }
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
