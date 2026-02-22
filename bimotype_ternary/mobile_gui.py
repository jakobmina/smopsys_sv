import flet as ft
import time
import os
import sys
import json
import io
import base64
import threading

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bimotype_ternary.network.p2p import MetriplecticPeer
from bimotype_ternary.network.discovery import PeerDiscovery
from bimotype_ternary.crypto.qr_transfer import QRTransferProtocol

def main(page: ft.Page):
    page.title = "BiMoType Metriplectic Console"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Custom colors matching Metriplectic Aesthetics
    BG_COLOR = "#0b0e14"
    ACCENT_COLOR = "#00d4ff"
    SURFACE_COLOR = "#161b22"
    TEXT_COLOR = "#e0e0e0"
    
    page.bgcolor = BG_COLOR
    
    # Session state equivalents
    state = {
        "peer": None,
        "local_fp": None,
        "messages": [],
        "handshake_requests": [],
        "target_fp": "",
        "h7_seed": 42
    }
    
    def on_peer_message(sender, packet):
        if state["peer"]:
            decoded = state["peer"].decoder.decode_bimotype_packet(packet)
            msg_text = decoded.get('decoded_message', 'Error al decodificar')
            state["messages"].append({"role": "assistant", "sender": sender[:8], "content": msg_text})
            # Update UI if we are on the chat view
            update_chat_ui()
    
    def on_handshake(sender):
        if sender not in state["handshake_requests"]:
            state["handshake_requests"].append(sender)
            update_handshake_ui()
            
    # Init peer mechanism
    import random
    port = random.randint(5100, 5200)
    state["peer"] = MetriplecticPeer(port=port)
    state["peer"].on_message_received = on_peer_message
    state["peer"].on_handshake_received = on_handshake
    
    def peer_thread_callback(thread=None):
        pass
        
    state["local_fp"] = state["peer"].start_listening(thread_callback=peer_thread_callback)
    PeerDiscovery.register_peer(state["local_fp"], "127.0.0.1", port)

    # UI Components
    
    # Tab 1: P2P Online
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
msg_input = ft.TextField(hint_text="Escribe tu mensaje...", expand=True, border_color=ACCENT_COLOR, color=ACCENT_COLOR, bgcolor=SURFACE_COLOR)
target_fp_input = ft.TextField(label="Fingerprint de Destino", hint_text="Huella del receptor...", border_color=ACCENT_COLOR, color=ACCENT_COLOR, bgcolor=SURFACE_COLOR)

handshake_column = ft.Column(spacing=5)

def update_handshake_ui():
    handshake_column.controls.clear()
    for req_fp in state["handshake_requests"]:
        target_data = PeerDiscovery.resolve_peer(req_fp)
        def acc_click(e, fp=req_fp, t_data=target_data):
            if t_data:
                state["peer"].send_handshake_ack(t_data[0], t_data[1], fp)
            state["handshake_requests"].remove(fp)
            page.snack_bar = ft.SnackBar(ft.Text(f"Conexión establecida con {fp[:8]}"), bgcolor=ft.Colors.GREEN_700)
            page.snack_bar.open = True
            update_handshake_ui()
    def ign_click(e, fp=req_fp):
        state["handshake_requests"].remove(fp)
        update_handshake_ui()
        
    row = ft.Row([
        ft.Text(f"📩 Solicitud: {req_fp[:8]}..."),
        ft.IconButton(ft.Icons.CHECK, on_click=acc_click, icon_color=ft.Colors.GREEN_400),
        ft.IconButton(ft.Icons.CLOSE, on_click=ign_click, icon_color=ft.Colors.RED_400)
    ])
    handshake_column.controls.append(ft.Container(content=row, bgcolor=ft.Colors.ORANGE_900, padding=5, border_radius=5))
page.update()

def update_chat_ui():
        chat_list.controls.clear()
        for msg in state["messages"]:
            align = ft.MainAxisAlignment.END if msg["role"] == "user" else ft.MainAxisAlignment.START
            color = ACCENT_COLOR if msg["role"] == "user" else ft.Colors.WHITE
            bg_color = "#1a1f29" if msg["role"] == "user" else SURFACE_COLOR
    
            chat_list.controls.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(f'[{msg.get("sender", "Tu")}] {msg["content"]}', color=color),
                        bgcolor=bg_color,
                        padding=10,
                border_radius=10,
                border=ft.Border.all(1, ACCENT_COLOR) if msg["role"]=="user" else None
            )
        ], alignment=align)
    )
page.update()

