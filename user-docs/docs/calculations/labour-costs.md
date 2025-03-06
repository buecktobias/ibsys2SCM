# Berechnungen


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
C_{M}(ws) = C_{Mfix}(ws) + C_{Mvar}(ws)
$$

---

### 4. Gesamtkosten pro Workstation

Die Gesamtkosten für jede Workstation $ws$ setzen sich zusammen aus:

$$
C_{total}(ws) = C_L(ws) + C_M(ws)
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