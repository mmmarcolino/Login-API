from login_api.run import get_app

import uvicorn

app = get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

