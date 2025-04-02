Got it! If Mermaid looks too raw or messy (which it often does), here's a cleaner alternative that works well in docs,
slides, or even on whiteboards:

---

## ✅ **Clean REST API Overview (Resource Table)**

| Resource               | Method | Description                              | Endpoint                                            |
|------------------------|--------|------------------------------------------|-----------------------------------------------------|
| `Game`                 | POST   | Create Game with Id $id                  | `/game/{id}`                                        |
| `Period Result`        | GET    | Get Period Result for aPeriod            | `/game/{id}/period-result/{period}`                 |
|                        | PUT    | Set Period Result For Game               | `/game/{id}/period-result/{period}`                 |
| `Primary Plan`         | GET    | Get Primary Plan For a Game              | `/game/{id}/primary-plan/{period}`                  |
|                        | POST   | Get Calculated est Primary Plan          | `/game/{id}/primary-plan/{period}/calulate`         |
|                        | PATCH  | Change Primary Plan                      | `/game/{id}/primary-plan/{period}`                  |
| `Production`           | GET    | Get Production For a Game                | `/game/{id}/production/{period}`                    |
|                        | POST   | Get Calculated est. Production           | `/game/{id}/production/{period}/calulate`           |
|                        | PATCH  | Change Production                        | `/game/{id}/production/{period}`                    |
| `Orders`               | GET    | Get Orders For a Game                    | `/game/{id}/order/{period}`                         |
|                        | POST   | Get Calculated est. Orders               | `/game/{id}/order/{period}/calulate`                |
|                        | PATCH  | Change Production                        | `/game/{id}/order/{period}`                         |
| `Workstation Capacity` | GET    | Get Workstation Capacity For a Game      | `/game/{id}/workstation-capacity/{period}`          |
|                        | POST   | Get Calculated est. Workstation Capacity | `/game/{id}/workstation-capacity/{period}/calulate` |
|                        | PATCH  | Change Production                        | `/game/{id}/workstation-capacity/{period}`          |
| `Simulation Input`     | GET    | Get Simulation Input                     | `/game/{id}/simulation-input/{period}`              |

---

## 🧭 **Or use a visual like this:**

```
📚 /book
  ├── GET      → List all books
  ├── POST     → Create book
  └── /{id}
      ├── GET  → Retrieve one
      ├── PUT  → Update
      └── DELETE → Delete

👤 /author
  ├── GET      → List all authors
  ├── POST     → Create author
  └── /{id}
      ├── GET  → Retrieve one
      └── DELETE → Delete
```

Super intuitive, no clutter, and easy to extend.

---

Want me to generate this kind of map for your simulation API (`/production`, `/order`, `/material`, etc.)? Just drop the
endpoints and I’ll format them like above.