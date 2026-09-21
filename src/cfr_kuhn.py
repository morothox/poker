class Node:
    def __init__(self, my_card, history):
        self.my_card = my_card
        self.history = history
        self.regrets = [0.0, 0.0]
        self.strategy = [0.0, 0.0]
        self.avg_strategy = [0.0, 0.0]

    def get_strategy(self, weight):
        p0 = max(0.0, self.regrets[0])
        p1 = max(0.0, self.regrets[1])
        total = p0 + p1
        if total > 0:
            self.avg_strategy[0] += weight * p0 / total
            self.avg_strategy[1] += weight * p1 / total
            self.strategy = [p0 / total, p1 / total]
            return self.strategy

        else:
            self.strategy = [0.5, 0.5]
            self.avg_strategy[0] += weight * 0.5
            self.avg_strategy[1] += weight * 0.5
            return self.strategy


# ## 1. Spezifikation: cfr(cards, history, p0, p1)
#
#   Deine Funktion durchläuft den Spielbaum von Kuhn Poker rekursiv, berechnet die Erwartungswerte (EV), aktualisiert das Bedauern (Regret) an jedem Entscheidungsknoten und gibt den
#   Gesamterwartungswert für den aktiven Spieler zurück.
#
#   ### Parameter
#
#   • cards: Eine Liste mit den beiden gezogenen Karten, z. B. ['J', 'Q'] (Index 0 = Karte von Spieler 0, Index 1 = Karte von Spieler 1).
#   • history: Ein String des bisherigen Spielablaufs ('p' = Pass/Check/Fold, 'b' = Bet/Call). Beispiele: "", "p", "pb", "pbp".
#   • p0: Die Erreichungswahrscheinlichkeit (Reach Probability) von Spieler 0 (0.0 ≤ p₀ ≤ 1.0).
#   • p1: Die Erreichungswahrscheinlichkeit (Reach Probability) von Spieler 1 (0.0 ≤ p₁ ≤ 1.0).
#   ──────
#   ## 2. Anforderungen & Verhalten
#
#   Deine Implementierung muss vier Phasen abbilden:
#
#   ### A. Wer ist am Zug?
#
#   Bestimme anhand der Länge von history, ob Spieler 0 oder Spieler 1 an der Reihe ist.
#
#   ### B. Spielende & Auszahlungen (Basisfälle / Terminal States)
#
#   Prüfe, ob das Spiel beendet ist, und gib den Reingewinn aus Sicht des aktiven Spielers zurück:
#
#   • Folds: Ein Spieler hat gebettet und der andere gefoldet. Derjenige, der gefoldet hat, verliert seinen Einsatz (-1), der Gewinner erhält +1.
#   • Showdowns: Beide haben gecheckt ("pp") oder ein Bet wurde gecallt ("bb" oder "pbb"). Vergleiche die Ränge (K > Q > J). Die höhere Karte gewinnt den Pot (+1 bei Check-Check, +2 bei Bet-
#   Call); die niedrigere Karte verliert den entsprechenden Betrag.
#
#   ### C. Rekursive Baum-Erkundung
#
#   Wenn das Spiel noch nicht zu Ende ist:
#
#   1. Ermittle oder erstelle die Node für das Information Set des aktiven Spielers (cards[player] + history).
#   2. Hole die aktuelle Aktions-Wahrscheinlichkeitsverteilung
#
#     σ = ⎡σ    ,σ   ⎤
#         ⎣ pass  bet⎦
#
#   von der Node ab.
#   3. Spiele beide möglichen Folge-Äste (history + "p" und history + "b") rekursiv durch und aktualisiere dabei die Erreichungswahrscheinlichkeiten.
#   4. Nullsummenspiel-Prinzip: Der Erwartungswert einer Aktion für den aktiven Spieler ist das Negative des Werts, den der rekursive Aufruf zurückgibt (da der Kindknoten den Gewinn aus
#   Sicht des Gegners berechnet).
#
#   ### D. Regret-Berechnung & Rückgabewert
#
#   1. Berechne den Gesamterwartungswert des aktuellen Knotens (
#
#     U     = ∑ σ(a)·U(a)
#      node   a
#
#   ).
#   2. Berechne für jede Aktion a ∈ { pass,bet } das kontrafaktische Bedauern:
#
#     Regret (a) = U(a) - U
#     			 node
#
#   3. Addiere dieses Regret auf das Langzeitgedächtnis der Node auf, gewichtet mit der Erreichungswahrscheinlichkeit des Gegners.
#   4. Gib
#
#     U
#      node
#
#   zurück.
#   ──────
#   ## 3. Verifikations-Kriterien
#
#   Wenn du deinen Solver über 100.000 Iterationen laufen lässt:
#
#   • Bluff-Frequenz: Spieler 0 mit einem Buben (J) bei Start "" sollte zu ca.
#
#      1
#     ───
#      3
#
#   (33.3%) bluffen (betten) und zu 66.7% checken.
#
#   • Value-Bet-Frequenz: Spieler 0 mit einem König (K) bei Start "" sollte fast immer betten (bzw. ≈3 × so oft wie er mit J blufft).
#   • Spielwert (Game Value): Der Gesamtspielwert für Spieler 0 konvergiert exakt gegen
#
#        1
#     - ──── ≈ -0.0555
#        18
#
#   (Kuhn Poker ist ein leichtes Positionsspiel zugunsten von Spieler 1).
#   ──────
#   Implementiere die Funktion cfr() in cfr_kuhn.py. Sag Bescheid, wenn du deinen ersten Entwurf testen möchtest!
# 1. "pp" (2 Züge): Check → Check → Showdown um 1 Ante (±1).
#  2. "bp" (2 Züge): Bet → Fold → P0 gewinnt kampflos (±1).
#  3. "bb" (2 Züge): Bet → Call → Showdown um 2 Chips (±2).
#  4. "pbp" (3 Züge): Check → Bet → Fold → P1 gewinnt kampflos (±1).
#  5. "pbb" (3 Züge): Check → Bet → Call → Showdown um 2 Chips (±2).


def cfr(history, cards, p0, p1):
    player = len(history) % 2

    opponent = 1 - player
    # terminal state
    if (len(history) == 2 and history != "pb") or len(history) >= 3:
        if history != "pp" and history.endswith("p"):
            return 1
        else:
            if history.endswith("b"):
                if cards[player] > cards[opponent]:
                    return 2
                else:
                    return -2
            if history.endswith("p"):
                if cards[player] > cards[opponent]:
                    return 1
                else:
                    return -1
        return NotImplemented
    # game is still running
    else:
        play = Node(cards[player], history)
        distribution = play.get_strategy(1)
        if player == 0:
            p0_p = p0 * distribution[0]
            p0_b = p0 * distribution[1]
            pass_func = -cfr(history + "p", cards, p0_p, p1)
            bet_func = -cfr(history + "b", cards, p0_b, p1)

        else:
            p1_p = p1 * distribution[0]
            p1_b = p1 * distribution[1]
            pass_func = -cfr(history + "p", cards, p0, p1_p)
            bet_func = -cfr(history + "b", cards, p0, p1_b)
        node_value = pass_func * distribution[0] + bet_func * distribution[1]
        if player == 0:
            p = p1
        else:
            p = p0
        play.regrets[0] += (pass_func - node_value) * p
        play.regrets[1] += (bet_func - node_value) * p

    return node_value
