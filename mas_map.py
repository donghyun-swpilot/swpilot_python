import pandas as pd


def print_csv_files():
    struct_category = pd.read_csv('area_category.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_map = pd.read_csv('area_map.csv')

    print(struct_category)
    print(area_struct)
    print(area_map)


def summarize_data():
    struct_category = pd.read_csv('area_category.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_map = pd.read_csv('area_map.csv')

    merged = pd.merge(area_struct, struct_category, on='category')
    merged_all = pd.merge(area_map, merged, on=['x', 'y'])
    final_data = merged_all.drop('category', axis=1)

    print(final_data)


def filter_area_one():
    df = pd.read_csv('area_struct.csv')
    area_one = df[df['area'] == 1]

    print(area_one)



print_csv_files()
summarize_data()
filter_area_one()


