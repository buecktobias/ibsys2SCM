# Workstation-Kapazitäten
## Variablen
### Basis
- **Eigenfabrikat $I_E$**
- **Arbeitsstellen (Workstations)** $ws$

### Prozess
**Jeder Prozess $p$** hat:
- Rüstzeit $p_rt$ ist $rt\in\mathbb{N}_{0}$ gibt die Rüstzeit in Minuten an.
- Bearbeitungszeit $p_pt$ $rt\in\mathbb{N}_{0}$ gibt die Bearbeitungszeit je Einheit in Minuten an.

## Gesamtbelastung

Da eine Workstation mehrere Produkte bearbeitet, summieren wir die Kapazität über alle Produkte, die
an dieser Workstation gefertigt werden müssen.
---

## Lieferverzögerungen bei Kaufteilen

- Eine **erwartete Lieferzeit** $\ell_k$
- Eine **Lieferzeitabweichung** $\sigma_k$

Falls ein Kaufteil $k$ an einer Workstation $ws$ benötigt wird, reduziert sich die verfügbare
Kapazität:

$$
EffKapa(ws) \equiv \text{Kapazität}(ws) - \sum_{k \in K(ws)} \sigma_k
$$

wobei:

- $K(ws)$ die Menge aller Kaufteile ist, die an Workstation $ws$ benötigt werden.
- $\sigma_k$ die Abweichung der Lieferzeit für das Kaufteil $k$ ist.

> Gilt die Verspätung auch für Eigenfertigungen? Diese werden ja wiederum auch verspätet sein, weil
> diese auf andere
> Kaufteile warten. Sowie auch wieder auf Eigenfertigungen.

---

## Verfügbare Arbeitszeiten

Die täglichen Kapazitäten einer Workstation ergeben sich aus dem eingesetzten Schichtmodell und den
möglichen Überstunden. Dabei gelten folgende Grundlagen:

### Basisarbeitszeit pro Schicht

Eine reguläre Schicht dauert 8 Stunden, was $B = 8h= 480min$
pro Tag ergibt.

### Überstunden

Es können zusätzlich Überstunden geleistet werden, die bis zu 50 % der Basisarbeitszeit betragen.
Das bedeutet, dass pro Schicht maximal

$$
O_{max} = 0.5 \times B = 0.5 \times 480min = 240min
$$

an Überstunden möglich sind.

### Mögliche Schichtmodelle und deren Kapazitäten

| Schichten | Basisarbeitszeit (min/d) | Überstunden (min/d) | Zulässiger Bereich (min/d) | 
|-----------|--------------------------|---------------------|----------------------------|
| 1         | 480                      | 0 - 240             | 480 - 720                  |
| 2         | 960                      | 0 - 240             | 960 - 1200                 |
| 3         | 1440                     | 0                   | 1440                       |

### Erforderliche Kapazität

Um wie geplant zu produzieren müssen wir den ersten größeren gleichen Möglichen Wert nehmen


### Beispiel 1

- Effektive Kapazität pro Tag für $ws_1$: $ECap_d(ws_1) = 500min$
- → 500 liegt im zulässigen Bereich einer Schicht (480–720 Min).
- **$PCap_d(ws_1) = 500 min$**

### Beispiel 2

- $ECap_d(ws_2) = 800 min$
- → 800 Min überschreiten den 1-Schicht-Bereich, aber liegen unter 960 Min (Minimum 2-Schicht).
- **PCap_d(ws_2) = 960 Min**

### Beispiel 3

- $ECap_d(ws_3) = 1300min$
- → 1300 Min liegen oberhalb des 2-Schicht-Bereichs (960–1200 Min).
- **PCap_d = 1440 Min**

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
