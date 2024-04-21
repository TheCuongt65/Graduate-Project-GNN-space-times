import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import folium
import streamlit as st
from streamlit_folium import folium_static
from util import get_index_pairs, get_json_data
import time

np.random.seed(42)
n_points = 184
start_time = datetime.now() - timedelta(hours=n_points)

json_data = get_json_data()

hanoi_data = {
    # 'Time': [start_time + timedelta(hours=i) for i in range(n_points)] * 10,
    'Index': [item['Index'] for item in json_data],
    'Tram': [item['Tram'] for item in json_data],
    'Latitude': [float(item['Latitude']) for item in json_data],
    'Longitude': [float(item['Longitude']) for item in json_data],
    'PM2.5': np.random.uniform(0, 50, 184),
    'BaoDong': np.random.choice([0, 0], 184)
}

hanoi_df = pd.DataFrame(hanoi_data)

print("Load xong Thông tin về trạm")

def create_map(df):
    # Tạo bản đồ với vị trí trung bình của Hà Nội
    map_center = [hanoi_df['Latitude'].mean(), hanoi_df['Longitude'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=10)

    # Thêm marker cho từng trạm
    for index, row in hanoi_df.iterrows():
        # Tùy chỉnh màu sắc dựa trên thông báo báo động
        color = 'red' if row['BaoDong'] == 1 else 'green'
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Tram']} - PM2.5: {row['PM2.5']:.2f} µg/m³",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(my_map)

    # Danh sách các cặp trạm cần nối
    pairs = sorted(list(get_index_pairs()))

    # Thêm đường nối giữa các cặp trạm
    for pair in pairs:
        tram1 = hanoi_df[hanoi_df['Index'] == str(pair[0])].iloc[0]
        tram2 = hanoi_df[hanoi_df['Index'] == str(pair[1])].iloc[0]
        folium.PolyLine(
            locations=[[tram1['Latitude'], tram1['Longitude']], [tram2['Latitude'], tram2['Longitude']]],
            color='blue'
        ).add_to(my_map)

    return my_map


def app():
    st.title('Heatmap of Hanoi')
    while True:
        print("Update !!!")
        # Update data
        hanoi_df['PM2.5'] = np.random.uniform(0, 50, 184)
        hanoi_df['BaoDong'] = np.random.choice([0, 1], 184)

        # Create map
        my_map = create_map(hanoi_df)
        print("Tạo xong bản đồ !!!")

        # Display map
        folium_static(my_map)

        # Wait for 10 seconds
        time.sleep(10)

def app2():
    st.title('Heatmap of Hanoi')
    print("Update !!!")
    # Create map
    my_map = create_map(hanoi_df)
    print("Tạo xong bản đồ !!!")

    # Display map
    folium_static(my_map)

    if st.button('Update'):
        hanoi_df['PM2.5'] = np.random.uniform(0, 50, 184)
        hanoi_df['BaoDong'] = np.random.choice([0, 1], 184)


if __name__ == '__main__':
    app2()