import base64
import json
import os
import urllib.parse
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Bienvenido a Rôle",
    page_icon="🥮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Helper para convertir imágenes locales a Base64 e inyectarlas en HTML
def get_base64_image(image_path: str) -> str:
    if os.path.exists(image_path):
        ext = image_path.split(".")[-1].lower()
        mime = "png" if ext == "png" else "jpeg"
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/{mime};base64,{encoded}"
    return ""


# Cargar imágenes locales desde assets/
IMG_LOGO_OFICIAL = get_base64_image("assets/logo_oficial.jpg")
IMG_BANNER_HERO = get_base64_image("assets/banner_hero.jpg")
IMG_LOGO_TEXTO = get_base64_image("assets/logo_texto.jpg")
IMG_ESPIRAL = get_base64_image("assets/images/espiral.png")

# ==========================================
# 2. ESTILOS CSS - DISEÑO OSCURO PREMIUM
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Reset global */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #071220 !important;
        color: #F1F5F9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent !important; }
    #MainMenu, footer { visibility: hidden; }

    /* PANTALLA DE LOGIN / PORTADA */
    .login-container {
        max-width: 500px;
        margin: 2rem auto;
        background-color: #0A1B2E;
        border: 1px solid #1A3656;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }

    .login-logo {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #D48B38;
        box-shadow: 0 0 25px rgba(212, 139, 56, 0.3);
        margin-bottom: 1rem;
    }

    /* BARRA NAVEGACIÓN SUPERIOR */
    .role-navbar {
        background-color: #0B1A2D;
        border-bottom: 1px solid #162C46;
        padding: 0.8rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .nav-logo-img {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        object-fit: cover;
        border: 1px solid #D48B38;
    }

    /* BARRA DE ESTADO DEL PAQUETE */
    .role-subbar {
        background-color: #091626;
        border-bottom: 1px solid #13243A;
        padding: 0.6rem 2rem;
        font-size: 0.85rem;
        color: #94A3B8;
    }

    /* BANNER HERO Y SECCIÓN CENTRAL */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: radial-gradient(circle at center, #0F2540 0%, #071220 75%);
    }

    .hero-logo-img {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #D48B38;
        box-shadow: 0 0 35px rgba(212, 139, 56, 0.4);
        margin-bottom: 1.2rem;
    }

    .badge-artesanal {
        display: inline-block;
        background-color: #0E253F;
        border: 1px solid #1E3E66;
        color: #D48B38;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-heading {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
    }

    .hero-heading span {
        font-style: italic;
        color: #D48B38;
        font-weight: 400;
    }

    .banner-hero-box {
        width: 100%;
        max-width: 900px;
        height: 320px;
        margin: 0 auto 2rem auto;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #1A3656;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .banner-hero-box img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* TARJETA DE MISIÓN */
    .mission-card {
        background-color: #0A1B2E;
        border: 1px solid #1A3656;
        border-radius: 16px;
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto 2rem auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .mission-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
    }

    .mission-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFFFFF;
    }

    .mission-body {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    /* CARACTERÍSTICAS */
    .feature-box {
        background-color: #0D223A;
        border: 1px solid #183354;
        border-radius: 10px;
        padding: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 12px;
        height: 100%;
    }

    .feature-icon-wrapper {
        background-color: #122B48;
        color: #D48B38;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #1E3E66;
        font-size: 18px;
    }

    .feature-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .feature-desc {
        font-size: 0.78rem;
        color: #94A3B8;
        line-height: 1.3;
    }

    /* BOTONES */
    .stButton>button {
        background-color: #102742 !important;
        color: #F1F5F9 !important;
        border: 1px solid #1E3E66 !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #D48B38 !important;
        color: #071220 !important;
        border-color: #D48B38 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

USER_FILE = "usuarios.json"
WHATSAPP_NUMBER = "5493530000000"


# ==========================================
# 3. MANEJO DE USUARIOS (PERSISTENCIA)
# ==========================================
def load_users():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"registrados": [], "invitados": []}


def save_user(user_data: dict, is_registered: bool):
    data = load_users()
    key = "registrados" if is_registered else "invitados"

    existing_index = -1
    for idx, u in enumerate(data[key]):
        if is_registered and u.get("telefono") == user_data.get("telefono"):
            existing_index = idx
            break
        elif not is_registered and u.get("id") == user_data.get("id"):
            existing_index = idx
            break

    if existing_index >= 0:
        data[key][existing_index] = user_data
    else:
        data[key].append(user_data)

    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ==========================================
# 4. DATOS DE PAQUETES Y PRODUCTOS
# ==========================================
PACKAGES = [
    {
        "id": "pack-3",
        "name": "Paquete Inicial",
        "unitRangeLabel": "3 productos",
        "minCount": 3,
        "itemCount": 3,
        "price": 12500,
        "description": "Ideal para disfrutar una degustación personal.",
    },
    {
        "id": "pack-6",
        "name": "Paquete Intermedio",
        "unitRangeLabel": "6 productos",
        "minCount": 6,
        "itemCount": 6,
        "price": 23000,
        "description": "La combinación ideal para compartir meriendas en familia.",
    },
    {
        "id": "pack-10",
        "name": "Paquete Familiar",
        "unitRangeLabel": "10 productos",
        "minCount": 10,
        "itemCount": 10,
        "price": 36000,
        "description": "Para eventos o fanáticos de la panificación artesanal.",
    },
]

PRODUCTS = [
    {
        "id": "r1",
        "name": "Roll de Canela Clásico",
        "category": "Rolls Dulces",
        "price": 4200,
        "desc": "Masa fermentada esponjosa con especias y glacé suave.",
        "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&auto=format&fit=crop&q=80",
    },
    {
        "id": "r2",
        "name": "Roll de Dulce de Leche y Nueces",
        "category": "Rolls Dulces",
        "price": 4500,
        "desc": "Relleno abundante de dulce de leche artesanal y crocante de nuez.",
        "image": "https://images.unsplash.com/photo-1583338917451-ace27954e268?w=400&auto=format&fit=crop&q=80",
    },
    {
        "id": "r3",
        "name": "Pan de Campo de Masa Madre",
        "category": "Panadería",
        "price": 3900,
        "desc": "Fermentación lenta de 24 hs, miga alveolada y corteza crocante.",
        "image": "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?w=400&auto=format&fit=crop&q=80",
    },
    {
        "id": "r4",
        "name": "Croissant de Mantequilla",
        "category": "Repostería",
        "price": 3500,
        "desc": "Hojaldrado perfecto con manteca de primera calidad.",
        "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&auto=format&fit=crop&q=80",
    },
]

# ==========================================
# 5. ESTADO DE SESIÓN E INICIALIZACIÓN
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_session" not in st.session_state:
    st.session_state.user_session = None

if "selected_package" not in st.session_state:
    st.session_state.selected_package = PACKAGES[1]

if "cart" not in st.session_state:
    st.session_state.cart = {}


def get_total_cart_count():
    return sum(st.session_state.cart.values())


def get_whatsapp_link():
    session = st.session_state.user_session or {}
    pkg = st.session_state.selected_package
    cart = st.session_state.cart
    user = session.get("user", {})

    msg = ["🌀 *NUEVO PEDIDO EN RÔLE REPOSTERÍA*\n"]
    msg.append(f"👤 *Cliente:* {user.get('nombre', 'N/A')}")
    if user.get("telefono"):
        msg.append(f"📱 *Teléfono:* {user.get('telefono')}")
    msg.append(
        f"🏷️ *Tipo:* {'Cuenta Registrada' if session.get('mode') == 'registered' else 'Invitado'}\n"
    )

    if pkg:
        msg.append(f"📦 *Paquete:* {pkg['name']} ({pkg['unitRangeLabel']})")

    msg.append("\n📋 *Detalle de Productos:*")
    for p in PRODUCTS:
        qty = cart.get(p["id"], 0)
        if qty > 0:
            msg.append(f"• {qty}x {p['name']}")

    msg.append(f"\n💰 *Total Paquete:* ${pkg['price']:,}")
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote('\n'.join(msg))}"


# ==========================================
# 6. PANTALLA DE ACCESO INICIAL (GATEWAY)
# ==========================================
if not st.session_state.authenticated:
    # Usamos la imagen de la espiral en la tarjeta de login
    logo_src = (
        IMG_ESPIRAL
        if IMG_ESPIRAL
        else "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"
    )

    st.markdown("<br/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        st.markdown(
            f"""
            <div class="login-container">
                <img src="{logo_src}" class="login-logo" alt="Rôle Logo" />
                <h1 style="font-family: 'Playfair Display', serif; color: #FFFFFF; margin-bottom: 1rem; margin-left: 30px; font-size:2.2rem;">Bienvenido a Rôle</h1>
                <p style="color: #D48B38; font-size: 0.85rem; font-weight: 600; letter-spacing: 1.5px; margin-bottom: 1.5rem; margin-top: 0.5rem;">PANADERÍA Y REPOSTERÍA ARTESANAL</p>
                <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 1.5rem;">Elige cómo deseas ingresar para realizar tu pedido</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab_cuenta, tab_invitado = st.tabs(
            ["🔑 Con Cuenta Propia", "👤 Entrar como Invitado"]
        )

        with tab_cuenta:
            st.write("")
            with st.form("form_login"):
                nombre = st.text_input(
                    "Nombre y Apellido", placeholder="Ej: Juan Pérez"
                )
                telefono = st.text_input(
                    "Teléfono / WhatsApp", placeholder="Ej: 3534123456"
                )
                submit = st.form_submit_button(
                    "Ingresar con mi Cuenta", use_container_width=True
                )

                if submit:
                    if nombre.strip() and telefono.strip():
                        user_data = {
                            "nombre": nombre.strip(),
                            "telefono": telefono.strip(),
                        }
                        save_user(user_data, is_registered=True)
                        st.session_state.user_session = {
                            "mode": "registered",
                            "user": user_data,
                        }
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error(
                            "Por favor completa tu nombre y teléfono para ingresar."
                        )

        with tab_invitado:
            st.write("")
            st.info(
                "Puedes explorar el catálogo y armar tu caja como invitado. Solo te pediremos un nombre al enviar la orden."
            )
            nombre_invitado = st.text_input(
                "Nombre rápido (opcional)",
                placeholder="Ej: Invitado",
                key="input_guest",
            )

            if st.button("Continuar como Invitado ➔", use_container_width=True):
                nombre_final = (
                    nombre_invitado.strip() if nombre_invitado.strip() else "Invitado"
                )
                user_data = {"id": f"guest_{os.urandom(3).hex()}", "nombre": nombre_final}
                save_user(user_data, is_registered=False)
                st.session_state.user_session = {
                    "mode": "guest",
                    "user": user_data,
                }
                st.session_state.authenticated = True
                st.rerun()

    st.stop()


# ==========================================
# 7. DIÁLOGOS (MODALES)
# ==========================================
@st.dialog("👤 Perfil de Usuario")
def show_auth_dialog():
    session = st.session_state.user_session or {}
    user = session.get("user", {})
    mode = session.get("mode", "guest")

    st.write(
        f"Modo actual: **{'Cuenta Registrada' if mode == 'registered' else 'Invitado'}**"
    )

    with st.form("form_update_user"):
        nombre = st.text_input("Nombre", value=user.get("nombre", ""))
        telefono = st.text_input("Teléfono / WhatsApp", value=user.get("telefono", ""))
        if st.form_submit_button("Guardar Cambios", use_container_width=True):
            user_data = {"nombre": nombre, "telefono": telefono}
            save_user(user_data, is_registered=(mode == "registered"))
            st.session_state.user_session["user"] = user_data
            st.success("Datos actualizados.")
            st.rerun()

    st.divider()
    if st.button("🚪 Cerrar Sesión / Cambiar de Usuario", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_session = None
        st.rerun()


@st.dialog("🛒 Tu Caja de Selección Rôle", width="large")
def show_cart_dialog():
    pkg = st.session_state.selected_package
    cart = st.session_state.cart
    total_units = get_total_cart_count()
    target_quota = pkg["itemCount"]

    st.subheader(f"Caja Seleccionada: {pkg['name']}")
    st.write(f"Estado: **{total_units} de {target_quota} productos en tu caja**")
    st.progress(min(1.0, total_units / target_quota))

    st.divider()

    if total_units == 0:
        st.info("Tu caja está vacía. Elige tus productos abajo.")
    else:
        st.write("### Productos en la caja:")
        for prod in PRODUCTS:
            qty = cart.get(prod["id"], 0)
            if qty > 0:
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{prod['name']}**")
                c2.write(f"Unidades: **{qty}**")

        st.divider()
        st.markdown(f"### Total del Paquete: **${pkg['price']:,}**")

        if total_units < pkg["minCount"]:
            st.warning(
                f"Debes completar el mínimo de {pkg['minCount']} productos para enviar tu pedido."
            )
        else:
            wa_url = get_whatsapp_link()
            st.markdown(
                f"""
                <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #D48B38; color: #071220; padding: 14px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.1rem; margin-top: 15px;">
                        📲 Enviar Pedido directo por WhatsApp
                    </div>
                </a>
                """,
                unsafe_allow_html=True,
            )


# ==========================================
# 8. BARRA DE NAVEGACIÓN PRINCIPAL
# ==========================================
current_user = st.session_state.user_session.get("user", {})
user_name = current_user.get("nombre", "Invitado")
is_guest = st.session_state.user_session.get("mode") == "guest"
current_cart_count = get_total_cart_count()
target_quota = st.session_state.selected_package["itemCount"]

logo_nav_src = (
    IMG_ESPIRAL
    if IMG_ESPIRAL
    else "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=100"
)

st.markdown(
    f"""
    <div class="role-navbar">
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="{logo_nav_src}" class="nav-logo-img" alt="Rôle Logo" />
            <div>
                <div style="font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #FFFFFF; letter-spacing: 2px; line-height: 1;">RÔLE</div>
                <div style="font-size: 0.65rem; color: #D48B38; letter-spacing: 1.5px; font-weight: 600;">LO MEJOR EN CADA UNO</div>
            </div>
        </div>
        <div style="display: flex; gap: 2rem; color: #CBD5E1; font-size: 0.9rem; font-weight: 500;">
            <a href="#mision" style="color: inherit; text-decoration: none;">Misión & Historia</a>
            <a href="#paquetes" style="color: inherit; text-decoration: none;">Oferta de Paquetes</a>
            <a href="#productos" style="color: inherit; text-decoration: none;">Catálogo de Productos</a>
        </div>
        <div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_c1, top_c2 = st.columns([5, 1])
with top_c2:
    col_u, col_c = st.columns(2)
    with col_u:
        label_user = (
            f"👤 {user_name[:10]}..."
            if len(user_name) > 10
            else f"👤 {user_name}"
        )
        if is_guest:
            label_user += " (Inv)"
        if st.button(label_user):
            show_auth_dialog()
    with col_c:
        if st.button(f"🛒 Caja {current_cart_count}/{target_quota}"):
            show_cart_dialog()

# ==========================================
# 9. SUB-BARRA DE ESTADO DEL PAQUETE
# ==========================================
pkg_active_name = st.session_state.selected_package["name"]
st.markdown(
    f"""
    <div class="role-subbar">
        <div>📦 <strong>{pkg_active_name}:</strong> {current_cart_count} de {target_quota} productos en tu caja</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 10. SECCIÓN HERO CENTRAL CON LOGO OFICIAL
# ==========================================
logo_official_src = (
    IMG_LOGO_OFICIAL
    if IMG_LOGO_OFICIAL
    else "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300"
)

st.markdown(
    f"""
    <div class="hero-container">
        <img src="{logo_official_src}" class="hero-logo-img" alt="Emblema Rôle" />
        <br />
        <div class="badge-artesanal">✨ REPOSTERÍA & PANADERÍA ARTESANAL</div>
        <h1 class="hero-heading">Descubre el arte de cada <span>Rôle</span></h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# BANNER MOSTRANDO LA MESA ARTESANAL
if IMG_BANNER_HERO:
    st.markdown(
        f"""
        <div class="banner-hero-box">
            <img src="{IMG_BANNER_HERO}" alt="Mesa Artesanal Rôle" />
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# 11. TARJETA DE NUESTRA MISIÓN
# ==========================================
logo_text_src = (
    IMG_LOGO_TEXTO
    if IMG_LOGO_TEXTO
    else "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=100"
)

st.markdown('<div id="mision"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="mission-card">
        <div class="mission-header">
            <img src="{logo_text_src}" style="height: 35px; border-radius: 4px;" alt="Rôle Paris Logo" />
            <div class="mission-title">Nuestra Misión</div>
        </div>
        <div class="mission-body">
            Brinda panificación y repostería a la labor del cliente mediante la venta online de producto contenidos en paquetes diversos, de calidad artesanal a precio moderado, para el consumo diario, con el objetivo de satisfacer la demanda de desayunos y meriendas de la población de Villa María.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tres Tarjetas de Características
feat_c1, feat_c2, feat_c3 = st.columns(3)

with feat_c1:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-icon-wrapper">🔥</div>
            <div>
                <div class="feature-title">MASA FERMENTADA</div>
                <div class="feature-desc">Masa fermentada para una textura esponjosa y digerible.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat_c2:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-icon-wrapper">🍃</div>
            <div>
                <div class="feature-title">INGREDIENTES REALES</div>
                <div class="feature-desc">Ingredientes de calidad en el mercado.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feat_c3:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-icon-wrapper">🧡</div>
            <div>
                <div class="feature-title">ARMA A TU GUSTO</div>
                <div class="feature-desc">Elige exactamente qué rolls incluir en tu paquete personalizado.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.divider()

# ==========================================
# 12. SECCIÓN DE PAQUETES
# ==========================================
st.markdown('<div id="paquetes"></div>', unsafe_allow_html=True)
st.markdown(
    '<h2 style="text-align: center; color: #FFFFFF; font-family: \'Playfair Display\', serif;">Oferta de Paquetes</h2>',
    unsafe_allow_html=True,
)
st.write("")

pkg_cols = st.columns(3)
for idx, pkg in enumerate(PACKAGES):
    with pkg_cols[idx]:
        is_sel = st.session_state.selected_package["id"] == pkg["id"]
        st.markdown(
            f"""
            <div style="background-color: {'#0E2540' if is_sel else '#0A1B2E'}; border: 2px solid {'#D48B38' if is_sel else '#1A3656'}; border-radius: 16px; padding: 1.5rem; text-align: center;">
                <h3 style="color: {'#D48B38' if is_sel else '#FFFFFF'}; margin-bottom: 5px;">{pkg['name']}</h3>
                <h2 style="color: #FFFFFF; margin: 10px 0;">${pkg['price']:,}</h2>
                <p style="color: #94A3B8; font-size: 0.85rem;">{pkg['unitRangeLabel']}</p>
                <p style="color: #CBD5E1; font-size: 0.8rem;">{pkg['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"{'✓ Seleccionado' if is_sel else 'Elegir Paquete'}",
            key=f"pkg_{pkg['id']}",
            use_container_width=True,
        ):
            st.session_state.selected_package = pkg
            st.rerun()

st.divider()

# ==========================================
# 13. CATÁLOGO DE PRODUCTOS
# ==========================================
st.markdown('<div id="productos"></div>', unsafe_allow_html=True)
st.markdown(
    '<h2 style="text-align: center; color: #FFFFFF; font-family: \'Playfair Display\', serif;">Catálogo de Productos</h2>',
    unsafe_allow_html=True,
)
st.write("")

prod_cols = st.columns(2)
for idx, prod in enumerate(PRODUCTS):
    col_i = idx % 2
    with prod_cols[col_i]:
        c_qty = st.session_state.cart.get(prod["id"], 0)

        st.image(prod["image"], use_container_width=True)
        st.markdown(f"### {prod['name']}")
        st.caption(f"Categoría: {prod['category']}")
        st.write(f"*{prod['desc']}*")

        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            if st.button("➖", key=f"dec_{prod['id']}"):
                if c_qty > 0:
                    st.session_state.cart[prod["id"]] = c_qty - 1
                    st.rerun()
        with b2:
            st.markdown(
                f"<h4 style='text-align: center; margin: 0; color: #FFFFFF;'>{c_qty}</h4>",
                unsafe_allow_html=True,
            )
        with b3:
            if st.button("➕", key=f"inc_{prod['id']}"):
                if current_cart_count < target_quota:
                    st.session_state.cart[prod["id"]] = c_qty + 1
                    st.rerun()
                else:
                    st.warning("Alcanzaste el límite de tu paquete.")

st.divider()

# ==========================================
# 14. PIE DE PÁGINA
# ==========================================
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 2rem 0;">
        <p>© 2026 Rôle Repostería & Panadería Artesanal - Villa María, Córdoba.</p>
    </div>
    """,
    unsafe_allow_html=True,
)