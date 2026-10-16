"""Flet Android shell for the original Persian Word Guess game.

The HTML/CSS/JavaScript game is bundled locally and rendered in Android WebView.
This preserves the original Persian gameplay and offline word bank.
"""
import os
from pathlib import Path

import flet as ft
import flet_webview as fwv


APP_TITLE = "حدس کلمه"
BACKGROUND = "#0b0820"
ACCENT = "#a855f7"


def assets_directory() -> Path:
    """Resolve bundled Flet assets in both local runs and packaged builds."""
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
                expand=True,
                content=ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=BACKGROUND,
                    padding=24,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=14,
                        controls=[
                            ft.Text("🎯", size=54),
                            ft.Text(
                                APP_TITLE,
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color="#c4b5fd",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "فایل بازی پیدا نشد. مطمئن شو assets/game.html "
                                "همراه برنامه بسته‌بندی شده است.",
                                size=14,
                                color="#cbd5e1",
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                ),
            )
        )
        return

    loading = ft.Container(
        expand=True,
        bgcolor=BACKGROUND,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Container(
                    width=104,
                    height=104,
                    border_radius=30,
                    bgcolor="#1b1540",
                    border=ft.Border.all(1, "#6144a9"),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("🎯", size=58),
                ),
                ft.Text(
                    APP_TITLE,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#e9d5ff",
                ),
                ft.ProgressRing(width=32, height=32, color=ACCENT, stroke_width=3),
                ft.Text(
                    "در حال آماده‌سازی بازی…",
                    size=14,
                    color="#cbd5e1",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )

    def page_loaded(_event) -> None:
        loading.visible = False
        page.update()

    game_view = fwv.WebView(
        url=game_file.as_uri(),
        bgcolor=BACKGROUND,
        expand=True,
        on_page_ended=page_loaded,
        on_console_message=lambda event: print(f"[Word Guess JavaScript] {event}"),
        on_web_resource_error=lambda event: print(
            f"[Word Guess WebView] Resource error: {event.data}"
        ),
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Stack(expand=True, controls=[game_view, loading]),
        )
    )


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
