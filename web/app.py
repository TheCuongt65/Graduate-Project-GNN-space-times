import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import plotly.express as px
import streamlit as st
from util import get_index_pairs, get_json_data, smaller_than
import time

#2018

n_points = 184


st.set_page_config(layout="wide")
st.title('Heatmap of China')
number = st.number_input("Nhập kịch bản thử nghiệm (1 ,2 hoặc 3): ", placeholder="Nhập một số", step=1, value=1)



if number == 1:
    predict_result = np.load('data_web/predict.npy')
    predict_result = predict_result.reshape(2880, 25, 184)
elif number == 2:
    predict_result = np.load('data_web/predict2.npy')
    predict_result = predict_result.reshape(predict_result.shape[0], 25, 184)
else:
    predict_result = np.load('data_web/predict3.npy')
    predict_result = predict_result.reshape(predict_result.shape[0], 25, 184)
############
json_data = get_json_data()

hanoi_data = {
    'Index': [item['Index'] for item in json_data],
    'Tram': [item['Tram'] for item in json_data],
    'Latitude': [float(item['Latitude']) for item in json_data],
    'Longitude': [float(item['Longitude']) for item in json_data],
    'PM2.5': predict_result[0, 0],
    'BaoDong': smaller_than(predict_result[0, 0] / 75)
}

hanoi_df = pd.DataFrame(hanoi_data)
print(hanoi_df)

unique_tram_names = hanoi_df['Tram'].unique().tolist()
unique_tram_names.insert(0, None)

home_name = st.selectbox("Lựa chọn trạm quan sát: ", unique_tram_names)
if home_name is not None:
    lat_home = float(hanoi_df[hanoi_df['Tram'] == home_name]['Latitude'])
    lon_home = float(hanoi_df[hanoi_df['Tram'] == home_name]['Longitude'])
print("Load xong Thông tin về trạm")

############

if number == 1:
    label = np.load('data_web/label.npy')
    label = predict_result.reshape(2880, 25, 184)
elif number == 2:
    label = np.load('data_web/label2.npy')
    label = predict_result.reshape(predict_result.shape[0], 25, 184)
else:
    label = np.load('data_web/label3.npy')
    label = predict_result.reshape(predict_result.shape[0], 25, 184)

json_data = get_json_data()

hanoi_data_label = {
    'Index': [item['Index'] for item in json_data],
    'Tram': [item['Tram'] for item in json_data],
    'Latitude': [float(item['Latitude']) for item in json_data],
    'Longitude': [float(item['Longitude']) for item in json_data],
    'PM2.5': label[0, 0],
    'BaoDong': smaller_than(label[0, 0] / 75)
}

hanoi_label_df = pd.DataFrame(hanoi_data_label)

print("Load xong Thông tin về trạm label")

###############################

def create_map(df):
    # Create a scatter mapbox with plotly
    if home_name is not None:
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="BaoDong", size="PM2.5",
                                color_continuous_scale=px.colors.sequential.Plasma[::-1], size_max=20, zoom=4.7,
                                mapbox_style="carto-positron", range_color=(0, 1), center=dict(lat=lat_home, lon=lon_home))
    else:
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="BaoDong", size="PM2.5",
                                color_continuous_scale=px.colors.sequential.Plasma[::-1], size_max=20, zoom=4.7,
                                mapbox_style="carto-positron", range_color=(0, 1))

    return fig

def app():
    st.title('Heatmap of China')
    start_time = datetime(2018, 1, 1)
    j = 0
    date_placehoder = st.empty()
    text_placeholder = st.empty()
    map_placeholder = st.empty()

    date_placehoder_label = st.empty()
    text_placeholder_label = st.empty()
    map_placeholder_label = st.empty()

    col1, col2 = st.columns(2)
    for i in range(25):
        print(f"Update {i} !!!")
        hanoi_df['PM2.5'] = predict_result[j, i]
        hanoi_df['BaoDong'] = smaller_than(predict_result[j, i] / 75)

        hanoi_label_df['PM2.5'] = label[j, i]
        hanoi_label_df['BaoDong'] = smaller_than(label[j, i] / 75)

        # Create map
        my_map = create_map(hanoi_df)
        my_map_label = create_map(hanoi_label_df)
        print("Tạo xong bản đồ !!!")
        with col1:
            with map_placeholder.container():
                date_placehoder.write(f'{start_time}')
                text_placeholder.write(f'(Dự báo) Trạng thái thứ {i}')
                map_placeholder.plotly_chart(my_map)

        with col2:
            with map_placeholder_label.container():
                date_placehoder_label.write(f'{start_time}')
                text_placeholder_label.write(f'(Thực tế) Trạng thái thứ {i}')
                map_placeholder_label.plotly_chart(my_map_label)

        start_time = start_time + timedelta(hours=1)
        # Wait for 10 seconds
        time.sleep(3)

def app2():
    st.title('Heatmap of China')
    start_time = datetime(2018, 1, 1)
    j = 0
    map_placeholder = st.empty()
    col1, col2 = st.columns(2)
    for i in range(25):
        print(f"Update {i} !!!")
        hanoi_df['PM2.5'] = predict_result[j, i]
        hanoi_df['BaoDong'] = smaller_than(predict_result[j, i] / 75)

        hanoi_label_df['PM2.5'] = label[j, i]
        hanoi_label_df['BaoDong'] = smaller_than(label[j, i] / 75)

        # Create map
        my_map = create_map(hanoi_df)
        my_map_label = create_map(hanoi_label_df)
        print("Tạo xong bản đồ !!!")
        with map_placeholder.container():
            with col1:
                st.write(f'{start_time}')
                st.write(f'(Dự báo) Trạng thái thứ {i}')
                st.plotly_chart(my_map)

            with col2:
                st.write(f'{start_time}')
                st.write(f'(Thực tế) Trạng thái thứ {i}')
                st.plotly_chart(my_map_label)

        start_time = start_time + timedelta(hours=1)
        # Wait for 10 seconds
        time.sleep(3)

def app3():
    start_time = datetime(2018, 1, 1)
    j = 0

    col1, col2 = st.columns(2)

    # Tạo các widget trống
    date_placeholder = col1.empty()
    text_placeholder = col1.empty()
    map_placeholder = col1.empty()

    date_placeholder_label = col2.empty()
    text_placeholder_label = col2.empty()
    map_placeholder_label = col2.empty()

    for i in range(25):
        print(f"Update {i} !!!")
        hanoi_df['PM2.5'] = predict_result[j, i]
        hanoi_df['BaoDong'] = smaller_than(predict_result[j, i] / 75)

        hanoi_label_df['PM2.5'] = label[j, i]
        hanoi_label_df['BaoDong'] = smaller_than(label[j, i] / 75)

        # Create map
        my_map = create_map(hanoi_df)
        my_map_label = create_map(hanoi_label_df)
        print("Tạo xong bản đồ !!!")

        # Cập nhật các widget
        date_placeholder.write(f'{start_time}')
        text_placeholder.write(f'(Dự báo) Trạng thái thứ {i}')
        map_placeholder.plotly_chart(my_map)

        date_placeholder_label.write(f'{start_time}')
        text_placeholder_label.write(f'(Thực tế) Trạng thái thứ {i}')
        map_placeholder_label.plotly_chart(my_map_label)

        start_time = start_time + timedelta(hours=1)
        # Wait for 10 seconds
        time.sleep(3)


if __name__ == '__main__':
    app3()
