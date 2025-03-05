# Berechnungen

## Materialbedarf

- **Endprodukte:**
    - Jedes Endprodukt (P1, P2, P3) besteht aus einer Kombination von Zwischenprodukten und
      Eigenfertigungsprodukten.
    - Die Stücklisten enthalten auch die benötigten Kaufteile.

Wir können die Stücklisten in einem Directed Acyclic Graph (DAG) darstellen, um die Abhängigkeiten
der Produkte darzustellen.

````mermaid
graph TD
%% Ebene 1: Endprodukte
    subgraph Level1[Endprodukte]
        direction LR
        P1
        P2
        P3
    end

%% Ebene 2: Herstellte Baugruppen
    subgraph Level2[Eigen Fabrikate 1]
        direction LR
        E1
        E2
    end

%% Ebene 3: Unterbaugruppen
    subgraph Level3[Eigen Fabrikate 2]
        direction LR
        E11
        E12
        E13
    end

%% Ebene 4: Gekaufte Materialien
    subgraph Level4[Gekaufte Materialien]
        direction LR
        K1
        K2
        K3
    end

%% Abhängigkeiten der Endprodukte
    P1 -->|1x| E1
    P1 -->|3x| E11
    P2 -->|10x| E2
    P3 -->|2x| E2
    P3 -->|2x| K3
%% Abhängigkeiten der Baugruppen
    E1 -->|3x| E11
    E2 -->|2x| E12
    E2 -->|4x| E13
    E2 -->|1x| K3
%% Abhängigkeiten der Unterbaugruppen
    E11 -->|1x| K1
    E11 -->|2x| K2
    E12 -->|8x| K2
    E13 -->|1x| K3
%% Klassen-Definition für Gekaufte Materialien (Dark Theme)
    classDef bought stroke: yellow, stroke-width: 2px;
    class K1 bought;
    class K2 bought;
    class K3 bought;
    classDef product stroke: green, stroke-width: 2px;
    class P1 product;
    class P2 product;
    class P3 product;
````

#### Einleitung

Eine Stückliste (Bill of Materials, BOM) kann als gerichteter azyklischer Graph (DAG) dargestellt
werden. Dabei repräsentieren die Knoten die einzelnen **Produkte**, **Eigenfabrikate**
und **Kaufteile** (zusammenfassend als **Komponenten** bezeichnet). Die gerichteten Kanten zwischen
den
Knoten geben an, welche Komponenten zur Herstellung einer übergeordneten Komponente benötigt werden.
Jeder Kante ist eine **Menge** $q$ zugeordnet, die angibt, wie viele Einheiten der
untergeordneten Komponente benötigt werden.

#### Mathematische Herleitung

Sei $ P $ ein Endprodukt und $ X $ eine beliebige Komponente (Eigenfabrikat oder Kaufteil). Die
gesamte benötigte Menge von $ X $ ergibt sich aus der Summe der Mengen,
die auf allen möglichen **Pfade** von $ P $ zu $ X $ benötigt werden.
Jeder einzelne Pfad $ p $ von $ P $ nach $ X $ trägt
dabei mit folgender Berechnung zur Gesamtmenge bei:

$$
\text{Total}_p(X) = \prod_{(i \rightarrow j) \in p} q_{ij}
$$

Die gesamte benötigte Menge von $ X $ ist dann:

$$
\text{Total}(X) = \sum_{p \in \text{Pfade}(P \rightarrow X)} \text{Total}_p(X)
$$

Das bedeutet: Für jede einzelne **Komponente** summieren wir über alle möglichen Produktionspfade
hinweg das Produkt der aufeinanderfolgenden Mengen entlang der Kanten.

---

#### Produkt Materialanforderungen

Wir verwenden eine rekursive Methode zur Berechnung des gesamten Materialbedarfs einer Komponente,
indem wir den Graphen von oben nach unten durchlaufen. Jeder Knoten multipliziert seinen aktuellen
Bedarfsfaktor mit der benötigten Menge seiner untergeordneten Komponenten.

##### Python-Implementierung

