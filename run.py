from app import  app
import os

app.run(
    port=os.environ['DOOFLASK_PORT'],
    host=os.environ['DOOFLASK_HOST']
)