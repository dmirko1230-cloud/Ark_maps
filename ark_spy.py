import flet as ft
import requests

# Finale Server-Liste
SERVER_LISTE = {
    "THE ISLAND":    {"id": "36953667", "url": "https://asamap.axi92.at/map/c6c6f105-06f1-41de-9f5e-9f38afe18502"},
    "EXTINCTION":    {"id": "36959230", "url": "https://asamap.axi92.at/map/558c1013-0989-40b7-86b4-bbd2b6c529a8"},
    "SE":            {"id": "36959212", "url": "https://asamap.axi92.at/map/a2865e94-22f4-47a7-bc62-daefe2b5c2e8"},
    "TESTBUDE":      {"id": "39135057", "url": None},
    "VALGUERO":      {"id": "38696507", "url": "https://asamap.axi92.at/map/fde35796-7865-48f2-a680-8680525a1962"},
    "SVARTALFHEIM":  {"id": "36953585", "url": "https://asamap.axi92.at/map/2d6e46e1-267c-4229-89c1-8be4fdbeb9f6"},
    "CENTER":        {"id": "36959198", "url": "https://asamap.axi92.at/map/cd7a8226-4396-48ad-93f6-6af18d9eb627"},
    "ABERRATION":    {"id": "36959246", "url": "https://asamap.axi92.at/map/14dc4038-1df6-4055-a65e-66ced672b366"},
    "ASTRAEOS":      {"id": "38696478", "url": "https://asamap.axi92.at/map/543e8878-779c-4694-84b1-cc5fbfcdec21"},
    "RAGNARÖK":      {"id": "38696502", "url": "https://asamap.axi92.at/map/9c404416-0263-42c7-a067-a14723f502bc"},
    "LOST CITY":     {"id": "36953589", "url": "https://asamap.axi92.at/map/80196515-b882-4819-926c-dc381adcb0dc"},
    "LOST COLONY":   {"id": "36959287", "url": "https://asamap.axi92.at/map/f7df5ef9-212b-453d-bc46-e8357a566a36"}
}


def hole_spieler_anzahl(server_id):
    url = f"https://api.battlemetrics.com/servers/{server_id}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            daten = response.json()
            return daten["data"]["attributes"]["players"]

        return "N/A"

    except Exception as e:
        print(f"Fehler bei Server {server_id}: {e}")
        return "Fehler"


def main(page: ft.Page):
    page.title = "Ruhrpott Survivor - Radar"
    page.window_width = 500
    page.window_height = 850
    page.bgcolor = "#0d1117"
    page.scroll = ft.ScrollMode.AUTO

    titel = ft.Text(
        "🦖 CLUSTER LIVE-RADAR 🦖",
        size=24,
        weight="bold",
        color="#00ffcc",
        text_align=ft.TextAlign.CENTER
    )

    status_bereich = ft.Column(spacing=5)

    def aktualisiere_status(e):
        scan_button.disabled = True
        scan_button.text = "Aktualisiere..."
        page.update()

        status_bereich.controls.clear()

        for name, info in SERVER_LISTE.items():

            anzahl = hole_spieler_anzahl(info["id"])

            # Sichere Farbwahl
            if isinstance(anzahl, int):
                spieler_farbe = "#00ff66" if anzahl > 0 else "#888888"
            else:
                spieler_farbe = "#ff5555"

            # MAP-Link
            if info["url"]:
                map_klick_bereich = ft.TextButton(
                    text="MAP",
                    on_click=lambda e, u=info["url"]: page.launch_url(u)
                )
            else:
                map_klick_bereich = ft.Text(
                    "-",
                    color="#555555",
                    width=50
                )

            status_bereich.controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"■ {name}:",
                            width=160,
                            weight="bold",
                            color="#ffaa00"
                        ),
                        ft.Text(
                            f"{anzahl} Spieler",
                            width=100,
                            color=spieler_farbe
                        ),
                        map_klick_bereich
                    ]
                )
            )

            status_bereich.controls.append(
                ft.Divider(color="#22333b")
            )

        scan_button.disabled = False
        scan_button.text = "CLUSTER AKTUALISIEREN"
        page.update()

    scan_button = ft.FilledButton(
        text="CLUSTER AKTUALISIEREN",
        bgcolor="#00ffcc",
        width=450,
        height=60,
        on_click=aktualisiere_status
    )

    # Test-Button für Android
    test_button = ft.TextButton(
        text="TEST LINK",
        on_click=lambda e: page.launch_url("https://www.google.de")
    )

    page.add(
        titel,
        ft.Container(height=10),
        test_button,
        ft.Container(height=10),
        scan_button,
        ft.Container(height=20),
        status_bereich
    )


ft.run(main)
