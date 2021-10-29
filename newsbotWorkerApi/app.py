from fastapi import FastAPI
from newsbotWorkerApi.routes import SchedulerRouter, RedditRouter
from newsbotWorkerApiService.api import ApiEventsService


app = FastAPI(
    title="NewsBot Worker",
    description="The backend agent to collect articles and send notifications.",
    version="0.9.0"
)

app.include_router(SchedulerRouter)
app.include_router(RedditRouter)

#@app.get('/health')
#def healthCheck() -> HealthModel:
#    hs = HealthService().check()
#    return hs.check

@app.on_event('startup')
def startupEvent() -> None:
    ApiEventsService().startup()
    pass

@app.on_event('shutdown')
def shutdownEvent() -> None:
    ApiEventsService().shutdown()
