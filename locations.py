import utm
import folium

# Sample UTM coordinates: (Easting, Northing, Zone Number, Zone Letter)
utm_coords = [
    (500000, 4649776, 33, 'T'),
    (400000, 4650000, 33, 'T'),
    (600000, 4649000, 33, 'T')
]

# Convert UTM to Latitude/Longitude
latlon_coords = [utm.to_latlon(easting, northing, zone_number, zone_letter)
                 for easting, northing, zone_number, zone_letter in utm_coords]

# Create a map centered at the first coordinate
m = folium.Map(location=latlon_coords[0], zoom_start=10)

# Add markers for each coordinate
for lat, lon in latlon_coords:
    folium.CircleMarker(location=(lat, lon),
                        radius=6,
                        color='blue',
                        fill=True,
                        fill_color='blue',
                        fill_opacity=0.7).add_to(m)

# Save to HTML file
m.save("utm_map.html")
