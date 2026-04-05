import tkinter as tk
import heapq

# -------------------------------
# Graph (Road Network)
# -------------------------------
graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'D': 5, 'E': 10},
    'C': {'A': 2, 'F': 3},
    'D': {'B': 5},
    'E': {'B': 10, 'F': 4, 'G': 3},
    'F': {'C': 3, 'E': 4, 'G': 6},
    'G': {}  # Hospital
}

# -------------------------------
# Heuristic Values
# -------------------------------
heuristic = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 7,
    'E': 3,
    'F': 6,
    'G': 0
}

# -------------------------------
# A* Algorithm
# -------------------------------
def a_star(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))

    g_cost = {node: float('inf') for node in graph}
    g_cost[start] = 0

    parent = {start: None}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1], g_cost[goal]

        for neighbor in graph[current]:
            tentative_g = g_cost[current] + graph[current][neighbor]

            if tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_cost = tentative_g + heuristic[neighbor]
                heapq.heappush(open_list, (f_cost, neighbor))
                parent[neighbor] = current

    return None, float('inf')

# -------------------------------
# GUI Setup
# -------------------------------
window = tk.Tk()
window.title("🚑Emergency Route For Ambulance ")
window.geometry("600x500")

# Canvas for drawing graph
canvas = tk.Canvas(window, width=600, height=350, bg="white")
canvas.pack()

# Node positions
positions = {
    'A': (100, 150),
    'B': (200, 50),
    'C': (200, 250),
    'D': (350, 50),
    'E': (350, 150),
    'F': (350, 250),
    'G': (500, 150)
}

# Draw edges
for node in graph:
    for neighbor in graph[node]:
        x1, y1 = positions[node]
        x2, y2 = positions[neighbor]
        canvas.create_line(x1, y1, x2, y2)

# Draw nodes
node_circles = {}
for node, (x, y) in positions.items():
    circle = canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
    canvas.create_text(x, y, text=node)
    node_circles[node] = circle

# -------------------------------
# Find Route Function
# -------------------------------
def find_route():
    start = entry.get().upper()
    goal = 'G'

    # Reset colors
    for node in node_circles:
        canvas.itemconfig(node_circles[node], fill="lightblue")

    path, cost = a_star(start, goal)

    if path:
        for node in path:
            canvas.itemconfig(node_circles[node], fill="green")

        result_label.config(
            text=f"Route: {' -> '.join(path)} | Time: {cost}"
        )
    else:
        result_label.config(text="No route found!")

# -------------------------------
# UI Elements
# -------------------------------
tk.Label(window, text="Enter Start Location (A-G):").pack()

entry = tk.Entry(window)
entry.pack()

tk.Button(window, text="Find Fastest Route", command=find_route).pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack()

# Run GUI
window.mainloop()