from fastapi import FastAPI
from fastapi_healthcheck import HealthCheckFactory, healthCheckRoute
from fastapi_healthcheck_uri import HealthCheckUri
from workerApi.routes import SchedulerRouter, RedditRouter
from .apiEventsService import ApiEventsService


app = FastAPI(
    title="NewsBot Worker",
    description="The backend agent to collect articles and send notifications.",
    version="0.9.0"
)

app.include_router(SchedulerRouter)
app.include_router(RedditRouter)

_health = HealthCheckFactory()
_health.add(HealthCheckUri(connectionUri='https://reddit.com/r/aww.json', alias='reddit', tags=('reddit', "uri")))
app.add_api_route('/health', endpoint=healthCheckRoute(_health))

@app.on_event('startup')
def startupEvent() -> None:
    ApiEventsService().startup()
    pass

@app.on_event('shutdown')
def shutdownEvent() -> None:
    ApiEventsService().shutdown()
