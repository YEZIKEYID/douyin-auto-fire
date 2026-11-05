"""Keep cloud runs check-only until SEND_ENABLED is explicitly set."""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping

def command(env: Mapping[str, str], python: str = sys.executable) -> list[str]:
    enabled = env.get("SEND_ENABLED", "").strip().lower() == "true"
    event = env.get("EVENT_NAME", "")
    requested_send = event == "workflow_dispatch" and env.get("REQUESTED_DRY_RUN", "").lower() == "false"
    scheduled_send = event == "schedule"
    send = enabled and (requested_send or scheduled_send)
    return [python, "run.py"] + ([] if send else ["--dry-run"])

def main() -> int:
    args = command(os.environ)
    print("仅检查登录和好友，不发送消息" if "--dry-run" in args else "执行已启用的消息发送任务", flush=True)
    root = Path(__file__).resolve().parents[1]
    return subprocess.run(args, cwd=root, check=False).returncode

if __name__ == "__main__":
    raise SystemExit(main())
