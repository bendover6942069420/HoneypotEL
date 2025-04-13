from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from collections import defaultdict
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

def init_dashboard(app):
    dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')
    
    # Add layout with real-time updates
    dash_app.layout = html.Div([
        html.Link(rel='stylesheet', href='/static/css/dashboard.css'),
        html.Div([
            html.H1('Honeypot Analytics Dashboard', className='dashboard-header'),
            
            # Stats cards
            html.Div([
                html.Div([
                    html.H3('Total Attempts'),
                    html.Div(id='total-attempts', className='value')
                ], className='stat-card'),
                html.Div([
                    html.H3('Unique IPs'),
                    html.Div(id='unique-ips', className='value')
                ], className='stat-card'),
                html.Div([
                    html.H3('Most Common Username'),
                    html.Div(id='common-username', className='value')
                ], className='stat-card'),
                html.Div([
                    html.H3('Most Common Location'),
                    html.Div(id='common-location', className='value')
                ], className='stat-card')
            ], className='stats-grid'),
            
            # Tabs for different visualizations
            dcc.Tabs([
                dcc.Tab(label='Time Analysis', children=[
                    html.Div([
                        dcc.Graph(id='time-series-plot')
                    ], className='graph-container')
                ]),
                dcc.Tab(label='Geographic Distribution', children=[
                    html.Div([
                        dcc.Graph(id='world-map-plot')
                    ], className='graph-container')
                ]),
                dcc.Tab(label='Attack Patterns', children=[
                    html.Div([
                        dcc.Graph(id='username-password-patterns')
                    ], className='graph-container')
                ]),
                dcc.Tab(label='User Agents', children=[
                    html.Div([
                        dcc.Graph(id='user-agent-distribution')
                    ], className='graph-container')
                ])
            ])
        ], className='dashboard-container'),
        
        # Update interval
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # updates every 30 seconds
            n_intervals=0
        )
    ])
    
    @dash_app.callback(
        [Output('total-attempts', 'children'),
         Output('unique-ips', 'children'),
         Output('common-username', 'children'),
         Output('common-location', 'children'),
         Output('time-series-plot', 'figure'),
         Output('world-map-plot', 'figure'),
         Output('username-password-patterns', 'figure'),
         Output('user-agent-distribution', 'figure')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_metrics(n):
        # Load and parse log data
        attempts = []
        try:
            with open('honeypot.log', 'r') as f:
                for line in f:
                    try:
                        if '"timestamp":' in line:  # Only parse JSON log entries
                            data = json.loads(line.split(' - ')[-1])
                            attempts.append(data)
                    except:
                        continue
        except FileNotFoundError:
            attempts = []
        
        df = pd.DataFrame(attempts)
        
        if len(df) == 0:
            empty_fig = go.Figure()
            empty_fig.update_layout(title="No data available")
            return "0", "0", "None", "None", empty_fig, empty_fig, empty_fig, empty_fig
        
        # Calculate metrics
        total_attempts = len(df)
        unique_ips = len(df['ip_address'].unique())
        common_user = df['username'].mode()[0] if not df.empty else "None"
        common_location = f"{df['city'].mode()[0]}, {df['country'].mode()[0]}" if not df.empty else "Unknown"
        
        # Time series plot
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        time_series = df.groupby(pd.Grouper(key='timestamp', freq='1H')).size().reset_index(name='count')
        time_fig = px.line(time_series, x='timestamp', y='count', 
                          title='Login Attempts Over Time')
        time_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Number of Attempts",
            plot_bgcolor='white'
        )
        
        # World map plot
        geo_df = df.groupby(['country', 'city']).size().reset_index(name='count')
        map_fig = px.choropleth(geo_df, 
                               locations='country',
                               locationmode='country names',
                               color='count',
                               hover_data=['city'],
                               title='Geographic Distribution of Attacks',
                               color_continuous_scale='Viridis')
        map_fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            plot_bgcolor='white'
        )
        
        # Username patterns
        pattern_df = df.groupby(['username']).size().nlargest(10).reset_index(name='count')
        pattern_fig = px.bar(pattern_df, x='username', y='count',
                           title='Top 10 Attempted Usernames')
        pattern_fig.update_layout(
            xaxis_title="Username",
            yaxis_title="Number of Attempts",
            plot_bgcolor='white'
        )
        
        # User agent distribution
        ua_df = df.groupby('user_agent').size().nlargest(10).reset_index(name='count')
        ua_fig = px.pie(ua_df, values='count', names='user_agent',
                       title='Top User Agents Used in Attacks')
        ua_fig.update_layout(plot_bgcolor='white')
        
        return (
            str(total_attempts),
            str(unique_ips),
            common_user,
            common_location,
            time_fig,
            map_fig,
            pattern_fig,
            ua_fig
        )
    
    return dash_app