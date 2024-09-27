import os
import sys
import streamlit as st
import folium
from folium import Marker, Icon
from streamlit_folium import st_folium

# Add scripts
relative_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'aia-script', '3_module_pathfinder/sandbox'))
sys.path.append(relative_path)
from script_pathfinder_one import get_intermediate_stations, get_coordinates, load_station_data

# Load stations
df_stations = load_station_data()

# Config
st.set_page_config(
    page_title="Commande de voyage",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Menu")
menu = st.sidebar.radio("Navigation", ["Home", "Autre"])

# Home page
st.title("Application de commande de voyage")
btn = st.button("🎙️ Entrez votre commande vocale")

# Manage state for calculating intermediate stations
if 'calculate' not in st.session_state:
    st.session_state['calculate'] = False
    st.session_state['start_coords'] = None
    st.session_state['end_coords'] = None

departure_city = st.text_input("Ville de départ", value="Nantes")
arrival_city = st.text_input("Ville d'arrivée", value="Paris Montparnasse")

def handle_calculate():
    st.session_state['calculate'] = True
    st.session_state['start_coords'] = get_coordinates(departure_city, df_stations)
    st.session_state['end_coords'] = get_coordinates(arrival_city, df_stations)

if st.button("Calculer les gares intermédiaires", on_click=handle_calculate):
    pass # the button will update the state

# Display the map and the list of stations in columns
if st.session_state['calculate']:
    start_coords = st.session_state['start_coords']
    end_coords = st.session_state['end_coords']

    if start_coords is None or end_coords is None:
        st.error("Vérifier si le nom de la ville est correct et réessayer")
    elif start_coords and end_coords:
        try:
            intermediate_stations = get_intermediate_stations(df_stations, start_coords, end_coords)
            if not intermediate_stations.empty:
                # 2 columns in UI
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Calculate the center of the map
                    center_lat = (start_coords[0] + end_coords[0]) / 2
                    center_lon = (start_coords[1] + end_coords[1]) / 2
                    travel_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)
                    # Add markers
                    for index, row in intermediate_stations.iterrows():
                        Marker([row['latitude'], row['longitude']], popup=row['nom'], icon=Icon(color='blue')).add_to(travel_map)
                    # Display the map
                    st_folium(travel_map, width=700, height=500)

                # Display the list of intermediate stations
                with col2:
                    st.write("#### Liste des gares intermédiaires")
                    nb_stations = len(intermediate_stations)
                    st.write(f"{nb_stations} Gares trouvées")
                    st.dataframe(intermediate_stations[['nom', 'latitude', 'longitude']])

            else:
                st.warning("Aucune gare intermédiaire trouvée")
        except Exception as e:
            st.error(f"Erreur lors du traitement, vérifier si le nom de la ville est correct et réessayer : {e}")
