from Graph import Graph
from HazaData import HazeData
import numpy as np
import json
import pandas as pd
import yaml

def smaller_than(array):
  array[array >= 1] = 1
  return array

def get_index_pairs():
    hist_len = 1 #config['train']['hist_len']
    pred_len = 24 #config['train']['pred_len']
    dataset_num = 1
    graph = Graph()
    test_data = HazeData(graph, hist_len, pred_len, dataset_num, flag='Test')
    adj = test_data.graph.adj.numpy()
    indices = np.where(adj == 1)
    index_pairs = list(zip(*indices))
    index_pairs = set(tuple(sorted(pair)) for pair in index_pairs)
    return index_pairs

def get_json_data():
    with open('web/data_web/city.txt') as file:
        data = file.read()

    df = pd.DataFrame([line.split() for line in data.split('\n') if line],
                      columns=['Index', 'Tram', 'Longitude', 'Latitude'])
    json_data = df.to_json(orient='records')
    json_data = json.loads(json_data)
    return json_data
