import flet as ft
import requests
from datetime import datetime


SERVER_LISTE = {
    "THE ISLAND": {"id": "36953667", "url": "https://asamap.axi92.at/map/c6c6f105-06f1-41de-9f5e-9f38afe18502"},
    "EXTINCTION": {"id": "36959230", "url": "https://asamap.axi92.at/map/558c1013-0989-40b7-86b4-bbd2b6c529a8"},
    "SE": {"id": "36959212", "url": "https://asamap.axi92.at/map/a2865e94-22f4-47a7-bc62-daefe2b5c2e8"},
    "TESTBUDE": {"id": "39135057", "url": None},
    "VALGUERO": {"id": "38696507", "url": "https://asamap.axi92.at/map/fde35796-7865-48f2-a680-8680525a1962"},
    "SVARTALFHEIM": {"id": "36953585", "url": "https://asamap.axi92.at/map/2d6e46e1-267c-4229-89c1-8be4fdbeb9f6"},
    "CENTER": {"id": "36959198", "url": "https://asamap.axi92.at/map/cd7a8226-4396-48ad-93f6-6af18d9eb627"},
    "ABERRATION": {"id": "36959246", "url": "https://asamap.axi92.at/map/14dc4038-1df6-4055-a65e-66ced672b366"},
    "ASTRAEOS": {"id": "38696478", "url": "https://asamap.axi92.at/map/543e8878-779c-4694-84b1-cc5fbfcdec21"},
    "RAGNARÖK": {"id": "38696502", "url": "https://asamap.axi92.at/map/9c404416-0263-42c7-a067-a14723f502bc"},
    "LOST CITY": {"id": "36953589", "url": "https://asamap.axi92.at/map/80196515-b882-4819-926c-dc381adcb0dc"},
    "LOST COLONY": {"id": "36959287", "url": "https://asamap.axi92.at/map/f7df5ef9-212b-453d-bc46-e8357a566a36"}
}


VOTE_ASA = [
    ("Island", "https://asa-server.de/server/ruhrpott-survivor-pve-island-crossark-clustert5h5x25-49"),
    ("SE", "https://asa-server.de/server/ruhrpott-survivor-pve-se-crossark-clustert5h5x25-50"),
    ("Center", "https://asa-server.de/server/ruhrpott-survivor-pve-center-crossark-clustert5h5x25-51"),
    ("Ragnarok", "https://asa-server.de/server/ruhrpott-survivor-pve-ragnarok-crossark-clustert5h5x25-52"),
    ("Aberration", "https://asa-server.de/server/ruhrpott-survivor-pve-aberration-crossark-clustert5h5x25-57"),
    ("Extinction", "https://asa-server.de/server/ruhrpott-survivor-pve-extinction-crossark-clustert5h5x25-112"),
    ("Astraeos", "https://asa-server.de/server/ruhrpott-survivor-pve-astraeos-crossark-clustert5h5x25-113"),
    ("Svartalfheim", "https://asa-server.de/server/ruhrpott-survivor-pve-svartalfheim-crossark-clustert5h5x25-132"),
    ("Valguero", "https://asa-server.de/server/ruhrpott-survivor-pve-valguero-crossark-clustert5h5x25-170"),
    ("Lost Colony", "https://asa-server.de/server/ruhrpott-survivor-pve-lostcolony-crossark-clustert5h5x25-193"),
    ("Lost City", "https://asa-server.de/server/ruhrpott-survivor-pve-lostcitycrossark-clustert5h5x25-194"),
]

VOTE_DE = [
    ("Island (DE)", "https://deutsche-arkserver.de/server/ruhrpott-survivor-pve-island-crossark-cluster-t5h5x2-5.46322/"),
    ("Ragnarok (DE)", "https://deutsche-arkserver.de/server/ruhrpott-survivor-pve-ragnarok-crossark-cluster-t5h5x2-5.46373/")
]


def heute():
    return datetime.now().strftime("%Y-%m-%d")


