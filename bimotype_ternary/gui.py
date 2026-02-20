import streamlit as st
import time
import os
import sys
import json

# Añadir el directorio padre al sys.path para permitir ejecución de streamlit y resolver imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bimotype_ternary.network.p2p import MetriplecticPeer
from bimotype_ternary.crypto.qr_transfer import QRTransferProtocol
import io
import base64

# ... (inside layout setup) ...
# Modifying layout to use tabs
tab1, tab2 = st.tabs(["P2P Online Console", "Offline QR Transfer"])

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Tu Identidad (Local)")
        st.markdown(f'<div class="fingerprint-box">{st.session_state.local_fp}</div>', unsafe_allow_html=True)
        
        st.divider()
        
        st.subheader("Contactos de Confianza")
        trusted = st.session_state.peer.trusted_peers
        if not trusted:
            st.write("No tienes contactos autorizados aún.")
        else:
            for t_fp in list(trusted):
                st.code(f"🔒 {t_fp[:12]}...")

        st.divider()
        
        st.subheader("Descubrimiento P2P")
        if os.path.exists("peer_cache.json"):
            with open("peer_cache.json", "r") as f:
                peers = json.load(f)
                for fp in peers:
                    if fp != st.session_state.local_fp:
                        is_trusted = fp in st.session_state.peer.trusted_peers
                        label = f"💬 {fp[:8]}" if is_trusted else f"🤝 Vincular {fp[:8]}"
                        if st.button(label, key=f"btn_{fp}"):
                            st.session_state.target_fp = fp
                            if not is_trusted:
                                target_data = PeerDiscovery.resolve_peer(fp)
                                if target_data:
                                    st.session_state.peer.request_handshake(target_data[0], target_data[1])
                                    st.info(f"Solicitud enviada a {fp[:8]}. Esperando respuesta...")
        else:
            st.write("No se detectan otros pares.")

    with col2:
        st.subheader("Chat Metripléctico")
        
        target_fp = st.text_input("Fingerprint de Destino", value=st.session_state.get("target_fp", ""), placeholder="Introduce la huella del receptor...")
        
        # Verificar estado de confianza
        if target_fp:
            if target_fp not in st.session_state.peer.trusted_peers:
                st.warning("⚠️ Este contacto no es de confianza. Debes realizar un handshake primero.")
                if st.button("🚀 Enviar Solicitud de Handshake"):
                    t_data = PeerDiscovery.resolve_peer(target_fp)
                    if t_data:
                        st.session_state.peer.request_handshake(t_data[0], t_data[1])
                        st.info("Solicitud enviada.")
                    else:
                        st.error("No se encontró la dirección de este peer.")
        
        chat_container = st.container(height=400)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Escribe tu mensaje..."):
            if not target_fp:
                st.error("Por favor, introduce un Fingerprint de destino.")
            elif target_fp not in st.session_state.peer.trusted_peers:
                st.error("Debes establecer una conexión de confianza antes de enviar datos.")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                target_data = PeerDiscovery.resolve_peer(target_fp)
                if target_data:
                    success = st.session_state.peer.send_packet(target_data[0], target_data[1], prompt, target_fp)
                    if not success:
                        st.error("Error al enviar el paquete.")
                else:
                    st.error("Huella de destino no encontrada.")
                st.rerun()

with tab2:
    st.header("📴 Transferencia Segura Offline (Animated QR)")
    st.write("Transmite archivos o texto a dispositivos desconectados de Internet usando cámaras y la sincronización de la Razón Áurea.")
    
    h7_seed_input = st.number_input("Semilla Compartida (H7 Index)", min_value=1, value=42)
    
    qr_col1, qr_col2 = st.columns(2)
    
    with qr_col1:
        st.subheader("Emitir Archivo 📤")
        uploaded_file = st.file_uploader("Selecciona archivo a enviar", type=None)
        
        if uploaded_file is not None:
            if st.button("Generar QR Animado"):
                with st.spinner("Encriptando y fragmentando..."):
                    protocol = QRTransferProtocol(h7_index=h7_seed_input, chunk_size=400)
                    file_bytes = uploaded_file.read()
                    frames = protocol.prepare_payload(file_bytes, uploaded_file.name)
                    images = protocol.generate_qr_images(frames)
                    
                    st.success(f"Archivo dividido en {len(frames)} QRs.")
                    
                    # Convert images to base64 for display in Streamlit
                    b64_images = []
                    for img in images:
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        img_str = base64.b64encode(buf.getvalue()).decode()
                        b64_images.append(img_str)
                    
                    # Pass the array to javascript to animate
                    js_code = f"""
                    <div id="qr-container" style="display:flex; justify-content:center; align-items:center; flex-direction:column;">
                        <img id="qr-image" src="data:image/png;base64,{b64_images[0]}" width="300" height="300" />
                        <h4 id="qr-counter">1 / {len(b64_images)}</h4>
                    </div>
                    <script>
                        var frames = {json.dumps(b64_images)};
                        var idx = 0;
                        setInterval(function() {{
                            idx = (idx + 1) % frames.length;
                            document.getElementById('qr-image').src = "data:image/png;base64," + frames[idx];
                            document.getElementById('qr-counter').innerText = (idx + 1) + " / " + frames.length;
                        }}, 150); // Velocidad: 150ms per frame
                    </script>
                    """
                    st.components.v1.html(js_code, height=400)

    with qr_col2:
        st.subheader("Recibir Archivo 📥")
        st.info("Apunta tu cámara al QR animado de tu contacto.")
        
        if st.button("📸 Abrir Escáner de Cámara"):
            protocol = QRTransferProtocol(h7_index=h7_seed_input, chunk_size=400)
            with st.spinner("Escaneando... Mira la ventana de la cámara de tu escritorio."):
                file_bytes, filename = protocol.scan_animated_qr_from_camera()
                
            if file_bytes and filename:
                st.success(f"¡Transferencia completa! Archivo: {filename}")
                st.download_button("Guardar Archivo Decodificado", data=file_bytes, file_name=filename)
            else:
                st.error("Escaneo cancelado o error en transferencia.")

st.sidebar.markdown("---")
st.sidebar.caption("BiMoType v1.3.0-secure")
st.sidebar.write("Estado: Conectado 🟢")
st.sidebar.write(f"Pares Confiables: {len(st.session_state.peer.trusted_peers)}")
