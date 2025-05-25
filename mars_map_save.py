import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_data():
    struct_category = pd.read_csv('area_category.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_map = pd.read_csv('area_map.csv')

    
    area_struct = area_struct[area_struct['category'] != 0]

   
    merged = pd.merge(area_struct, struct_category, on='category')

   
    merged_all = pd.merge(area_map, merged, on=['x', 'y'], how='left')
    return merged_all


def draw_mars_map(data):
    max_x = data['x'].max() + 1
    max_y = data['y'].max() + 1

    fig, ax = plt.subplots(figsize=(10, 10))


    for x in range(1, max_x + 1):
        ax.axvline(x=x - 0.5, color='lightgray', linewidth=1)
    for y in range(1, max_y + 1):
        ax.axhline(y=y - 0.5, color='lightgray', linewidth=1)


    for _, row in data.dropna(subset=['struct']).iterrows():
        pos = (row['x'], row['y'])
        category = row['struct']

        if category == 'radder':
            circle = plt.Circle((pos[0], pos[1]), 0.5, color='brown')
            ax.add_patch(circle)
        elif category in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            triangle = patches.RegularPolygon(
                (pos[0], pos[1]),
                numVertices=3,
                radius=0.5,
                orientation=0,
                color='green'
            )
            ax.add_patch(triangle)
        else:
            square = patches.Rectangle(
                (pos[0] - 0.4, pos[1] - 0.4),
                0.8, 0.8,
                color='gray'
            )
            ax.add_patch(square)

    ax.set_xlim(0.5, max_x - 0.5)
    ax.set_ylim(0.5, max_y - 0.5)
    ax.set_aspect('equal')
    ax.set_xticks(range(1, max_x))
    ax.set_yticks(range(1, max_y))
    ax.invert_yaxis()


    plt.savefig('mars_map.png')
    plt.close()


if __name__ == '__main__':
    merged_data = load_data()
    draw_mars_map(merged_data)