```python
def compute_requirements(component, multiplier):
    """
    Berechnet den gesamten Materialbedarf für eine gegebene Komponente.

    :param component: Die aktuelle Komponente (Produkt, Eigenfabrikat oder Kaufteil)
    :param multiplier: Die Menge, die von dieser Komponente benötigt wird
    :return: Ein Dictionary mit der Gesamtmenge jeder benötigten Komponente
    """
    requirements = {}

    # Wenn die Komponente keine weiteren Abhängigkeiten hat (also ein Kaufteil ist)
    if component.is_leaf():
        requirements[component] = multiplier
        return requirements

    # Iteriere über alle abhängigen Komponenten
    for child, amount in component.children:
        quantity = multiplier * amount
        child_requirements = compute_requirements(child, quantity)

        # Aggregiere die Anforderungen
        for item, count in child_requirements.items():
            requirements[item] = requirements.get(item, 0) + count

    return requirements
```

---

#### Gesamtbedarfs für Produktionsplan

Ein **Produktionsplan** gibt an, wie viele Einheiten jedes Endprodukts produziert werden sollen. Um
den gesamten Materialbedarf für die geplante Produktion zu berechnen, iterieren wir über alle
Endprodukte und summieren die berechneten Anforderungen.

##### Python-Implementierung

```python
def compute_total_requirements(production_plan):
    """
    Berechnet den gesamten Materialbedarf für einen Produktionsplan.

    :param production_plan: Dictionary mit Endprodukten und geplanten Produktionsmengen
    :return: Dictionary mit der Gesamtmenge jeder benötigten Komponente
    """
    total_requirements = {}

    for product, planned_quantity in production_plan.items():
        # Berechne Anforderungen für das einzelne Endprodukt
        # noinspection PyUnresolvedReferences
        requirements = compute_requirements(product, planned_quantity)

        # Summiere die Mengen für alle Komponenten auf
        for component, amount in requirements.items():
            total_requirements[component] = total_requirements.get(component, 0) + amount

    return total_requirements
```

---

#### Materialbedarf bei vorhandenem Lagerbestand

Neben den berechneten Anforderungen aus dem Produktionsplan gibt es auch einen **Lagerbestand**, der
angibt, wie viele Einheiten jeder Komponente bereits verfügbar sind. Um zu bestimmen, wie viel
zusätzlich produziert oder eingekauft werden muss, vergleichen wir die berechneten *
*Gesamtanforderungen** mit dem vorhandenen Bestand.

##### Vorgehensweise

1. Berechne mit `compute_total_requirements` den gesamten Materialbedarf für den Produktionsplan.
2. Vergleiche den berechneten Bedarf mit dem vorhandenen Lagerbestand.
3. Falls der Lagerbestand eine Komponente bereits abdeckt, wird diese nicht weiter produziert oder
   gekauft.
4. Falls der Lagerbestand nicht ausreicht, wird die Differenz als **tatsächlicher Produktions- oder
   Beschaffungsbedarf** gespeichert.

##### Python-Implementierung

```python
def compute_production_needs(production_plan, inventory):
    """
    Berechnet den Produktions-, Bestellbedarfs basierend auf dem Produktionsplan und Lager.

    :param production_plan: Dictionary mit geplanten Produktionsmengen für Endprodukte
    :param inventory: Dictionary mit der vorhandenen Menge jeder Komponente im Lager
    :return: Dictionary mit der zusätzlichen Menge, die produziert oder eingekauft werden muss
    """
    # noinspection PyUnresolvedReferences
    total_requirements = compute_total_requirements(production_plan)
    production_needs = {}

    for component, required_amount in total_requirements.items():
        stock = inventory.get(component, 0)

        # Falls Lagerbestand reicht, Bedarf = 0
        production_needs[component] = max(required_amount - stock, 0)

    return production_needs
```

---

#### Fazit

Mit diesem Ansatz kann für einen gegebenen Produktionsplan der **exakte Materialbedarf** für alle
Komponenten berechnet werden. Zudem kann durch den Abgleich mit dem Lagerbestand bestimmt werden,
**wie viel tatsächlich hergestellt oder beschafft** werden muss.

**Vorteile dieser Methode:**

- Berücksichtigt verschachtelte Stücklisten (mehrstufige BOMs)
- Aggregiert Materialanforderungen über verschiedene Endprodukte hinweg
- Verhindert Überproduktion durch Einbezug des Lagerbestands
- Nutzt eine rekursive Implementierung zur einfachen Verarbeitung des BOM-Graphs

Dieser Algorithmus ist essenziell für die **Produktionsplanung**,
**Materialdisposition** und **Lageroptimierung** in Fertigungsunternehmen. 🚀

### Workstation-Kapazitäten

#### 1. Definition der Variablen

