import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label("Enter Input:"),
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div', children="Hello World!")
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_div(input):
    return 'You\'ve entered "{}"'.format(input)


if __name__ == '__main__':
    app.run_server(debug=True)