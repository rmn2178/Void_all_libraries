import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =================================================================
# 1. CORE ASTRONOMICAL DATA (REALISTIC SCALING)
# =================================================================
# Distance in AU (scaled for visibility), Radius in relative units
# Colors based on high-res NASA spectral data
DATA = {
    "Sun": {"r": 8.0, "d": 0, "color": "#FFCC33", "period": 1, "tilt": 0, "atmo": True},
    "Mercury": {"r": 0.8, "d": 15.1, "color": "#A5A5A5", "period": 0.24, "tilt": 0.03, "atmo": False},
    "Venus": {"r": 1.4, "d": 21.3, "color": "#E3BB76", "period": 0.62, "tilt": 177.3, "atmo": True},
    "Earth": {"r": 1.5, "d": 30.0, "color": "#1F77B4", "period": 1.00, "tilt": 23.4, "atmo": True},
    "Mars": {"r": 1.1, "d": 38.2, "color": "#B22222", "period": 1.88, "tilt": 25.2, "atmo": False},
    "Jupiter": {"r": 4.5, "d": 55.4, "color": "#D39C7E", "period": 11.8, "tilt": 3.1, "atmo": True},
    "Saturn": {"r": 3.8, "d": 75.6, "color": "#C5AB6E", "period": 29.4, "tilt": 26.7, "atmo": True},
    "Uranus": {"r": 2.5, "d": 95.8, "color": "#B5E3E3", "period": 84.0, "tilt": 97.8, "atmo": True},
    "Neptune": {"r": 2.4, "d": 110.2, "color": "#4B70DD", "period": 164.8, "tilt": 28.3, "atmo": True}
}


# =================================================================
# 2. PHYSICS & GEOMETRY ENGINE
# =================================================================

def create_sphere_mesh(radius, distance, res=80):
    """Generates high-resolution parametric coordinates for a sphere."""
    phi = np.linspace(0, 2 * np.pi, res)
    theta = np.linspace(0, np.pi, res)
    phi, theta = np.meshgrid(phi, theta)

    x = radius * np.sin(theta) * np.cos(phi) + distance
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)
    return x, y, z


def apply_axial_tilt(x, y, z, center_x, tilt_deg):
    """Rotates vertex data to match real axial tilt."""
    rad = np.radians(tilt_deg)
    x_rel = x - center_x
    x_rot = x_rel * np.cos(rad) + z * np.sin(rad)
    z_rot = -x_rel * np.sin(rad) + z * np.cos(rad)
    return x_rot + center_x, y, z_rot


def generate_surface_texture(name, x_shape):
    """Procedural texture generation for planetary surfaces."""
    if name in ["Jupiter", "Saturn"]:
        # Latitudinal gas bands
        return np.tile(np.sin(np.linspace(0, 20, x_shape[0])), (x_shape[1], 1)).T
    elif name == "Sun":
        # Plasma turbulence
        return np.random.rand(*x_shape) * 0.15
    else:
        # Stochastic terrain simulation
        return np.random.normal(0, 0.1, size=x_shape)


# =================================================================
# 3. TRACE BUILDERS
# =================================================================

def build_planet(name, specs):
    """Builds the primary surface mesh for a planet."""
    x, y, z = create_sphere_mesh(specs['r'], specs['d'])
    x, y, z = apply_axial_tilt(x, y, z, specs['d'], specs['tilt'])
    tex = generate_surface_texture(name, x.shape)

    # Lighting engine parameters
    lighting = dict(ambient=0.5, diffuse=0.8, roughness=0.6, specular=0.1, fresnel=0.4)

    return go.Surface(
        x=x, y=y, z=z,
        surfacecolor=tex,
        colorscale=[[0, specs['color']], [1, 'black' if name != "Sun" else 'white']],
        showscale=False, name=name, hoverinfo='name', lighting=lighting
    )


