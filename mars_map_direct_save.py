import pandas as pd
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_map():
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_category = pd.read_csv('area_category.csv')

    # 암석 위치 추출
    area_struct = area_struct[area_struct['category'] != 0]
    merged = pd.merge(area_struct, area_category, on='category')
    rocks = merged[merged['struct'] == 'radder'][['x', 'y']]

    # 기지 위치 추출
    home_base = merged[merged['struct'] == 'Korea Mars Base'][['x', 'y']].values[0]
    us_base = merged[merged['struct'] == 'U.S. Mars Base Camp'][['x', 'y']].values[0]

    return area_map, set(map(tuple, rocks.values)), tuple(home_base), tuple(us_base), merged


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

        x, y = current
        neighbors = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ]

        for nx, ny in neighbors:
            if (1 <= nx <= width and 1 <= ny <= height and
                    (nx, ny) not in rocks and (nx, ny) not in visited):
                heapq.heappush(heap, (cost + 1, (nx, ny), path))

    return []  # 경로 없음


def save_path_to_csv(path):
    df = pd.DataFrame(path, columns=['x', 'y'])
    df.to_csv('home_to_us_camp.csv', index=False)


def draw_path_map(area_map, merged, rocks, path):
    max_x = area_map['x'].max() + 1
    max_y = area_map['y'].max() + 1

    fig, ax = plt.subplots(figsize=(10, 10))

    # 격자 라인
    for x in range(1, max_x + 1):
        ax.axvline(x=x - 0.5, color='lightgray', linewidth=1)
    for y in range(1, max_y + 1):
        ax.axhline(y=y - 0.5, color='lightgray', linewidth=1)

    # 구조물
    for _, row in merged.iterrows():
        pos = (row['x'], row['y'])
        category = row['struct']

        if category == 'radder':
            circle = plt.Circle(pos, 0.4, color='brown')
            ax.add_patch(circle)
        elif category in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            triangle = patches.RegularPolygon(
                xy=pos,
                numVertices=3,
                radius=0.5,
                orientation=0,
                facecolor='green'
            )
            ax.add_patch(triangle)
        else:
            square = patches.Rectangle((pos[0] - 0.4, pos[1] - 0.4), 0.8, 0.8, color='gray')
            ax.add_patch(square)

    # 경로 표시
    if path:
        x_vals, y_vals = zip(*path)
        ax.plot(x_vals, y_vals, color='blue', linewidth=2, marker='o', markersize=4)

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
