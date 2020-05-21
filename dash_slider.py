import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(id='slider-wrapper', children=[
    # dcc.Slider(
    #     id='my-slider',
    #     min=0,
    #     max=20,
    #     step=0.5,
    #     value=10,
    #     #updatemode='drag',
    #     tooltip = { 'always_visible': True }
    # ),
    dcc.Slider(
        id='my-slider',
        min=0,
        max=10,
        step=1,
        marks={
            0: '0 °F',
            3: '3 °F',
            5: '5 °F',
            7.65: '7.65 °F',
            10: '10 °F'
        },
        value=5
    ),
    html.Div(id='output-container-range-slider'),
    # Need onload script: $('#slider-wrapper .rc-slider-handle').appendChild($('#output-container-range-slider'));
])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return str(value)


if __name__ == '__main__':
    app.run_server(debug=True)