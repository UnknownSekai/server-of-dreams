# server-of-dreams
A certain EOSing mobile theatre idol rhythm game's private server implementation.

began development 2026/07/17 will take a while

## Layout

```
app.py            FastAPI app - includes every router
models/           Pydantic request/response models (enums.py, entities.py)
routes/           one APIRouter per controller (203 routes, 32 controllers)
mitm_wds.py       standalone mitmproxy addon to decode game traffic
CLIENT_REVERSED/  the reversed game client (routes/models/crypto reference)
```

## Run

```bash
pip install -r requirements.txt
python main.py
```