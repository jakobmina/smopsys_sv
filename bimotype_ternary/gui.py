import streamlit as st
import time
import os
import json
from bimotype_ternary.network.p2p import MetriplecticPeer
from bimotype_ternary.network.discovery import PeerDiscovery
try:
    from streamlit.runtime.scriptrunner import add_script_run_ctx
except ImportError:
    from streamlit.report_thread import add_script_run_ctx as add_script_run_ctx

# Page Config
st.set_page_config(
    page_title="BiMoType Metriplectic Console",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for Metriplectic Aesthetics
st.markdown("""
<style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stTextInput>div>div>input { background-color: #1a1f29; color: #00d4ff; border-radius: 5px; }
    .stChatMessage { background-color: #161b22; border-left: 3px solid #00d4ff; }
    h1, h2, h3 { color: #00d4ff !important; font-family: 'Inter', sans-serif; }
    .fingerprint-box { 
        background-color: #161b22; 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px dashed #00d4ff;
        font-family: monospace;
        color: #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "handshake_requests" not in st.session_state:
    st.session_state.handshake_requests = []

def init_peer():
    if "peer" not in st.session_state:
        import random
        port = random.randint(5100, 5200)
        st.session_state.peer = MetriplecticPeer(port=port)
        
        def on_msg(sender, packet):
            decoded = st.session_state.peer.decoder.decode_bimotype_packet(packet)
            msg_text = decoded.get('decoded_message', 'Error al decodificar')
            st.session_state.messages.append({"role": "assistant", "content": f"**[{sender[:8]}]**: {msg_text}"})
            st.rerun()

        def on_handshake(sender):
            if sender not in st.session_state.handshake_requests:
                st.session_state.handshake_requests.append(sender)
                st.rerun()

        st.session_state.peer.on_message_received = on_msg
        st.session_state.peer.on_handshake_received = on_handshake
        
        # Vincular el hilo al contexto de Streamlit
        def thread_callback(thread):
            add_script_run_ctx(thread)
            
        st.session_state.local_fp = st.session_state.peer.start_listening(thread_callback=thread_callback)
        
        PeerDiscovery.register_peer(st.session_state.local_fp, "127.0.0.1", port)

# --- Layout ---
init_peer()

st.title("⚛️ BiMoType Metriplectic Console")
st.markdown(f"**Sistema de Comunicación P2P con Handshake Mutuo**")

# Notificaciones de Handshake
for req_fp in st.session_state.handshake_requests:
    with st.warning(f"📩 Solicitud de conexión de: `{req_fp[:16]}...`"):
        col_acc, col_ign = st.columns(2)
        if col_acc.button(f"Aceptar ✅", key=f"acc_{req_fp}"):
            target_data = PeerDiscovery.resolve_peer(req_fp)
            if target_data:
                st.session_state.peer.send_handshake_ack(target_data[0], target_data[1], req_fp)
                st.session_state.handshake_requests.remove(req_fp)
                st.success(f"Conexión establecida con {req_fp[:8]}")
                st.rerun()
        if col_ign.button(f"Ignorar ❌", key=f"ign_{req_fp}"):
            st.session_state.handshake_requests.remove(req_fp)
            st.rerun()

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

st.sidebar.markdown("---")
st.sidebar.caption("BiMoType v1.3.0-secure")
st.sidebar.write("Estado: Conectado 🟢")
st.sidebar.write(f"Pares Confiables: {len(st.session_state.peer.trusted_peers)}")
