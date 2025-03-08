# Planung & Optimierung

## Schritt-für-Schritt-Planungsablauf

### Primärbedarf ermitteln

- Einlesen der Verkaufsaufträge und Prognosen.
- Berechnung des Bedarfs an Endprodukten (P1, P2, P3) unter Abzug des vorhandenen Lagerbestands.

### Bestandsprüfung

- Abgleich des vorhandenen Lagerbestands (Vorperiode) mit dem Bedarf.
- Festlegung des Soll-Lagerbestands (Sicherheitsbestand).

### Berechnung des Sekundärbedarfs

- Auswertung der Stücklisten der Endprodukte.
- Ermittlung des Bedarfs an Eigenfertigungsprodukten und Zwischenprodukten.
- Berücksichtigung der Werte der einzelnen Komponenten zur späteren Kostenkalkulation.

### Berechnung des Tertiärbedarfs

- Ableitung der benötigten Kaufteile aus den Stücklisten der internen Fertigungsprodukte.
- Abgleich mit vorhandenen Beständen und Ermittlung von Bestellmengen unter Berücksichtigung von
  Lieferzeiten.

### Kapazitätsprüfung:

- Ermittlung des Gesamt-Kapazitätsbedarfs (Produktionszeit + Rüstzeiten + Rückstände).
- Vergleich mit den verfügbaren Kapazitäten der Arbeitsplätze.
- Falls Engpässe vorliegen: Priorisierung und ggf. Verteilung der Aufträge über mehrere Perioden.

### Erstellung der Produktions- und Bestellaufträge:

- Festlegung der **Produktionsaufträge** für Endprodukte sowie für Zwischen- und
  Eigenfertigungsprodukte.
- Ableiten von **Bestellaufträgen** für Kaufteile.
- Zusammenführung aller Aufträge und Festschreibung der geplanten Produktion.

### Kalkulation und Dokumentation:

- Berechnung der Herstellkosten unter Einbeziehung:
    - Materialwerte (aus Stücklisten, inkl. Zwischenprodukte)
    - Fertigungs- und Rüstzeiten (Arbeits- und Maschinenkosten)
    - Lagerhaltungskosten (auf Basis des Lagerwerts)
- Speicherung der **geplanten Produktionsaufträge**, der **Bestellaufträge** sowie der **erwarteten
  Lagerbestände**
  als Eingangsgrößen für die nächste Periode.

---

## Datenfluss im Planungsprogramm

1. **Eingabe:**
    - **Stammdaten:** Produktionsstruktur, Stücklisten (mit Mengen und Werten), Kapazitätsdaten,
      Anfangslagerbestände.
    - **Periodenspezifische Daten:** Verkaufsaufträge, Prognosen, Rückstände, Bestände, offene
      Fertigungsaufträge.

2. **Berechnungsmodul:**
    - Ermittlung von Primär-, Sekundär- und Tertiärbedarf.
    - Kapazitätsplanung (inkl. Rüstzeiten und Überstunden).
    - Kostenkalkulation (Materialwerte, Produktionszeiten, Lagerhaltung).

3. **Ausgabe:**
    - Produktionsplan: Welche Endprodukte, Zwischenprodukte und Eigenfertigungsprodukte in welcher
      Menge hergestellt
      werden.
    - Bestellplan: Welche Kaufteile in welcher Menge bestellt werden müssen.
    - Aktualisierte Lagerbestände und Kapazitätsauslastungen.
    - Kalkulierte Herstellkosten und Vergleich Soll/Ist (über Formularvorlagen).

### Diagramm

!!! note Vereinfachung
    Keine Beachtung der Optimierung über mehrere Perioden. Keine Einbeziehung der Prognosen.


```mermaid
flowchart TD
%% Stammdaten (konstant)
    subgraph "Stammdaten"
        PRODSTR["Produktionsstruktur"]
    end

%% Periodendaten (variabel)
    subgraph "Periodendaten"
        OPEN_SALES["Offene Aufträge"]
        SALES["Neue Aufträge"]
        CURINV["Lagerbestand"]
    end

%% Berechnungen
    subgraph "Berechnungen"
        PRIM["Primärbedarf"]
        SEK["Sekundärbedarf"]
    end

%% Ergebnis
    subgraph "Ergebnis"
        PRODORD["Produktionsaufträge"]
        BESTORD["Bestellaufträge"]
    end

%% Datenfluss
SALES --> PRIM
OPEN_SALES --> PRIM
CURINV --> PRIM
PRODSTR --> SEK
PRIM --> SEK
SEK --> BESTORD
SEK --> PRODORD
class PRODSTR,TEILDAT,CAPCOST,SALES,OPEN_SALES,CURINV inputData;
class PRIM,NET,SEK,TER,PRODORD,BESTORD,NEWINV calcData;
classDef inputData fill: green, stroke:white;
classDef calcData fill: blue, stroke: white;
classDef resultData fill: yellow, stroke: white;
```

## Wichtiges zur Optimierung

### Primärbedarf

Der Primärbedarf berechnet sich sehr einfach aus den Verkaufsaufträgen und den offenen Aufträgen.

#### Höhere Produktion als Bedarf
Wie optimiert man den Primärbedarf? Sollte man immer genau so viel produzieren wie beauftragt wird.
Es könnte durchaus Sinn machen mehr zu produzieren vor allem, wenn das Inventar niedrig ist und es
wenig Bestellungen gibt.
Da man so schon für die nächste Periode produziert hat. Dies führt zu komplizierten Berechnungen.

#### Niedrigere Produktion als Bedarf
Man sollte weniger produzieren als bestellt wurde, wenn bei weiterer Produktion die Kosten anfangen
höher zu sien als
der Verkaufswert.

