"""Windows launcher for the local Qicheng Tianxia game."""
from __future__ import annotations

import http.server
import os
import signal
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path


def resource_path(name: str) -> Path:
    """Find bundled files both in source mode and in the packaged executable."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / name


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    game_dir = resource_path("index.html").parent
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(game_dir), **kwargs)

    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/"
        print(f"  器成天下走 · 瓷业长卷")
        print(f"  ──────────────────────────")
        print(f"  服务器已启动：{url}")
        print(f"  按 Ctrl+C 停止服务\n")

        # 打开浏览器
        threading.Thread(target=lambda: webbrowser.open(url, new=1), daemon=True).start()

        # 优雅退出信号处理
        shutdown_event = threading.Event()

        def handle_signal(signum, frame):
            print("\n  正在关闭服务...")
            shutdown_event.set()
            server.shutdown()

        if sys.platform == "win32":
            # Windows 上 signal.SIGINT 会触发 KeyboardInterrupt
            pass
        else:
            signal.signal(signal.SIGINT, handle_signal)
            signal.signal(signal.SIGTERM, handle_signal)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n  正在关闭服务...")
        finally:
            server.server_close()
            print("  服务已停止。")
            os._exit(0)


if __name__ == "__main__":
    main()
