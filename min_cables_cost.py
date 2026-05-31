import heapq 

def min_cost_cable_connect(cables: list[int]) -> tuple[int, list[tuple]]:
    """
    Connects cable with minimum total cost using a min-heap
    Args: 
        cables: list of cable lengths
    Return:
        tuple of (total_cost, steps)
    """
    if len(cables) <= 1:
        return 0, []
    
    heap = cables[:]
    heapq.heapify(heap) 
    total_cost = 0
    steps = []

    while len(heap) > 1:
        cable1 = heapq.heappop(heap)
        cable2 = heapq.heappop(heap)
        cost = cable1 + cable2 
        total_cost += cost
        steps.append((cable1, cable2, cost))

        heapq.heappush(heap, cost) # Marged cable goes back into the heap

    return total_cost, steps


def run_demo() -> None:
    print("\n", "#" * 10, " Cable Connections Minimum Cost Demo ", "#" * 10, "\n")
    cables = [9, 12, 4, 5, 13, 12]
    total, steps = min_cost_cable_connect(cables)

    print(f"Cables: \"{cables}\"")
    print("\n", f"Connection order:")
    for i, (cable1, cable2, combined) in enumerate(steps, 1):
        print(f"    Step {i:<2}: Connect {cable1:^4} + {cable2:^4} = {combined:^8} (cost: {combined})")
    print("\n", f"Total cost: {total}")


if __name__ == "__main__":
    run_demo()