### Sekundärbedarf

Der Sekundärbedarf wird ganz einfach berechnet. Dort gibt es nicht zu optimieren. Die Frage ist ob
es Sinn machen kann
mehr von etwas zu produzieren, was man aber garnicht direkt benötigt.
Je nach Rüstzeiten und Kosten kann es durchaus Sinn machen mehr von einem Zwischenprodukt zu
produzieren. Vorallem, wenn dies
von mehreren Endprodukten benötigt wird. Oder Rüstzeiten an Maschine hoch sind. Diese Periode eine
geringe Auslastung
ist und im Lager noch Platz ist.

### Tertiärbedarf - Kaufteile

Die Kaufteile sind ziemlich kompliziert zu optimieren. Je nachdem kann es durchaus Sinn ergeben mehr
zu kaufen als
direkt benötigt wird. Vor allem, wenn Lager Platz hat und Lieferzeiten große Abweichungen haben.
Außerdem ist es wichtig
10 % Rabatt zu bekommen durch die bestellte Menge. So, dass man prinzipiell einen Kostenvorteil hat wenn
man mehr Bestellt.

### Benötigte Workstations

Aus Sekundärbedarf berechnet sich die benötigten Arbeiten je Arbeitsstation Workstation

### Arbeitsschichten

Wie viele Schichten müssen für welche Workstations angeordnet werden?
Kann das klar berechnet werden? Also für festgelegte Produktionen gibt es eine direkt zu
berechnende einfache optimale?
Könnte es Sinn machen etwas zu produzieren aber dann nicht die Kapazität zu haben?
Eher nicht.

### Maschinenkosten & Arbeitskosten

Aus den Arbeitsschichten und der Produktion berechnen sich die Arbeitskosten und die
Maschinenkosten. Diese sind sehr wichtig. Müssen auf jedenfall optimiert werden.
Also, wenn Kosten zu hoch muss weniger produziert werden.
Nötige Kapazitäten sollten natürlich optimal genutzt werden. Weitere Schichten kosten deutlich mehr
als vorherige.

### Geplantes Inventar

Aus den KKaufteilen sowie dem geplanten Verbrauch ergibt sich natürlich ein Plan dafür wie viel das
Lager kosten wird

### Gesamt Kosten

Aus den Maschinenkosten, Arbeitskosten und Lagerkosten ergibt sich die Gesamtkosten. Diese sollten
natürlich minimiert werden.

### Erträge

Aus den Verkaufsaufträgen und den geplanten Produktionen ergibt sich der Ertrag.

### Gewinn

Der Gewinn ergibt sich aus den Erträgen abzüglich der Gesamtkosten.

### Flowchart Planung Optimiert

```mermaid
flowchart TD

%% Stammdaten (konstant)
    subgraph "Stammdaten"
        PRODSTR["Produktionsstruktur"]
    end

%% Periodendaten (variabel)
    subgraph "Periodendaten"
        OPEN_SALES["Offene Aufträge"]
        SALES["Neue Aufträge"]
        CURINV["Lagerbestand"]
    end

%% Berechnungen
    subgraph "Berechnungen"
        PRIM["Primärbedarf"]
        SEK["Sekundärbedarf"]
        WORKSTATION_REQ["Zeit je WS"]
        WORK_TIMES["WS Schichten"]
        WORK_COST["Personal Kosten"]
        MACHINE_COST["Machinen Kosten"]
        PLANNED_INV["Geplantes Inventar"]
        EXPECTED_INV_COST["Erwartete Lagerkosten"]
        TOTAL_COST["Gesamt Kosten"]
        REVENUE["Erträge"]
        EARNINGS["Gewinn"]
        PRODORD["Produktionsaufträge"]
        BESTORD["Bestellaufträge"]
    end

%% Datenfluss
    SALES --> PRIM
    OPEN_SALES --> PRIM
    CURINV --> PRIM
    PRODSTR --> SEK
    PRIM --> SEK
    PRODORD --> WORKSTATION_REQ
    PRODORD --> PLANNED_INV
    WORKSTATION_REQ --> WORK_TIMES
    WORK_TIMES --> WORK_COST
    WORK_TIMES --> MACHINE_COST
    PRIM --> REVENUE
    WORK_COST --> TOTAL_COST
    MACHINE_COST --> TOTAL_COST
    SEK --> BESTORD
    SEK --> PRODORD
    BESTORD --> PLANNED_INV
    PLANNED_INV --> EXPECTED_INV_COST
    EXPECTED_INV_COST --> TOTAL_COST
    REVENUE --> EARNINGS
    TOTAL_COST --> EARNINGS
class PRODSTR,CAPCOST,SALES,OPEN_SALES,CURINV inputData;
class PRIM,NET,SEK,TER,PRODORD,BESTORD,NEWINV,WORK_TIMES,WORKSTATION_REQ,PLANNED_INV calcData;
class EARNINGS,REVENUE,TOTAL_COST,MACHINE_COST,EXPECTED_INV_COST.WORK_COST calcData;
class RES resultData;
classDef inputData fill:#223, stroke: white, stroke-width: 2px, color: #fff;
classDef calcData fill:#333, stroke: white, stroke-width: 2px, color: #fff;
classDef resultData fill:#232, stroke: white, stroke-width: 2px, color: #fff;
```

!!! question Optimierung
    Ist das ganze nicht ein lineares Optimierungsproblem?
    mit Variablen und Bedingungen?
    Sowie einer Zielfunktion!
    
    Optimierungsproblem mit Variablen und Bedingungen, sollte man mit Google OR Tools lösen können.
