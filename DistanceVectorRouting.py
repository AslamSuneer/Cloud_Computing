import copy

INFINITY = 999
NODES = ['A', 'B', 'C', 'D']

initial_costs = {
    'A': {'A': 0, 'B': 2,   'C': INFINITY,   'D': 1},
    'B': {'A': 2, 'B': 0,   'C': 3,   'D': 7},
    'C': {'A': INFINITY, 'B': 3,   'C': 0,   'D': 11},
    'D': {'A': 1, 'B': 7, 'C': 11,   'D': 0}
}

# Initialize routing tables with next hop information
def initialize_routing_tables(costs):
    routing_tables = {}
    next_hops = {}
    
    for node in NODES:
        routing_tables[node] = {}
        next_hops[node] = {}
        for dest in NODES:
            routing_tables[node][dest] = costs[node][dest]
            if node == dest:
                next_hops[node][dest] = '-'  # No hop needed to reach self
            elif costs[node][dest] != INFINITY:
                next_hops[node][dest] = dest  # Direct connection
            else:
                next_hops[node][dest] = '-'   # No path known
    
    return routing_tables, next_hops

def print_routing_table(router, table, next_hops):
    print(f"\nRouting table for {router}:")
    print("Destination\tCost\tNext Hop")
    for dest in NODES:
        print(f"{dest}\t\t{table[router][dest]}\t{next_hops[router][dest]}")

def distance_vector_routing(costs):
    routing_tables, next_hops = initialize_routing_tables(costs)

    # Print initial routing tables
    print("\n---Initial Routing Tables---")
    for node in NODES:
        print_routing_table(node, routing_tables, next_hops)
    
    updated = True
    rounds = 0
    while updated:
        updated = False
        rounds += 1
        print(f"\n--- Round {rounds} ---")
        for node in NODES:
            for neighbor in NODES:
                if neighbor == node or costs[node][neighbor] == INFINITY:
                    continue
                for dest in NODES:
                    new_distance = costs[node][neighbor] + routing_tables[neighbor][dest]
                    if new_distance < routing_tables[node][dest]:
                        print(f"[Update] {node} to {dest} via {neighbor}: {routing_tables[node][dest]} -> {new_distance}")
                        routing_tables[node][dest] = new_distance
                        next_hops[node][dest] = neighbor  # Update next hop
                        updated = True

        # Print routing tables after each round
        print(f"\n--- Routing Tables after Round {rounds} ---")
        for node in NODES:
            print_routing_table(node, routing_tables, next_hops)

    print("\n--- Final Routing Tables ---")
    for node in NODES:
        print_routing_table(node, routing_tables, next_hops)
    print("Final Routing Table : ")
    for node in NODES:
        print(f"Node {node} : ")
        print(routing_tables[node])


if __name__ == "__main__":
    distance_vector_routing(initial_costs)
    