Ein Produkt **$p$** wird nicht an einer einzigen Workstation gefertigt, sondern kann mehrere *
*Bearbeitungsschritte** durchlaufen. Jeder dieser Schritte wird an einer bestimmten **Workstation (
ws)** durchgeführt.

Jede Workstation **$ws$** ist dabei mit einer spezifischen **Rüstzeit ($rt$) und
Bearbeitungszeit ($pt$) pro Einheit** verbunden.

Für ein Produkt $p$ gibt es eine **Sequenz von Arbeitsschritten**, wobei jeder Arbeitsschritt an
einer bestimmten Workstation $ws$ durchgeführt wird:

$$
S(p) = \{(ws_1, rt_1, pt_1), (ws_2, rt_2, pt_2), \dots, (ws_n, rt_n, pt_n) \}
$$

wobei:

- $S(p)$ die Menge aller Bearbeitungsschritte für Produkt $p$ ist.
- Jeder Schritt ein Tupel $(ws, rt, pt)$ ist:
    - $ws$: Die Workstation, die den Schritt ausführt.
    - $rt$: Die für diesen Schritt benötigte Rüstzeit (fix, unabhängig von der Produktionsmenge).
    - $pt$: Die Bearbeitungszeit pro Einheit des Produkts an dieser Workstation.

Die benötigte **Kapazität einer einzelnen Workstation $ws$** für ein Produkt $p$ ergibt sich aus:

$$
T(ws, p, q_p) = rt(ws, p) + q_p \cdot pt(ws, p)
$$

wobei:

- $q_p$ die Produktionsmenge des Produkts $p$ ist.
- $T(ws, p)$ die gesamte benötigte Kapazität für dieses Produkt an dieser Workstation ist.

---

#### 2. Berechnung der Gesamtbelastung einer Workstation

Da eine Workstation mehrere Produkte bearbeitet, summieren wir die Kapazität über alle Produkte, die
an dieser Workstation gefertigt werden müssen:

Wir können die Formel klarer und kompakter formulieren, indem wir die Bedingung, dass der
Bearbeitungsschritt an der Workstation $ws$ durchgeführt wird, direkt in die Summationsnotation
einfließen lassen. Eine verbesserte Darstellung lautet:

