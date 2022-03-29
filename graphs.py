import plotly.express as px
import pandas as pd

def get_map_graph(result_geo,selection_geo):
    point = selection_geo.geometry.values[0].centroid
    avg_people = (result_geo['Población 2022']*result_geo['Extensión Territorial (km2)']).sum()/result_geo['Extensión Territorial (km2)'].sum()

    fig = px.choropleth_mapbox (result_geo,
                                geojson=selection_geo.geometry,
                                locations=selection_geo.index,
                                color="Población 2022", hover_data=["Extensión Territorial (km2)"],
                                color_continuous_midpoint=avg_people,
                                hover_name="Parroquia", # column to add to hover information
                                color_continuous_scale=["red", "yellow", "green"],
                                mapbox_style="open-street-map",
                                center = {"lat": point.y, "lon": point.x},zoom=8,
                                )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(font=dict(family="Courier",size=9.5,color="black"),
                  autosize=True,height=285,margin=dict(l=10, r=10, t=10, b=30))
    return fig

def get_pie_chart(df_selected,condition):
    data_pie = pd.pivot_table(df_selected, index=['cobertura'],values=['km2_1'],aggfunc='sum')
    data_pie = data_pie['km2_1'].sort_values(ascending=False)

    suma = data_pie.iloc[9:].sum()
    out = data_pie.iloc[:9]
    row = pd.Series({'OTROS':suma})
    out = out.append(row)

    fig = px.pie(out, values= out.values, names=out.index, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textposition='inside', textinfo='percent')
    if (condition==1):
        fig.update_layout(legend=dict(font=dict(family="Courier",size=9.5,color="black")),
                    autosize=True,height=220,margin=dict(l=10, r=10, t=10, b=10))
    else:
        fig.update_layout(legend=dict(font=dict(family="Courier",size=9.5,color="black")),
                    autosize=True,height=275,margin=dict(l=10, r=10, t=10, b=50))

    return fig

def get_line_chart(vab_selected):
    fig = px.line(vab_selected, x=vab_selected['Anio'], y=vab_selected['Valor'], 
                markers=True, labels=None,color_discrete_sequence=px.colors.qualitative.Dark2,
                text=vab_selected['Valor'])
    fig.update_traces(textposition="top right")
    fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_layout(yaxis_title=None, xaxis_title='Año',paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',font=dict(family="Courier",size=10,color="black"),
                    autosize=True,height=300,margin=dict(l=10, r=10, t=10, b=10))
    return fig

def get_bar_chart(df_vab_2020):
    fig = px.bar(df_vab_2020, x=df_vab_2020.index, y='Valor',color=df_vab_2020.index,
                color_discrete_sequence=px.colors.qualitative.Dark2,text_auto=True)
    fig.update_yaxes(showgrid=True, gridwidth=0.01, gridcolor='rgba(230, 230, 230, 0.8)')
    fig.update_layout(yaxis_title=None, xaxis_title=None,paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    plot_bgcolor= 'rgba(0, 0, 0, 0)',autosize=True,height=300,
                    margin=dict(l=10, r=10, t=10, b=10),legend_title_text=None,
                    legend=dict(orientation="h",yanchor="bottom",y=-0.2,xanchor="right",x=1,
                                font=dict(family="Courier",size=9.5,color="black")),
                    )
    fig.update_xaxes(visible=False)
    fig.update_xaxes(visible=False)
    return fig

####### CHARTS SUBSTATE

