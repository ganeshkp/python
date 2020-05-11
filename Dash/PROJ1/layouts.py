import dash_core_components as dcc
import dash_html_components as html


indexPage = html.Div([
    html.H2("Select project to go Dashboard",
            className="index_text",
            # style={"textAlign":"center",
            #        "color":"green"}
            ),
    dcc.Link("LCP",href="/lcp",
             style={"textAlign": "center",
                    "color": "blue",
                    "fontSize": 30}
             ),
    html.Br(),
    dcc.Link("Kepco", href="/kepco",
             style={"textAlign": "center",
                    "color": "blue",
                    "fontSize": 30}
             )
])

layout1 = html.Div([
    html.H3('LCP'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to Main Page', href='/')
])

layout2 = html.Div([
    html.H3('Kepco'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to Main Page', href='/')
])