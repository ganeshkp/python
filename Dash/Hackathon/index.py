import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



def getIndiaLayout():
    layout=html.Div(children=[

        html.Div(children=[
            html.Div(children=[
                html.Label("Status Information")
            ], style={"backgroundColor":"blue", "color":"white"}),

            html.Div(id="topTable", children=[
                getIndiaTopTable()
            ], style={"backgroundColor": "white", "textAlign": "center", "padding": "2px"}),
        ], style={"width":"40%", "margin":"10px"}),


        html.Div(children=[
            html.Div(children=[
               html.Label("Hospital Beds Information")
            ], style={"backgroundColor":"blue", "color":"white"}),

            html.Div(id="oHospInfo", children=[
                getIndiaHospInfo()
            ], style={"backgroundColor": "white", "textAlign":"center", "padding":"2px"}),
        ], style={"width":"95%", "margin":"10px"}),

        html.Div(children=[
            dcc.Graph(id="icmrChart1",
                      figure=getTotSamplesFigure())
        ], style={"width":"49%", "margin":"6px", "display":"inline-block"}),

        html.Div(children=[
            dcc.Graph(id="icmrChart2",
                      figure=getTotIndFigure())
        ], style={"width": "49%", "margin": "6px", "display":"inline-block"}),

        html.Div(children=[
            dcc.Graph(id="icmrChart3",
                      figure=getPosCasesFigure())
        ], style={"width": "49%", "margin": "6px", "display":"inline-block"}),


        # html.Div(id="oInfectionTrendDiv", children=[
        #     dcc.Graph(id="oInfectionTrendGraph",
        #               figure=getIndiaInfectionTrendGraph())
        # ],
        # style={"width":"49%", "display":"inline-block"}),

    ])
    return layout

def getIndiaInfectionTrendGraph():
    india = pd.read_csv("./inputs/covid_19_india.csv")

    #india["Date"]=pd.to_datetime(india["Date"])
    date=list(india["Date"])

    india["Confirmed"] = pd.to_numeric(india["Confirmed"], errors="coerce")
    india["cumConfirmed"] = india["Confirmed"].cumsum()
    confirmed=india["cumConfirmed"]

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=date, y=confirmed))
    return fig

def getTotSamplesFigure():
    icmrTemp=pd.read_csv("./inputs/ICMRTestingDetails.csv")
    icmr=icmrTemp.dropna(axis=0, how="any")

    date=list(icmr["DateTime"])
    totSamplesTested=list(icmr["TotalSamplesTested"])
    totIndTested=list(icmr["TotalIndividualsTested"])
    totPosCases=list(icmr["TotalPositiveCases"])

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=date, y=totSamplesTested, name="Total Samples Tested"))
    #fig.add_trace((go.Scatter(x=date, y=totIndTested, name="Total Individuals Tested")))
    #fig.add_trace((go.Scatter(x=date, y=totPosCases, name="Total Positive Cases")))
    fig.update_layout(title={"text":"ICMR Total Samples Test Trend", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig

def getTotIndFigure():
    icmrTemp=pd.read_csv("./inputs/ICMRTestingDetails.csv")
    icmr=icmrTemp.dropna(axis=0, how="any")

    date=list(icmr["DateTime"])
    totSamplesTested=list(icmr["TotalSamplesTested"])
    totIndTested=list(icmr["TotalIndividualsTested"])
    totPosCases=list(icmr["TotalPositiveCases"])

    fig=go.Figure()
    #fig.add_trace(go.Scatter(x=date, y=totSamplesTested, name="Total Samples Tested"))
    fig.add_trace((go.Scatter(x=date, y=totIndTested, name="Total Individuals Tested")))
    #fig.add_trace((go.Scatter(x=date, y=totPosCases, name="Total Positive Cases")))
    fig.update_layout(title={"text":"ICMR Total Individuals Test Trend", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig

def getPosCasesFigure():
    icmrTemp=pd.read_csv("./inputs/ICMRTestingDetails.csv")
    icmr=icmrTemp.dropna(axis=0, how="any")

    date=list(icmr["DateTime"])
    totSamplesTested=list(icmr["TotalSamplesTested"])
    totIndTested=list(icmr["TotalIndividualsTested"])
    totPosCases=list(icmr["TotalPositiveCases"])

    fig=go.Figure()
    #fig.add_trace(go.Scatter(x=date, y=totSamplesTested, name="Total Samples Tested"))
    #fig.add_trace((go.Scatter(x=date, y=totIndTested, name="Total Individuals Tested")))
    fig.add_trace((go.Scatter(x=date, y=totPosCases, name="Total Positive Cases")))
    fig.update_layout(title={"text":"ICMR Total Positive Cases Trend", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig

def getIndiaTopTable():
    india=pd.read_csv("./inputs/covid_19_india.csv")

    header=["Confirmed Indian National", "Confirmed Foreign National", "Cured", "Deaths", "Confirmed"]
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

def getIndiaHospInfo():
    hosp = pd.read_csv("./inputs/HospitalBedsIndia.csv")
    hosp.set_index("State/UT", inplace=True)

    header = ["Primary Health Centres", "Community Health Centers", "Sub Dist Hospitals", "District Hospitals",
              "Public Health Facilities", "Public Beds", "Rural Hospitals", "Rural Beds", "Urban Hospitals",
              "Urban Beds"]
    data = []
    rows = []

    data_style = {"textAlign": "center"}

    data.append(html.Td(hosp.loc["All India"]["NumPrimaryHealthCenters_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumCommunityHealthCenters_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumSubDistrictHospitals_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumDistrictHospitals_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["TotalPublicHealthFacilities_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumPublicBeds_HMIS"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumRuralHospitals_NHP18"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumRuralBeds_NHP18"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumUrbanHospitals_NHP18"], style=data_style))
    data.append(html.Td(hosp.loc["All India"]["NumUrbanBeds_NHP18"], style=data_style))

    rows.append(html.Tr(data))
    return html.Table(
        [html.Tr([html.Th(col) for col in header])] + rows,
        style={"textAlign": "center"}
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
    'backgroundColor': '#ff9900',
    'color': 'white',
    'padding': '6px'
}

app.layout=html.Div([
    html.Div(children=[
        html.H2("Covid-19 India Dashboard")
    ],
    style={"textAlign":"center", "color":"blue", "padding":"2px", "fontWeight":"bold"}),

    html.Div(id="body", children=[
        dcc.Tabs(id="mainTabs",
                 value="india",
                 children=[
                     dcc.Tab(label="Overall",
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
style={"backgroundColor":"#6699ff"})





if __name__ == '__main__':
    app.run_server(debug=True)