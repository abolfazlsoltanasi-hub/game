"""Flet Android shell for the original Persian Word Guess game.

The game itself lives in assets/game.html. Hosting it in Android WebView keeps
its existing CSS, JavaScript game rules, local saves, and Persian word bank
intact instead of replacing it with a different game.
"""
import os
from pathlib import Path

import flet as ft
import flet_webview as fwv


APP_TITLE = "حدس کلمه"
BACKGROUND = "#0b0820"


def assets_directory() -> Path:
    configured = os.environ.get("FLET_ASSETS_DIR")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path(__file__).resolve().parent / "assets").resolve()


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BACKGROUND
    page.padding = 0
    page.spacing = 0

    game_file = assets_directory() / "game.html"
    if not game_file.is_file():
        page.add(
            ft.SafeArea(
                content=ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=BACKGROUND,
                    padding=24,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.Text("🎯", size=48),
                            ft.Text(
                                APP_TITLE,
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color="#c4b5fd",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "فایل بازی پیدا نشد. مطمئن شو assets/game.html "
                                "در بستهٔ برنامه قرار گرفته است.",
                                size=15,
                                color="#cbd5e1",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
                expand=True,
            )
        )
        return

    game_view = fwv.WebView(
        url=game_file.as_uri(),
        bgcolor=BACKGROUND,
        expand=True,
        on_web_resource_error=lambda event: print(
            f"[Word Guess WebView] Resource error: {event.data}"
        ),
        on_console_message=lambda event: print(
            f"[Word Guess JavaScript] {event}"
        ),
    )

    page.add(
        ft.SafeArea(
            content=game_view,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
