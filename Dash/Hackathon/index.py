import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_table as table


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
        ], style={"width":"50%", "margin":"10px"}),


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


        html.Div(id="oInfectionTrendDiv", children=[
            dcc.Graph(id="oInfectionTrendGraph",
                      figure=getAffectedVsPopulation())
        ],
        style={"width":"95%", "display":"inline-block", "margin":"10px"}),

    ])
    return layout

def getAffectedVsPopulation():
    india = pd.read_csv("./inputs/covid_19_india.csv")
    india["Confirmed"]=india["Confirmed"].ffill()
    india["Confirmed"] = pd.to_numeric(india["Confirmed"], errors="coerce")

    population=pd.read_csv("./inputs/population_india_census2011.csv")
    population.set_index("State / Union Territory", inplace=True)


    states = list(india["State/UnionTerritory"].unique())
    states = sorted(states)

    pData=[]
    cData=[]
    for state in states:

        sDF=india[india["State/UnionTerritory"]==state]
        cData.append(sDF["Confirmed"].max())
        pData.append(int(population.loc[state]["Population"]))

    figure={
        "data":[
            {
                "x":states,
                "y":cData,
                "type":"bar",
                "name":"Affected"
            },
            {
                "x": states,
                "y": pData,
                "type": "bar",
                "name": "Population"
            },
        ],
        "layout":{
            "title":"Affected numbers Vs Population numbers",
            "xaxis":{"title":"States"},
            "yaxis":{"title":"Count"}
        }
    }
    return figure

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
    try:
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
            [html.Tr([html.Th(col, style={"textAlign":"center"}) for col in header])] + rows,
            style={"textAlign": "center"}
        )
    except:
        return html.Table()

def getStateLayout():

    india=pd.read_csv("./inputs/covid_19_india.csv")
    states=list(india["State/UnionTerritory"].unique())
    states=sorted(states)
    options=[]

    for state in states:
        d={}
        d["label"]=state
        d["value"]=state
        options.append(d)

    #print(options)

    layout=html.Div(children=[
        html.Div(children=[
            html.Label("Select State", style={"color":"white"}),
            dcc.Dropdown(id="states-dropdown",
                         options=options,
                         value="Karnataka")
        ], style={"width":"49%", "display":"inline-block", "backgroundColor":"green",
                  "margin":"10px"}),

        # html.Div(children=[
        #
        # ], style={"width":"49%", "display":"inline-block"}),

        html.Div(children=[
            html.Label("Infection Information", style={"backgroundColor":"blue", "color":"white"}),
            html.Div(id="infection-table")
        ], style={"width":"45%", "display":"inline-block", "margin":"15px", "backgroundColor":"white"}),

        html.Div(children=[
            html.Label("Hospital Bed Information", style={"backgroundColor":"blue", "color":"white"}),
            html.Div(id="state-hospital-bed-information")
        ], style={"margin":"10px", "backgroundColor":"white"}),

        #Infection trend
        html.Div(children=[
            dcc.Graph(id="infection-trend")
        ], style={"width":"48%", "display":"inline-block", "margin":"10px"}),

        #Statewide testing details/Total Samples
        html.Div(children=[
            dcc.Graph(id="state-total-samples-tested")
        ], style={"width":"48%", "display":"inline-block", "margin":"10px"}),

        # Statewide testing details/Negative
        html.Div(children=[
            dcc.Graph(id="state-total-negative")
        ], style={"width": "48%", "display": "inline-block", "margin": "10px"}),

        # Statewide testing details/Positive
        html.Div(children=[
            dcc.Graph(id="state-total-positive")
        ], style={"width": "48%", "display": "inline-block", "margin": "10px"}),

        html.Div(children=[
            html.Label("Affected Individual Details in the state",
                       style={"backgroundColor":"gray", "textAlign":"center",
                              "fontWeight":"bold", "color":"white"}),
            html.Div(id="state-individual-details")
        ], style={"width": "98%", "display": "inline-block", "margin": "5px"})

    ])
    return layout


