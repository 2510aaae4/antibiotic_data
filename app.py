#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd


full = ["Ampicillin","Augmentin","Amikacin","Clindamycin","Ceftazidime","Cefixime","Ciprofloxacin","Cefuroxime",
        "Cefotaxime","Cefazolin","Erythromycin","Ertapenem","Fusidic acid","Cefepime","Flomoxef","Cefoxitin","Gentamicin",
        "Imipenem",'Levofloxacin','Linezolid','Meropenem','Metronidazole','Moxifloxacin','Oxacillin',
        'Penicillin','Piperacillin','Rifampin','Streptomycin','Unaysnm','Baktar','Teicoplanin','Tazocin','Vancomycin','ceftriaxone']

short = ['AM','AMC','AN','CC','CAZ','CFM',"CIP",'CXM',
        'CTX','CZ','E','Etp','FA','FEP','FLO','FOX','GN',
        'IPM','LVX','LZD','MEM','MET',"MxF",'OX',
        'P','PIP','RA','S','SAM','SXT','TEC','TZP','VA','CRO']
shift_anti_list = {}
for i in range(len(full)):
    shift_anti_list[short[i]] = full[i]

url = 'https://raw.githubusercontent.com/2510aaae4/antibiotic_data/main/antibiotic.csv'
df = pd.read_csv(url)
df = df.replace({"anti": shift_anti_list})


# In[2]:


GPC = ['Coagulase(-)Staphylococcus',
       'Staphylococcus aureus', 'ORSA', 'OSSA', 'Enterococcus faeclais',
       'Enterococcus faecium',
       'Enterococcus gallinarum/Enterococcus casseliflavus',
       'Enterococcus species', 'β-hemolytic streptococci',
       'Streptococcus pneumoniae', 'Streptococcus species']
GPB = ['Cutibacterium species',]
GNB = ['Acinetobacter baumannii complex', 'Acinetobacter baumannii',
       'Acinetobacter calcoaceticus', 'Acinetobacter nosocomialis',
       'Acinetobacter pittii', 'Acinetobacter species','Burkholderia cepacia complex',
       'Stenotrophomonas maltophilia','Pseudomonas aeruginosa','Citrobacter species',
       'Enterobacter cloacae complex', 'Escherichia coli',
       'Klebsiella pneumoniae', 'Klebsiella aerogenes',
       'Klebsiella oxytoca', 'Morganella morganii', 'Proteus mirabilis',
       'Proteus species', 'Providencia species', 'Serratia marcescens',
       'Salmonella species','Fusobacterium species','Haemophilus influenzae', 'Haemophilus parainfluenzae',
       'Neisseria gonorrhoeae','Aeromonas species'
      ]
Anaerobes = ['Bacteroides fragilis','Bacteroides species', 'Clostridium difficile',
             'Clostridium species','Peptostreptococcus species','Prevotella species','Veillonella parvula',
            ]

bacteria_dict = {'GPC':GPC,'GPB':GPB,'GNB':GNB,'Anaerobes':Anaerobes}
names = list(bacteria_dict.keys())


# In[3]:


# Create a application which we can change year and continent
anti = list(df.anti.unique())


#app = dash.Dash()

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    dcc.Dropdown(id = 'bacteria_type_picker_1',options = [{'label':name, 'value':name} for name in names]
                 ,value = list(bacteria_dict.keys())[0]),
    
    dcc.Dropdown(id = 'bacteria_picker_1'),
    
    html.Button('Submit', id='submit-val_1', n_clicks=0),
    dcc.Graph(id = 'graph_1'),
##################################################### Second part
    
    dcc.Dropdown(id = 'bacteria_type_picker_2',options = [{'label':name, 'value':name} for name in names]
                 ,value = list(bacteria_dict.keys())[0]),
    
    dcc.Dropdown(id = 'bacteria_picker_2'),
    
    html.Button('Submit', id='submit-val_2', n_clicks=0),
    dcc.Graph(id = 'graph_2')
    
    
])

@app.callback(Output('bacteria_picker_1', 'options'),
              [Input('bacteria_type_picker_1',"value")] 
             )

def update_dropdown(name):
    return [{'label': i, 'value': i} for i in bacteria_dict[name]]




@app.callback(Output(component_id = 'graph_1',component_property = 'figure'),
              Input(component_id = 'submit-val_1',component_property = 'n_clicks'),
              State('bacteria_picker_1', 'value')
             )


def update_figure(n_clicks,selected_bacteria):
    filtered_df = df[df['bacteria'] == selected_bacteria]
    
    traces = []
    
    for anti_ in anti:
        df_by_anti = filtered_df[filtered_df['anti'] == anti_]
        traces.append(go.Scatter(
            x = df_by_anti['year'],
            y = df_by_anti['dst'],
            mode = 'lines+markers',
            #opacity = 0.7,
            #marker = {'size':15},
            name = anti_
        ))
    layout = go.Layout(title = "DST Charts "+selected_bacteria,
                      xaxis = {"title":"year",'categoryorder':'array', 'categoryarray': ['2019下半年', '2020上半年', "2020下半年", "2021上半年"]},
                      yaxis = {"title":"DST result"},
                      yaxis_range=[-5,105])
    
    return {'data':traces,'layout':layout}

#################### Second portion to compare

@app.callback(Output('bacteria_picker_2', 'options'),
              [Input('bacteria_type_picker_2',"value")] 
             )

def update_dropdown(name):
    return [{'label': i, 'value': i} for i in bacteria_dict[name]]




@app.callback(Output(component_id = 'graph_2',component_property = 'figure'),
              Input(component_id = 'submit-val_2',component_property = 'n_clicks'),
              State('bacteria_picker_2', 'value')
             )


def update_figure(n_clicks,selected_bacteria):
    filtered_df = df[df['bacteria'] == selected_bacteria]
    
    traces = []
    
    for anti_ in anti:
        df_by_anti = filtered_df[filtered_df['anti'] == anti_]
        traces.append(go.Scatter(
            x = df_by_anti['year'],
            y = df_by_anti['dst'],
            mode = 'lines+markers',
            #opacity = 0.7,
            #marker = {'size':15},
            name = anti_
        ))
    layout = go.Layout(title = "DST Charts "+selected_bacteria,
                      xaxis = {"title":"year",'categoryorder':'array', 'categoryarray': ['2019下半年', '2020上半年', "2020下半年", "2021上半年"]},
                      yaxis = {"title":"DST result"},
                      yaxis_range=[-5,105])
    
    return {'data':traces,'layout':layout}


# In[ ]:





# In[ ]:




