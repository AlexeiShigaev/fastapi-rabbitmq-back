import uvicorn
from fastapi import FastAPI

from db import init_models
from processing import consumer_cor
from routes import router as gw_router
from processing import sender, consumer


def create_gateway():
    app = FastAPI(docs_url='/')
    app.include_router(gw_router)
    app.state.sender = sender
    app.state.consumer = consumer

    @app.get("/hello")
    async def root():
        return "Hello, I'm bookworm"

    @app.on_event('startup')
    async def startup_event():
        print('\tstartup')
        await init_models()
        await sender.start()
        await app.state.consumer.start()
        await app.state.consumer.set_consumer(consumer_cor)

    return app


def main():
    uvicorn.run(
        'main:create_gateway',
        host='0.0.0.0', port=8888,
        workers=4,
        reload=True
    )


if __name__ == '__main__':
    main()