@app.callback(Output("state-individual-details", "children"),
              [Input("states-dropdown", "value")])
def getStatesIndInfo(state):
    try:
        indInfoTemp=pd.read_csv("./inputs/IndividualDetails.csv")
        indInfo=indInfoTemp[indInfoTemp["detected_state"]==state]

        indInfo.drop(["id","detected_state"], axis=1, inplace=True)

        return table.DataTable(id="indDetails",
                            columns=[{"name":i, "id":i} for i in indInfo.columns],
                            data=indInfo.to_dict("records"),
                            style_cell={"textAlign":"left", "font_family":"verdana", "font_size":"12px", "whiteSpace":"normal"},
                            style_header={"backgroundColor":"blue", "color":"white", "fontWeight":"bold","font_size":"12px",
                                          "whiteSpace": "normal", "textAlign":"center"},
                            css=[{'selector': '.dash-cell div.dash-cell-value',
                                 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                            )
    except:
        table.DataTable()

@app.callback(Output("state-total-samples-tested", "figure"),
              [Input("states-dropdown", "value")])
def getStateTotalSamplesTested(state):
    try:
        testTemp=pd.read_csv("./inputs/StatewiseTestingDetails.csv")
        test=testTemp[testTemp["State"]==state]

        totSamples = list(test["TotalSamples"])
        dt = list(test["Date"])
        test["TotalSamples"]=test["TotalSamples"].ffill()
        totSamples=list(test["TotalSamples"])

        figure={
            "data":[
                {
                    "x":dt,
                    "y":totSamples,
                    "type":"lines",
                    "name":"Total Samples"
                },
            ],
            "layout":{
                "title":"Total Samples Tested",
                "xaxis":{"title":"Date"},
                "yaxis":{"title":"Samples"}
            }
        }
    except:
        figure={}
    return figure

@app.callback(Output("state-total-negative", "figure"),
              [Input("states-dropdown", "value")])
def getStateTestedNegative(state):
    try:
        testTemp=pd.read_csv("./inputs/StatewiseTestingDetails.csv")
        test=testTemp[testTemp["State"]==state]

        totSamples = list(test["Negative"])
        dt = list(test["Date"])
        test["Negative"]=test["Negative"].ffill()
        negative=list(test["Negative"])

        figure={
            "data":[
                {
                    "x":dt,
                    "y":negative,
                    "type":"lines",
                    "name":"Negative Tested"
                },
            ],
            "layout":{
                "title":"Tested Negative",
                "xaxis":{"title":"Date"},
                "yaxis":{"title":"Samples"}
            }
        }
    except:
        figure={}
    return figure

@app.callback(Output("state-total-positive", "figure"),
              [Input("states-dropdown", "value")])
def getStateTestedNegative(state):
    try:
        testTemp=pd.read_csv("./inputs/StatewiseTestingDetails.csv")
        test=testTemp[testTemp["State"]==state]

        totSamples = list(test["Positive"])
        dt = list(test["Date"])
        test["Positive"]=test["Positive"].ffill()
        positive=list(test["Positive"])

        figure={
            "data":[
                {
                    "x":dt,
                    "y":positive,
                    "type":"lines",
                    "name":"Positive Tested"
                },
            ],
            "layout":{
                "title":"Tested Positive",
                "xaxis":{"title":"Date"},
                "yaxis":{"title":"Samples"}
            }
        }
    except:
        figure={}
    return figure



@app.callback(Output("infection-trend", "figure"),
              [Input("states-dropdown", "value")])
def getInfectionTrendFig(state):
    india=pd.read_csv("./inputs/covid_19_india.csv")
    state=india[india["State/UnionTerritory"]==state]

    state["Cured"]=state["Cured"].ffill()
    state["Deaths"]=state["Deaths"].ffill()
    state["Confirmed"]=state["Confirmed"].ffill()

    date=list(state["Date"])
    cured=list(state["Cured"])
    deaths=list(state["Deaths"])
    confirmed=list(state["Confirmed"])

    fig=go.Figure()
    fig.add_trace(go.Scatter(x=date, y=cured, name="Cured"))
    fig.add_trace((go.Scatter(x=date, y=deaths, name="Deaths")))
    fig.add_trace((go.Scatter(x=date, y=confirmed, name="Confirmed")))
    fig.update_layout(title={"text":"Infection Trend", 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig


@app.callback(Output("infection-table", "children"),
              [Input("states-dropdown", "value")])
def getinfectionTable(state):
    india=pd.read_csv("./inputs/covid_19_india.csv")
    state=india[india["State/UnionTerritory"]==state]

    header = ["Confirmed Indian National", "Confirmed Foreign National", "Cured", "Deaths", "Confirmed"]
    data = []
    rows = []

    data_style = {"textAlign": "center"}

    cIn=0
    try:
        state["ConfirmedIndianNational"]=state["ConfirmedIndianNational"].ffill()
        state["ConfirmedIndianNational"] = pd.to_numeric(state["ConfirmedIndianNational"], errors="coerce")
        cIn = int(state["ConfirmedIndianNational"].max())
    except:
        pass
    data.append(html.Td(cIn, style=data_style))

    cFn = 0
    try:
        state["ConfirmedForeignNational"]=state["ConfirmedForeignNational"].ffill()
        state["ConfirmedForeignNational"] = pd.to_numeric(state["ConfirmedForeignNational"], errors="coerce")
        cFn = int(state["ConfirmedForeignNational"].max())
    except:
        pass
    data.append(html.Td(cFn, style=data_style))

    cured=0
    try:
        state["Cured"]=state["Cured"].ffill()
        state["Cured"] = pd.to_numeric(state["Cured"], errors="coerce")
        cured = int(state["Cured"].max())
    except:
        pass
    data.append(html.Td(cured, style=data_style))

    deaths=0
    try:
        state["Deaths"]=state["Deaths"].ffill()
        state["Deaths"] = pd.to_numeric(state["Deaths"], errors="coerce")
        deaths = int(state["Deaths"].max())
    except:
        pass
    data.append(html.Td(deaths, style=data_style))

    totConfirmed=0
    try:
        state["Confirmed"]=state["Confirmed"].ffill()
        state["Confirmed"] = pd.to_numeric(state["Confirmed"], errors="coerce")
        totConfirmed = int(state["Confirmed"].max())
    except:
        pass
    data.append(html.Td(totConfirmed, style=data_style))

    rows.append(html.Tr(data))
    return html.Table(
        [html.Tr([html.Th(col) for col in header])] + rows,
        style={"textAlign": "center"}
    )


@app.callback(Output("state-hospital-bed-information", "children"),
              [Input("states-dropdown", "value")])
def getStateHospInfo(state):
    try:
        hosp = pd.read_csv("./inputs/HospitalBedsIndia.csv")
        hosp.set_index("State/UT", inplace=True)

        header = ["Primary Health Centres", "Community Health Centers", "Sub Dist Hospitals", "District Hospitals",
                  "Public Health Facilities", "Public Beds", "Rural Hospitals", "Rural Beds", "Urban Hospitals",
                  "Urban Beds"]
        data = []
        rows = []

        data_style = {"textAlign": "center"}

        data.append(html.Td(hosp.loc[state]["NumPrimaryHealthCenters_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumCommunityHealthCenters_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumSubDistrictHospitals_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumDistrictHospitals_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["TotalPublicHealthFacilities_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumPublicBeds_HMIS"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumRuralHospitals_NHP18"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumRuralBeds_NHP18"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumUrbanHospitals_NHP18"], style=data_style))
        data.append(html.Td(hosp.loc[state]["NumUrbanBeds_NHP18"], style=data_style))

        rows.append(html.Tr(data))
        return html.Table(
            [html.Tr([html.Th(col,style={"textAlign":"center"}) for col in header])] + rows,
            style={"textAlign": "center"})
    except:
        return html.Table()

#------------------------------------------------------------------
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