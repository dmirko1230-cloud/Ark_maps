import flet as ft
import requests
from datetime import datetime, timedelta
import calendar
import json


# ============================================================
# Ruhrpott Survivor App
# Kleine Android-taugliche Flet-App
# Features:
# - BattleMetrics Spielerzahlen
# - Map Links
# - Vote Links
# - Tageshaken
# - Vote Counter
# - Monatspunkte
# - vollständige Vote-Tage
# - globaler Streak über Monats-/Jahreswechsel
# - offener Streak ohne Enddatum
# - Badges bis "Ruhrpott Gott"
# ============================================================


SERVER_LISTE = {
    "THE ISLAND": {"id": "36953667", "url": "https://asamap.axi92.at/map/c6c6f105-06f1-41de-9f5e-9f38afe18502"},
    "EXTINCTION": {"id": "36959230", "url": "https://asamap.axi92.at/map/558c1013-0989-40b7-86b4-bbd2b6c529a8"},
    "SE": {"id": "36959212", "url": "https://asamap.axi92.at/map/a2865e94-22f4-47a7-bc62-daefe2b5c2e8"},
    "VALGUERO": {"id": "38696507", "url": "https://asamap.axi92.at/map/fde35796-7865-48f2-a680-8680525a1962"},
    "SVARTALFHEIM": {"id": "36953585", "url": "https://asamap.axi92.at/map/2d6e46e1-267c-4229-89c1-8be4fdbeb9f6"},
    "CENTER": {"id": "36959198", "url": "https://asamap.axi92.at/map/cd7a8226-4396-48ad-93f6-6af18d9eb627"},
    "ABERRATION": {"id": "36959246", "url": "https://asamap.axi92.at/map/14dc4038-1df6-4055-a65e-66ced672b366"},
    "ASTRAEOS": {"id": "38696478", "url": "https://asamap.axi92.at/map/543e8878-779c-4694-84b1-cc5fbfcdec21"},
    "RAGNARÖK": {"id": "38696502", "url": "https://asamap.axi92.at/map/9c404416-0263-42c7-a067-a14723f502bc"},
    "LOST CITY": {"id": "36953589", "url": "https://asamap.axi92.at/map/80196515-b882-4819-926c-dc381adcb0dc"},
    "LOST COLONY": {"id": "36959287", "url": "https://asamap.axi92.at/map/f7df5ef9-212b-453d-bc46-e8357a566a36"},
}


