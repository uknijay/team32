import flet as ft
import asyncio
import sys, os
import numpy as np


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))


from sim import Game               
from hilo import HiLo
from wong_halves import WongHalves
from Hi_opt_II import Hi_Opt_II

PALETTE = {
    "bg": "#0B0F1A",
    "surface": "#0F172A",
    "primary": "#00A3FF",
    "text": "#E2E8F0",
}

def glass(content=None, padding=10, expand=False, height=None, margin=ft.margin.all(0)):
    return ft.Container(
        content=content,
        padding=padding,
        margin=margin,
        bgcolor=ft.Colors.with_opacity(0.14, PALETTE["surface"]),   # new Colors.with_opacity API
        border_radius=10,
        border=ft.border.all(1, ft.Colors.with_opacity(0.22, "#FFFFFF")),
        shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.with_opacity(0.25, PALETTE["primary"])),
        expand=expand,
        height=height,
    )

def make_strategy_block(idx: int) -> ft.Control:
    return glass(
        ft.Column(
            [
                ft.Dropdown(
                    label=f"Strategy #{idx}",
                    hint_text="Select counting system",
                    options=[
                        ft.dropdown.Option("Hi-Lo"),
                        ft.dropdown.Option("Wong Halves"),
                        ft.dropdown.Option("Hi-Opt II"),
                    ],
                    value="Hi-Lo",
                    bgcolor=PALETTE["surface"],
                    border_color=PALETTE["surface"],
                    focused_border_color=PALETTE["primary"],
                    text_style=ft.TextStyle(color=PALETTE["text"]),
                ),
                ft.TextField(
                    label="Name",
                    hint_text=f"e.g. Player {idx}",
                    bgcolor=PALETTE["surface"],
                    border_color=PALETTE["surface"],
                    focused_border_color=PALETTE["primary"],
                    cursor_color=PALETTE["primary"],
                    text_style=ft.TextStyle(color=PALETTE["text"]),
                    border_radius=8,
                ),
            ],
            spacing=6,
        ),
        padding=8,
        margin=ft.margin.only(bottom=6),
    )

STRAT_MAP = {
    "Hi-Lo": HiLo,
    "Wong Halves": WongHalves,
    "Hi-Opt II": Hi_Opt_II,
}

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = PALETTE["bg"]
    page.padding = 0


    log_view = ft.ListView(expand=True, spacing=6, auto_scroll=True)

    def log(msg: str):
        log_view.controls.append(ft.Text(msg, color=PALETTE["text"]))
        page.update()


    tf_sims      = ft.TextField(label="Number of Simulations", hint_text="e.g. 50", keyboard_type=ft.KeyboardType.NUMBER,
                                bgcolor=PALETTE["surface"], border_color=PALETTE["surface"], focused_border_color=PALETTE["primary"],
                                cursor_color=PALETTE["primary"], text_style=ft.TextStyle(color=PALETTE["text"]), border_radius=8)
    tf_rounds    = ft.TextField(label="Number of Rounds", hint_text="e.g. 500", keyboard_type=ft.KeyboardType.NUMBER,
                                bgcolor=PALETTE["surface"], border_color=PALETTE["surface"], focused_border_color=PALETTE["primary"],
                                cursor_color=PALETTE["primary"], text_style=ft.TextStyle(color=PALETTE["text"]), border_radius=8)
    tf_min_stake = ft.TextField(label="Min Stake", hint_text="e.g. 15", prefix_icon=ft.Icons.CURRENCY_POUND, keyboard_type=ft.KeyboardType.NUMBER,
                                bgcolor=PALETTE["surface"], border_color=PALETTE["surface"], focused_border_color=PALETTE["primary"],
                                cursor_color=PALETTE["primary"], text_style=ft.TextStyle(color=PALETTE["text"]), border_radius=8)
    tf_bankroll  = ft.TextField(label="Starting Bankroll", hint_text="e.g. 1000", prefix_icon=ft.Icons.CURRENCY_POUND, keyboard_type=ft.KeyboardType.NUMBER,
                                bgcolor=PALETTE["surface"], border_color=PALETTE["surface"], focused_border_color=PALETTE["primary"],
                                cursor_color=PALETTE["primary"], text_style=ft.TextStyle(color=PALETTE["text"]), border_radius=8)

    game_environment_values = glass(
        ft.Column(
            [
                tf_sims, tf_rounds, tf_min_stake, tf_bankroll,
                ft.Divider(color=ft.Colors.with_opacity(0.15, "white")),
            ],
            spacing=8,
        )
    )


    strategies_col = ft.Column(spacing=6, controls=[make_strategy_block(1)])

    def add_strategy(_):
        strategies_col.controls.append(make_strategy_block(len(strategies_col.controls) + 1))
        page.update()

    strategies_header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Strategies", size=14, color=PALETTE["text"]),
            ft.IconButton(icon=ft.Icons.ADD, tooltip="Add strategy", icon_color=PALETTE["primary"], on_click=add_strategy),
        ],
    )


    run_btn = ft.FilledButton("Start Simulation", icon=ft.Icons.ROCKET_LAUNCH)
    start_button = glass(ft.Column([run_btn], spacing=8))


    sidebar = ft.Container(
        width=300,
        bgcolor=PALETTE["surface"],
        padding=12,
        content=ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("MENU", size=14, color=PALETTE["text"]),
                start_button,
                game_environment_values,
                ft.Divider(color=ft.Colors.with_opacity(0.15, "white")),
                strategies_header,
                strategies_col,
                ft.Container(expand=True),
                ft.Text("v1.0", size=12, color="#64748B"),
            ],
        ),
    )


    main_area = ft.Container(
        expand=True,
        padding=24,
        bgcolor=PALETTE["bg"],
        content=glass(
            ft.Column([ft.Text("Run output (raw):", color=PALETTE["text"], size=16), log_view], spacing=8),
            expand=True,
        ),
    )

    page.add(ft.Row([sidebar, main_area], expand=True))


    def parse_int(field: ft.TextField, default: int) -> int:
        try:
            return int(field.value)
        except:
            return default

    def collect_player_list(bankroll: int):
        players = []
        idx = 0
        for card in strategies_col.controls:
            if isinstance(card, ft.Container) and isinstance(card.content, ft.Column):
                c = card.content.controls
                if len(c) >= 2 and isinstance(c[0], ft.Dropdown) and isinstance(c[1], ft.TextField):
                    strat = c[0].value or "Hi-Lo"
                    name  = (c[1].value or "").strip() or f"{strat}#{idx+1}"
                    players.append((STRAT_MAP.get(strat, HiLo), name, bankroll))
                    idx += 1
        return players


    async def run_simulation_async():
        # clear previous logs
        log_view.controls.clear()
        page.update()

        simulations = parse_int(tf_sims, 50)
        rounds      = parse_int(tf_rounds, 500)
        min_stake   = parse_int(tf_min_stake, 10)
        bankroll    = parse_int(tf_bankroll, 1000)
        deck_count  = 6

        players = collect_player_list(bankroll)
        if not players:
            log("[error] No strategies selected; add at least one.")
            return

        log("---------------------------------------------------")
        log(f"Starting sim: sims={simulations}, rounds={rounds}, min_stake=£{min_stake}, bankroll=£{bankroll}, decks={deck_count}")
        log(f"Players: {', '.join(name for _, name, _ in players)}")

        results = {name: [] for _, name, _ in players}


        for s in range(1, simulations + 1):
            game = Game(players, deck_count, min_stake)
            for r in range(rounds):
                if not game.playing:
                    break
                game.new_turn()
                if r % 50 == 0:
                    await asyncio.sleep(0)  

            iter_players = getattr(game, "starting_players", getattr(game, "players", []))
            for p in iter_players:
                # record this sim's final bankroll for each player 
                try:
                    results[p.name].append(p.money)
                except KeyError:
                    results[p.name] = [p.money]
                results.setdefault(p.name, []).append(p.money)

            if s % max(1, simulations // 10) == 0:
                log(f"Progress: {s}/{simulations} sims…")
                await asyncio.sleep(0)

        log("----- Summary (per player) -----")
        for name, vals in results.items():
            if not vals:
                continue
            arr = np.array(vals, dtype=float)
            mean = arr.mean()
            med  = float(np.median(arr))
            p25  = float(np.percentile(arr, 25))
            p75  = float(np.percentile(arr, 75))
            mn   = float(arr.min())
            mx   = float(arr.max())
            log(f"{name}: mean=£{mean:.2f} | median=£{med:.2f} | p25=£{p25:.2f} | p75=£{p75:.2f} | min=£{mn:.2f} | max=£{mx:.2f}")

        log("Done.")

    async def on_start_click(e):
        await run_simulation_async()

    run_btn.on_click = on_start_click

if __name__ == "__main__":
    ft.app(target=main)