import pandas as pd
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def read_csv_file(filename):
    return pd.read_csv(filename)


def get_rocks_and_bases(area_struct, area_category):
    area_struct = area_struct[area_struct['category'] != 0]
    merged = pd.merge(area_struct, area_category, on='category')
    rocks = merged[merged['struct'] == 'radder'][['x', 'y']]
    home_base = merged[merged['struct'] == 'Korea Mars Base'][['x', 'y']].values[0]
    us_base = merged[merged['struct'] == 'U.S. Mars Base Camp'][['x', 'y']].values[0]
    return merged, set(map(tuple, rocks.values)), tuple(home_base), tuple(us_base)


def load_map():
    area_map = read_csv_file('area_map.csv')
    area_struct = read_csv_file('area_struct.csv')
    area_category = read_csv_file('area_category.csv')
    merged, rocks, home_base, us_base = get_rocks_and_bases(area_struct, area_category)
    return area_map, rocks, home_base, us_base, merged


def get_neighbors(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def dijkstra(area_map, rocks, start, goal):
    width = area_map['x'].max()
    height = area_map['y'].max()
    visited = set()
    heap = [(0, start, [])]

    while heap:
        cost, current, path = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]
        if current == goal:
            return path
        for neighbor in get_neighbors(*current):
            if (1 <= neighbor[0] <= width and 1 <= neighbor[1] <= height and
                    neighbor not in rocks and neighbor not in visited):
                heapq.heappush(heap, (cost + 1, neighbor, path))

    return []


def save_path_to_csv(path):
    pd.DataFrame(path, columns=['x', 'y']).to_csv('home_to_us_camp.csv', index=False)


def draw_grid(ax, max_x, max_y):
    for x in range(1, max_x + 1):
        ax.axvline(x=x - 0.5, color='lightgray', linewidth=1)
    for y in range(1, max_y + 1):
        ax.axhline(y=y - 0.5, color='lightgray', linewidth=1)


def draw_structures(ax, merged):
    for _, row in merged.iterrows():
        pos = (row['x'], row['y'])
        category = row['struct']
        if category == 'radder':
            ax.add_patch(plt.Circle(pos, 0.4, color='brown'))
        elif category in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            ax.add_patch(patches.RegularPolygon(xy=pos, numVertices=3, radius=0.5, orientation=0, facecolor='green'))
        else:
            ax.add_patch(patches.Rectangle((pos[0] - 0.4, pos[1] - 0.4), 0.8, 0.8, color='gray'))


def draw_path(ax, path):
    if path:
        x_vals, y_vals = zip(*path)
        ax.plot(x_vals, y_vals, color='blue', linewidth=2, marker='o', markersize=4)


def draw_path_map(area_map, merged, rocks, path):
    max_x = area_map['x'].max() + 1
    max_y = area_map['y'].max() + 1
    fig, ax = plt.subplots(figsize=(10, 10))
    draw_grid(ax, max_x, max_y)
    draw_structures(ax, merged)
    draw_path(ax, path)
    ax.set_xlim(0.5, max_x - 0.5)
    ax.set_ylim(0.5, max_y - 0.5)
    ax.set_aspect('equal')
    ax.set_xticks(range(1, max_x))
    ax.set_yticks(range(1, max_y))
    ax.invert_yaxis()
    plt.axis('off')
    plt.savefig('mars_path.png')
    plt.close()


if __name__ == '__main__':
    area_map, rocks, start, goal, merged = load_map()
    shortest_path = dijkstra(area_map, rocks, start, goal)
    save_path_to_csv(shortest_path)
    draw_path_map(area_map, merged, rocks, shortest_path)

