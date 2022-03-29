from dash import dcc, html
from utils import Header_p, make_dash_table
import dataservice
import graphs
import numpy as np

# get relative data folder
'''
df_suelo = []
'''
province_gdf = dataservice.get_province_dataframe()


def create_layout(app,value,df_p,df_suelo):

    selection = df_p.loc[df_p['Parroquia'] == value]
    selection_geo = province_gdf.loc[province_gdf['DPA_PARROQ'] == str(selection['DPA_PARROQUIA'].values[0])]
    selection_geo = selection_geo.rename(columns={"DPA_PARROQ":"DPA_PARROQUIA"})
    selection_geo['DPA_PARROQUIA'] = selection_geo['DPA_PARROQUIA'].astype(str).astype(int)
    result_geo = dataservice.merge_dataframes_geopandas(selection,selection_geo)
    df_selected = df_suelo.loc[df_suelo['DPA_PARROQ'] == selection['DPA_PARROQUIA'].values[0]]

    # Page layouts
    return html.Div(
        [
            html.Div(
                html.Div([Header_p(app,value)],className="row"),
            ),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Mapa",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_map_graph_p(result_geo,selection_geo)),
                                ],
                                className="col-6",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Uso de Suelo",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_pie_chart(df_selected,1)),
                                ],
                                className="col-6",
                            ),

                        ],
                        className="row",
                        style = {'margin-bottom':'20px'},
                    ),
      
                    # Row 4
                    html.Div(
                        [

                            html.Div(
                                [
                                    html.H6(
                                        ["Características Población"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(graphs.get_stats_people_p(selection,df_p))),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Acceso a Servicios",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_service_access_p(selection))),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Infraestructura de Salud",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_health_infrastructure_p(selection))),
                                ],
                                className="col-4",
                            ),
                        ],
                        className="row",
                        style = {'margin-bottom':'0px'},
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )