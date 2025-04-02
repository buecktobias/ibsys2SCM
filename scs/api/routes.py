from fastapi import FastAPI
from models import SimulationInput
from fastapi.openapi.utils import get_openapi

app = FastAPI()


@app.post("/simulate/")
def simulate_plan(input_data: SimulationInput):
    return {
            "message": "Simulation executed",
            "period": input_data.period,
            "produced_items": len(input_data.production_plans)
    }


# Custom OpenAPI schema generation (optional)
@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    return get_openapi(
            title="Bike Manufacturing Simulation API",
            version="1.0.0",
            description="API for running simulation and planning production",
            routes=app.routes,
    )


schema = get_openapi(
        title="Bike Manufacturing Simulation API",
        version="1.0.0",
        description="API for planning bike manufacturing simulation",
        routes=app.routes,
)

with open("openapi_schema.json", "w") as f:
    json.dump(schema, f, indent=2)
