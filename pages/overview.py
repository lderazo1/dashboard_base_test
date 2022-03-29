from dash import dcc, html
from utils import Header, make_dash_table
import dataservice
import graphs

# get relative data folder

countries_gdf = dataservice.get_geodf()

#'''
df_2017 = dataservice.get_selected_dataframe('2017','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2018 = dataservice.get_selected_dataframe('2018','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2019 = dataservice.get_selected_dataframe('2019','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
df_2020 = dataservice.get_selected_dataframe('2020','1EOEmsm1R8ubMSXEcPBKbLF5dAOqVM5tTUIy702WSJmM')
#'''

def create_layout(app,value,df,df_p,df_suelo):
    selection = df.loc[df['CANTON'] == value]
    selection_p = df_p.loc[df_p['Canton'] == str(selection['CANTON'].values[0]).upper()] #Selección Parroquia
    selection_geo = countries_gdf.loc[countries_gdf['DPA_CANTON'] == str(selection['DPA_CANTON'].values[0])]
    selection_geo = selection_geo.rename(columns={"DPA_PARROQ":"DPA_PARROQUIA"})
    selection_geo['DPA_PARROQUIA'] = selection_geo['DPA_PARROQUIA'].astype(str).astype(int)
    result_geo = dataservice.merge_dataframes_geopandas(selection_p,selection_geo)
    df_selected = df_suelo.loc[df_suelo['DPA_CANTON'] == selection['DPA_CANTON'].values[0]]
    vab_selected = graphs.get_vab_values(df_2017,df_2018,df_2019,df_2020,selection)
    df_vab_2020 = graphs.get_vab_sector_values(df_2020,selection)
    # Page layouts
    return html.Div(
        [
            html.Div(
                html.Div([Header(app,value)],className="row"),
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
                                        ["Características Población"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(graphs.get_stats_people(selection))),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Índice de Prosperidad Territorial 2021",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_index_prosperity(selection))),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Acceso a Servicios",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_service_access(selection))),
                                ],
                                className="col-4",
                            ),
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Mapa",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_map_graph(result_geo,selection_geo)),
                                ],
                                className="col-6",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Uso de Suelo",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_pie_chart(df_selected,2)),
                                ],
                                className="col-6",
                            ),
                        ],
                        className="row",
                        style = {'margin-bottom':'35px'},
                    ),
                    html.Div(
                        [   
                            html.Div(
                                [
                                    html.H6(
                                        "Evolución VAB 2017-2020",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_line_chart(vab_selected)),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "Infraestructura de Salud",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(graphs.get_health_infrastructure(selection))),
                                ],
                                className="col-4",
                            ),

                            html.Div(
                                [
                                    html.H6(
                                        "TOP 3 Sectores por VAB",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(figure=graphs.get_bar_chart(df_vab_2020)),
                                ],
                                className="col-4",
                            ),
                            
                        ],
                        className="row",
                        style = {'margin-top':'35px'},
                    ),
                    # Row 5
                    html.Div(
                        [

                        ],
                        className="row ",
                    ),

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )