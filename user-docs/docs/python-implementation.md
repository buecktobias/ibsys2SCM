
## Python Implementierung

### Produktionsplanung

In diesem Modell gehen wir davon aus, dass unsere Produktionsstruktur (BOM – Bill of Materials) als
gerichteter azyklischer Graph (DAG) modelliert wird. Jeder Kante wird eine Menge zugeordnet, die
angibt, wie viele Einheiten einer untergeordneten Komponente benötigt werden. Alle Komponenten –
seien es Endprodukte, In-House-Products (Eigenfabrikate) oder PurchaseParts (Kaufteile) – werden
zusammenfassend als *Items* betrachtet.

#### Konzept

- **Item (Basisklasse):**  
  Enthält gemeinsame Attribute wie `id`, `value` und zusätzlich eine BOM-Struktur, dargestellt durch
  ein Attribut `children`.
    - **children:** Eine Liste von Tupeln `(child: Item, quantity: int)`.  
      Komponenten ohne weitere Abhängigkeiten (z.B. Kaufteile) haben keine Kinder.

- **Spezialisierungen:**
    - `EndProduct`: Repräsentiert das Endprodukt.
    - `InHouseProduct`: Repräsentiert intern hergestellte Produkte (Eigenfabrikate).
    - `PurchasePart`: Repräsentiert zugekaufte Teile mit zusätzlichen Attributen wie
      `discountQuantity`, `orderTime` und `orderTimeDeviation`.

- **Inventory:**  
  Ein `InventoryEntry` verbindet ein `Item` mit dem Lagerbestand. Die Klasse `Inventory` verwaltet
  diese Einträge (z.B. in einem Dictionary) und bietet Methoden wie `getQuantity` und
  `calculateTotalValue`.

- **PlanningData & PrimaryDemandCalculator:**  
  `PlanningData` enthält die periodenspezifischen Eingaben, z.B. einen Forecast für EndProducts und
  den aktuellen Lagerbestand. Der `PrimaryDemandCalculator` nutzt diese Daten, um den primären
  Bedarf zu ermitteln.

- **BOMCalculator:**  
  Hier werden die rekursiven Berechnungen des Materialbedarfs durchgeführt. Es kommen die folgenden
  Funktionen zum Einsatz:
    - `compute_requirements`: Berechnet den Bedarf für einen einzelnen Item-Knoten (rekursiv entlang
      der BOM).
    - `compute_total_requirements`: Aggregiert den Bedarf für alle EndProducts eines
      Produktionsplans.
    - `compute_production_needs`: Vergleicht den Gesamtbedarf mit dem Lagerbestand und ermittelt den
      zusätzlichen Produktions- bzw. Einkaufsbedarf.

### Aktualisiertes PlantUML-Diagramm

Siehe class_diagram.puml
