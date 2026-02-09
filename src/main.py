from __future__ import annotations

import wx

try:
    from .app import RecorderApp
except ImportError:  # pragma: no cover
    from app import RecorderApp


def main() -> None:
    app = RecorderApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
