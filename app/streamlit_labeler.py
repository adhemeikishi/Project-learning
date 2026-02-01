"""Streamlit app: uploader multiple images, select category per image, save results to CSV.
Usage: streamlit run app/streamlit_labeler.py
"""
import streamlit as st
from PIL import Image
import pandas as pd
import io
import os
from datetime import datetime

st.set_page_config(page_title="Image Labeler", layout="centered")
st.title("Classification simple")

DEFAULT_CATEGORIES = ["Chat", "Chien", "Voiture", "Autre..."]

# Initialize session state
if 'annotations' not in st.session_state:
    st.session_state.annotations = pd.DataFrame(columns=['image', 'category'])

st.sidebar.header("Options")
cats = st.sidebar.text_input('Catégories (séparées par des virgules)', value=','.join(DEFAULT_CATEGORIES))
categories = [c.strip() for c in cats.split(',') if c.strip()]

st.markdown("**1. Uploader des images**")
uploaded = st.file_uploader("Sélectionnez des images (jpg, png, jpeg)", type=['jpg','jpeg','png'], accept_multiple_files=True)

if uploaded:
    st.markdown("**2. Aperçu et assignation de catégories**")
    cols = st.columns(3)
    for i, up in enumerate(uploaded):
        with cols[i % 3]:
            try:
                img = Image.open(io.BytesIO(up.read())).convert('RGB')
                st.image(img, use_column_width=True)
            except Exception as e:
                st.error(f"Impossible d'afficher {up.name}: {e}")
            # selection
            key = f"select_{up.name}_{i}"
            sel = st.selectbox('Catégorie', ['<Aucune>'] + categories, key=key)
            if sel and sel != '<Aucune>':
                # add or update row
                row = {'image': up.name, 'category': sel}
                # remove old entry for same image if any
                st.session_state.annotations = st.session_state.annotations[st.session_state.annotations['image'] != up.name]
                st.session_state.annotations = pd.concat([st.session_state.annotations, pd.DataFrame([row])], ignore_index=True)

st.markdown('---')
st.markdown('**3. Résumé des annotations**')
st.dataframe(st.session_state.annotations)

col1, col2 = st.columns(2)

# Télécharger CSV côté utilisateur
with col1:
    if st.button('Sauvegarder CSV (télécharger)'):
        if st.session_state.annotations.empty:
            st.warning('Aucune annotation à sauvegarder')
        else:
            csv = st.session_state.annotations.to_csv(index=False).encode('utf-8')
            st.download_button('Télécharger CSV', data=csv, file_name='annotations.csv')

# Sauvegarder CSV côté serveur avec date/heure pour éviter écrasement
with col2:
    if st.button('Sauvegarder CSV (serveur)'):
        if st.session_state.annotations.empty:
            st.warning('Aucune annotation à sauvegarder')
        else:
            os.makedirs('outputs', exist_ok=True)
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join('outputs', f'annotations_{now}.csv')
            st.session_state.annotations.to_csv(out_path, index=False)
            st.success(f'Sauvegardé: {out_path}')

st.markdown('---')
st.write('NOTES:')
st.write('- Vous pouvez ajouter / modifier les catégories depuis la sidebar.')
st.write('- Les images uploadées ne sont pas stockées sur le serveur par défaut (seulement leurs noms sont sauvegardés dans le CSV).')