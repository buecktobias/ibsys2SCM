# Planung Verspätungen Produktion

Durch Materialverspätungen kann sich der gesamte Produktionsprozess verspäten. HTML ist toll.

## Einfachster Fall

Wenn wir ein Produkt produzieren wollen, das nur ein Kaufteil benötigt, kann man die Verspätung
deutlich einfacher berechnen.

```mermaid
graph LR
    K1((K1))
    WS[[Workstation 1]]
    E1((E1))
    K1 -- 1 --> WS
    WS -- 1 --> E1
    classDef bought fill: #443333, stroke: white, stroke-width: 1px;
    class K1 bought;
    classDef product fill: #333344, stroke: white, stroke-width: 1px;
    class E1 product;
    classDef workstation fill: #222266, stroke: white, stroke-width: 1px;
    class WS workstation;
```

**Gegeben:**

- K1 (das Kaufteil) hat eine **durchschnittliche Lieferzeit** $D_{K1}$ 
- und eine **Standardabweichung** $\sigma_{K1}$.
- Die Workstation $WS$ benötigt zur Produktion von E1 aus K1 an $ws1$ eine feste **Rüstzeit**
  sowie eine mengenabhängige **Durchlaufzeit**.
- $P_{K1}$ gibt an, wie viele Minuten zur Produktion einer Einheit von E1 aus K1 benötigt werden.

## Berechnung der voraussichtlichen Lieferzeit

In unserem Modell setzt sich die **voraussichtliche Lieferzeit** $L_v$ aus folgenden Komponenten
zusammen:

1. **Lieferzeit des Kaufteils:** \(D_{K1}\)
2. **Fixe Rüstzeit der Produktion:** \(R\)
3. **Mengenabhängige Produktionszeit:** Diese berechnet sich aus der Produktionszeit pro Einheit
   $P_{K1}$ multipliziert mit der herzustellenden Menge $Q$.

Die Gesamtformel lautet:

$$
L_v = D_{K1} + R + P_{K1} \times Q
$$

- $D_{K1}$: durchschnittliche Lieferzeit des Kaufteils
- \(R\): fixe Rüstzeit der Produktion
- \(P_{K1}\): Produktionszeit pro Einheit
- \(Q\): Produktionsmenge

### Berücksichtigung von Unsicherheiten

Um auch die Schwankungen bzw. Unsicherheiten in den Zeiten zu erfassen, kann die Standardabweichung
der voraussichtlichen Lieferzeit wie folgt abgeschätzt werden:

\[
\sigma_{L_v} = \sqrt{ \sigma_{K1}^2 + \sigma_R^2 + \left(Q \times \sigma_{P}\right)^2 }
\]

- \(\sigma_{K1}\): Standardabweichung der Lieferzeit des Kaufteils
- \(\sigma_R\): Unsicherheit in der Rüstzeit (falls vorhanden)
- \(\sigma_{P}\): Standardabweichung der Produktionszeit pro Einheit

Diese Abschätzung hilft dabei, abzuschätzen, ob und in welchem Umfang es zu Produktionsverspätungen
kommen kann, wenn sich einzelne Zeitkomponenten verändern.

---

Mit dieser Dokumentation wird die Berechnung der voraussichtlichen Lieferzeit klar definiert und die
wesentlichen Einflussgrößen (Lieferzeit, Rüstzeit, Produktionszeit und deren Unsicherheiten) werden
berücksichtigt.

# Einfluss eines vorhandenen Lagers von K1

Verfügt man über einen Lagerbestand an K1, verkürzt sich die effektive Lieferzeit des Materials. Dadurch wird die Produktionsdauer reduziert, da auf eine externe Materiallieferung verzichtet werden kann – zumindest teilweise.

## Variablendefinitionen

- $I_{K1}$: Lagerbestand von K1 (verfügbare Kaufteile)
- $X$: zu produzierende Stückzahl
- $D_{K1}$: durchschnittliche Lieferzeit des Kaufteils (ohne Lager)
- $R$: fixe Rüstzeit der Produktion
- $t_p$: Produktionszeit pro Einheit (in Minuten)
- $T_{\text{prod}}$: Gesamtproduktionsdauer

## Szenarien

### 1. Kein Lagerbestand

Wenn überhaupt kein Lager vorhanden ist, muss das Material geliefert werden. Dann ergibt sich:
$$
T_{\text{prod}} = D_{K1} + R + t_p \cdot X
$$

### 2. Ausreichender Lagerbestand

Ist der Lagerbestand ausreichend, also $I_{K1} \geq X$, können alle Produkte ohne Wartezeit produziert werden:
$$
T_{\text{prod}} = R + t_p \cdot X
$$

### 3. Unzureichender Lagerbestand

Wenn der Lagerbestand $I_{K1}$ kleiner als die Produktionsmenge $X$ ist, müssen nur die fehlenden $X - I_{K1}$ Einheiten extern geliefert werden. Eine Abschätzung der Gesamtproduktionsdauer erfolgt dann beispielsweise durch:
$$
T_{\text{prod}} = R + t_p \cdot X + \left(\frac{X - I_{K1}}{X}\right) \cdot D_{K1}
$$
Hierbei wird angenommen, dass der Anteil der fehlenden Kaufteile proportional zu $D_{K1}$ die Produktionsdauer erhöht.

