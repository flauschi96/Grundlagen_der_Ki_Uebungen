# ==============================================================================
# GAMES.02: MINIMAX UND ALPHA-BETA-PRUNING FÜR TIC TAC TOE
# ==============================================================================

# Definition der Spieler und des leeren Feldes
MAX = 1  # 'X' (Computer)
MIN = -1  # 'O' (Mensch)
LEER = 0

# Globale Zähler für den Vergleich (werden bei jedem rekursiven Aufruf inkrementiert)
KNOTEN_GEZAEHLT_MINIMAX = 0
KNOTEN_GEZAEHLT_ALPHABETA = 0


# ------------------------------------------------------------------------------
# ZUSTANDS- UND BEWERTUNGSFUNKTIONEN
# ------------------------------------------------------------------------------

def bewerte(brett):
    """Bewertet den Endzustand: +10 für Sieg von X, -10 für Sieg von O, 0 für Unentschieden."""

    # 8 mögliche Gewinnlinien: 3 Zeilen, 3 Spalten, 2 Diagonalen
    linien = (
        # Zeilen
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
        # Spalten
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
        # Diagonalen
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
    )

    for lin in linien:
        # Summe der Werte in der Linie (X=1, O=-1)
        summe = sum(brett[r][c] for r, c in lin)

        if summe == 3:  # 3 * MAX (X gewinnt)
            return 10
        if summe == -3:  # 3 * MIN (O gewinnt)
            return -10

    return 0  # Kein Sieg


def ist_ende(brett):
    """Prüft, ob das Spiel beendet ist (Sieg, Niederlage oder volles Brett)."""
    if bewerte(brett) != 0:
        return True  # Sieg/Niederlage

    # Prüfen, ob noch leere Felder vorhanden sind
    for reihe in brett:
        if LEER in reihe:
            return False  # Noch Züge möglich

    return True  # Unentschieden (volles Brett)


def get_freie_felder(brett):
    """Gibt eine Liste der Koordinaten aller leeren Felder zurück."""
    return [(r, c) for r in range(3) for c in range(3) if brett[r][c] == LEER]


# ------------------------------------------------------------------------------
# (2P) MINIMAX-ALGORITHMUS (REIN)
# ------------------------------------------------------------------------------

def minimax(brett, spieler):
    """
    Rekursive Minimax-Funktion ohne Alpha-Beta-Pruning.
    Gibt den optimalen Wert für den aktuellen Spieler zurück.
    """
    global KNOTEN_GEZAEHLT_MINIMAX
    KNOTEN_GEZAEHLT_MINIMAX += 1

    if ist_ende(brett):
        return bewerte(brett)

    # MAX-Spieler
    if spieler == MAX:
        max_wert = -float('inf')
        for r, c in get_freie_felder(brett):
            brett[r][c] = MAX  # Zug ausführen
            wert = minimax(brett, MIN)  # Nächste Ebene (MIN)
            brett[r][c] = LEER  # Zug rückgängig machen (Backtracking)
            max_wert = max(max_wert, wert)
        return max_wert

    # MIN-Spieler
    else:
        min_wert = float('inf')
        for r, c in get_freie_felder(brett):
            brett[r][c] = MIN  # Zug ausführen
            wert = minimax(brett, MAX)  # Nächste Ebene (MAX)
            brett[r][c] = LEER  # Zug rückgängig machen
            min_wert = min(min_wert, wert)
        return min_wert


# ------------------------------------------------------------------------------
# (1P) MINIMAX MIT ALPHA-BETA-PRUNING
# ------------------------------------------------------------------------------

def minimax_alphabeta(brett, spieler, alpha, beta):
    """
    Rekursive Minimax-Funktion mit Alpha-Beta-Pruning.
    Gibt den optimalen Wert für den aktuellen Spieler zurück.
    """
    global KNOTEN_GEZAEHLT_ALPHABETA
    KNOTEN_GEZAEHLT_ALPHABETA += 1

    # Basisfall: Spielende
    if ist_ende(brett):
        return bewerte(brett)

    # MAX-Spieler
    if spieler == MAX:
        max_wert = -float('inf')
        for r, c in get_freie_felder(brett):
            brett[r][c] = MAX
            wert = minimax_alphabeta(brett, MIN, alpha, beta)
            brett[r][c] = LEER

            max_wert = max(max_wert, wert)
            alpha = max(alpha, max_wert)  # Update Alpha (beste Garantie für MAX)

            if alpha >= beta:  # Pruning-Check MAX-Knoten
                break  # Schneidet den Rest des Astes ab
        return max_wert

    # MIN-Spieler
    else:
        min_wert = float('inf')
        for r, c in get_freie_felder(brett):
            brett[r][c] = MIN
            wert = minimax_alphabeta(brett, MAX, alpha, beta)
            brett[r][c] = LEER

            min_wert = min(min_wert, wert)
            beta = min(beta, min_wert)  # Update Beta (beste Garantie für MIN)

            if alpha >= beta:  # Pruning-Check MIN-Knoten (Beta <= Alpha)
                break  # Schneidet den Rest des Astes ab
        return min_wert


