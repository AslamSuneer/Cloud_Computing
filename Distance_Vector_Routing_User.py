# Distance Vector Routing with User Input

INFINITY = 999

# Step 1: Take user input for nodes
N = int(input("Enter number of nodes: "))
NODES = []
for i in range(N):
    node = input(f"Enter name of node {i+1}: ")
    NODES.append(node)

# Step 2: Take user input for adjacency matrix
print("\nEnter adjacency matrix (use 999 for infinity):")
graph = {}
for i in range(N):
    graph[NODES[i]] = {}
    row = input(f"Enter costs from {NODES[i]} to all nodes (space separated): ").split()
    for j in range(N):
        graph[NODES[i]][NODES[j]] = int(row[j])

# Step 3: Initialize the routing tables
routing_tables = {}
for node in NODES:
    routing_tables[node] = {}
    for dest in NODES:
        cost = graph[node][dest]
        routing_tables[node][dest] = {
            'cost': cost,
            'next_hop': dest if cost != INFINITY and node != dest else None
        }

# Distance Vector Algorithm
def distance_vector():
    updated = True
    iteration = 1
    while updated:
        print(f"\n=== Iteration {iteration} ===")
        updated = False
        for node in NODES:
            for neighbor in NODES:
                if node == neighbor or graph[node][neighbor] == INFINITY:
                    continue
                for dest in NODES:
                    new_distance = routing_tables[node][neighbor]['cost'] + routing_tables[neighbor][dest]['cost']
                    if new_distance < routing_tables[node][dest]['cost']:
                        routing_tables[node][dest]['cost'] = new_distance
                        routing_tables[node][dest]['next_hop'] = neighbor
                        updated = True
            # Display routing table after processing each node
            print(f"\nRouting table for node {node}:")
            print("Destination | Cost | Next Hop")
            for dest in NODES:
                cost = routing_tables[node][dest]['cost']
                next_hop = routing_tables[node][dest]['next_hop']
                print(f"     {dest}      |  {cost:<4} |   {next_hop}")
        iteration += 1

# Display initial routing tables
print("\n=== Initial Routing Tables ===")
for node in NODES:
    print(f"\nRouting table for node {node}:")
    print("Destination | Cost | Next Hop")
    for dest in NODES:
        cost = routing_tables[node][dest]['cost']
        next_hop = routing_tables[node][dest]['next_hop']
        print(f"     {dest}      |  {cost:<4} |   {next_hop}")

# Run the distance vector algorithm
distance_vector()

# Display final routing tables
print("\n=== Final Routing Tables after Distance Vector Routing ===")
for node in NODES:
    print(f"\nRouting table for node {node}:")
    print("Destination | Cost | Next Hop")
    for dest in NODES:
        cost = routing_tables[node][dest]['cost']
        next_hop = routing_tables[node][dest]['next_hop']
        print(f"     {dest}      |  {cost:<4} |   {next_hop}")



------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#INPUT:
Enter number of nodes: 4
Enter name of node 1: A
Enter name of node 2: B
Enter name of node 3: C
Enter name of node 4: D

Enter adjacency matrix (use 999 for infinity):
Enter costs from A to all nodes (space separated): 0 2 999 1
Enter costs from B to all nodes (space separated): 2 0 3 7
Enter costs from C to all nodes (space separated): 999 3 0 11
Enter costs from D to all nodes (space separated): 1 7 11 0
