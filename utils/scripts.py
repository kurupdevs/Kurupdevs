"""Script utilities."""
import logging
logger=logging.getLogger(__name__)

async def progress(cur,total,msg,action="Processing"):
 pct=cur*100/total;bar="█"*int(pct/5)+"░"*(20-int(pct/5))
 await msg.edit(f"**{action}:** [{bar}] {pct:.1f}%")
