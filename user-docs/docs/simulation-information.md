# Allgemeine Informationen

## Wichtige Informationen:

1 Periode = 5 Tage = 40 Stunden = 2400 Minuten

Statischer Wert des Inventars, daraus ergeben sich die Lagerkosten, welche Sprung fix sind.

Die benötigten Ressourcen, Kaufteile und Eigen Erzeugnisse.
Daraus ergibt sich ein Produktionsgraph, ein Gozinto Graph

## Wichtige Eingabe Daten je Periode:

Aktuelles Inventar und Aufträge, Vorhersage der Aufträge (bzw. ich weiß die genaue Zahl der
zukünftigen Nachfrage)

## Zwischen Berechnungen:

Aus Inventar und aufträge ergebende benötigte Produkte für nächste Periode ? Risiko

Was muss ich eingeben? Bzw. welche Dinge muss ich planen?

## Ausgangsdaten

### Produktionsstruktur

- **Endprodukte (Erzeugnisse):**
    - **P1:** Kinderfahrrad
    - **P2:** Damenfahrrad
    - **P3:** Herrenfahrrad
- **Zwischenprodukte / Baugruppen:**
    - Teilfertigungen, die als Zwischenstufen in der Produktion (z. B. Rahmen- und Radsätze)
      hergestellt werden.
    - Werden sowohl als eigenfertigte Produkte (E) als auch als Baugruppen in den Stücklisten
      aufgeführt.
- **Eigenfertigungsprodukte (E):**
    - 27 intern hergestellte Teile, die direkt in die Fertigung der Endprodukte eingehen.
- **Kaufteile (K):**
    - 29 von externen Lieferanten bezogene Teile.

- **Stücklisten der Endprodukte:**  
  Jede Endproduktdefinition (P1, P2, P3) enthält:
    - **Zwischenprodukte** (z. B. Baugruppen) und direkt verwendete Eigenfertigungsprodukte (E).
    - **Zuordnung der benötigten Kaufteile (K)** über die Stücklisten der Eigenfertigungsprodukte.
- **Werte der Teile:**
    - Jeder Artikel (Endprodukt, Zwischenprodukt, Eigenfertigungsprodukt, Kaufteil) hat einen
      zugeordneten **Wert** (Preis pro Stück).
    - Diese Werte fließen in die Herstellkosten- und Kostenkalkulation ein.

### Produktionskapazitäten und Kostenparameter

- **Arbeitsplätze:**
    - Teilefertigung: 5 Arbeitsplätze
    - Vormontage: 8 Arbeitsplätze
    - Endmontage: 1 Arbeitsplatz
- **Verfügbare Zeit pro Periode:**  
  (z. B. 2400 Minuten pro Periode, je nachdem wie viele Schichten und Überstunden man anordnet.

> Überstunden sind viel teurer als Schichten. Jede weiter Schicht ist teurer als bisher!
> Außerdem sind die Variablen machinenkosten fast immer billiger als Lohnkosten und die
> Fixenmaschinenkosten noch
> billiger.
> Kaufteile welche eine längere Bestellzeit haben sollte ich natürlich deutlich mehr einlagern.
> (Obwohl ich ja weiß wie viel in den nächsten Perioden benötigt wird; eigentlich sollte ich diese
> Info nicht haben; Bug
> im Programm)
> Lagerkosten sind sprungfix, also muss ich aufpassen nicht über disen Betrag zu kommen.

- **Rüstzeiten:**
    - Für jeden Arbeitsplatz sind feste Rüstzeiten vor Produktionswechseln definiert.
- **Kostenparameter:**
    - Lohn-/Maschinenkosten (variable und fixe Anteile)
    - Lagerhaltungskostensatz (z. B. 0,6 % pro Woche)
- **Anfangsbestände:**
    - Lagerbestände für Kaufteile, Eigenfertigungsprodukte (inkl. Zwischenprodukte) und Endprodukte
      sind vorgegeben.

## Periodenspezifische Daten

### Nachfrage / Primärbedarf

- **Verbindliche Verkaufsaufträge und Prognosen:**
    - Beispielwerte (Periode 1):
        - P1: 150 Stück
        - P2: 100 Stück
        - P3: 50 Stück
- **Abgleich mit Sicherheitsbeständen:**
    - Geplanter Lagerbestand am Periodenende (Sicherheitsbestand).

### Lagerbestand und Bestandsveränderungen

- **Lagerbestand Vorperiode:**
    - Aktuelle Bestände an Endprodukten, Zwischenprodukten und Kaufteilen.
- **Berechnung:**
  ```plaintext
  Neuer Lagerbestand = Alter Lagerbestand + Produktion – Verkäufe
  ```

- **Auswirkung:**
    - Bestimmt, ob zusätzliche Produktionsaufträge notwendig sind.

### Sekundärbedarf

- **Ermittlung über Stücklisten:**
    - Abgeleitet aus der Endproduktnachfrage wird der Bedarf an internen Fertigungsprodukten (E) und
    - **Zwischenprodukten/Baugruppen** berechnet.
- **Wertinformationen:**
    - Die Stücklisten enthalten auch die Werte der einzelnen Komponenten, die in die
      Herstellkostenkalkulation
      einfließen.

### Tertiärbedarf – Kaufteile

- **Ableitung aus den Stücklisten der Eigenfertigungsprodukte:**
    - Ermittelt, welche und in welcher Menge Kaufteile (K) benötigt werden.
- **Besonderheiten:**
    - Lieferzeiten und Lieferabweichungen müssen berücksichtigt werden.
    - Lagerbestand der Kaufteile ist abzufragen, um Überbestellungen zu vermeiden.

### Kapazitätsprüfung

- **Berechnung des Gesamt-Kapazitätsbedarfs:**
    - Zusammensetzung aus:
        - Produktionszeit (Fertigungszeit pro Stück)
        - Rüstzeiten (neu und aus Vorperioden)
        - Rückstände (Aufträge in Bearbeitung oder Warteschlange)
- **Verfügbare Kapazitäten:**
    - Stunden pro Arbeitsplatz und Schicht, Überstundenoptionen.
- **Ziel:**
    - Sicherstellen, dass die geplanten Produktionsaufträge innerhalb der verfügbaren Kapazitäten
      realisierbar sind.
