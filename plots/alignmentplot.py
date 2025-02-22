
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import numpy as np
import scipy.spatial.distance as sd
from operations.alignment import calc_domainAveraged_FOSCTTM
from app_main.utilities import df_to_data
from app_main.constants import dataset_titles, marker_size, font_size


def plot_alignment(df_1, df_2, label_1, label_2, dataset, x, y, z):

    d_1 = df_to_data(df_1)
    d_2 = df_to_data(df_2)
    marker_size_3d = 1.25

    fig = go.Figure()
    fig.add_trace(go.Scatter3d(x=d_1[:, x], y=d_1[:, y], z=d_1[:, z],
                               mode='markers',
                               marker={'color': 'red', 'size': marker_size_3d},
                               name=label_1,
                               showlegend=True))
    fig.add_trace(go.Scatter3d(x=d_2[:, x], y=d_2[:, y], z=d_2[:, z],
                               mode='markers',
                               marker={'color': 'blue', 'size': marker_size_3d},
                               name=label_2,
                               showlegend=True))
    fig.update_layout(title_text=f'Dataset alignment in latent space: {dataset_titles.get(dataset, "Background job")}',
                      legend={'itemsizing': 'constant'})

    return fig


def plot_alignment_error(df_1, df_2, dataset):

    d_1 = df_to_data(df_1)
    d_2 = df_to_data(df_2)

    pairwise_distances = [sd.euclidean(d_1[i, :], d_2[i, :]) for i in range(d_1.shape[0])]
    foscttm = calc_domainAveraged_FOSCTTM(d_1, d_2)

    titles = (f'$\mu = {np.mean(pairwise_distances):.4f}$', f'$\mu = {np.mean(foscttm):.4f}$')

    fig = make_subplots(rows=1, cols=2,
                        column_titles=titles,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}]])

    # box plot of distances between corresponding cells in latent space
    fig.add_trace(go.Box(y=pairwise_distances, name='Pairwise cell distance', showlegend=False), row=1, col=1)

    # box plot of FOSCTTM scores (Fraction of Samples Closer Than True Match)
    fig.add_trace(go.Box(y=foscttm, name='FOSCTTM', showlegend=False), row=1, col=2)

    fig.update_layout(title_text=f'Dataset alignment in latent space: {dataset_titles.get(dataset, "Background job")}',
                      legend={'itemsizing': 'constant'})

    return fig


def plot_alignment_and_error(df_1, df_2, label_1, label_2, dataset, x, y, z, size_key='default'):

    d_1 = df_to_data(df_1)
    d_2 = df_to_data(df_2)

    pairwise_distances = [sd.euclidean(d_1[i, :], d_2[i, :]) for i in range(d_1.shape[0])]
    foscttm = calc_domainAveraged_FOSCTTM(d_1, d_2)

    plot_font_size = font_size[size_key]['plot_font_size']
    plot_title_font_size = font_size[size_key]['plot_title_font_size']
    tickfont_size = font_size[size_key]['tickfont_size']
    tickfont_size_3d = font_size[size_key]['tickfont_size_3d']
    marker_size_3d = marker_size[size_key]['3d']

    if size_key == 'big':
        titles = (f'$\Huge{{\mu = {np.mean(pairwise_distances):.4f}}}$', f'$\Huge{{\mu = {np.mean(foscttm):.4f}}}$', 'Alignment')
    else:
        titles = (f'$\mu = {np.mean(pairwise_distances):.4f}$', f'$\mu = {np.mean(foscttm):.4f}$', 'Alignment')

    fig = make_subplots(rows=1, cols=3,
                        column_widths=[0.15, 0.15, 0.7],
                        column_titles=titles,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'scene'}]])

    # box plot of distances between corresponding cells in latent space
    fig.add_trace(go.Box(y=pairwise_distances, name='Pairwise<br>cell distance', showlegend=False), row=1, col=1)

    # box plot of FOSCTTM scores (Fraction of Samples Closer Than True Match)
    fig.add_trace(go.Box(y=foscttm, name='FOSCTTM', showlegend=False), row=1, col=2)

    fig.add_trace(go.Scatter3d(x=d_1[:, x], y=d_1[:, y], z=d_1[:, z],
                               mode='markers',
                               marker={'color': 'red', 'size': marker_size_3d},
                               name=label_1,
                               showlegend=True),
                  row=1, col=3)
    fig.add_trace(go.Scatter3d(x=d_2[:, x], y=d_2[:, y], z=d_2[:, z],
                               mode='markers',
                               marker={'color': 'blue', 'size': marker_size_3d},
                               name=label_2,
                               showlegend=True),
                  row=1, col=3)

    fig.update_layout(title_text=f'Alignment in latent space: {dataset_titles.get(dataset, "Background job")}',
                      legend={'itemsizing': 'constant'},
                      font_size=plot_font_size,
                      title_font_size=plot_title_font_size,
                      title_yanchor='bottom',
                      title_pad={'b': plot_title_font_size * 1.5},
                      margin={'t': 100 + plot_title_font_size * 1.5},
                      scene_camera={'eye': {'x': 1.5, 'y': 1.5, 'z': 1.5}}
                      )
    fig.update_annotations(font_size=plot_title_font_size)  # subplot titles are annotations
    fig.update_scenes(xaxis_tickfont_size=tickfont_size_3d,
                      yaxis_tickfont_size=tickfont_size_3d,
                      zaxis_tickfont_size=tickfont_size_3d)

    return fig