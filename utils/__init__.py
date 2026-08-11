"""KurupDevs utilities package."""
from .config import getc, setc
from .db import get, setv, remove
from .scripts import progress, safe_edit, safe_del, parse_args

__all__=["getc","setc","get","setv","remove","progress","safe_edit","safe_del","parse_args"]
