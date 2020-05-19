# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/map.ipynb (unless otherwise specified).

__all__ = ['build_sounding_scatter', 'build_sounding_map', 'build_world_map']

# Cell
import plotly.graph_objects as go

# Cell
def build_sounding_scatter(df_sounding, gaussian_param, with_dash = False):
    sounding_plot = {
            'data': [
                go.Scatter(
                    x=df_sounding['distance'],
                    y=df_sounding['xco2'],
                    text='xco2',
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name="xco2"
                ),
                go.Scatter(x=df_sounding['distance'], y=df_sounding['gaussian_y'], name="Gaussian fit",
                    hoverinfo='name',
                    line_shape='spline')
            ],
            'layout': go.Layout(
                xaxis={'title': 'Distance (km)'},
                yaxis={'title': 'CO² level in ppm'},
                #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    return sounding_plot

# Cell
def build_sounding_map(df_sounding, mapbox_token):
    df = df_sounding
    center_lat = df.latitude.min() + (df.latitude.max() - df.latitude.min())/2
    center_lon = df.longitude.min() + (df.longitude.max() - df.longitude.min())/2
    xco_sounding_mapbox = go.Figure(go.Scattermapbox(
        lat=df.latitude,
        lon=df.longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            color = df['xco2'], size=5
        ),

        text=df.xco2,
    ))
    xco_sounding_mapbox.update_layout(
        mapbox_style="satellite-streets",
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=6
        )
    )
    return xco_sounding_mapbox

# Cell
import folium
def build_world_map(data):
    folium_map = folium.Map([43, 0], zoom_start=4)
    folium.TileLayer("CartoDB dark_matter", name="Dark mode").add_to(folium_map)

    # Adding detected peaks
    peaks_group = folium.FeatureGroup(name="Peaks").add_to(folium_map)
    peaks_group_circle = folium.FeatureGroup(name=" - 50km Circles").add_to(folium_map)
    peaks_group_wind = folium.FeatureGroup(name=" - Wind Vectors").add_to(folium_map)

    for _, row in data.iterrows():
        radius = row["amplitude"]/20
        color="#FF3333" # red
        tooltip =  "GPS : ["+str(round(row['latitude'],2))+" ; "+str(round(row['longitude'],2))+"]"
        sounding = str(row['sounding_id'])
        date = str(row['sounding_id'])
        orbit = str(row['orbit'])
        wind = [[row['latitude'],row['longitude']],[row['latitude']+row['windspeed_u'],row['longitude']+row['windspeed_v']]]

        popup_html="""<h4>"""+tooltip+"""</h4>"""+date+"""<p>sounding_id: """+sounding+"""</br>orbit: """+orbit+"""</p>"""
        popup_html+='<p><input type="button" value="Show plot"'
        # Injecting JavaScript in popup to fire the Dash Callback
        popup_html+='onclick="\
            let bco_input = parent.document.getElementById(\'input_sounding\'); \
            let lastValue = bco_input.value;'
        popup_html+=f'bco_input.value = \'{sounding}\';'
        popup_html+="let bco_event = new Event('input', { bubbles: true });\
            bco_event.simulated = true;\
            let tracker = bco_input._valueTracker;\
            if (tracker) {\
            tracker.setValue(lastValue);\
            }\
            bco_input.dispatchEvent(bco_event);\
            elt.dispatchEvent(new Event('change'));\
            \"/></p>"
        #onclick="plot_data(\'{url}\', {slope}, {intercept}, {amplitude}, {sigma});"/></p>'

        popup=folium.Popup(popup_html, max_width=450)

        peaks_group.add_child(folium.CircleMarker(location=(row["latitude"],
                                    row["longitude"]),
                            radius=radius,
                            color=color,
                            tooltip=tooltip,
                            popup=popup,
                            fill=True))

        peaks_group_circle.add_child(folium.Circle(location=(row["latitude"],
                            row["longitude"]),
                            radius=50000,
                            color='#949494',
                            weight = 1,
                            fill=False))

        peaks_group_wind.add_child(folium.PolyLine(wind,
                        color='#B2B2B2',
                        weight = 1))
    return folium_map