def send_click(e):
    target_fp = target_fp_input.value
    prompt = msg_input.value
    if not target_fp:
        page.snack_bar = ft.SnackBar(ft.Text("Introduce un Fingerprint de destino"), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
    elif target_fp not in state["peer"].trusted_peers:
        page.snack_bar = ft.SnackBar(ft.Text("Aún no es de confianza. Solicita Handshake primero."), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
    elif prompt:
        state["messages"].append({"role": "user", "sender": "Tu", "content": prompt})
        target_data = PeerDiscovery.resolve_peer(target_fp)
        if target_data:
            state["peer"].send_packet(target_data[0], target_data[1], prompt, target_fp)
            msg_input.value = ""
        update_chat_ui()
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Huella de destino no encontrada"), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
page.update()

p2p_view = ft.Column([
ft.Text("Identidad Local", color=ACCENT_COLOR, weight=ft.FontWeight.BOLD),
ft.Container(content=ft.Text(state["local_fp"], selectable=True, color=ACCENT_COLOR, font_family="monospace"), bgcolor=SURFACE_COLOR, padding=10, border_radius=5, border=ft.Border.all(1, ACCENT_COLOR)),
handshake_column,
target_fp_input,
ft.Container(content=chat_list, expand=True, border=ft.Border.all(1, ft.Colors.BLUE_GREY_800), border_radius=5, padding=5),
ft.Row([msg_input, ft.IconButton(icon=ft.Icons.SEND, on_click=send_click, icon_color=ACCENT_COLOR)])
], expand=True, visible=True)

# Tab 2: Offline QR
qr_image_control = ft.Image(src="", width=300, height=300, fit=ft.ImageFit.CONTAIN if hasattr(ft, 'ImageFit') else "contain")
qr_counter_text = ft.Text("0 / 0", color=ACCENT_COLOR)

animating = False
qr_frames_b64 = []
    
def animate_qr():
        nonlocal animating
        if animating or not qr_frames_b64: return
        animating = True
        idx = 0
        while animating and qr_frames_b64:
            qr_image_control.src_base64 = qr_frames_b64[idx]
            qr_counter_text.value = f"{idx + 1} / {len(qr_frames_b64)}"
            page.update()
            idx = (idx + 1) % len(qr_frames_b64)
            time.sleep(0.15)
            
def stop_animating():
    nonlocal animating
    animating = False
    
def pick_files_result(e: ft.FilePickerResultEvent):
    if not e.files: return
    file_path = e.files[0].path
    filename = e.files[0].name
        
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()
                
        protocol = QRTransferProtocol(h7_index=state["h7_seed"], chunk_size=400)
        frames = protocol.prepare_payload(file_bytes, filename)
        images = protocol.generate_qr_images(frames)
            
        nonlocal qr_frames_b64
        qr_frames_b64.clear()
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            qr_frames_b64.append(base64.b64encode(buf.getvalue()).decode())
                
        page.snack_bar = ft.SnackBar(ft.Text(f"Archivo dividido en {len(frames)} QRs."), bgcolor=ft.Colors.GREEN_700)
        page.snack_bar.open = True
            
        # Start animation in background
        threading.Thread(target=animate_qr, daemon=True).start()
    except Exception as ex:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED_700)
        page.snack_bar.open = True
    page.update()

file_picker = ft.FilePicker(on_result=pick_files_result)
page.overlay.append(file_picker)
    
# Scanner logic
def scan_qr_click(e):
    page.snack_bar = ft.SnackBar(ft.Text("Abriendo escáner... (Asegúrate de conceder permisos)"), bgcolor=ft.Colors.BLUE_700)
    page.snack_bar.open = True
    page.update()
        
    # We run the camera logic in a blocking wait but inside a thread or directly if desktop
    # In this hybrid we just call the native cv2 from protocol because Flet doesn't have native camera yet out of the box without plugins.
    def _scan():
        protocol = QRTransferProtocol(h7_index=state["h7_seed"], chunk_size=400)
        file_bytes, filename = protocol.scan_animated_qr_from_camera()
        if getattr(sys, 'gettrace', None):
            # if inside debugger or something...
            pass
                
        def ui_update():
            if file_bytes and filename:
                # Save to downloads or current dir
                out_path = os.path.join(os.path.expanduser("~"), "Downloads", "bimo_rec_" + filename)
                try:
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with open(out_path, "wb") as f:
                        f.write(file_bytes)
                    page.snack_bar = ft.SnackBar(ft.Text(f"¡Éxito! Guardado en {out_path}"), bgcolor=ft.Colors.GREEN_700)
                except Exception as _ex:
                    # Fallback
                    with open(filename, "wb") as f:
                        f.write(file_bytes)
                    page.snack_bar = ft.SnackBar(ft.Text(f"¡Éxito! Guardado en directorio actual as {filename}"), bgcolor=ft.Colors.GREEN_700)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Escaneo cancelado o fallido."), bgcolor=ft.Colors.RED_700)
            page.snack_bar.open = True
            page.update()
            
        # Use page.run_thread to safely update UI from another thread if needed, or just standard thread and invoke
        # Since we are not in async mode, we can just call page.update() from thread
        ui_update()
            
    threading.Thread(target=_scan, daemon=True).start()

    qr_view = ft.Column([
        ft.Text("Transferencia Offline", color=ACCENT_COLOR, weight=ft.FontWeight.BOLD, size=20),
        ft.Divider(color=ACCENT_COLOR),
        ft.Text("Emitir Archivo 📤", color=ft.Colors.WHITE),
        ft.ElevatedButton("Seleccionar y Emitir", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(), bgcolor=SURFACE_COLOR, color=ACCENT_COLOR),
        ft.Container(
            content=ft.Column([qr_image_control, qr_counter_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=20
        ),
        ft.Divider(color=ACCENT_COLOR),
        ft.Text("Recibir Archivo 📥", color=ft.Colors.WHITE),
        ft.ElevatedButton("📸 Abrir Escáner", on_click=scan_qr_click, bgcolor=SURFACE_COLOR, color=ACCENT_COLOR)
    ], expand=True, visible=False, scroll=ft.ScrollMode.AUTO)

    # Navigation
    def nav_change(e):
        p2p_view.visible = (e.control.selected_index == 0)
        qr_view.visible = (e.control.selected_index == 1)
        if not qr_view.visible:
            stop_animating()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        bgcolor=SURFACE_COLOR,
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.MESSAGE_OUTLINED, selected_icon=ft.Icons.MESSAGE, label="P2P Chat"),
            ft.NavigationDestination(icon=ft.Icons.QR_CODE_SCANNER_OUTLINED, selected_icon=ft.Icons.QR_CODE, label="QR Offline"),
        ],
        on_change=nav_change
    )
    
    page.add(ft.SafeArea(ft.Column([p2p_view, qr_view], expand=True)))

if __name__ == "__main__":
    ft.app(main)
