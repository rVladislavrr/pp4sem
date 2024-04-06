import numpy as np
import pandas as pd
import sqlite3

if __name__ == '__main__':
    df = pd.read_json("../Subject_graph.json", orient='columns')
    nodes = df.nodes.dropna()
    edges = df.edges.dropna()


    def get_filtered_df(keys, graph_object):
        graph_object_new = []
        for data in graph_object:
            graph_object_new.append([(key, data.get(key)) for key in keys])

        columns_names = [x[0] for x in graph_object_new[0]]
        values_from_tuples = np.array([y for rows in graph_object_new for (x, y) in rows]) \
            .reshape(graph_object.shape[0], len(keys))

        return pd.DataFrame(values_from_tuples, columns=columns_names)


    edges_df = get_filtered_df(['id', 'from', 'to', 'label'], edges)
    nodes_df = get_filtered_df(['id', 'label'], nodes)
    nodes_df['id'] = nodes_df['id'].astype(int)
    edges_df['from'] = edges_df['from'].astype(int)
    edges_df['to'] = edges_df['to'].astype(int)
    nodes_df.label = nodes_df.label.str.replace('\n', '')
    nodes_df.rename(columns={'id': 'id', 'label': 'themes'}, inplace=True)

    conn = sqlite3.connect("../graph.db")

    edges_df[['from', 'to']].to_sql(name='links', con=conn, if_exists='replace')
    nodes_df.to_sql(name='themes', con=conn, if_exists='replace', index=False)