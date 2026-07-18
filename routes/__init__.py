import importlib
import pkgutil

routers = []
for _m in pkgutil.iter_modules(__path__):
    _mod = importlib.import_module(f"{__name__}.{_m.name}")
    if hasattr(_mod, "router"):
        routers.append(_mod.router)
