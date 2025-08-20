import os
import time
import shutil
from typing import Dict, List

DEFAULT_DISKS = 5
FRAME_DELAY   = 0.25
USE_CLEAR     = True

Peg = str
Towers = Dict[Peg, List[int]]

def clear_screen():
    if not USE_CLEAR:
        print("\n" * 4)
        return
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        print("\n" * 10)

def center_text(s: str, width: int) -> str:
    pad_total = max(0, width - len(s))
    left = pad_total // 2
    right = pad_total - left
    return " " * left + s + " " * right

def render_towers(towers: Towers, n: int, move_info: str = "", move_count: int = 0):
    term_width = shutil.get_terminal_size((80, 24)).columns
    peg_width = 2 * n - 1
    gap = 4
    columns: Dict[Peg, List[str]] = {}
    for peg in ("A", "B", "C"):
        stack = towers[peg]
        rows: List[str] = []
        padded = [None] * (n - len(stack)) + stack[:]
        for disk in padded:
            if disk is None:
                rows.append(center_text("|", peg_width))
            else:
                disk_width = 2 * disk - 1
                rows.append(center_text("=" * disk_width, peg_width))
        base = "-" * peg_width
        name = center_text(peg, peg_width)
        columns[peg] = rows + [base, name]
    total_rows = n + 2
    lines: List[str] = []
    for r in range(total_rows):
        line = columns["A"][r] + (" " * gap) + columns["B"][r] + (" " * gap) + columns["C"][r]
        lines.append(line)
    title = f"Tower of Hanoi — n={n}    Moves: {move_count}"
    if move_info:
        title += f"    Last move: {move_info}"
    title_line = title[:term_width]
    clear_screen()
    print(title_line)
    print("=" * min(term_width, max(20, len(title_line))))
    print("\n".join(lines))
    time.sleep(FRAME_DELAY)

def move_disk(towers: Towers, src: Peg, dst: Peg):
    disk = towers[src].pop()
    towers[dst].append(disk)
    return disk

def hanoi(n: int, src: Peg, aux: Peg, dst: Peg, towers: Towers, move_counter: List[int]):
    if n == 0:
        return
    hanoi(n - 1, src, dst, aux, towers, move_counter)
    disk = move_disk(towers, src, dst)
    move_counter[0] += 1
    render_towers(towers, total_disks, move_info=f"{src} → {dst} (disk {disk})", move_count=move_counter[0])
    hanoi(n - 1, aux, src, dst, towers, move_counter)

def validate(n: int):
    if n < 1:
        raise ValueError("Number of disks must be at least 1.")
    if n > 12:
        print("Note: Large n produces many moves and can overwhelm the terminal. Proceeding anyway...")

if __name__ == "__main__":
    try:
        user = input(f"Enter number of disks [default {DEFAULT_DISKS}]: ").strip()
        total_disks = int(user) if user else DEFAULT_DISKS
    except Exception:
        total_disks = DEFAULT_DISKS
    validate(total_disks)
    towers: Towers = {"A": list(range(total_disks, 0, -1)), "B": [], "C": []}
    render_towers(towers, total_disks, move_info="Start", move_count=0)
    counter = [0]
    start = time.time()
    hanoi(total_disks, "A", "B", "C", towers, counter)
    end = time.time()
    clear_screen()
    render_towers(towers, total_disks, move_info="Completed", move_count=counter[0])
    print(f"Solved in {counter[0]} moves. Optimal moves = 2^n - 1 = {2**total_disks - 1}")
    print(f"Time elapsed: {end - start:.2f} s")