def hole_spieler_anzahl(server_id):
    try:
        r = requests.get(f"https://api.battlemetrics.com/servers/{server_id}", timeout=5)
        if r.status_code == 200:
            return r.json()["data"]["attributes"]["players"]
    except:
        pass
    return "Fehler"


def build_vote_block(page, title, links):
    rows = []

    for name, url in links:
        storage_key = f"vote_{title}_{name}"
        gespeichert = page.client_storage.get(storage_key)

        status_text = ft.Text(
            "✓" if gespeichert == heute() else "",
            width=45,
            color="#00ff66",
            weight=ft.FontWeight.BOLD,
            size=24,
            text_align=ft.TextAlign.CENTER
        )

        def vote_click(e, vote_url=url, key=storage_key, status=status_text):
            page.client_storage.set(key, heute())
            status.value = "✓"
            page.update()
            page.launch_url(vote_url)

        rows.append(
            ft.Row(
                controls=[
                    ft.Text(name, width=150, color="#ffffff"),
                    ft.TextButton(
                        text="VOTE",
                        width=80,
                        on_click=vote_click
                    ),
                    status_text
                ],
                alignment=ft.MainAxisAlignment.START
            )
        )

    return ft.Container(
        padding=10,
        bgcolor="#111827",
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text(title, color="#00ffcc", weight=ft.FontWeight.BOLD),
                *rows
            ]
        )
    )


def main(page: ft.Page):
    page.title = "Ruhrpott Survivor PVE Radar"
    page.bgcolor = "#0d1117"
    page.scroll = ft.ScrollMode.AUTO

    page.padding = ft.padding.only(
        top=45,
        bottom=90,
        left=10,
        right=10
    )

    titel = ft.Row(
        controls=[
            ft.Text(
                "🦖 RUHRPOTT SURVIVOR 🦖",
                size=22,
                weight=ft.FontWeight.BOLD,
                color="#00ffcc",
                no_wrap=True,
                text_align=ft.TextAlign.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    status_bereich = ft.Column(spacing=5)

    def aktualisiere_status(e):
        scan_button.disabled = True
        scan_button.text = "Aktualisiere..."
        page.update()

        status_bereich.controls.clear()

        for name, info in SERVER_LISTE.items():
            anzahl = hole_spieler_anzahl(info["id"])

            if isinstance(anzahl, int):
                farbe = "#00ff66" if anzahl > 0 else "#888888"
            else:
                farbe = "#ff5555"

            map_btn = (
                ft.TextButton(
                    text="MAP",
                    width=100,
                    on_click=lambda e, u=info["url"]: page.launch_url(u)
                )
                if info["url"]
                else ft.Text("-", width=100, color="#555555", text_align=ft.TextAlign.CENTER)
            )

            status_bereich.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"■ {name}:", width=150, color="#ffaa00", weight=ft.FontWeight.BOLD),
                        ft.Text(f"{anzahl} Spieler", width=100, color=farbe, text_align=ft.TextAlign.CENTER),
                        map_btn
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )

            status_bereich.controls.append(ft.Divider(color="#22333b"))

        scan_button.disabled = False
        scan_button.text = "CLUSTER AKTUALISIEREN"
        page.update()

    scan_button = ft.FilledButton(
        text="CLUSTER AKTUALISIEREN",
        bgcolor="#00ffcc",
        color="#0d1117",
        width=450,
        height=55,
        on_click=aktualisiere_status
    )

    vote_asa = build_vote_block(page, "🔥 ASA SERVER VOTES", VOTE_ASA)
    vote_de = build_vote_block(page, "🇩🇪 DEUTSCHE ARKSERVER VOTES", VOTE_DE)

    page.add(
        titel,
        ft.Container(height=10),
        scan_button,
        ft.Container(height=15),
        status_bereich,
        ft.Container(height=20),
        vote_asa,
        ft.Container(height=10),
        vote_de
    )


if __name__ == "__main__":
    ft.app(target=main)
