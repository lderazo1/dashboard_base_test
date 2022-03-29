from dash import Dash, dcc, html, Input, Output

import pandas as pd
import pathlib

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            # page 1
            html.Div(
                [
                    html.H1("Seleccione un Cantón o Parroquia")
                ]
            )
        ],
        className="page",
    )