VOTE_ASA = [
    ("Island", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-island-crossark-clustert5h5x25-49"),
    ("SE", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-se-crossark-clustert5h5x25-50"),
    ("Center", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-center-crossark-clustert5h5x25-51"),
    ("Ragnarok", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-ragnarok-crossark-clustert5h5x25-52"),
    ("Aberration", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-aberration-crossark-clustert5h5x25-57"),
    ("Extinction", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-extinction-crossark-clustert5h5x25-112"),
    ("Astraeos", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-astraeos-crossark-clustert5h5x25-113"),
    ("Svartalfheim", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-svartalfheim-crossark-clustert5h5x25-132"),
    ("Valguero", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-valguero-crossark-clustert5h5x25-170"),
    ("Lost Colony", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-lostcolony-crossark-clustert5h5x25-193"),
    ("Lost City", 100, "https://asa-server.de/server/ruhrpott-survivor-pve-lostcitycrossark-clustert5h5x25-194"),
]


VOTE_DE = [
    ("Island DE", 550, "https://deutsche-arkserver.de/server/ruhrpott-survivor-pve-island-crossark-cluster-t5h5x2-5.46322/"),
    ("Ragnarok DE", 550, "https://deutsche-arkserver.de/server/ruhrpott-survivor-pve-ragnarok-crossark-cluster-t5h5x2-5.46373/"),
]


# Globale Storage Keys.
# Diese laufen NICHT monatlich aus.
STREAK_KEY = "rs_global_streak"
LAST_FULL_DAY_KEY = "rs_last_full_vote_day"



def heute():
    return datetime.now().strftime("%Y-%m-%d")


def gestern():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def aktueller_monat():
    return datetime.now().strftime("%Y-%m")


def tage_im_monat():
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def format_punkte(zahl):
    return f"{zahl:,}".replace(",", ".")



def hole_spieler_anzahl(server_id):
    try:
        r = requests.get(f"https://api.battlemetrics.com/servers/{server_id}", timeout=5)
        if r.status_code == 200:
            return r.json()["data"]["attributes"]["players"]
    except Exception:
        pass

    return "Fehler"


def main(page: ft.Page):
    page.title = "Ruhrpott Survivor"
    page.bgcolor = "#0d1117"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.padding.only(top=35, left=10, right=10, bottom=90)

    alle_votes = [
        ("🔥 ASA Votes", VOTE_ASA),
        ("🇩🇪 Deutsche Arkserver", VOTE_DE),
    ]

    gesamt_votes = sum(len(votes) for _, votes in alle_votes)
    max_punkte_tag = sum(punkte for _, votes in alle_votes for _, punkte, _ in votes)
    max_punkte_monat = max_punkte_tag * tage_im_monat()

    stats_text = ft.Text(
        "",
        color="#00ffcc",
        size=14,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    streak_text = ft.Text(
        "",
        color="#ffaa00",
        size=14,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    kalender_text = ft.Text(
        "",
        color="#ffffff",
        size=13,
        text_align=ft.TextAlign.CENTER,
    )

    progress_text = ft.Text(
        "",
        color="#c0c0c0",
        size=12,
        text_align=ft.TextAlign.CENTER,
    )

    status_bereich = ft.Column(spacing=4)

    def vote_key(gruppe, name):
        return f"vote_{gruppe}_{name}"

    def month_key():
        return f"month_{aktueller_monat()}"

    def load_json(key, default):
        raw = page.client_storage.get(key)
        if not raw:
            return default

        try:
            return json.loads(raw)
        except Exception:
            return default

    def save_json(key, data):
        page.client_storage.set(key, json.dumps(data))

    def load_month():
        return load_json(month_key(), {})

    def save_month(data):
        save_json(month_key(), data)

    def safe_int_storage(key, default=0):
        try:
            return int(page.client_storage.get(key) or default)
        except Exception:
            return default

    def zaehle_heute():
        count = 0
        punkte = 0

        for gruppe, votes in alle_votes:
            for name, wert, _ in votes:
                if page.client_storage.get(vote_key(gruppe, name)) == heute():
                    count += 1
                    punkte += wert

        return count, punkte

    def ist_heute_voll():
        count, _ = zaehle_heute()
        return count == gesamt_votes

    def update_month_data():
        count, punkte = zaehle_heute()
        data = load_month()

        data[heute()] = {
            "punkte": punkte,
            "votes": count,
            "voll": count == gesamt_votes,
        }

        save_month(data)
        return data

    def update_global_streak(is_full_today):
        """
        Der Streak wird global gespeichert.
        Dadurch bleibt er über Monatswechsel und Jahreswechsel erhalten.

        Logik:
        - Heute nicht vollständig: aktuellen Streak nur anzeigen.
        - Heute schon gespeichert: nichts doppelt zählen.
        - Letzter voller Tag war gestern: +1.
        - Letzter voller Tag liegt länger zurück: Neustart bei 1.
        """
        streak = safe_int_storage(STREAK_KEY, 0)
        letzter_tag = page.client_storage.get(LAST_FULL_DAY_KEY)

        if not is_full_today:
            return streak


        if letzter_tag == heute():
            return streak

        if letzter_tag == gestern():
            streak += 1
        else:
            streak = 1

        page.client_storage.set(STREAK_KEY, str(streak))
        page.client_storage.set(LAST_FULL_DAY_KEY, heute())

        return streak

    def badge_for_streak(streak):
        if streak >= 1095:
            return "🔥 Ruhrpott Gott"
        elif streak >= 730:
            return "👑 Mythos"
        elif streak >= 365:
            return "💎 Legende"
        elif streak >= 180:
            return "🏆 Gold"
        elif streak >= 90:
            return "🥈 Silber"
        elif streak >= 45:
            return "🟠 Kupfer"
        elif streak >= 30:
            return "🥉 Bronze"
        elif streak >= 7:
            return "🔥 Aktiv"
        return "🌱 Vote-Neuling"

    def naechster_badge(streak):
        ziele = [
            (7, "🔥 Aktiv"),
            (30, "🥉 Bronze"),
            (45, "🟠 Kupfer"),
            (90, "🥈 Silber"),
            (180, "🏆 Gold"),
            (365, "💎 Legende"),
            (730, "👑 Mythos"),
            (1095, "🔥 Ruhrpott Gott"),
        ]

        for ziel, name in ziele:
            if streak < ziel:
                return ziel, name

        return None, "Maximalrang erreicht"

    def progress_bar(aktuell, ziel, breite=18):
        if ziel <= 0:
            return "█" * breite

        anteil = min(max(aktuell / ziel, 0), 1)
        voll = int(anteil * breite)
        leer = breite - voll

        return "█" * voll + "░" * leer

    def baue_kalender(data):
        now = datetime.now()
        tage = calendar.monthrange(now.year, now.month)[1]
        zeilen = []

        for i in range(1, tage + 1):
            key = f"{now.year}-{now.month:02d}-{i:02d}"

            if key in data and data[key].get("voll"):
                zeilen.append("✅")
            elif key in data and data[key].get("punkte", 0) > 0:
                zeilen.append("🟡")
            else:
                zeilen.append("⬛")

        gruppen = [" ".join(zeilen[i:i + 7]) for i in range(0, len(zeilen), 7)]
        return "\n".join(gruppen)

    def update_stats():
        count, punkte_heute = zaehle_heute()
        data = update_month_data()

        punkte_monat = sum(tag.get("punkte", 0) for tag in data.values())
        volle_tage = sum(1 for tag in data.values() if tag.get("voll"))

        is_full = count == gesamt_votes
        streak = update_global_streak(is_full)
        badge = badge_for_streak(streak)

        stats_text.value = (
            f"Votes heute: {count} / {gesamt_votes}\n"
            f"Punkte heute: {format_punkte(punkte_heute)} / {format_punkte(max_punkte_tag)}\n"
            f"Monatspunkte: {format_punkte(punkte_monat)} / {format_punkte(max_punkte_monat)}\n"
            f"Vollständige Vote-Tage: {volle_tage} / {tage_im_monat()}"
        )

        streak_text.value = (
            f"🔥 Streak: {streak} Tage\n"
            f"{badge}"
        )

        if is_full:
            streak_text.value += "\n⭐ Heute vollständig gevotet!"

        ziel, ziel_name = naechster_badge(streak)

        if ziel:
            balken = progress_bar(streak, ziel)
            progress_text.value = (
                f"Nächster Rang: {ziel_name} bei {ziel} Tagen\n"
                f"{balken} {streak}/{ziel}"
            )
        else:
            progress_text.value = "Maximalrang erreicht"

        kalender_text.value = baue_kalender(data)

    def vote_click(vote_url, key, status):
        page.client_storage.set(key, heute())
        status.value = "✓"
        update_stats()
        page.update()
        page.launch_url(vote_url)

    def build_vote_block(title, votes):
        rows = []

        for name, punkte, url in votes:
            key = vote_key(title, name)
            erledigt = page.client_storage.get(key) == heute()

            status = ft.Text(
                "✓" if erledigt else "",
                width=28,
                color="#00ff66",
                weight=ft.FontWeight.BOLD,
                size=22,
                text_align=ft.TextAlign.CENTER,
            )

            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(name, width=115, color="#ffffff", size=13),
                        ft.Text(f"{punkte} 🪙", width=65, color="#c0c0c0", size=13, text_align=ft.TextAlign.CENTER),
                        ft.TextButton(
                            text="VOTE",
                            width=70,
                            on_click=lambda e, u=url, k=key, s=status: vote_click(u, k, s),
                        ),
                        status,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
            )

        return ft.Container(
            padding=10,
            bgcolor="#111827",
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text(title, color="#00ffcc", weight=ft.FontWeight.BOLD),
                    *rows,
                ],
                spacing=3,
            ),
        )

    def aktualisiere_status(e):
        scan_button.disabled = True
        scan_button.text = "Lade..."
        page.update()

        status_bereich.controls.clear()

        for name, info in SERVER_LISTE.items():
            anzahl = hole_spieler_anzahl(info["id"])

            if isinstance(anzahl, int):
                farbe = "#00ff66" if anzahl > 0 else "#888888"
            else:
                farbe = "#ff5555"

            map_button = (
                ft.TextButton(
                    text="MAP",
                    width=80,
                    on_click=lambda e, u=info["url"]: page.launch_url(u),
                )
                if info["url"]
                else ft.Text("-", width=80, color="#555555", text_align=ft.TextAlign.CENTER)
            )

            status_bereich.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(name, width=135, color="#ffaa00", weight=ft.FontWeight.BOLD, size=12),
                        ft.Text(f"{anzahl} Spieler", width=90, color=farbe, size=12, text_align=ft.TextAlign.CENTER),
                        map_button,
                    ]
                )
            )

        scan_button.disabled = False
        scan_button.text = "CLUSTER AKTUALISIEREN"
        page.update()

    scan_button = ft.FilledButton(
        text="CLUSTER AKTUALISIEREN",
        bgcolor="#00ffcc",
        color="#0d1117",
        height=48,
        on_click=aktualisiere_status,
    )

    update_stats()

    page.add(
        ft.Text(
            "🦖 RUHRPOTT SURVIVOR 🦖",
            size=21,
            weight=ft.FontWeight.BOLD,
            color="#00ffcc",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            "Vote Radar",
            size=12,
            color="#888888",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Container(height=8),
        ft.Container(
            padding=10,
            bgcolor="#111827",
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    stats_text,
                    ft.Divider(color="#22333b"),
                    streak_text,
                    progress_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
        ),
        ft.Container(height=10),
        ft.Container(
            padding=10,
            bgcolor="#111827",
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Text("📅 Monatskalender", color="#00ffcc", weight=ft.FontWeight.BOLD),
                    kalender_text,
                    ft.Text("✅ voll · 🟡 teilweise · ⬛ offen", color="#888888", size=11),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
        ),
        ft.Container(height=12),
        scan_button,
        ft.Container(height=10),
        status_bereich,
        ft.Container(height=15),
        build_vote_block("🔥 ASA Votes", VOTE_ASA),
        ft.Container(height=10),
        build_vote_block("🇩🇪 Deutsche Arkserver", VOTE_DE),
    )


if __name__ == "__main__":
    ft.app(target=main)

