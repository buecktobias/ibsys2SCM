import uvicorn
import yaml
from fastapi import Body, FastAPI, Path
from fastapi.openapi.utils import get_openapi

from scs.api.dto_models import (
    GameDTO,
    OrderDTO,
    PeriodResultDTO,
    PrimaryPlanDTO,
    ProductionDTO,
    SimulationInputDTO,
    WorkstationCapacityDTO,
)

app = FastAPI(
        title="Simulation Planning API",
        version="1.0.0",
        description="""
# 🚀 Simulation Planning API

This API supports simulation-based production planning. It allows you to:

- ✍️ Create and manage simulation runs
- 📅 Submit or calculate plans for a specific period
- 🔢 Retrieve production, orders, workstation capacity, and simulation results

## Key Concepts

- **Simulation Run**: A planning session identified by a unique `game_id`
- **Period**: Each simulation run consists of multiple periods
- **DTOs**: Request and response schemas used in planning, all versioned under v1
    """
)

api_prefix = "/api/v1"


# --- Game ---
@app.post(f"{api_prefix}/game/{{id}}", response_model=GameDTO, status_code=201, summary="Create Simulation Run")
def create_game(id: int = Path(description="Unique simulation run ID")):
    """Create a new simulation run (planning session)."""
    return GameDTO(id=id)


# --- Period Result ---
@app.get(
        f"{api_prefix}/game/{{id}}/period-result/{{period}}",
        response_model=PeriodResultDTO,
        summary="Get Period Result"
)
def get_period_result(id: int, period: int):
    """Retrieve the simulation result (XML) for a specific period."""
    pass


@app.put(f"{api_prefix}/game/{{id}}/period-result/{{period}}", status_code=204, summary="Save Period Result")
def update_period_result(
        id: int, period: int,
        data: PeriodResultDTO = Body(..., example={"game_id": 1, "period": 1, "xml_file": {"content": "<xml></xml>"}})):
    """Save or update the simulation result XML for a period."""
    pass


# --- Primary Plan ---
@app.get(f"{api_prefix}/game/{{id}}/primary-plan/{{period}}", response_model=PrimaryPlanDTO, summary="Get Primary Plan")
def get_primary_plan(id: int, period: int):
    """Retrieve the primary production plan for a period."""
    pass


@app.post(
        f"{api_prefix}/game/{{id}}/primary-plan/{{period}}/calculate",
        response_model=PrimaryPlanDTO,
        summary="Calculate Primary Plan"
)
def calculate_primary_plan(id: int, period: int):
    """Calculate a primary plan from simulation inputs."""
    pass


@app.patch(f"{api_prefix}/game/{{id}}/primary-plan/{{period}}", status_code=204, summary="Update Primary Plan")
def update_primary_plan(id: int, period: int, data: PrimaryPlanDTO = Body(...)):
    """Update the primary production plan manually."""
    pass


# --- Production ---
@app.get(f"{api_prefix}/game/{{id}}/production/{{period}}", response_model=ProductionDTO, summary="Get Production Plan")
def get_production(id: int, period: int):
    """Retrieve the production item configuration for a period."""
    pass


@app.post(
        f"{api_prefix}/game/{{id}}/production/{{period}}/calculate",
        response_model=ProductionDTO,
        summary="Calculate Production"
)
def calculate_production(id: int, period: int):
    """Calculate the recommended production setup."""
    pass


@app.patch(f"{api_prefix}/game/{{id}}/production/{{period}}", status_code=204, summary="Update Production")
def update_production(id: int, period: int, data: ProductionDTO = Body(...)):
    """Modify the production details for a period."""
    pass


# --- Order ---
@app.get(f"{api_prefix}/game/{{id}}/order/{{period}}", response_model=OrderDTO, summary="Get Orders")
def get_orders(id: int, period: int):
    """Get all order details for a period."""
    pass


@app.post(f"{api_prefix}/game/{{id}}/order/{{period}}/calculate", response_model=OrderDTO, summary="Calculate Orders")
def calculate_orders(id: int, period: int):
    """Automatically determine optimal ordering strategy."""
    pass


@app.patch(f"{api_prefix}/game/{{id}}/order/{{period}}", status_code=204, summary="Update Orders")
def update_orders(id: int, period: int, data: OrderDTO = Body(...)):
    """Update order decisions (e.g. quantity, mode)."""
    pass


# --- Workstation Capacity ---
@app.get(
        f"{api_prefix}/game/{{id}}/workstation-capacity/{{period}}",
        response_model=WorkstationCapacityDTO,
        summary="Get Workstation Capacity"
)
def get_workstation_capacity(id: int, period: int):
    """Get current shift and overtime settings per workstation."""
    pass


@app.post(
        f"{api_prefix}/game/{{id}}/workstation-capacity/{{period}}/calculate",
        response_model=WorkstationCapacityDTO,
        summary="Calculate Workstation Capacity"
)
def calculate_workstation_capacity(id: int, period: int):
    """Calculate workstation shifts and overtime needs based on plan."""
    pass


@app.patch(
        f"{api_prefix}/game/{{id}}/workstation-capacity/{{period}}",
        status_code=204,
        summary="Update Workstation Capacity"
)
def update_workstation_capacity(id: int, period: int, data: WorkstationCapacityDTO = Body(...)):
    """Modify existing shift/overtime plan manually."""
    pass


# --- Simulation Input ---
@app.get(
        f"{api_prefix}/game/{{id}}/simulation-input/{{period}}",
        response_model=SimulationInputDTO,
        summary="Get Simulation Input"
)
def get_simulation_input(id: int, period: int):
    """Retrieve XML simulation input for the specified period."""
    pass


if __name__ == '__main__':
    openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
    )

    with open("openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)

    uvicorn.run(
            "scs.api.routes:app",
            host="127.0.0.1",
            port=8000,
            reload=True
    )