$$
\text{Cap}(ws) = \sum_{p \in P} \; \sum_{\substack{(ws',\, rt,\, pt) \in S(p) \\ ws' = ws}} \Bigl( rt + q_p \cdot pt \Bigr)
$$

Hierbei gilt:

- $P$ ist die Menge aller zu produzierenden Produkte.
- $S(p)$ ist die Menge aller Bearbeitungsschritte für Produkt $p$, wobei jeder Schritt als
  Tupel $(ws', rt, pt)$ gegeben ist.
- $rt$ und $pt$ stehen für Rüstzeit und Bearbeitungszeit pro Einheit.
- $q_p$ ist die Produktionsmenge des Produkts $p$.
- $rt + q_p \cdot pt$ entspricht der benötigten Kapazität (in Minuten) für den jeweiligen Schritt.

Diese Formel summiert somit für jede Workstation $ws$ über alle Produkte $p$ und über alle ihrer
Bearbeitungsschritte, die an $ws$ durchgeführt werden, die erforderliche Kapazität.


---

#### 3. Berücksichtigung von Lieferverzögerungen bei Kaufteilen

Falls für ein Produkt $p$ Kaufteile benötigt werden, kann deren verspätete Lieferung zu einer
Kapazitätsminderung führen. Jede Kaufteil-Lieferung besitzt:

- Eine **erwartete Lieferzeit** $\ell_k$
- Eine **Lieferzeitabweichung** $\sigma_k$

Falls ein Kaufteil $k$ an einer Workstation $ws$ benötigt wird, reduziert sich die verfügbare
Kapazität:

$$
\text{EKapa}(ws) = \text{Kapazität}(ws) - \sum_{k \in K(ws)} \sigma_k
$$

wobei:

- $K(ws)$ die Menge aller Kaufteile ist, die an Workstation $ws$ benötigt werden.
- $\sigma_k$ die Abweichung der Lieferzeit für das Kaufteil $k$ ist.

> Gilt die Verspätung auch für Eigenfertigungen? Diese werden ja wiederum auch verspätet sein, weil
> diese auf andere
> Kaufteile warten. Sowie auch wieder auf Eigenfertigungen.

---

### Erläuterung der zulässigen Workstation-Kapazitäten

Die täglichen Kapazitäten einer Workstation ergeben sich aus dem eingesetzten Schichtmodell und den
möglichen Überstunden. Dabei gelten folgende Grundlagen:

#### Basisarbeitszeit pro Schicht

Eine reguläre Schicht dauert 8 Stunden, was $ B = 8\text{h}= 480\text{min}$
pro Tag ergibt.

#### Überstunden

Es können zusätzlich Überstunden geleistet werden, die bis zu 50 % der Basisarbeitszeit betragen.
Das bedeutet, dass pro Schicht maximal  
$$
O_{max} = 0.5 \times B = 0.5 \times 480\text{min} = 240\text{min}
$$
an Überstunden möglich sind.

#### Mögliche Schichtmodelle und deren Kapazitäten

| Schichten | Basisarbeitszeit (min/d) | Überstunden (min/d) | Zulässiger Bereich (min/d) | 
|-----------|--------------------------|---------------------|----------------------------|
| 1         | 480                      | 0 - 240             | 480 - 720                  |
| 2         | 960                      | 0 - 240             | 960 - 1200                 |
| 3         | 1440                     | 0                   | 1440                       |

#### Erforderliche Kapazität

Die finale geplante Tageskapazität einer Workstation wird auf den nächstgrößeren zulässigen Wert
angepasst. Dabei gelten folgende Beispiele:

- Beispiel 1:  
  Effektive Kapazität pro Tag $ECap_d = 500min$

  → 500 liegt im zulässigen Bereich einer Schicht (480–720 Min).  
  **$PCap_d = 500 min$**

- Beispiel 2:  
  $ECap_d = 800 min$
-

→ 800 Min überschreiten den 1-Schicht-Bereich, aber liegen unter 960 Min (Minimum 2-Schicht).  
**PCap_d = 960 Min**

- Beispiel 3:  
  $ECap_d = 1300min$

  → 1300 Min liegen oberhalb des 2-Schicht-Bereichs (960–1200 Min).  
  **PCap_d = 1440 Min**

Mathematisch formuliert ergibt sich die geplante Tageskapazität $\text{PCap}_d$ aus der effektiven
Tageskapazität $\text{ECap}_d$:

$$
\text{PCap}_d =
\begin{cases}
480, & \text{ECap}_d \leq 480 \\
\text{ECap}_d, & 480 < \text{ECap}_d \leq 720 \\
960, & 720 < \text{ECap}_d \leq 960 \\
\text{ECap}_d, & 960 < \text{ECap}_d \leq 1200 \\
1440, & \text{ECap}_d > 1200
\end{cases}
$$

Diese Regelung sorgt dafür, dass die Kapazitätsplanung immer auf einem der realistisch möglichen
Schichtmodelle (1-, 2- oder 3-Schicht) basiert.

#### 5. Gesamtmodell

Die Berechnung der Workstation-Kapazitäten erfolgt in folgenden Schritten:

1. **Bestimmung der Belastung jeder Workstation durch die Produktion**  
   $$  
   \text{Cap}_{p}(ws) = \sum_{p \in P} \sum_{(ws', rt, pt) \in S(p)~\land~{ws' = ws}} \cdot \left( rt + q_p \cdot pt \right)  
   $$

2. **Umrechnung auf Tageskapazität**  
   $$  
   \text{Cap}_d(ws) = \frac{\text{Cap}_P(ws)}{5}
   $$

3. **Abzug von Lieferverzögerungen der Kaufteile**  
   $$  
   \text{ECap}_d(ws) = \text{Cap}_d(ws) - \sum_{k \in K(ws)} \sigma_k  
   $$

4. **Zulässigen Kapazitätswert bestimmen**  
   $$
   \text{PCap}_d =
   \begin{cases}
   480, & \text{ECap}_d \leq 480 \\
   \text{ECap}_d, & 480 < \text{ECap}_d \leq 720 \\
   960, & 720 < \text{ECap}_d \leq 960 \\
   \text{ECap}_d, & 960 < \text{ECap}_d \leq 1200 \\
   1440, & \text{ECap}_d > 1200
   \end{cases}
   $$

---

#### 6. Fazit

##### 🔹 Vorteile dieses Modells:

✅ Berücksichtigt **mehrstufige Produktionsprozesse**, in denen ein Produkt mehrere Workstations
durchläuft.  
✅ Aggregiert **alle Produkte**, die an einer Workstation gefertigt werden, um die Gesamtauslastung
zu berechnen.  
✅ Bezieht **Lieferverzögerungen von Kaufteilen** mit ein, um realistische Kapazitätsplanungen zu
ermöglichen.  
✅ **Kapazitätsplanung erfolgt in Minuten pro Tag**, um eine detaillierte Produktionsplanung zu
ermöglichen.  
✅ **Kapazitätswerte werden an realistisch verfügbare Werte angepasst**, um praktikable Schichtpläne
zu ermöglichen.

Dieses Modell stellt eine **präzise Grundlage für die Kapazitätsplanung und Kostenoptimierung** in
einem Produktionssystem dar. 🚀

### Personal und Maschinenkosten

Bei festgelegten Workstation Kapazitäten können die Personalkosten einfach berechnet werden.
Funktionsweise der Schichten und Personalkosten.
Sei

- $B = 480$ Minuten, die Basisarbeitszeit pro Schicht, und
- $Cap_d(ws)$ die geplante Kapazität pro Tag in Minuten für eine Workstation $ws$.

Dann gilt:

$$
s(ws) = \max\Big(\min\Big(round(\frac{Cap_d(ws)}{B}),\, 3\Big),\, 1\Big)
$$

Dabei gilt:

- $round(X)$ rundet den Quotienten nach round to nearest, ties to zero.
- Durch $\min(\cdot,\, 3)$ wird sichergestellt, dass maximal 3 Schichten verwendet werden.
- Durch $\max(\cdot,\, 1)$ wird garantiert, dass mindestens 1 Schicht vorliegt.

Die Anzahl der Überstunden pro Tag $O_d$ berechnet sich dann als Differenz zwischen der geplanten
Kapazität und der Basiskapazität der ermittelten Schichten:

$$
O_d(ws) = \max\Big(Cap_d(ws) - s(ws) \cdot B,\, 0\Big)
$$

Diese mathematische Darstellung erlaubt es, aus einer vorgegebenen Tageskapazität $Cap_d$ die nötige
Anzahl an Schichten ($s$) sowie den Umfang der Überstunden ($O_d$) zu berechnen.

Es gibt für jede Workstation unterschiedliche Kosten

#### Berechnung der Personalkosten für jede Workstation

Um die Personalkosten für jede Workstation zu berechnen, benötigen wir folgende Informationen:

- **Geplante Kapazität pro Tag** $PCap_d(ws)$ für jede Workstation $ws$
- **Anzahl der Schichten** $s(ws)$ für jede Workstation $ws$
- **Überstunden pro Tag** $O_d(ws)$ für jede Workstation $ws$
- **Lohnkosten je Schicht und Überstunden** aus der Tabelle
- **Maschinenkosten (fix und variabel) pro Minute** aus der Tabelle

---

##### 1. Berechnung der aufgewendeten Minuten je Schichttyp

Da jede reguläre Schicht genau **480 Minuten** dauert, ergibt sich der Minutenaufwand je Workstation
folgendermaßen:
Wie oben $B = 480min$, die Basisarbeitszeit pro Schicht. Ebenso wie bereits definiert $Cap_d$ die
geplante Kapazität pro Tag in Minuten.

- **Gesamte produktive Minuten**  
  $$
  Cap_d(ws)
  $$

---

##### 2. Berechnung der Lohnkosten je Workstation

Die Lohnkosten hängen von der Anzahl der eingesetzten Schichten ab, da jede Schicht einen
unterschiedlichen Lohnsatz hat:

**Gesamtkosten für die regulären Schichten**  
Die Lohnkosten pro Minute variieren je nach Schicht:
- **Schicht 1:** Lohnsatz $L_1(ws)$
- **Schicht 2:** Lohnsatz $L_2(ws)$
- **Schicht 3:** Lohnsatz $L_3(ws)$
- **Überstunden:** Lohnsatz $L_{o}(ws)$

Je nach Anzahl der Schichten ergibt sich der reguläre Lohnkostenblock: (**L**abour cost per **d**
ay)
$$
L_{\text{d}}(ws) = L_o(ws) \cdot O_d(ws) +
\begin{cases}
L_1(ws) \cdot B.& s(ws) = 1 \\
L_1(ws) \cdot B + L_2(ws) \cdot B, & s(ws) = 2 \\
L_1(ws) \cdot B + L_2(ws) \cdot B + L_3(ws) \cdot B, & s(ws) = 3
\end{cases}
$$

Die **Kapazitätsauslastung** einer Workstation $ws$ beschreibt den Anteil der tatsächlich genutzten
Kapazität im Vergleich zur geplanten Kapazität:

$$
util(ws) = \frac{M_{used}(ws)}{M_{total}(ws)}
$$

wobei:

- $M_{used}(ws)$ die tatsächlich produktiv genutzten Minuten sind (Bearbeitungszeit).
- $M_{total}(ws)$ die gesamte eingeplante Kapazität (Schichten + Überstunden).

Wenn eine Workstation vollständig genutzt wird, beträgt die Auslastung **100 %** $(= 1)$. Liegt sie
darunter, entstehen **Leerkosten**.

---

Die Maschinenkosten setzen sich aus **fixen** und **variablen** Kosten zusammen:
Die **variablen Maschinenkosten** fallen nur für produktiv genutzte Minuten an:

$$
C_{Mvar}(ws) = M_{used}(ws) \cdot c_{Mvar}(ws)
$$

wobei:

- $c_{Mvar}(ws)$ die variablen Maschinenkosten pro Minute sind.
- $M_{used}(ws)$ die Minuten, in denen tatsächlich produziert wird.

Variable Maschinenkosten entstehen **nur dann**, wenn produziert wird. Falls eine Workstation eine
Schicht eingeplant hat, aber keine Produktion stattfindet, sind die variablen Maschinenkosten **0**.

---

Die **fixen Maschinenkosten** fallen an für Leerzeiten innerhalb der Schichten

$$
C_{Mfix}(ws) = M_{total}(ws) - M_{used}(ws) \cdot c_{Mfix}(ws)
$$

wobei:

- $M_{total}(ws) = s(ws) \cdot B + O_d(ws)$ die gesamte geplante Kapazität ist.
- $c_{Mfix}(ws)$ die fixen Maschinenkosten pro Minute sind.

Fixe Maschinenkosten entstehen auch dann, wenn eine Workstation nicht voll ausgelastet ist. Falls
eine Schicht eingeplant wurde, aber die tatsächliche Produktion geringer ist als die geplante
Kapazität, entstehen **Leerkosten**.


#### 4. Gesamtformel für Maschinenkosten

Die gesamten Maschinenkosten einer Workstation setzen sich aus fixen und variablen Kosten zusammen:

$$
C_{M}(ws) = C_{Mfix}(ws) + C_{mach,var}(ws)
$$

bzw.

$$
C_{M}(ws) = (M_{total}(ws)- M_used(ws)) \cdot c_{Mfix}(ws)) + (M_{used}(ws) \cdot c_{mach,var}(ws))
$$

---

## 5. Fazit

🔹 **Fixe Maschinenkosten** fallen immer an, wenn eine Schicht eingeplant wurde – unabhängig von der
tatsächlichen Nutzung.  
🔹 **Variable Maschinenkosten** entstehen nur, wenn tatsächlich produziert wird.  
🔹 **Leerkosten** entstehen, wenn die eingeplante Schicht nicht vollständig ausgelastet wird.  
🔹 **Kapazitätsauslastung** gibt an, wie effizient eine Workstation genutzt wird – je höher die
Auslastung, desto geringer die Leerkosten.

Diese Berechnungen helfen dabei, **Produktionskosten zu minimieren**, indem ineffiziente Nutzung (z.
B. überflüssige Schichten oder hohe Leerkosten) erkannt wird. 🚀

---

### 4. Gesamtkosten pro Workstation

Die Gesamtkosten für jede Workstation $ws$ setzen sich zusammen aus:

$$
K_{\text{Gesamt}}(ws) = K_{\text{Personal}}(ws) + K_{\text{Maschine}}(ws)
$$

Falls eine Workstation **nicht ausgelastet** ist (Leerlaufzeiten), entstehen Leerkosten. Diese
müssten separat berechnet werden.

---

## Fazit

Mit dieser Berechnungsmethode können wir für jede Workstation:
✅ Die Lohnkosten basierend auf den eingesetzten Schichten und Überstunden berechnen  
✅ Die Maschinenkosten aus variablen und fixen Anteilen ermitteln  
✅ Die Gesamtkosten einer Workstation bestimmen  
Dies ermöglicht eine detaillierte Kostenanalyse pro Arbeitsplatz!
---