def get_map_graph_p(result_geo,selection_geo):
    point = selection_geo.geometry.values[0].centroid

    fig = px.choropleth_mapbox(result_geo, geojson=selection_geo.geometry,
                            locations=selection_geo.index, hover_data=["Extensión Territorial (km2)"],
                            hover_name="Parroquia", # column to add to hover information
                            mapbox_style="open-street-map",
                            center = {"lat": point.y, "lon": point.x},zoom=9,
                            color_discrete_sequence=px.colors.qualitative.Vivid
                            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(font=dict(family="Courier",size=9.5,color="black"),
                    autosize=True,height=220,margin=dict(l=10, r=10, t=0, b=0),showlegend=False)
    return fig

########    TABLES   #########
def get_stats_people(selection):
    base_stats = []
    rows_name = ["% Hombres","% Mujeres","% Población Rural","% Población Urbana","PEA","Extensión Territorial","Población Total"]
    total = selection['Poblacion Hombres 2022'].values[0] + selection['Poblacion Mujeres 2022'].values[0]
    base_stats.append(str(round(((selection['Poblacion Hombres 2022'].values[0]/total)*100), 2))+"%")
    base_stats.append(str(round(((selection['Poblacion Mujeres 2022'].values[0]/total)*100), 2))+"%")
    base_stats.append(str(round(selection['% Poblacion Rural'].values[0], 2))+"%")
    base_stats.append(str(round(100-selection['% Poblacion Rural'].values[0], 2))+"%")
    base_stats.append(str(round(selection['PEA'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Extension Territorial'].values[0], 2)))
    base_stats.append(str(total))
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    
    return df_stats_people

def get_vab_values(df_2017,df_2018,df_2019,df_2020,selection):
    rows_name = ['2017','2018','2019','2020']
    vab_value = [
        (df_2017.loc[df_2017['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2018.loc[df_2018['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2019.loc[df_2019['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0],
        (df_2020.loc[df_2020['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])['ECONOMÍA TOTAL'].values[0]
    ]
    vab_selected = pd.DataFrame({'Anio': rows_name,'Valor': vab_value})
    return vab_selected

def get_vab_sector_values(df_2020,selection):
    f_20 = (df_2020.loc[df_2020['CÓDIGO CANTÓN'] == selection['DPA_CANTON'].values[0]])
    f_20 = f_20.drop(columns=['PROVINCIA', 'CÓDIGO PROVINCIA','CANTÓN','CÓDIGO CANTÓN','ECONOMÍA TOTAL'])
    df_vab_2020 = f_20.rename({f_20.index[0]: 'Valor'}, axis='index').T
    df_vab_2020 = df_vab_2020.sort_values(by="Valor", ascending=False).iloc[:3]
    df_vab_2020.index.name = 'Actividad'
    return df_vab_2020

def get_index_prosperity(selection):
    base_stats = []
    rows_name = ["Tasa de Alfabetismo","Ingreso Medio de Hogares USD (Mensual)",
                 "Población en asentamientos Precarios","Población Afectada por eventos naturales (cada mil personas)"]
    base_stats.append(str(round(selection['Tasa de Alfabetismo'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Ingreso Medio Hogares  USD (Mensual)'].values[0], 2)))
    base_stats.append(str(round(selection['Poblacion en asentamientos precarios'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Poblacion afectada por eventos naturales'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people

def get_service_access(selection):
    base_stats = []
    rows_name = ["Acceso a Agua Mejorada (% Población)","Acceso a Saneamiento Adecuado (%Población)","Acceso a Electricidad (% Población)",
                 "Acceso a Internet (Usuarios de internet por cada 100 habitantes)", "Acceso Computadores (% Hogares)"]
    #column_name = ['Indicador','%']
    base_stats.append(str(round(selection['Acceso a Agua Mejorada'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Saneamiento Adecuado'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Electricidad'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso a Internet'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso Computadores (% Hogares)'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people

def get_health_infrastructure(selection):
    base_stats = []
    rows_name = ["Centro de Salud Tipo A","Centro de Salud Tipo B","Centro de Salud Tipo C - Maternidad e Infantil",
                 "Centros Especializados","Hospital Básico","Hospital de Especialidades","Hospital General","Puesto de Salud"]
    base_stats.append(str(round(selection['Centro de Salud Tipo A'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo B'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo C'].values[0])))
    base_stats.append(str(round(selection['Centros especializados'].values[0])))
    base_stats.append(str(round(selection['Hospital Basico'].values[0])))
    base_stats.append(str(round(selection['Hospital de especialidades'].values[0])))
    base_stats.append(str(round(selection['Hospital General'].values[0])))
    base_stats.append(str(round(selection['Puesto de Salud'].values[0])))
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    return df_stats_people

###### TABLE BY SUBSTATE

def get_stats_people_p(selection,df_p):
    temp_selection = df_p.loc[df_p['Canton'] == selection['Canton'].values[0]]
    total = temp_selection['Población 2022'].sum()
    base_stats = []
    rows_name = ["Población Proyección Inec 2022","Densidad Poblacional","% Pobres por NBI","% Analfabetismo","% Población Cantonal", "% Personas Afiliadas al iess"]
    base_stats.append(str(round(selection['Población 2022'].values[0])))
    base_stats.append("habitantes/km2")
    base_stats.append(str(round(selection['Porcentaje de pobres por NBI'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Tasa de Analfabetismo'].values[0], 2))+"%")
    base_stats.append(str(round(((selection['Población 2022'].values[0]/total)*100), 2))+"%")
    base_stats.append(str(round(selection['Personas Afiliadas al Seguro Social (% Población)'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    
    return df_stats_people

def get_service_access_p(selection):
    base_stats = []
    rows_name = ["Cobertura Agua Red Pública (% Familias)","Cobertura Alcantarillado (% Familias)","Cobertura energía red pública (% Familias)",
                 "Acceso a Internet (% Familias)", "Acceso Computadores (% Familias)"]
    base_stats.append(str(round(selection['Cobertura Agua Red Pública (% Familias)'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Cobertura Alcantarillado (% Familias)'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Cobertura Electricidad Red Pública (% Familias)'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso internet (%)'].values[0], 2))+"%")
    base_stats.append(str(round(selection['Acceso computadora (%)'].values[0], 2))+"%")
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})
    
    return df_stats_people

def get_health_infrastructure_p(selection):
    base_stats = []
    rows_name = ["Centro de Salud Tipo A","Centro de Salud Tipo B","Centro de Salud Tipo C - Maternidad e Infantil",
                 "Centros Especializados","Hospital Básico","Hospital de Especialidades","Hospital General","Puesto de Salud"]
    base_stats.append(str(round(selection['Centro de Salud Tipo A'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo B'].values[0])))
    base_stats.append(str(round(selection['Centro de Salud Tipo C- Maternidad e infantil'].values[0])))
    base_stats.append(str(round(selection['Centros especializados'].values[0])))
    base_stats.append(str(round(selection['Hospital Basico'].values[0])))
    base_stats.append(str(round(selection['Hospital de especialidades'].values[0])))
    base_stats.append(str(round(selection['Hospital General'].values[0])))
    base_stats.append(str(round(selection['Puestos de salud'].values[0])))
    df_stats_people = pd.DataFrame({'Indicador': rows_name,'%': base_stats})

    return df_stats_people