## Zusammenfassung

- **Ohne Lager:**  
  $$ T_{\text{prod}} = D_{K1} + R + t_p \cdot X $$

- **Mit ausreichendem Lager ($I_{K1} \geq X$):**  
  $$ T_{\text{prod}} = R + t_p \cdot X $$

- **Mit unzureichendem Lager ($I_{K1} < X$):**  
  $$ T_{\text{prod}} = R + t_p \cdot X + \left(\frac{X - I_{K1}}{X}\right) \cdot D_{K1} $$

Diese Formeln dokumentieren, wie sich ein vorhandener Lagerbestand an K1 auf die voraussichtliche Produktionsdauer von $X$ Produkten auswirkt.



Die Verzögerung der Produktion an der Workstation hängt davon ab, wann genügend Material A und B verfügbar sind, um die Produktion von \( P_C \) Einheiten von C zu ermöglichen.

### Gegeben:
- **Lagerbestand**:
    - \( A_Q \) (Bestand an A)
    - \( B_Q \) (Bestand an B)
- **Bestellmengen**:
    - \( x \) Einheiten von A bestellt (Ankunftszeit \( T_A \) mit Standardabweichung \( SD(T_A) \))
    - \( y \) Einheiten von B bestellt (Ankunftszeit \( T_B \) mit Standardabweichung \( SD(T_B) \))
- **Produktionsanforderungen** für 1 Einheit C:
    - \( 2 \) Einheiten von A
    - \( 3 \) Einheiten von B
- **Produktionskapazität**:
    - Maximal \( P_C \) Einheiten C pro Tag produzierbar

---

### Berechnung:
#### 1. Berechnung des aktuellen maximal möglichen Produktionsvolumens
Zunächst berechnen wir, wie viele Einheiten C **sofort** produziert werden können:

\[
C_{\text{max sofort}} = \min \left( \frac{A_Q}{2}, \frac{B_Q}{3} \right)
\]

Das bedeutet, dass maximal \( C_{\text{max sofort}} \) Einheiten C ohne Verzögerung produziert werden können.

---

#### 2. Fehlmengen bestimmen
Um die volle Produktionskapazität von \( P_C \) Einheiten pro Tag zu erreichen, benötigen wir:
\[
A_{\text{bedarf}} = 2 P_C, \quad B_{\text{bedarf}} = 3 P_C
\]
Falls der aktuelle Lagerbestand nicht ausreicht:
\[
A_{\text{fehlend}} = \max(0, 2 P_C - A_Q)
\]
\[
B_{\text{fehlend}} = \max(0, 3 P_C - B_Q)
\]
Diese müssen durch Bestellungen abgedeckt werden.

---

#### 3. Bestellverfügbarkeit
Die bestellten Materialien treffen mit einer Unsicherheit ein. Die Zeit bis die fehlenden Mengen von A und B eintreffen, ist durch die jeweilige Lieferzeitverteilung gegeben:

\[
T_A \sim \mathcal{N}(\mu_A = T_A, \sigma_A = SD(T_A))
\]
\[
T_B \sim \mathcal{N}(\mu_B = T_B, \sigma_B = SD(T_B))
\]

Die Produktion kann erst fortgesetzt werden, wenn **beide** Materialien in ausreichender Menge eintreffen. Die effektive Wartezeit ergibt sich aus:

\[
T_{\text{verzögerung}} = \max(T_A' , T_B')
\]

wobei:
- \( T_A' \) die Zeit bis **mindestens** \( A_{\text{fehlend}} \) Einheiten von A angekommen sind.
- \( T_B' \) die Zeit bis **mindestens** \( B_{\text{fehlend}} \) Einheiten von B angekommen sind.

Da die Lieferzeiten normalverteilt sind, ist \( T_{\text{verzögerung}} \) eine **Maximum-Verteilung**, die approximativ als:

\[
T_{\text{verzögerung}} \approx \max(\mathcal{N}(T_A, SD(T_A)), \mathcal{N}(T_B, SD(T_B)))
\]

modelliert werden kann.

---

### Simulation oder Näherung
Die mittlere Verzögerung kann als:

\[
E[T_{\text{verzögerung}}] \approx \mu_A \Phi\left(\frac{\mu_A - \mu_B}{\sqrt{SD(T_A)^2 + SD(T_B)^2}}\right) + \mu_B \Phi\left(\frac{\mu_B - \mu_A}{\sqrt{SD(T_A)^2 + SD(T_B)^2}}\right)
\]

geschätzt werden, wobei \( \Phi(x) \) die kumulative Verteilungsfunktion der Standardnormalverteilung ist.

Alternativ kann eine Monte-Carlo-Simulation verwendet werden, um die Verteilung genauer zu bestimmen.

---

### Fazit:
- Falls genügend A und B auf Lager sind: **keine Verzögerung**.
- Falls Material fehlt: Die Verzögerung entspricht dem **späteren** Eintreffen der Bestellungen für A oder B.
- Falls die Lieferzeiten zufällig verteilt sind, muss die **Maximum-Verteilung** berücksichtigt werden.
- Eine Näherung kann über die Erwartungswerte der Lieferzeiten erfolgen oder durch eine Monte-Carlo-Simulation berechnet werden.

Soll ich eine Simulation für dich durchführen?