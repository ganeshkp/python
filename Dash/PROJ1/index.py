import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout1, layout2,indexPage
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/lcp':
         return layout1
    elif pathname == '/kepco':
         return layout2
    else:
        return indexPage
        #return html.H1("THIS IS MAIN PAGE")

if __name__ == '__main__':
    app.run_server(debug=True)