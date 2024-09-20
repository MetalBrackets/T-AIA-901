import streamlit as st

st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Settings"]
)

import folium
from streamlit_folium import st_folium

# Une fonction pour simuler le retour de la réponse à la commande vocale
def process_voice_command(command):
    if "paris" in command.lower() and "marseille" in command.lower():
        return {
            "departure": "Marseille",
            "destination": "Paris",
            "optimized_route": [
                {"station": "Marseille", "lat": 43.296482, "lon": 5.36978},
                {"station": "Lyon", "lat": 45.764043, "lon": 4.835659},
                {"station": "Paris", "lat": 48.856614, "lon": 2.3522219}
            ]
        }
    else:
        return None

# Carte avec les trajets
def create_map(route):
    map_center = [(route[0]["lat"] + route[-1]["lat"]) / 2, (route[0]["lon"] + route[-1]["lon"]) / 2]
    travel_map = folium.Map(location=map_center, zoom_start=6)

    # Marqueurs et lignes de trajet
    for i in range(len(route)):
        folium.Marker([route[i]["lat"], route[i]["lon"]], popup=route[i]["station"]).add_to(travel_map)
        if i < len(route) - 1:
            folium.PolyLine(
                locations=[[route[i]["lat"], route[i]["lon"]], [route[i+1]["lat"], route[i+1]["lon"]]],
                color="blue"
            ).add_to(travel_map)

    return travel_map

# -------------------------------------------------------------
# Home page
# -------------------------------------------------------------
st.title("Travel Order Application")


# Création du bouton avec icône et texte
btn = st.button("🎙️ Entrez votre commande vocale")

if btn:
    st.success("Enregistrement en cours...")

# Commande vocale simulée (input texte pour démo)
command = st.text_input("Exemple : 'Je souhaite aller à Paris depuis Marseille'")

# Processus IA pour le trajet optimisé
if command:
    result = process_voice_command(command)
    if result:
        st.success(f"Optimized route from {result['departure']} to {result['destination']}:")
        
        # Afficher les informations du trajet
        for stop in result["optimized_route"]:
            st.write(f"Station: {stop['station']} (Lat: {stop['lat']}, Lon: {stop['lon']})")

        # Créer la carte avec le trajet optimisé
        travel_map = create_map(result["optimized_route"])
        st_folium(travel_map, width=700, height=500)
    else:
        st.error("No optimized route found for the given voice command.")
else:
    st.info("Please enter a voice command to see the optimized route.")
