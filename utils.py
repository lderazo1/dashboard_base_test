from dash import dcc, html


def Header(app,value):
    return html.Div([get_header(app,value), html.Br([]), get_menu()])

def Header_p(app,value):
    return html.Div([get_header_p(app,value), html.Br([]), get_menu()])

def get_header(app,value):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="base-image",
                        ),
                        href="https://www.manabi.gob.ec/",
                        className='col-8'
                    ),
                    html.Div(
                        [
                            html.H5("Cantón "+ value),
                        ],
                        className="col-4 product_normal",
                        style={"color": "#ffffff"}
                    ),
                ],
                className="row",
            ),
            html.Div(
                [html.H5("Información")],
                className="main-title",
            ),
        ],
        
    )
    return header


def get_header_p(app,value):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="base-image",
                        ),
                        href="#",
                        className='col-8'
                    ),
                    html.Div(
                        [
                            html.H5(("PARROQUIA "+ value),style={"font-size": "16px"}),
                        ],
                        className="col-4 product",
                        style={"color": "#ffffff"}
                    ),
                ],
                className="row",
            ),
            html.Div(
                [html.H5("Información")],
                className="main-title",
            ),
        ],
        
    )
    return header

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                ".",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
        ],
        className="row",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table



'''
html.Div(
    [
        html.A(
            html.Img(
                src=app.get_asset_url("dash-financial-logo.png"),
                className="logo",
            ),
            href="https://www.manabi.gob.ec/",
        ),
        
        html.A(
            html.Button(id="learn-more-button", className="fa fa-facebook",
                style={"margin-left": "-20px"},),
            href="https://www.facebook.com/gobiernodemanabi",
        ),
        html.A(
            html.Button(id="learn-more-button", className="fa fa-instagram",
                style={"margin-left": "-20px"},),
            href="https://www.manabi.gob.ec/#",
        ),
        html.A(
            html.Button(id="learn-more-button", className="fa fa-twitter",
                style={"margin-rigth": "-20px"},),
            href="https://twitter.com/gobiernomanabi",
        ),
        
    ],
),
html.Div(
    [
        dcc.Link(
            "Full View",
            href="/dash-financial-report/full-view",
            className="full-view-link",
        )
    ],
    className="five columns",
),
'''