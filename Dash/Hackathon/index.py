import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



def getIndiaLayout():
    layout=html.Div(children=[
        html.Div(id="topTable", children=[
            getIndiaTopTable()
        ],
        style={"width":"50%", "display":"inline-block", "backgroundColor":"white",
               "textAlign":"center"})

    ])
    return layout

def getIndiaTopTable():
    india=pd.read_csv("./inputs/covid_19_india.csv")

    header=["Confirmed Indian National", "Confirmed Foreign National", "Cured", "Deaths", "Confirmed Total"]
    data=[]
    rows=[]

    data_style={"textAlign":"center"}

    india["ConfirmedIndianNational"]=pd.to_numeric(india["ConfirmedIndianNational"], errors="coerce")
    cIn=int(india["ConfirmedIndianNational"].max())
    data.append(html.Td(cIn, style=data_style))

    india["ConfirmedForeignNational"] = pd.to_numeric(india["ConfirmedForeignNational"], errors="coerce")
    cFn = int(india["ConfirmedForeignNational"].max())
    data.append(html.Td(cFn, style=data_style))

    india["Cured"] = pd.to_numeric(india["Cured"], errors="coerce")
    cured = int(india["Cured"].max())
    data.append(html.Td(cured, style=data_style))

    india["Deaths"] = pd.to_numeric(india["Deaths"], errors="coerce")
    deaths = int(india["Deaths"].max())
    data.append(html.Td(deaths, style=data_style))

    india["Confirmed"] = pd.to_numeric(india["Confirmed"], errors="coerce")
    totConfirmed = int(india["Confirmed"].max())
    data.append(html.Td(totConfirmed, style=data_style))

    rows.append(html.Tr(data))
    return html.Table(
        [html.Tr([html.Th(col) for col in header])] + rows,
        style={"textAlign":"center"}
    )


def getStateLayout():
    pass


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout=html.Div([
    html.Div(children=[
        html.H2("Covid-19 Dashboard")
    ],
    style={"textAlign":"center", "color":"green", "font_size":"40px", "fontWeight":"bold"}),

    html.Div(id="body", children=[
        dcc.Tabs(id="mainTabs",
                 value="india",
                 children=[
                     dcc.Tab(label="India",
                             value="india",
                             style=tab_style,
                             selected_style=tab_selected_style,
                             children=[
                                 getIndiaLayout()
                             ]
                             ),
                     dcc.Tab(label="Statewise",
                             value="statewise",
                             style=tab_style,
                             selected_style=tab_selected_style,
                             children=[
                                 getStateLayout()
                             ])
                 ])
    ])


],
style={"backgroundColor":"gray"})





if __name__ == '__main__':
    app.run_server(debug=True)