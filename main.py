from __future__ import annotations

import asyncio
import json
import random
import time
from pathlib import Path

import flet as ft


BG = "#080B18"
PANEL = "#111831"
PANEL_2 = "#171F3F"
CYAN = "#53F5E7"
PURPLE = "#A78BFA"
PINK = "#FF5D9E"
GOLD = "#FFD166"
WHITE = "#F5F7FF"
MUTED = "#99A6C9"
BOARD_H = 410
LANES = 5
ROUND_SECONDS = 45


def main(page: ft.Page):
    page.title = "نئون‌ران | Neon Run"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.rtl = True
    page.scroll = ft.ScrollMode.AUTO

    save_path = Path.home() / ".neonran-save.json"
    save = {"best": 0, "stars": 0, "games": 0}
    try:
        if save_path.exists():
            loaded = json.loads(save_path.read_text(encoding="utf-8"))
            for key in save:
                save[key] = int(loaded.get(key, save[key]))
    except (OSError, ValueError, TypeError):
        pass

    state = {
        "mode": "home",
        "paused": False,
        "lane": 2,
        "score": 0,
        "round_stars": 0,
        "lives": 3,
        "seconds": ROUND_SECONDS,
        "elapsed": 0.0,
        "shield_until": 0.0,
        "streak": 0,
    }

    def label(value: str, size: int = 16, color: str = WHITE,
              weight: ft.FontWeight = ft.FontWeight.NORMAL,
              text_align: ft.TextAlign = ft.TextAlign.CENTER) -> ft.Text:
        return ft.Text(value, size=size, color=color, weight=weight, text_align=text_align)

    def card(content, padding: int = 16, bgcolor: str = PANEL, width=None):
        return ft.Container(
            content=content,
            padding=padding,
            bgcolor=bgcolor,
            border_radius=20,
            width=width,
        )

    def action_button(caption: str, handler, bgcolor: str = CYAN,
                      color: str = BG, width=None):
        return ft.Button(
            content=caption,
            on_click=handler,
            width=width,
            bgcolor=bgcolor,
            color=color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=16),
                padding=16,
            ),
        )

    def persist():
        try:
            save_path.write_text(json.dumps(save, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass

    def set_screen(content):
        page.controls.clear()
        page.add(ft.SafeArea(content=content, expand=True))
        page.update()

    def show_home():
        state["mode"] = "home"
        page.scroll = ft.ScrollMode.AUTO
        width = max(280, min(float(page.width or 380) - 28, 440))
        hero = ft.Container(
            content=ft.Column(
                controls=[
                    label("🚀", 64),
                    label("نِئون‌ران", 36, CYAN, ft.FontWeight.BOLD),
                    label("NEON RUN  •  ARCADE SURVIVAL", 11, PURPLE, ft.FontWeight.BOLD),
                    label("به فضای نئونی خوش اومدی؛ تا می‌تونی زنده بمون!", 14, MUTED),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.Padding(18, 22, 18, 22),
            bgcolor="#101733",
            border_radius=28,
            width=width,
        )
        stats = ft.Row(
            controls=[
                card(ft.Column([label("🏆", 23), label(str(save["best"]), 22, GOLD, ft.FontWeight.BOLD),
                                label("رکورد", 12, MUTED)], spacing=4,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                     padding=10, bgcolor=PANEL, width=width / 3 - 8),
                card(ft.Column([label("✨", 23), label(str(save["stars"]), 22, CYAN, ft.FontWeight.BOLD),
                                label("ستاره‌ها", 12, MUTED)], spacing=4,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                     padding=10, bgcolor=PANEL, width=width / 3 - 8),
                card(ft.Column([label("🎮", 23), label(str(save["games"]), 22, PURPLE, ft.FontWeight.BOLD),
                                label("بازی‌ها", 12, MUTED)], spacing=4,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                     padding=10, bgcolor=PANEL, width=width / 3 - 8),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )
        how_to = card(
            ft.Column(
                controls=[
                    label("چطور بازی کنی؟", 17, WHITE, ft.FontWeight.BOLD),
                    ft.Row([label("⬅️ ➡️", 21), label("با دکمه‌ها بین ۵ مسیر جابه‌جا شو", 13, MUTED)],
                           alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Row([label("✨", 21), label("ستاره‌ها رو جمع کن و امتیاز بگیر", 13, MUTED)],
                           alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    ft.Row([label("☄️", 21), label("از شهاب‌سنگ‌ها دوری کن؛ سپر کمکت می‌کنه", 13, MUTED)],
                           alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
            bgcolor=PANEL,
            width=width,
        )
        content = ft.Column(
            controls=[
                ft.Container(height=10),
                hero,
                stats,
                action_button("▶   شروع بازی", start_game, bgcolor=CYAN, color=BG, width=width),
                action_button("📖   راهنمای کامل", show_help, bgcolor=PANEL_2, color=WHITE, width=width),
                how_to,
                label("ساخته‌شده برای عاشقان بازی‌های آرکید 💜", 11, MUTED),
                ft.Container(height=12),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
        )
        set_screen(ft.Container(content=content, padding=14, alignment=ft.Alignment(0, 0)))

    def show_help(e=None):
        width = max(280, min(float(page.width or 380) - 28, 440))
        details = card(
            ft.Column(
                controls=[
                    label("📘 راهنمای نئون‌ران", 25, CYAN, ft.FontWeight.BOLD),
                    label("هدف: در ۴۵ ثانیه بیشترین امتیاز را جمع کن و سه جانت را حفظ کن.", 15, WHITE),
                    ft.Divider(color="#293458"),
                    label("✨ ستاره", 25, GOLD, ft.FontWeight.BOLD),
                    label("هر ستاره ۱۰ امتیاز دارد. پنج ستارهٔ پشت‌سرهم، امتیاز جایزه می‌دهد.", 14, MUTED),
                    label("☄️ شهاب‌سنگ", 25, PINK, ft.FontWeight.BOLD),
                    label("برخورد با شهاب‌سنگ یک جان کم می‌کند و ۵ امتیاز از دست می‌دهی.", 14, MUTED),
                    label("🛡️ سپر نئونی", 25, CYAN, ft.FontWeight.BOLD),
                    label("با گرفتن سپر، برای ۵ ثانیه از برخورد با شهاب‌سنگ در امان می‌مانی.", 14, MUTED),
                    ft.Divider(color="#293458"),
                    label("هرچه بیشتر زنده بمانی، سرعت بازی و تعداد خطرها بیشتر می‌شود!", 14, PURPLE),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=22,
            width=width,
        )
        set_screen(ft.Container(
            content=ft.Column(
                [details, action_button("بازگشت به خانه", show_home, bgcolor=CYAN, width=width)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
            padding=14,
            alignment=ft.Alignment(0, 0),
        ))

    def show_game_over():
        final_score = state["score"]
        new_record = final_score >= save["best"] and final_score > 0
        save["best"] = max(save["best"], final_score)
        save["stars"] += state["round_stars"]
        save["games"] += 1
        persist()

        width = max(280, min(float(page.width or 380) - 28, 440))
        report = card(
            ft.Column(
                controls=[
                    label("💥" if state["lives"] <= 0 else "⏱️", 48),
                    label("پایان بازی!", 30, PINK, ft.FontWeight.BOLD),
                    label("رکورد جدید! 🎉" if new_record else "دفعهٔ بعد قوی‌تر برگرد!", 16, GOLD if new_record else MUTED),
                    ft.Divider(color="#293458"),
                    label("امتیاز نهایی", 14, MUTED),
                    label(str(final_score), 48, CYAN, ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            card(ft.Column([label("✨", 22), label(str(state["round_stars"]), 20, GOLD, ft.FontWeight.BOLD),
                                            label("ستاره", 12, MUTED)], spacing=2,
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                 padding=10, bgcolor="#1A2344", width=width / 2 - 34),
                            card(ft.Column([label("❤️", 22), label(str(state["lives"]), 20, PINK, ft.FontWeight.BOLD),
                                            label("جان باقی‌مانده", 12, MUTED)], spacing=2,
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                 padding=10, bgcolor="#1A2344", width=width / 2 - 34),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            padding=22,
            width=width,
        )
        set_screen(ft.Container(
            content=ft.Column(
                [
                    report,
                    action_button("🔁   بازی دوباره", start_game, bgcolor=CYAN, width=width),
                    action_button("⌂   بازگشت به خانه", show_home, bgcolor=PANEL_2, color=WHITE, width=width),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
            ),
            padding=14,
            alignment=ft.Alignment(0, 0),
        ))

    async def start_game(e=None):
        state.update({
            "mode": "playing",
            "paused": False,
            "lane": 2,
            "score": 0,
            "round_stars": 0,
            "lives": 3,
            "seconds": ROUND_SECONDS,
            "elapsed": 0.0,
            "shield_until": 0.0,
            "streak": 0,
        })
        show_game()
        page.run_task(game_loop)

    def show_game():
        page.scroll = ft.ScrollMode.AUTO
        width = max(280, min(float(page.width or 380) - 24, 440))
        lane_step = width / LANES

        score_text = label("امتیاز  0", 15, CYAN, ft.FontWeight.BOLD)
        time_text = label("⏱ 45", 15, GOLD, ft.FontWeight.BOLD)
        lives_text = label("❤️ ❤️ ❤️", 15, PINK, ft.FontWeight.BOLD)
        shield_text = label("", 12, CYAN, ft.FontWeight.BOLD)
        hint_text = label("ستاره‌ها رو بگیر، از شهاب‌سنگ‌ها فرار کن!", 12, MUTED)

        hud = card(
            ft.Column(
                [
                    ft.Row([score_text, time_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([lives_text, shield_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                spacing=8,
            ),
            padding=14,
            width=width,
        )

        background_items = []
        rng = random.Random(9)
        for _ in range(22):
            dot_size = rng.choice([2, 3, 4])
            background_items.append(ft.Container(
                left=rng.randrange(max(1, int(width - dot_size))),
                top=rng.randrange(0, BOARD_H - dot_size),
                width=dot_size,
                height=dot_size,
                bgcolor=rng.choice(["#37416F", "#56618F", "#26315B"]),
                border_radius=dot_size,
            ))
        for lane in range(1, LANES):
            background_items.append(ft.Container(
                left=lane_step * lane,
                top=0,
                width=1,
                height=BOARD_H,
                bgcolor="#252D52",
            ))

        player = ft.Container(
            left=lane_step * 2 + (lane_step - 48) / 2,
            top=BOARD_H - 65,
            width=48,
            height=52,
            content=label("🚀", 34),
            alignment=ft.Alignment(0, 0),
            bgcolor="#202A53",
            border_radius=16,
            border=ft.Border.all(1, CYAN),
        )
        arena = ft.Stack(
            width=width,
            height=BOARD_H,
            controls=background_items + [player],
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        board = ft.Container(
            content=arena,
            width=width,
            height=BOARD_H,
            bgcolor="#0B1026",
            border=ft.Border.all(1, "#28345F"),
            border_radius=22,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
        pause_button = ft.Button(
            content="⏸ مکث",
            bgcolor=PANEL_2,
            color=WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), padding=14),
            width=width / 2 - 8,
        )

        def move_player(delta: int):
            state["lane"] = max(0, min(LANES - 1, state["lane"] + delta))
            player.left = lane_step * state["lane"] + (lane_step - 48) / 2
            page.update()

        def toggle_pause(e=None):
            state["paused"] = not state["paused"]
            pause_button.content = "▶ ادامه" if state["paused"] else "⏸ مکث"
            hint_text.value = "بازی متوقف شده" if state["paused"] else "برگرد به بازی؛ رکوردت منتظرته!"
            page.update()

        pause_button.on_click = toggle_pause

        controls = ft.Row(
            controls=[
                ft.Button(
                    content="◀  چپ",
                    on_click=lambda e: move_player(-1),
                    bgcolor="#252D52",
                    color=WHITE,
                    width=width / 2 - 8,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), padding=14),
                ),
                ft.Button(
                    content="راست  ▶",
                    on_click=lambda e: move_player(1),
                    bgcolor="#252D52",
                    color=WHITE,
                    width=width / 2 - 8,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), padding=14),
                ),
            ],
            spacing=16,
        )

        set_screen(ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [label("NEON RUN", 16, CYAN, ft.FontWeight.BOLD),
                         label("مرحلهٔ بقا", 13, PURPLE, ft.FontWeight.BOLD)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=width,
                    ),
                    hud,
                    board,
                    hint_text,
                    controls,
                    ft.Row([pause_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            alignment=ft.Alignment(0, 0),
        ))

        state["arena"] = arena
        state["player"] = player
        state["score_text"] = score_text
        state["time_text"] = time_text
        state["lives_text"] = lives_text
        state["shield_text"] = shield_text
        state["hint_text"] = hint_text
        state["objects"] = []
        state["board_width"] = width
        state["lane_step"] = lane_step

    async def game_loop():
        spawn_clock = 0.0
        previous = time.monotonic()
        while state["mode"] == "playing":
            await asyncio.sleep(0.05)
            now = time.monotonic()
            dt = min(now - previous, 0.12)
            previous = now

            if state["paused"]:
                continue

            state["elapsed"] += dt
            state["seconds"] = max(0.0, ROUND_SECONDS - state["elapsed"])
            state["shield_until"] = max(0.0, state["shield_until"] - dt)
            speed = 158 + state["elapsed"] * 3.2
            spawn_clock += dt
            spawn_gap = max(0.30, 0.72 - state["elapsed"] * 0.008)

            arena = state["arena"]
            lane_step = state["lane_step"]
            board_width = state["board_width"]
            objects = state["objects"]

            if spawn_clock >= spawn_gap:
                spawn_clock = 0.0
                lane = random.randrange(LANES)
                kind = random.choices(["star", "meteor", "shield"], weights=[58, 34, 8], k=1)[0]
                glyph, size = {"star": ("✨", 26), "meteor": ("☄️", 29), "shield": ("🛡️", 26)}[kind]
                item = ft.Container(
                    left=lane_step * lane + (lane_step - 40) / 2,
                    top=-42,
                    width=40,
                    height=40,
                    content=label(glyph, size),
                    alignment=ft.Alignment(0, 0),
                )
                arena.controls.append(item)
                objects.append({"view": item, "lane": lane, "y": -42.0, "kind": kind})

            hit_low = BOARD_H - 91
            hit_high = BOARD_H - 43
            for obj in list(objects):
                obj["y"] += speed * dt
                obj["view"].top = obj["y"]

                collision = (
                    obj["lane"] == state["lane"]
                    and hit_low <= obj["y"] <= hit_high
                )
                if collision:
                    objects.remove(obj)
                    if obj["view"] in arena.controls:
                        arena.controls.remove(obj["view"])
                    if obj["kind"] == "star":
                        state["streak"] += 1
                        bonus = 10
                        if state["streak"] % 5 == 0:
                            bonus += 15
                            state["hint_text"].value = "🔥 کمبو! ۱۵ امتیاز جایزه گرفتی!"
                        else:
                            state["hint_text"].value = "✨ آفرین! یک ستاره گرفتی"
                        state["score"] += bonus
                        state["round_stars"] += 1
                    elif obj["kind"] == "shield":
                        state["shield_until"] = 5.0
                        state["hint_text"].value = "🛡️ سپر فعال شد؛ ۵ ثانیه مصونیت!"
                    elif state["shield_until"] > 0:
                        state["hint_text"].value = "💫 سپر نئونی ضربه رو دفع کرد!"
                    else:
                        state["lives"] -= 1
                        state["score"] = max(0, state["score"] - 5)
                        state["streak"] = 0
                        state["hint_text"].value = "💥 برخورد! یک جان و ۵ امتیاز از دست رفت"
                elif obj["y"] > BOARD_H + 5:
                    objects.remove(obj)
                    if obj["view"] in arena.controls:
                        arena.controls.remove(obj["view"])

            remaining_lives = max(0, state["lives"])
            state["score_text"].value = f"امتیاز  {state['score']}"
            state["time_text"].value = f"⏱  {int(state['seconds'] + 0.99)}"
            state["lives_text"].value = " ".join(["❤️"] * remaining_lives) or "🖤"
            state["shield_text"].value = f"🛡️ {state['shield_until']:.1f}s" if state["shield_until"] > 0 else ""
            page.update()

            if state["lives"] <= 0 or state["seconds"] <= 0:
                break

        if state["mode"] == "playing":
            state["mode"] = "over"
            show_game_over()

    def start_game_from_event(e=None):
        page.run_task(start_game, e)

    # Replace the callback helper with a task-safe entry point for sync UI events.
    show_home()


if __name__ == "__main__":
    ft.run(main)