def build_saturn_rings(dist, r_planet):
    """Generates complex multi-band rings with valid colorscale."""
    r_in, r_out = r_planet + 1.5, r_planet + 5.5
    r_coords = np.linspace(r_in, r_out, 40)
    theta_coords = np.linspace(0, 2 * np.pi, 200)
    R, T = np.meshgrid(r_coords, theta_coords)

    # Interference pattern for Cassini Division simulation
    ring_tex = np.sin(R * 12)

    # Using 'earth' or a custom scale instead of 'Tau'
    custom_scale = [[0, "#4b3d2b"], [0.5, "#c5ab6e"], [1, "#4b3d2b"]]

    return go.Surface(
        x=R * np.cos(T) + dist, y=R * np.sin(T), z=np.zeros_like(R),
        surfacecolor=ring_tex,
        colorscale=custom_scale,
        opacity=0.7, showscale=False, name="Saturn's Rings"
    )


# =================================================================
# 4. SCENE CONSTRUCTION
# =================================================================

fig = go.Figure()

# 4.1 Starfield (1,800 points)
stars_x, stars_y, stars_z = [np.random.uniform(-350, 350, 1800) for _ in range(3)]
fig.add_trace(go.Scatter3d(
    x=stars_x, y=stars_y, z=stars_z, mode='markers',
    marker=dict(size=1.3, color='white', opacity=0.7), name="Deep Space"
))

# 4.2 Build Bodies
nav_buttons = [
    dict(label="System Overview", method="relayout", args=[{"scene.camera.eye": {"x": 1.7, "y": 1.7, "z": 1.2}}])]

for name, specs in DATA.items():
    # Orbit Path
    if specs['d'] > 0:
        t_orbit = np.linspace(0, 2 * np.pi, 350)
        fig.add_trace(go.Scatter3d(
            x=specs['d'] * np.cos(t_orbit), y=specs['d'] * np.sin(t_orbit), z=np.zeros(350),
            mode='lines', line=dict(color='rgba(255,255,255,0.08)', width=1.2), showlegend=False
        ))

    # Planet / Sun Surface
    fig.add_trace(build_planet(name, specs))

    # Atmospheric Haze (Blue marble/Venusian glow)
    if specs.get('atmo') and name != "Sun":
        ax, ay, az = create_sphere_mesh(specs['r'] * 1.08, specs['d'], res=45)
        fig.add_trace(
            go.Surface(x=ax, y=ay, z=az, opacity=0.12, colorscale=[[0, specs['color']], [1, 'white']], showscale=False,
                       name=f"{name} Haze"))

    # Special Case: The Sun's Burning Corona
    if name == "Sun":
        for i in [1.2, 1.5]:
            sx, sy, sz = create_sphere_mesh(specs['r'] * i, 0, res=35)
            fig.add_trace(
                go.Surface(x=sx, y=sy, z=sz, opacity=0.08, colorscale='solar', showscale=False, name="Solar Flare"))

    # Special Case: Saturn's Rings
    if name == "Saturn":
        fig.add_trace(build_saturn_rings(specs['d'], specs['r']))

    # Navigation HUD Update
    nav_buttons.append(dict(
        label=f"Fly to: {name}",
        method="relayout",
        args=[{"scene.camera.center": {"x": specs['d'] / 220, "y": 0, "z": 0},
               "scene.camera.eye": {"x": (specs['d'] / 220) + 0.12, "y": 0.12, "z": 0.08}}]
    ))

# =================================================================
# 5. DYNAMIC UI & RENDER
# =================================================================

fig.update_layout(
    title=dict(
        text=f"<b>REALISTIC INTERACTIVE ORBITER v3.0</b><br>Simulation Epoch: {datetime.now().strftime('%Y')}",
        font=dict(family="Verdana", size=20, color="#FFFFFF"), x=0.05, y=0.95
    ),
    updatemenus=[dict(
        buttons=nav_buttons, direction="down", showactive=True,
        x=0.05, y=0.88, bgcolor="rgba(30,30,30,0.8)", font=dict(color="white")
    )],
    scene=dict(
        xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
        bgcolor="black", aspectmode='data'
    ),
    paper_bgcolor="black", margin=dict(l=0, r=0, b=0, t=0), height=950,
    showlegend=False
)

fig.show()