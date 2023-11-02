# this doesn't work quite yet
load("ext://dotenv", "dotenv")

dotenv()

secret_settings(disable_scrub=True)

docker_compose(
    "./docker-compose.yaml",
    env_file=".env",
)

other_components = ["redis", "postgres"]

for component in other_components:
    dc_resource(component, labels=["infrastructure"])

dc_resource(
    "api-init",
    labels=["api-init"],
    resource_deps=other_components,
    trigger_mode=TRIGGER_MODE_MANUAL
)

core_components = ["api"]
for component in core_components:
    dc_resource(
        component,
        labels=["api"],
        resource_deps=["api-init"]+other_components
    )
