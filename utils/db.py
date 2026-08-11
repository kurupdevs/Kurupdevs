"""Database utils."""
import json,threading
from pathlib import Path

DD=Path("data");DD.mkdir(exist_ok=True)
_lock=threading.Lock()

def _load(p):
 if not p.exists():return{}
 try:
  with open(p)as f:return json.load(f)
 except:return{}

def _save(p,d):
 try:
  t=p.with_suffix(".tmp")
  with open(t,"w")as f:json.dump(d,f,indent=2)
  t.rename(p);return True
 except:return False

def get(col,key,default=None):
 with _lock:
  p=DD/f"{col}.json";d=_load(p);return d.get(key,default)

def setv(col,key,val):
 with _lock:
  p=DD/f"{col}.json";d=_load(p);d[key]=val;return _save(p,d)

def remove(col,key):
 with _lock:
  p=DD/f"{col}.json";d=_load(p);d.pop(key,None);return _save(p,d)
