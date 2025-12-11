# app/cli/utils.py
import asyncio
from functools import partial
import aiohttp
import sys

# ---- async input helper ----
async def async_input(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(input, prompt))

# ---- wait for service to be ready ----
async def wait_for_service(url: str, name: str, retries: int = 6, timeout: int = 2):
    for i in range(retries):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, timeout=aiohttp.ClientTimeout(total=3)) as r:
                    if r.status == 200:
                        print(f"✅ {name} is online.")
                        return True
        except Exception:
            pass
        print(f"⏳ Waiting for {name} to be ready... ({i+1}/{retries})")
        await asyncio.sleep(timeout)
    print(f"❌ {name} not reachable. Exiting.")
    sys.exit(1)

# ---- pretty board printer (option 2: show ships, hits, misses) ----
def print_board(grid):
    """
    grid: list[list[str]] using Board.grid conventions:
      "~" water
      "O" ship
      "X" hit
      "M" miss
    We render:
      ~ -> ~
      O -> S (ship)
      X -> X (hit)
      M -> o (miss)
    """
    if not grid:
        print("(empty board)")
        return

    size = len(grid)
    header = "    " + " ".join(f"{i:2}" for i in range(size))
    print(header)
    for r_idx, row in enumerate(grid):
        rendered = []
        for cell in row:
            if cell == "~":
                rendered.append("~ ")
            elif cell == "O":
                rendered.append("S ")
            elif cell == "X":
                rendered.append("X ")
            elif cell == "M":
                rendered.append("o ")
            else:
                rendered.append(f"{cell} ")
        print(f"{r_idx:2}  " + " ".join(rendered))
    print()
