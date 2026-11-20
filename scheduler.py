from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int


def load_processes(filename: str) -> List[Process]:
    processes: List[Process] = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                pid, arrival, burst = parts[0], int(parts[1]), int(parts[2])
                processes.append(Process(pid=pid, arrival=arrival, burst=burst))
    return processes


def fcfs_schedule(processes: List[Process]) -> List[Tuple[str, int, int, int, int, int, int]]:
    # Returns tuples of (pid, arrival, burst, start, completion, turnaround, waiting)
    ordered = sorted(processes, key=lambda p: (p.arrival, p.pid))
    current_time = 0
    results = []

    for p in ordered:
        start = max(current_time, p.arrival)
        completion = start + p.burst
        turnaround = completion - p.arrival
        waiting = start - p.arrival
        current_time = completion
        results.append((p.pid, p.arrival, p.burst, start, completion, turnaround, waiting))

    return results


def srtf_schedule(processes: List[Process]) -> List[Tuple[str, int, int, int, int, int, int]]:
    # Preemptive Shortest Remaining Time First
    remaining = {p.pid: p.burst for p in processes}
    arrival_map = {p.pid: p.arrival for p in processes}
    start_map = {}
    completion_map = {}

    completed = 0
    n = len(processes)
    t = 0

    while completed < n:
        ready = [
            p.pid
            for p in processes
            if p.arrival <= t and remaining[p.pid] > 0
        ]

        if not ready:
            t += 1
            continue

        current_pid = min(ready, key=lambda pid: (remaining[pid], arrival_map[pid], pid))
        if current_pid not in start_map:
            start_map[current_pid] = t

        remaining[current_pid] -= 1
        t += 1

        if remaining[current_pid] == 0:
            completion_map[current_pid] = t
            completed += 1

    results = []
    for p in sorted(processes, key=lambda x: (x.arrival, x.pid)):
        comp = completion_map[p.pid]
        tat = comp - p.arrival
        wt = tat - p.burst
        results.append((p.pid, p.arrival, p.burst, start_map[p.pid], comp, tat, wt))

    return results


def print_table(title: str, rows: List[Tuple[str, int, int, int, int, int, int]]) -> None:
    print(f"\n=== {title} ===")
    print(f"{'PID':<6} {'Arr':<5} {'Burst':<6} {'Start':<6} {'Comp':<6} {'TAT':<6} {'WT':<6}")
    print("-" * 48)
    total_tat = 0
    total_wt = 0
    for pid, arr, burst, start, comp, tat, wt in rows:
        total_tat += tat
        total_wt += wt
        print(f"{pid:<6} {arr:<5} {burst:<6} {start:<6} {comp:<6} {tat:<6} {wt:<6}")
    count = len(rows) if rows else 1
    print("-" * 48)
    print(f"Average Turnaround Time: {total_tat / count:.2f}")
    print(f"Average Waiting Time:    {total_wt / count:.2f}")


def main() -> None:
    processes = load_processes("input.txt")
    if not processes:
        print("No processes found in input.txt.")
        return

    fcfs_rows = fcfs_schedule(processes)
    srtf_rows = srtf_schedule(processes)

    print_table("FCFS (First-Come, First-Served)", fcfs_rows)
    print_table("SRTF (Shortest Remaining Time First)", srtf_rows)


if __name__ == "__main__":
    main()
