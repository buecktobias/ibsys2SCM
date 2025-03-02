# Supply Chain Management
## Allgemeine Informationen
Wichtige Informationen:

1 Periode = 5 Tage = 40 Stunden = 2400 Minuten

Statischer Wert des Inventars, daraus ergeben sich die Lagerkosten, welche Sprung fix sind.

Die benötigten Ressourcen, Kaufteile und Eigen Erzeugnisse.
Daraus ergibt sich ein Produktionsgraph, ein Gozinto Graph

Wichtige Eingabe Daten je Periode:

Aktuelles Inventar und Aufträge, Vorhersage der Aufträge (bzw. ich weiß die genaue Zahl der zukünftigen Nachfrage)

Zwischen Berechnungen:

Aus Inventar und aufträge ergebende benötigte Produkte für nächste Periode ? Risiko

Was muss ich eingeben? Bzw. welche Dinge muss ich planen?

# Supply Chain Simulation – Datenbasis und Planungsablauf

Diese Zusammenfassung fasst alle relevanten Daten zusammen, die von Beginn an vorliegen, und zeigt, welche
periodenspezifischen Werte sich ändern. Dabei wird insbesondere darauf eingegangen, wie Endprodukte, Zwischenprodukte,
Eigenfertigungsprodukte und Kaufteile in den Planungsprozess einfließen – inklusive der zugehörigen Stücklisten und
Werte. Diese Informationen bilden die Grundlage für ein automatisiertes Planungsprogramm.

---

## 1. Ausgangsdaten (Konstant über alle Perioden)

### 1.1 Produktionsstruktur und Produktkategorien

- **Endprodukte (Erzeugnisse):**
    - **P1:** Kinderfahrrad
    - **P2:** Damenfahrrad
    - **P3:** Herrenfahrrad
- **Zwischenprodukte / Baugruppen:**
    - Teilfertigungen, die als Zwischenstufen in der Produktion (z. B. Rahmen- und Radsätze) hergestellt werden.
    - Werden sowohl als eigenfertigte Produkte (E) als auch als Baugruppen in den Stücklisten aufgeführt.
- **Eigenfertigungsprodukte (E):**
    - 27 intern hergestellte Teile, die direkt in die Fertigung der Endprodukte eingehen.
- **Kaufteile (K):**
    - 29 von externen Lieferanten bezogene Teile.

Welche der Eigenfertigungsprodukte werden für mehrere Endproduke benötigt?


### 1.2 Stücklisten und Werte

- **Stücklisten der Endprodukte:**  
  Jede Endproduktdefinition (P1, P2, P3) enthält:
    - **Zwischenprodukte** (z. B. Baugruppen) und direkt verwendete Eigenfertigungsprodukte (E).
    - **Zuordnung der benötigten Kaufteile (K)** über die Stücklisten der Eigenfertigungsprodukte.
- **Werte der Teile:**
    - Jeder Artikel (Endprodukt, Zwischenprodukt, Eigenfertigungsprodukt, Kaufteil) hat einen zugeordneten **Wert** (
      Preis pro Stück).
    - Diese Werte fließen in die Herstellkosten- und Kostenkalkulation ein.

### 1.3 Produktionskapazitäten und Kostenparameter

- **Arbeitsplätze:**
    - Teilefertigung: 5 Arbeitsplätze
    - Vormontage: 8 Arbeitsplätze
    - Endmontage: 1 Arbeitsplatz
