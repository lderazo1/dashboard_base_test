# -*- coding: utf-8 -*-
from pydoc import classname
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from plotly.express import data
import dataservice
import pandas as pd
import numpy as np

#df = []
df =  dataservice.get_selected_dataframe('CANTON','1FvE33JAUWO8mgzcoaZF7H1iYCEYm6da06rmEX8lGJaM')
df_p =  dataservice.get_selected_dataframe('PARROQUIA','1FvE33JAUWO8mgzcoaZF7H1iYCEYm6da06rmEX8lGJaM')
df_p = (df_p.replace(r'^\s*$', np.NaN, regex=True)).fillna(0)
df_suelo = dataservice.get_selected_dataframe('Uso_S_Manabi','1LgCKDvc1JFc_F0pAzmHUNE0QeNHPc9VoU_NOton1tw0')
province_gdf = dataservice.get_province_dataframe()
province_gdf = province_gdf.rename(columns={"DPA_PARROQ":"DPA_PARROQUIA"})
province_gdf['DPA_PARROQUIA'] = province_gdf['DPA_PARROQUIA'].astype(str).astype(int)
result_province_gdf = pd.merge(df_p,province_gdf, how='inner', on = 'DPA_PARROQUIA')

from pages import (
    overview,
    overview_p,
)

app = Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',dbc.themes.SIMPLEX]
)
app.title = "Reportes Financieros"
server = app.server
app.config.suppress_callback_exceptions=True


dropdown_menu = dbc.Row(
    [
        dbc.Col(
            [
                html.H5('Cantón', style={"font-size": "17px","text-align": "center"},),
            ],
            className="col-2"
        ),
        dbc.Col(
            [
                dcc.Dropdown(options = [{'label': str(i).upper(), 'value': str(i)} for i in df['CANTON']],
                             id='dropdown-1', clearable=False, value = df['CANTON'][0]
                ),
                html.Div(id='output-container-1'),
            ],
            className="col-3"
        ),
        dbc.Col(
            [
                html.H5('Parroquia', style={"font-size": "19px","text-align": "center"},),
            ],
            className="col-2"
        ),
        dbc.Col(
            [
                dcc.Dropdown(options = [], id='dropdown-2', clearable=True, placeholder="Seleccionar",),
                html.Div(id='output-container-2'),
            ],
            className="col-5"
        ),
    ],
    className="g-0 ms-auto flex-nowrap",
    style={"width": "750px"},
    align="center",
)

# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        html.Div(
            [
                dbc.Navbar(
                    dbc.Container(
                        [
                            html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("dash-financial-logo.png"), height="40px")),
                                        dbc.Col(dbc.NavbarBrand(className="ms-1")),
                                    ],
                                    align="center",
                                    className="g-0",
                                ),
                                href="#",
                                style={"textDecoration": "none"},
                            ),
                            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                            dbc.Collapse(
                                dropdown_menu,
                                id="navbar-collapse",
                                navbar=True,
                            ),
                        ]
                    ),
                    #color="light",
                    #dark=False,
                )
            ],
            className="no-print"
        ),
        
        html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")],
        )
    ]
)

# Update page
@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname"),
     Input('dropdown-1', 'value'),
     Input('dropdown-2', 'value')]
)
def display_page(pathname,value,value_2):
    if(value_2):
        return overview_p.create_layout(app,value_2,df_p,df_suelo)
    else:
        return overview.create_layout(app,value,df,df_p,df_suelo)

#Update dropdown
@app.callback(
    Output('dropdown-2', 'options'),
    Input('dropdown-1', 'value')
)
def update_options_dropdown(value):
    selection_province = result_province_gdf.loc[result_province_gdf['Canton'] == str(value).upper()]
    #print("Llegué "+str(value)+" con "+str(len(selection_province['Parroquia']))+" Parroquia")
    return [{'label': i, 'value': i} for i in selection_province['Parroquia']]
    #return {'options':dict(selection_province['Parroquia'])}



if __name__ == "__main__":
    app.run_server(debug=True)