# ------------------------------------------------------------------------------
# (1P) VERGLEICH DER BERECHNETEN KNOTEN (Szenario: Leeres Brett)
# ------------------------------------------------------------------------------

def vergleiche_algorithmen():
    """Führt beide Algorithmen auf einem leeren Brett aus und vergleicht die Knotenanzahl."""
    global KNOTEN_GEZAEHLT_MINIMAX
    global KNOTEN_GEZAEHLT_ALPHABETA

    # Leeres 3x3 Brett (Tiefenkopie für beide Tests)
    start_brett_mm = [[LEER] * 3 for _ in range(3)]
    start_brett_ab = [[LEER] * 3 for _ in range(3)]

    # ------------------- 1. Minimax ohne Pruning --------------------
    KNOTEN_GEZAEHLT_MINIMAX = 0

    # Die oberste Ebene (Entscheidung des ersten Zuges) muss separat betrachtet werden
    bester_wert_minimax = -float('inf')

    # Zähler für die 9 Startzüge
    start_moves_count = len(get_freie_felder(start_brett_mm))

    for r, c in get_freie_felder(start_brett_mm):
        start_brett_mm[r][c] = MAX
        # Rufe Minimax für den MIN-Spieler (Gegner) auf der nächsten Ebene auf
        wert = minimax(start_brett_mm, MIN)
        start_brett_mm[r][c] = LEER

        bester_wert_minimax = max(bester_wert_minimax, wert)

    anzahl_minimax = KNOTEN_GEZAEHLT_MINIMAX + start_moves_count

    # ------------------- 2. Minimax mit Alpha-Beta-Pruning --------------------
    KNOTEN_GEZAEHLT_ALPHABETA = 0

    bester_wert_ab = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    # Zähler für die 9 Startzüge
    start_moves_count_ab = len(get_freie_felder(start_brett_ab))

    for r, c in get_freie_felder(start_brett_ab):
        start_brett_ab[r][c] = MAX
        # Rufe Alpha-Beta für den MIN-Spieler (Gegner) auf
        wert = minimax_alphabeta(start_brett_ab, MIN, alpha, beta)
        start_brett_ab[r][c] = LEER

        bester_wert_ab = max(bester_wert_ab, wert)

        # Aktualisiere Alpha für die nächste Iteration der obersten Ebene (MAX)
        alpha = max(alpha, bester_wert_ab)

    anzahl_alphabeta = KNOTEN_GEZAEHLT_ALPHABETA + start_moves_count_ab

    # ------------------- ERGEBNISAUSGABE --------------------

    # Der Wert 10 bedeutet, dass der MAX-Spieler (X) beim optimalen Spiel gewinnt.
    # Bei Tic-Tac-Toe auf leerem Brett kann X (der Startspieler) immer gewinnen.

    print("=========================================================")
    print("🚀 GAMES.02: Vergleich Minimax vs. Alpha-Beta (Leeres Brett)")
    print("=========================================================")
    print(f"Optimaler Minimax-Wert (MAX): {bester_wert_minimax}")
    print(f"Optimaler Alpha-Beta-Wert (MAX): {bester_wert_ab}")
    print("-" * 50)

    print(f"1. Minimax (Rein) untersuchte Knoten: {anzahl_minimax:,}")
    print(f"2. Alpha-Beta-Pruning untersuchte Knoten: {anzahl_alphabeta:,}")

    ersparnis = anzahl_minimax - anzahl_alphabeta
    prozent_ersparnis = (ersparnis / anzahl_minimax) * 100

    print(f"\n Ersparnis durch Pruning: {ersparnis:,} Knoten")
    print(f"   Dies entspricht einer Reduktion von: {prozent_ersparnis:.2f} %")
    print("=========================================================")


# Starte den Vergleich
if __name__ == "__main__":
    vergleiche_algorithmen()