- **Verfügbare Zeit pro Periode:**  
  (z. B. 2400 Minuten pro Periode, je nachdem wie viele Schichten und Überstunden man anordnet.
>Überstunden sind viel teurer als Schichten. Jede weiter Schicht ist teurer als bisher!
Außerdem sind die Variablen machinenkosten fast immer billiger als Lohnkosten und die Fixenmaschinenkosten noch billiger.
Kaufteile welche eine längere Bestellzeit haben sollte ich natürlich deutlich mehr einlagern. 
> (Obwohl ich ja weiß wie viel in den nächsten Perioden benötigt wird; eigentlich sollte ich diese Info nicht haben; Bug im Programm)
Lagerkosten sind sprungfix, also muss ich aufpassen nicht über disen Betrag zu kommen.



- **Rüstzeiten:**
    - Für jeden Arbeitsplatz sind feste Rüstzeiten vor Produktionswechseln definiert.
- **Kostenparameter:**
    - Lohn-/Maschinenkosten (variable und fixe Anteile)
    - Lagerhaltungskostensatz (z. B. 0,6 % pro Woche)
- **Anfangsbestände:**
    - Lagerbestände für Kaufteile, Eigenfertigungsprodukte (inkl. Zwischenprodukte) und Endprodukte sind vorgegeben.
---

## 2. Periodenspezifische Daten (Variabel von Periode zu Periode)

### 2.1 Nachfrage / Primärbedarf (Endprodukte)

- **Verbindliche Verkaufsaufträge und Prognosen:**
    - Beispielwerte (Periode 1):
        - P1: 150 Stück
        - P2: 100 Stück
        - P3: 50 Stück
- **Abgleich mit Sicherheitsbeständen:**
    - Geplanter Lagerbestand am Periodenende (Sicherheitsbestand).

### 2.2 Lagerbestand und Bestandsveränderungen

- **Lagerbestand Vorperiode:**
    - Aktuelle Bestände an Endprodukten, Zwischenprodukten und Kaufteilen.
- **Berechnung:**
  ```plaintext
  Neuer Lagerbestand = Alter Lagerbestand + Produktion – Verkäufe
  ```
- **Auswirkung:**
    - Bestimmt, ob zusätzliche Produktionsaufträge notwendig sind.

### 2.3 Sekundärbedarf – Eigenfertigungsprodukte und Zwischenprodukte

- **Ermittlung über Stücklisten:**
    - Abgeleitet aus der Endproduktnachfrage wird der Bedarf an internen Fertigungsprodukten (E) und *
      *Zwischenprodukten/Baugruppen** berechnet.
    - Beispiel:
        - 1× P1 benötigt 1× E26, 1× E16, 1× E50, 1× E4, …
        - Zusätzlich sind Baugruppen (Zwischenprodukte) in den Stücklisten definiert, deren Herstellung ebenfalls
          geplant werden muss.
- **Wertinformationen:**
    - Die Stücklisten enthalten auch die Werte der einzelnen Komponenten, die in die Herstellkostenkalkulation
      einfließen.

### 2.4 Tertiärbedarf – Kaufteile

- **Ableitung aus den Stücklisten der Eigenfertigungsprodukte:**
    - Ermittelt, welche und in welcher Menge Kaufteile (K) benötigt werden.
- **Besonderheiten:**
    - Lieferzeiten und Lieferabweichungen müssen berücksichtigt werden.
    - Lagerbestand der Kaufteile ist abzufragen, um Überbestellungen zu vermeiden.

### 2.5 Kapazitätsprüfung

- **Berechnung des Gesamt-Kapazitätsbedarfs:**
    - Zusammensetzung aus:
        - Produktionszeit (Fertigungszeit pro Stück)
        - Rüstzeiten (neu und aus Vorperioden)
        - Rückstände (Aufträge in Bearbeitung oder Warteschlange)
- **Verfügbare Kapazitäten:**
    - Stunden pro Arbeitsplatz und Schicht, Überstundenoptionen.
- **Ziel:**
    - Sicherstellen, dass die geplanten Produktionsaufträge innerhalb der verfügbaren Kapazitäten realisierbar sind.

---

## 3. Schritt-für-Schritt-Planungsablauf für die nächste Periode

1. **Primärbedarf ermitteln:**
    - Einlesen der Verkaufsaufträge und Prognosen.
    - Berechnung des Bedarfs an Endprodukten (P1, P2, P3) unter Abzug des vorhandenen Lagerbestands.

2. **Bestandsprüfung:**
    - Abgleich des vorhandenen Lagerbestands (Vorperiode) mit dem Bedarf.
    - Festlegung des Soll-Lagerbestands (Sicherheitsbestand).

3. **Berechnung des Sekundärbedarfs:**
    - Auswertung der Stücklisten der Endprodukte.
    - Ermittlung des Bedarfs an Eigenfertigungsprodukten und Zwischenprodukten.
    - Berücksichtigung der Werte der einzelnen Komponenten zur späteren Kostenkalkulation.

4. **Berechnung des Tertiärbedarfs:**
    - Ableitung der benötigten Kaufteile aus den Stücklisten der internen Fertigungsprodukte.
    - Abgleich mit vorhandenen Beständen und Ermittlung von Bestellmengen unter Berücksichtigung von Lieferzeiten.

5. **Kapazitätsprüfung:**
    - Ermittlung des Gesamt-Kapazitätsbedarfs (Produktionszeit + Rüstzeiten + Rückstände).
    - Vergleich mit den verfügbaren Kapazitäten der Arbeitsplätze.
    - Falls Engpässe vorliegen: Priorisierung und ggf. Verteilung der Aufträge über mehrere Perioden.

6. **Erstellung der Produktions- und Bestellaufträge:**
    - Festlegung der **Produktionsaufträge** für Endprodukte sowie für Zwischen- und Eigenfertigungsprodukte.
    - Ableiten von **Bestellaufträgen** für Kaufteile.
    - Zusammenführung aller Aufträge und Festschreibung der geplanten Produktion.

7. **Kalkulation und Dokumentation:**
    - Berechnung der Herstellkosten unter Einbeziehung:
        - Materialwerte (aus Stücklisten, inkl. Zwischenprodukte)
        - Fertigungs- und Rüstzeiten (Arbeits- und Maschinenkosten)
        - Lagerhaltungskosten (auf Basis des Lagerwerts)
    - Speicherung der **geplanten Produktionsaufträge**, der **Bestellaufträge** sowie der **erwarteten Lagerbestände**
      als Eingangsgrößen für die nächste Periode.

---

## 4. Datenfluss im Planungsprogramm

1. **Eingabe:**
    - **Stammdaten:** Produktionsstruktur, Stücklisten (mit Mengen und Werten), Kapazitätsdaten, Anfangslagerbestände.
    - **Periodenspezifische Daten:** Verkaufsaufträge, Prognosen, Rückstände, Bestände, offene Fertigungsaufträge.

2. **Berechnungsmodul:**
    - Ermittlung von Primär-, Sekundär- und Tertiärbedarf.
    - Kapazitätsplanung (inkl. Rüstzeiten und Überstunden).
    - Kostenkalkulation (Materialwerte, Produktionszeiten, Lagerhaltung).

3. **Ausgabe:**
    - Produktionsplan: Welche Endprodukte, Zwischenprodukte und Eigenfertigungsprodukte in welcher Menge hergestellt
      werden.
    - Bestellplan: Welche Kaufteile in welcher Menge bestellt werden müssen.
    - Aktualisierte Lagerbestände und Kapazitätsauslastungen.
    - Kalkulierte Herstellkosten und Vergleich Soll/Ist (über Formularvorlagen).

### Vereinfachtes Modell wenn man nur eine Periode planen würde

Und man das Lager nicht optimiert;

```mermaid
flowchart TD
%% Stammdaten (konstant)
    subgraph "Stammdaten"
        PRODSTR["Produktionsstruktur"]
        STKL["Stückliste & Werte"]
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
        PRODORD["Produktionsaufträge"]
        BESTORD["Bestellaufträge"]
        NEWINV["Neuer Lagerbestand"]
    end

%% Ergebnis
    RES["Result\n(ProdPlan, BestPlan)"]

%% Datenfluss
    SALES --> PRIM
    OPEN_SALES --> PRIM
    CURINV --> PRIM
    PRODSTR --> SEK

    PRIM --> SEK
    STKL --> SEK

    SEK --> BESTORD
    SEK --> PRODORD

    PRODORD --> NEWINV


    PRODORD --> RES
    BESTORD --> RES
    NEWINV --> RES

%% CSS Klassen
    class PRODSTR,STKL,TEILDAT,CAPCOST,SALES,OPEN_SALES,CURINV inputData;
    class PRIM,NET,SEK,TER,CAPREQ,PRODORD,BESTORD,NEWINV,COSTCALC calcData;
    class RES resultData;

    classDef inputData fill:#223,stroke:#000,stroke-width:2px,color:#fff;
    classDef calcData fill:#333,stroke:#000,stroke-width:2px,color:#fff;
    classDef resultData fill:#232,stroke:#000,stroke-width:2px,color:#fff;

````

Ist es theoretisch einfach eine eigene Simulation zu schreiben als ein Programm dass die Planung genau berechnet.
Außerdem kann ich ja sonst schwer prüfen ob meine Planung richtig ist ?

Alles nicht unbedingt ganz genau berechnen ?


Doch Abweichung macht auf jeden fall Unterschied bezüglich des Ausfall risikos 
und je nach Ausfallrisiko lohnt es sich größere Sicher Lagerung Sicherungsbestand

1. Primärbedarf berechnen
Also wie viel Endprodukte benötige ich in der nächsten Periode.
Dies berechne ich aus den vorherigen Aufträgen und den jetzigen Aufträgen. Dann habe ich noch die 10% Ausfall

https://www.scm-planspiel.de/scs_15/downloadFile?folderName=download&fileName=Foliensatz_DE.pdf

https://www.scm-planspiel.de/scs_15/downloadFile?folderName=output&fileName=63_3_3result.xml

Woher kommt der Unterschied im Stockvalue zu dem anderen Lager Gesamt Wert ? 

Also muss ich vielleicht einfach so planen dass der Lagerwert unter 230 000 bleibt!?


## Wichtiges zur Optimierung zu Beachten


- **Lagerkosten:**  
    - Lagerkosten sind sprungfix, also muss ich aufpassen nicht über disen Betrag(250 000) zu kommen.
    - Ich kann die Lagerkosten nicht genau planen, da es Lieferabweichungen gibt und die Bestellungen zu zufälligen Zeiten eintreffen ?
    - Werden die Lagerkosten über die durchschnittlische Lagermenge berechnet? Oder zahle ich die spungfixen Kosten wenn Lager kurze Zeit zu voll ist?
    - Risiko dafür berechnen, dass Lager zu voll. Risiko Lagerwert > 250 k. Risiko sollte unter 10% sein;
    - Durch Eilbestellungen höheres Risiko, aber höhere Bestellkosten.
    - Kaufteile mit größten Abweichungen führen zu höheren Risiken.
    - Von Kaufteilen mit langer Lieferzeit mehr im Lager haben. Von Kaufteilen mit hoher Abweichung mehr auf Lager haben.
    - Teile welche für mehrere Endprodukte benötigt werden, mehr auf Lager haben.
- **Kaufbestellungen**
    - Fixe Bestellkosten und 10% Rabatt ab bestimmter Menge.


