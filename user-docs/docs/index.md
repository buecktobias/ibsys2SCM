# Produktionsplanung & Optimierung

Dieses Projekt beschreibt die Berechnungen und Optimierungen zur Planung einer Produktionsumgebung,
einschließlich Materialbedarf, Kapazitätsplanung, Kostenkalkulation und Simulation. Dabei werden
verschiedene Berechnungen zur Bestimmung des Primär-, Sekundär- und Tertiärbedarfs durchgeführt, um
eine optimale Produktionsplanung zu gewährleisten.

---

## Inhalte

### 1. [Einführung](simulation-information.md)

Hier werden die zugrunde liegenden Annahmen und Modellparameter erläutert:

- **[Perioden und Zeiteinheiten](simulation-information.md#wichtige-informationen)**
- **[Produktionsstruktur & Inventar](simulation-information.md#produktionsstruktur)**
- **[Periodenspezifische Informationen](simulation-information.md#periodenspezifische-daten)**

---

### 2. [Berechnungen](calculation.md)

In diesem Abschnitt werden die grundlegenden Berechnungen zur Produktionsplanung erläutert:

- **[Materialbedarf](calculation.md#materialbedarf)**
- **[Kapazitätsberechnung](calculation.md#workstation-kapazitäten)**
- **[Kostenkalkulation](calculation.md#personal-und-maschinenkosten)**
- **[Mathematische Modelle](calculation.md#mathematische-herleitung)**

---

### 3. [Planung & Optimierung](optimization.md)

Hier wird die Planung der Produktion mit Optimierungsmöglichkeiten beschrieben:

- **[Primär-, Sekundär- und Tertiärbedarf](optimization.md#schritt-für-schritt-planungsablauf)**
- **[Kapazitätsprüfung](optimization.md#kapazitätsprüfung)**
- **[Optimierungsstrategien](optimization.md#wichtiges-zur-optimierung)**
- **[Lagerkostenoptimierung](optimization.md#lagerkosten)**

---

### 4. [Python-Implementierung](python-implementation.md)

Dieser Abschnitt beschreibt die technische Umsetzung der Produktionsplanung in Python:

- **[Struktur der Klassen und Datenmodelle](python-implementation.md#konzept)** Umsetzung der
  Stückliste als Directed Acyclic Graph (DAG).

---
