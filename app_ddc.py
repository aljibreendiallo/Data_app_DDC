import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from io import BytesIO
import plotly.express as px
import base64
import time
import os

# --- Configuration de la page ---
st.set_page_config(
    page_title="DDC – Smart Data Cleaner 🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS & HTML Styling Avancé ---
st.markdown("""
<style>
/* Fond animé en arrière-plan */
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    color: #e0e0ff;
    font-family: 'Segoe UI', sans-serif;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
/* Titre principal */
h1 {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00c8ff, #a64edd, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: 0.8px;
    text-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    animation: fadeInUp 1.2s ease-out forwards;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
/* Sous-titres */
h2, h3 {
    color: #ffffff;
    border-bottom: 2px solid #a64edd;
    padding-bottom: 0.4rem;
    margin-top: 1.8rem;
    font-weight: 600;
}
/* Sidebar stylisé */
.sidebar .sidebar-content {
    background: rgba(30, 30, 50, 0.95);
    backdrop-filter: blur(12px);
    border-right: 1px solid #4a4a60;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
}
/* Icônes dans le menu */
.option-menu .option-menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 15px;
    border-radius: 10px;
    margin-bottom: 6px;
    transition: all 0.3s ease;
    font-weight: 500;
}
.option-menu .option-menu-item:hover {
    background: rgba(166, 78, 221, 0.3);
    transform: translateX(4px);
}
.option-menu .option-menu-item.active {
    background-color: #00c8ff;
    color: white;
    font-weight: 700;
}
/* Boutons stylisés */
.stButton>button {
    background: linear-gradient(90deg, #00c8ff, #a64edd);
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 1rem;
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(166, 78, 221, 0.4);
    transition: all 0.3s ease;
    font-weight: 600;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(166, 78, 221, 0.5);
}
/* Téléchargement stylisé */
.stDownloadButton>button {
    background: linear-gradient(90deg, #2ecc71, #3498db);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    margin-top: 10px;
}
/* Input / Select custom */
.stSelectbox > div > div,
.stMultiselect > div > div {
    background-color: #2a2a40 !important;
    border: 1px solid #4a4a60 !important;
    border-radius: 10px !important;
    color: #e0e0ff !important;
}
/* Dataframe stylisé */
.dataframe {
    background-color: #252535;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid #4a4a60;
}
.dataframe th {
    background: linear-gradient(90deg, #00c8ff, #a64edd);
    color: white;
    font-weight: 600;
    text-align: center;
    padding: 14px 18px;
}
.dataframe td {
    padding: 10px 16px;
    text-align: center;
}
/* Messages d'alerte */
.stAlert {
    border-radius: 12px;
    padding: 12px 16px;
    font-weight: 500;
}
.stAlert--success {
    background-color: rgba(46, 204, 113, 0.2);
    border: 1px solid #2ecc71;
    color: #2ecc71;
}
.stAlert--warning {
    background-color: rgba(243, 156, 18, 0.2);
    border: 1px solid #f39c12;
    color: #f39c12;
}
/* Responsive */
@media (max-width: 768px) {
    h1 {
        font-size: 2.4rem;
    }
    .stButton>button {
        padding: 10px 20px;
        font-size: 0.9rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --- Icônes SVG personnalisées ---
def icon_svg(icon_name):
    icons = {
        "home": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>',
        "clean": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M14 8h4a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-4"></path><path d="M12 14v-2"></path><path d="M10 14h4"></path><path d="M12 18v-2"></path><path d="M10 18h4"></path></svg>',
        "dashboard": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>',
        "eda": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>',
        "chart": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>',
        "download": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>',
        "info": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
    }
    return icons.get(icon_name, "")


# --- Vérification de connexion ---
def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Connexion requise")
        st.markdown("Veuillez vous connecter pour accéder à l'application.")

        email = st.text_input("📧 Email", value="")
        password = st.text_input("🔒 Mot de passe", type="password")

        if st.button("Se connecter"):
            if email == "ddc@unchk.edu.sn" and password == "DDC@DDC":
                st.session_state.logged_in = True
                st.success("✅ Connexion réussie !")
                st.rerun()
            else:
                st.error("❌ Email ou mot de passe incorrect.")
        st.stop()


# --- Bouton de déconnexion ---
def show_logout():
    if st.sidebar.button("🔓 Se déconnecter"):
        st.session_state.logged_in = False
        st.session_state.df = None
        st.session_state.cleaned_data = None
        st.rerun()


# --- Vérifier la connexion ---
check_login()

# --- Barre latérale navigation ---
with st.sidebar:
    show_logout()
    selected = option_menu(
        "📊 DDC – Smart Data Cleaner",
        [
            "🏠 Accueil",
            "🧹 Nettoyage",
            "📊 Tableau de bord",
            "📊 EDA",
            "📈 Visualisation",
            "🧩 Tableau Croisé",
            "💾 Téléchargement",
            "ℹ️ À propos"
        ],
        icons=[
            icon_svg("home"),
            icon_svg("clean"),
            icon_svg("dashboard"),
            icon_svg("eda"),
            icon_svg("chart"),
            '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M3 12h18M4 4l16 16M4 20L20 4"></path></svg>',
            icon_svg("download"),
            icon_svg("info")
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "10px"},
            "nav-link": {"font-size": "1rem", "margin": "5px", "padding": "8px 12px"},
            "nav-link-selected": {
                "background-color": "#00c8ff",
                "color": "white",
                "font-weight": "bold"
            }
        }
    )

# --- Stockage des données ---
if "df" not in st.session_state:
    st.session_state.df = None
if "cleaned_data" not in st.session_state:
    st.session_state.cleaned_data = None

# --- Page Accueil ---
if selected == "🏠 Accueil":
    st.title("🎯 Welcome to the DDC Data Cleaner – Easily Clean and Analyze Your Data 🌟")
    st.markdown("""
    <div style='text-align:center; font-size:1.2rem; color:#b0b0d0; margin-bottom:2rem;'>
        L'application ultime pour nettoyer, analyser et visualiser vos données en un clin d'œil.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    ✅ Fonctionnalités :
    - 📥 Importer CSV / Excel
    - 🧹 Nettoyage intelligent (strip, minuscule, majuscule)
    - 🗑️ Suppression des doublons
    - 🔍 Filtres interactifs
    - 📊 Analyse exploratoire complète
    - 📈 Graphiques interactifs
    - 💾 Exporter en CSV, Excel
    - 🎨 Design moderne & responsive
    """, unsafe_allow_html=True)
    st.image("https://tse4.mm.bing.net/th/id/OIP.y2BQlvbMxYZ2cX3DVhgUOAHaFj?rs=1&pid=ImgDetMain&o=7&rm=3", use_container_width=True)
    if os.path.exists("mon_image.png"):
        st.image("mon_image.png", use_container_width=True)
    else:
        st.warning("L’image locale 'mon_image.png' est introuvable.")

# --- Page Nettoyage ---
if selected == "🧹 Nettoyage":
    st.header("🧹 Nettoyage des données")
    uploaded_file = st.file_uploader("📤 Importer un fichier CSV ou Excel", type=["csv", "xlsx"], key="upload_clean")
    if uploaded_file:
        with st.spinner("🔄 Chargement du fichier..."):
            time.sleep(0.8)
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state.df = df
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier : {e}")
                df = None

        if df is not None:
            st.success(f"✅ Fichier chargé avec succès ! {df.shape[0]} lignes et {df.shape[1]} colonnes.")
            n_duplicates = df.duplicated().sum()
            st.info(f"📋 Nombre total de doublons détectés : **{n_duplicates}** sur {df.shape[0]} lignes.")
            st.dataframe(df.head(10), use_container_width=True)

            st.subheader("🔧 Paramètres de nettoyage")
            object_cols = df.select_dtypes(include=['object']).columns.tolist()
            if not object_cols:
                st.warning("Aucune colonne textuelle détectée.")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    strip_cols = st.multiselect("✂️ Supprimer les espaces", object_cols, help="Supprime les espaces au début et à la fin")
                with col2:
                    lower_cols = st.multiselect("🔡 Minuscules", [c for c in object_cols if c not in strip_cols], help="Convertit en minuscules")
                with col3:
                    upper_cols = st.multiselect("🔠 Majuscules", [c for c in object_cols if c not in strip_cols + lower_cols], help="Convertit en majuscules")

            st.subheader("🗑️ Suppression des doublons")
            dup_cols = st.multiselect(
                "Colonnes pour détecter les doublons",
                df.columns.tolist(),
                default=df.columns.tolist() if n_duplicates > 0 else [],
                help="Les doublons seront supprimés en se basant sur ces colonnes"
            )
            if st.button("🧹 Appliquer le nettoyage", key="clean_btn"):
                df_clean = df.copy()
                for col in strip_cols:
                    df_clean[col] = df_clean[col].astype(str).str.strip()
                for col in lower_cols:
                    df_clean[col] = df_clean[col].astype(str).str.lower()
                for col in upper_cols:
                    df_clean[col] = df_clean[col].astype(str).str.upper()
                if len(dup_cols) > 0:
                    before = len(df_clean)
                    df_clean = df_clean.drop_duplicates(subset=dup_cols, keep='first')
                    after = len(df_clean)
                    st.success(f"🗑️ Doublons supprimés : {before - after} lignes retirées.")
                st.session_state.cleaned_data = df_clean
                st.success(f"🧹 Nettoyage terminé ! {df_clean.shape[0]} lignes restantes.")
                st.dataframe(df_clean.head(10), use_container_width=True)
    else:
        st.info("⬆️ Importez un fichier pour commencer.")

# --- Page Tableau de bord ---
if selected == "📊 Tableau de bord":
    st.header("📊 Tableau de bord interactif")
    df = st.session_state.cleaned_data
    if df is not None:
        if st.button("🔁 Réinitialiser les filtres", key="reset_filters_dash"):
            for key in list(st.session_state.keys()):
                if key.startswith("filter_") or key in ["global_search", "chart_type_dash", "cat_dash_chart"]:
                    del st.session_state[key]
            st.experimental_rerun()

        if 'filter_cols' not in st.session_state:
            st.session_state.filter_cols = df.columns.tolist()
        if 'global_search' not in st.session_state:
            st.session_state.global_search = ""

        cols = st.multiselect("📋 Colonnes à afficher", df.columns.tolist(), default=st.session_state.filter_cols)
        st.session_state.filter_cols = cols
        df_filtered = df[cols].copy()

        # 🔍 Recherche globale
        st.subheader("🔍 Recherche textuelle globale")
        global_search = st.text_input(
            "Rechercher dans toutes les colonnes texte",
            value=st.session_state.global_search,
            placeholder="Ex: 'paris', 'john'"
        )
        st.session_state.global_search = global_search
        if global_search:
            text_cols = df_filtered.select_dtypes(include=['object']).columns
            mask = pd.Series([False] * len(df_filtered))
            for col in text_cols:
                mask |= df_filtered[col].astype(str).str.contains(global_search, case=False, na=False)
            df_filtered = df_filtered[mask]

        # 🎛️ Filtres par colonne
        st.subheader("🎛️ Filtres par colonne")
        for col in cols:
            safe_key = col.replace(" ", "_").replace("'", "_").replace("(", "").replace(")", "")
            if df_filtered[col].dtype == 'object':
                unique_vals = df_filtered[col].dropna().astype(str).unique()
                unique_vals = sorted([x for x in unique_vals if x != 'nan'], key=str)
                st.multiselect(
                    f"🔤 {col}",
                    options=unique_vals,
                    default=st.session_state.get(f"filter_{safe_key}", []),
                    key=f"filter_{safe_key}"
                )
                selected_vals = st.session_state[f"filter_{safe_key}"]
                if selected_vals:
                    df_filtered = df_filtered[df_filtered[col].astype(str).isin(selected_vals)]
            elif df_filtered[col].dtype in ['int64', 'float64']:
                min_val, max_val = float(df_filtered[col].min()), float(df_filtered[col].max())
                st.slider(
                    f"🔢 {col}",
                    min_val, max_val,
                    st.session_state.get(f"range_{safe_key}", (min_val, max_val)),
                    key=f"range_{safe_key}"
                )
                range_val = st.session_state[f"range_{safe_key}"]
                df_filtered = df_filtered[
                    (df_filtered[col] >= range_val[0]) &
                    (df_filtered[col] <= range_val[1])
                ]

        # Affichage des résultats
        st.subheader(f"📋 Données filtrées ({df_filtered.shape[0]} lignes)")
        st.dataframe(df_filtered, use_container_width=True)

        # --- Visualisation interactive ---
        st.subheader("📊 Visualisation dynamique")
        cat_cols = df_filtered.select_dtypes(include='object').columns.tolist()
        if cat_cols:
            col_cat = st.selectbox("🧾 Choisissez une colonne catégorielle", cat_cols, key="cat_dash_chart")
            chart_type = st.radio("📉 Type de graphique", ["Diagramme en barres", "Camembert"], key="chart_type_dash")
            vc = df_filtered[col_cat].value_counts()
            if chart_type == "Diagramme en barres":
                fig = px.bar(
                    x=vc.index,
                    y=vc.values,
                    title=f"Distribution de '{col_cat}'",
                    labels={col_cat: "Catégorie", "y": "Nombre"},
                    color=vc.index,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
            else:
                fig = px.pie(
                    names=vc.index,
                    values=vc.values,
                    title=f"Distribution de '{col_cat}'",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e0e0ff",
                hovermode="x unified"
            )
            fig.update_traces(hovertemplate="<b>%{label}</b>: %{value} lignes")
            st.plotly_chart(fig, use_container_width=True)
            st.info("👉 Utilisez le bouton 📥 en haut à droite du graphique pour le télécharger.")
        else:
            st.info("Aucune colonne catégorielle disponible pour la visualisation.")

        # --- Téléchargement des données filtrées ---
        st.subheader("💾 Exporter les données filtrées")
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name='Données Filtrées')
        excel_data = excel_buffer.getvalue()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label=f"{icon_svg('download')} ⬇️ Télécharger en CSV",
                data=csv,
                file_name="donnees_filtrees.csv",
                mime="text/csv",
                key="dl_csv_filtre",
                help="Télécharge les données au format CSV",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label=f"{icon_svg('download')} 📊 Télécharger en Excel",
                data=excel_data,
                file_name="donnees_filtrees.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_excel_filtre",
                help="Télécharge les données filtrées au format Excel (.xlsx)",
                use_container_width=True
            )
    else:
        st.warning("⚠️ Veuillez d'abord nettoyer vos données.")

# --- Page EDA ---
if selected == "📊 EDA":
    st.header("📊 Analyse exploratoire des données (EDA)")
    df = st.session_state.cleaned_data
    if df is not None and not df.empty:
        st.subheader("🔍 Sélectionnez une ou plusieurs colonnes pour l'analyse")
        all_columns = df.columns.tolist()
        selected_cols = st.multiselect(
            "📋 Colonnes à analyser",
            options=all_columns,
            default=all_columns[:3] if len(all_columns) >= 3 else all_columns
        )
        if not selected_cols:
            st.info("Veuillez sélectionner au moins une colonne pour commencer l'analyse.")
        else:
            eda_data = []
            for col in selected_cols:
                with st.expander(f"📊 Analyse de : `{col}`", expanded=True):
                    col_type = df[col].dtype
                    n_unique = df[col].nunique()
                    n_missing = df[col].isna().sum()
                    n_total = len(df)
                    missing_pct = n_missing / n_total * 100
                    st.markdown(f"**Type :** `{col_type}` | **Uniques :** `{n_unique}`")
                    st.markdown(f"**Manquantes :** `{n_missing}` (`{missing_pct:.1f}%`)")
                    if pd.api.types.is_numeric_dtype(df[col]):
                        stats = {
                            "Min": df[col].min(),
                            "Max": df[col].max(),
                            "Moyenne": df[col].mean(),
                            "Écart-type": df[col].std(),
                            "Médiane": df[col].median()
                        }
                        for k, v in stats.items():
                            st.markdown(f"**{k} :** `{v:.2f}`" if isinstance(v, float) else f"**{k} :** `{v}`")
                        fig = px.histogram(
                            df,
                            x=col,
                            nbins=30,
                            title=f"Histogramme - {col}",
                            color_discrete_sequence=px.colors.qualitative.Bold
                        )
                        fig.update_layout(showlegend=False, font_color="#e0e0ff")
                        st.plotly_chart(fig, use_container_width=True)
                    elif pd.api.types.is_object_dtype(df[col]):
                        mode_val = df[col].mode()
                        mode_str = mode_val.iloc[0] if len(mode_val) > 0 else "Aucun"
                        st.markdown(f"**Mode :** `{mode_str}`")
                        top_vals = df[col].value_counts().head(10)
                        st.dataframe(top_vals.to_frame("Fréquence"), use_container_width=True)
                        fig = px.bar(
                            top_vals,
                            x=top_vals.index,
                            y=top_vals.values,
                            title=f"Top 10 - {col}",
                            labels={col: col, "y": "Fréquence"},
                            color=top_vals.index,
                            color_discrete_sequence=px.colors.qualitative.Bold
                        )
                        fig.update_layout(font_color="#e0e0ff")
                        st.plotly_chart(fig, use_container_width=True)
                    eda_data.append({
                        "Colonne": col,
                        "Type": str(col_type),
                        "Total": n_total,
                        "Uniques": n_unique,
                        "Manquantes": n_missing,
                        "% Manquants": round(missing_pct, 2),
                        "Min/Moyenne/Mode": stats["Min"] if pd.api.types.is_numeric_dtype(df[col]) else mode_str,
                        "Max/Exemple": stats["Max"] if pd.api.types.is_numeric_dtype(df[col]) else str(df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "—")
                    })
            # --- Télécharger le rapport EDA en Excel ---
            st.subheader("📥 Télécharger le rapport EDA en Excel")
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                summary_df = pd.DataFrame(eda_data)
                summary_df.to_excel(writer, sheet_name='Résumé EDA', index=False)
                missing_df = df[selected_cols].isna().sum().to_frame("Manquantes")
                missing_df["%"] = (missing_df["Manquantes"] / len(df)) * 100
                missing_df.to_excel(writer, sheet_name='Valeurs manquantes')
                df[selected_cols].head(100).to_excel(writer, sheet_name='Extrait données', index=False)
                workbook = writer.book
                worksheet = writer.sheets['Résumé EDA']
                worksheet.set_column("A:A", 18)
                worksheet.set_column("B:B", 12)
                worksheet.set_column("C:F", 14)
            excel_data = excel_buffer.getvalue()

            st.download_button(
                label=f"{icon_svg('download')} 📥 Télécharger le rapport EDA (Excel)",
                data=excel_data,
                file_name="rapport_eda.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="Télécharge un rapport complet avec statistiques, valeurs manquantes et extrait des données"
            )
    else:
        st.warning("⚠️ Veuillez importer et nettoyer un jeu de données d'abord.")

# --- Page Visualisation ---
if selected == "📈 Visualisation":
    st.header("📈 Visualisation Interactive")
    df = st.session_state.cleaned_data
    if df is not None:
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if cat_cols:
            col_cat = st.selectbox("🧾 Choisissez une colonne catégorielle", cat_cols, key="cat_col_visu")
            chart_type = st.radio("📉 Type de graphique", ["Barres", "Camembert"], key="chart_type_visu")
            if chart_type == "Barres":
                vc = df[col_cat].value_counts()
                fig = px.bar(
                    x=vc.index,
                    y=vc.values,
                    title=f"Distribution de '{col_cat}'",
                    labels={col_cat: "Catégorie", "y": "Nombre"},
                    color=vc.index,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
            else:
                vc = df[col_cat].value_counts()
                fig = px.pie(
                    names=vc.index,
                    values=vc.values,
                    title=f"Distribution de '{col_cat}'",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e0e0ff")
            st.plotly_chart(fig, use_container_width=True)
            st.info("👉 Utilisez le bouton 📥 en haut à droite du graphique pour le télécharger.")
        if num_cols:
            col_num = st.selectbox("🔢 Choisissez une colonne numérique", num_cols, key="num_col_visu")
            fig = px.histogram(df, x=col_num, nbins=20, title=f"Distribution de '{col_num}'", marginal="box")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e0e0ff")
            st.plotly_chart(fig, use_container_width=True)
            st.info("👉 Utilisez le bouton 📥 en haut à droite du graphique pour le télécharger.")
    else:
        st.warning("⚠️ Veuillez importer un jeu de données et le nettoyer d'abord.")

# --- Page Tableau Croisé Dynamique ---
if selected == "🧩 Tableau Croisé":
    st.header("🧩 Tableau Croisé Dynamique 🔄")
    df = st.session_state.cleaned_data

    if df is not None and not df.empty:
        st.info("Créez un tableau croisé dynamique en choisissant vos colonnes de regroupement (1 ou plusieurs).")

        all_cols = df.columns.tolist()

        # Sélection des colonnes de groupby
        group_cols = st.multiselect(
            "📋 Colonnes de regroupement (group by)",
            options=all_cols,
            default=all_cols[:2] if len(all_cols) >= 2 else all_cols[:1],
            help="Sélectionnez une ou plusieurs colonnes pour grouper les données"
        )

        if not group_cols:
            st.warning("Veuillez sélectionner au moins une colonne.")
        else:
            try:
                # 1. Calcul du tableau croisé
                if len(group_cols) == 1:
                    cross_tab = pd.crosstab(index=df[group_cols[0]], columns="Count")
                    cross_tab.columns = ['Count']
                elif len(group_cols) == 2:
                    cross_tab = pd.crosstab(index=df[group_cols[0]], columns=df[group_cols[1]])
                else:
                    cross_tab = df.groupby(group_cols).size().unstack(fill_value=0, level=-1)

                if cross_tab.empty:
                    st.warning("Le tableau croisé est vide. Vérifiez vos données.")
                else:
                    # 2. Initialisation des états
                    if 'pivoted' not in st.session_state:
                        st.session_state.pivoted = False
                    if 'sort_column' not in st.session_state:
                        st.session_state.sort_column = None
                    if 'sort_ascending' not in st.session_state:
                        st.session_state.sort_ascending = True

                    # 3. Boutons d'action
                    col1, col2, col3 = st.columns([2, 2, 2])
                    with col1:
                        metric = st.radio(
                            "📊 Métrique",
                            ["Compte (Count)", "Pourcentage du total", "Pourcentage par ligne", "Pourcentage par colonne"],
                            horizontal=True
                        )
                    with col2:
                        if st.button("🔄 Pivoter les colonnes", help="Échange lignes et colonnes du tableau"):
                            st.session_state.pivoted = not st.session_state.pivoted
                    with col3:
                        if st.button("🔁 Réinitialiser", help="Réinitialise pivot, tri et filtres"):
                            st.session_state.pivoted = False
                            st.session_state.sort_column = None
                            st.session_state.sort_ascending = True
                            st.experimental_rerun()

                    # 4. Appliquer le pivot
                    current_cross_tab = cross_tab.T if st.session_state.pivoted else cross_tab

                    # 5. Calculer la métrique
                    if metric == "Compte (Count)":
                        base_df = current_cross_tab.copy()
                        display_df = current_cross_tab.copy()
                    elif metric == "Pourcentage du total":
                        base_df = (current_cross_tab / current_cross_tab.sum().sum()) * 100
                        display_df = base_df.round(2).astype(str) + " %"
                    elif metric == "Pourcentage par ligne":
                        row_sums = current_cross_tab.sum(axis=1)
                        base_df = current_cross_tab.div(row_sums, axis=0) * 100
                        display_df = base_df.round(2).astype(str) + " %"
                    elif metric == "Pourcentage par colonne":
                        col_sums = current_cross_tab.sum(axis=0)
                        base_df = current_cross_tab.div(col_sums, axis=1) * 100
                        display_df = base_df.round(2).astype(str) + " %"

                    # 6. Ajouter la colonne "Total"
                    if metric == "Compte (Count)":
                        display_df["Total"] = display_df.sum(axis=1).astype(int)
                        total_row = display_df.sum(axis=0).astype(int)
                    else:
                        temp_numeric = display_df.replace("%", "", regex=True).astype(float)
                        display_df["Total"] = temp_numeric.sum(axis=1).round(2).astype(str) + " %"
                        total_row = temp_numeric.sum(axis=0).round(2).astype(str) + " %"

                    # 7. Ajouter la ligne "Total"
                    total_row.name = "Total"
                    display_df_with_total = pd.concat([display_df, pd.DataFrame([total_row])])

                    # 8. Afficher l'état du pivot
                    st.caption(f"🔁 Mode : {'Lignes ↔ Colonnes' if st.session_state.pivoted else 'Normal'}")

                    # 9. Affichage du tableau
                    st.subheader(f"📋 {metric} (avec totaux) {'- Vue pivotée' if st.session_state.pivoted else ''}")
                    st.dataframe(display_df_with_total, use_container_width=True)

                    # 10. Graphique (uniquement si 1 ou 2 dimensions)
                    if len(group_cols) <= 2:
                        st.subheader("📈 Visualisation")
                        plot_df = base_df.copy()
                        if "Total" in plot_df.index:
                            plot_df = plot_df.drop("Total")
                        if "Total" in plot_df.columns:
                            plot_df = plot_df.drop("Total", axis=1)

                        if len(plot_df.index.names) > 1 or len(plot_df.columns) == 0:
                            st.info("📊 Graphique non disponible pour cette structure.")
                        else:
                            if len(group_cols) == 1 or not st.session_state.pivoted:
                                x_col = plot_df.index.name or plot_df.index.names[0] or "Index"
                                melted = plot_df.reset_index().melt(id_vars=x_col, var_name="Catégorie", value_name="Valeur")
                                fig = px.bar(
                                    melted,
                                    x=x_col,
                                    y="Valeur",
                                    color="Catégorie",
                                    title=f"{metric} : {x_col} vs {melted.columns[-1]}",
                                    barmode="group",
                                    color_discrete_sequence=px.colors.qualitative.Bold
                                )
                            else:
                                fig = px.bar(
                                    plot_df.T,
                                    title=f"{metric} (vue transposée)",
                                    barmode="group",
                                    color_discrete_sequence=px.colors.qualitative.Bold
                                )
                            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e0e0ff")
                            st.plotly_chart(fig, use_container_width=True)

                    # 11. Export Excel
                    st.subheader("📥 Exporter le tableau (avec totaux)")
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        display_df_with_total.to_excel(writer, sheet_name='Tableau_Croisé')
                    excel_data = excel_buffer.getvalue()

                    st.download_button(
                        label="📊 Télécharger en Excel (.xlsx)",
                        data=excel_data,
                        file_name=f"tableau_croise_{metric.lower().replace(' ', '_')}_{'pivote_' if st.session_state.pivoted else ''}avec_totaux.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
    else:
        st.warning("⚠️ Veuillez d'abord importer et nettoyer un jeu de données.")

# --- Page Téléchargement ---
if selected == "💾 Téléchargement":
    st.header("💾 Exporter les données nettoyées")
    df = st.session_state.cleaned_data
    if df is not None and not df.empty:
        csv = df.to_csv(index=False).encode('utf-8')
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Données Nettoyées')
        excel_data = excel_buffer.getvalue()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label=f"{icon_svg('download')} ⬇️ Télécharger en CSV",
                data=csv,
                file_name="data_nettoyee.csv",
                mime="text/csv",
                key="download_csv",
                help="Format compatible avec tous les tableurs",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label=f"{icon_svg('download')} 📊 Télécharger en Excel",
                data=excel_data,
                file_name="data_nettoyee.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel",
                help="Format Excel (.xlsx)",
                use_container_width=True
            )
        st.success("✅ Les fichiers sont prêts à être téléchargés.")
    else:
        st.warning("⚠️ Aucune donnée à exporter.")

# --- Page À propos ---
if selected == "ℹ️ À propos":
    st.header("ℹ️ À propos de DDC – Smart Data Cleaner 🌟")
    st.markdown("""
    <div style='text-align:center; font-size:1.1rem; color:#b0b0d0; line-height:1.8;'>
        <p>✨ Créée par Alpha Oumar DIALLO.</p>
        <p>🚀 Une application entièrement gratuite, open-source et conçue pour rendre l’analyse de données accessible à tous.</p>
        <p>🔗 GitHub : <a href="https://github.com/votre-repo/dataclean-pro" target="_blank" style="color:#00c8ff;">https://github.com/votre-repo/dataclean-pro</a></p>
        <p>📧 Contact : contact@datapro.com</p>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1138/1138548.png", width=150, use_column_width=False)