import uvicorn

# Important: Do not remove import
# Some IDEs show this import as unused!
# (from translator import app)
from translator import app

if __name__ == '__main__':
    # not productive, only if run with python main.py
    # (Dockerfile use uvicorn directly)

    print(app.version)
    uvicorn.run("minecraft-cloud:app", host='0.0.0.0', port=8080, reload=True, reload_dirs="./minecraft-cloud")
