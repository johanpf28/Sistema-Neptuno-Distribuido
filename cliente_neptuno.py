import socket
import struct
import tkinter as tk
from tkinter import messagebox

# Configuración Pro
SERVER_IP = "34.57.53.3" 
PORT = 5000

class NeptunoApp:
    def __init__(self, master):
        self.master = master
        master.title("Neptuno Control Panel v2.5")
        master.geometry("1100x750")
        master.configure(bg="#0b0b11") # Fondo más profundo

        self.colors = {
            "bg_main": "#0f0f17",
            "sidebar": "#0b0b11",
            "card": "#1e1e2e",
            "accent": "#cba6f7",
            "input": "#28283d",
            "border": "#313244",
            "shadow": "#000000",
            "btn_green": "#a6e3a1",
            "btn_orange": "#fab387",
            "text": "#cdd6f4"
        }

        # --- SIDEBAR CURVO (Simulado con Padding) ---
        self.sidebar = tk.Frame(master, bg=self.colors["sidebar"], width=280)
        self.sidebar.pack(side="left", fill="y", padx=(0, 2)) # Pequeño gap para profundidad
        self.sidebar.pack_propagate(False)

        # Header Logo
        tk.Label(self.sidebar, text="⚡ NEPTUNO", font=("Segoe UI Black", 24), 
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack(pady=(60, 5), padx=30, anchor="w")
        tk.Label(self.sidebar, text="   ", font=("Consolas", 9, "bold"), 
                 bg=self.colors["sidebar"], fg="#45475a").pack(padx=35, anchor="w")

        # Botones de Navegación con efecto de cápsula
        self.create_nav_btn("PRODUCTOS", self.show_registrar)
        self.create_nav_btn("PEDIDOS", self.show_pedidos)

        # --- ÁREA DE CONTENIDO ---
        self.main_area = tk.Frame(master, bg=self.colors["bg_main"])
        self.main_area.pack(side="right", fill="both", expand=True)

        # EFECTO DE PROFUNDIDAD (Sombra proyectada)
        self.shadow_frame = tk.Frame(self.main_area, bg=self.colors["shadow"])
        self.shadow_frame.place(relx=0.51, rely=0.51, anchor="center", width=540, height=580)

        # TARJETA CENTRAL (Bordes suavizados mediante highlight)
        self.card = tk.Frame(self.main_area, bg=self.colors["card"], 
                            highlightbackground=self.colors["border"], 
                            highlightthickness=2, padx=45, pady=45)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=540, height=580)

        self.show_registrar()

    def create_nav_btn(self, text, command):
        # Frame contenedor para el botón (Simula el botón redondeado)
        btn_f = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        btn_f.pack(fill="x", padx=20, pady=10)
        
        btn = tk.Button(btn_f, text=f"   {text}", font=("Segoe UI Black", 10),
                        bg=self.colors["sidebar"], fg="#585b70", bd=0, 
                        activebackground=self.colors["card"], activeforeground="white",
                        anchor="w", cursor="hand2", command=command)
        btn.pack(fill="x", ipady=12)
        
        btn.bind("<Enter>", lambda e: btn.config(fg=self.colors["accent"]))
        btn.bind("<Leave>", lambda e: btn.config(fg="#585b70"))
        return btn

    def create_input_capsule(self, label):
        # Label superior
        tk.Label(self.card, text=label, font=("Segoe UI Black", 8), 
                 bg=self.colors["card"], fg="#6c7086").pack(anchor="w", pady=(15, 5))
        
        # El "Cajón" con profundidad (Inner Shadow simulada)
        outer_input = tk.Frame(self.card, bg=self.colors["shadow"])
        outer_input.pack(fill="x", ipady=1)
        
        inner_input = tk.Frame(outer_input, bg=self.colors["input"], 
                               highlightbackground=self.colors["border"], highlightthickness=1)
        inner_input.pack(fill="x", ipady=10)
        
        e = tk.Entry(inner_input, font=("Consolas", 13), bg=self.colors["input"], 
                     fg="white", bd=0, insertbackground="white", justify="center")
        e.pack(fill="x", padx=15)
        
        # Efecto Glow al enfocar
        e.bind("<FocusIn>", lambda event: inner_input.config(highlightbackground=self.colors["accent"]))
        e.bind("<FocusOut>", lambda event: inner_input.config(highlightbackground=self.colors["border"]))
        return e

    def show_registrar(self):
        self.clear_card()
        tk.Label(self.card, text="NUEVO PRODUCTO", font=("Segoe UI Black", 22), 
                 bg=self.colors["card"], fg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(self.card, text="Añadir items al inventario global de Neptuno", font=("Segoe UI", 9), 
                 bg=self.colors["card"], fg="#585b70").pack(anchor="w", pady=(0, 20))
        
        self.name_entry = self.create_input_capsule("NOMBRE DEL PRODUCTO")
        self.price_entry = self.create_input_capsule("PRECIO (S/.)")
        self.stock_entry = self.create_input_capsule("STOCK INICIAL")
        
        # Botón 3D
        btn = tk.Button(self.card, text="GUARDAR CAMBIOS", command=self.add_product, 
                        bg=self.colors["btn_green"], fg="#0b0b11", font=("Segoe UI Black", 12), 
                        bd=0, cursor="hand2", activebackground="#89b482")
        btn.pack(pady=(40, 0), fill="x", ipady=18)

    def show_pedidos(self):
        self.clear_card()
        tk.Label(self.card, text="REALIZAR PEDIDO", font=("Segoe UI Black", 22), 
                 bg=self.colors["card"], fg="white").pack(anchor="w", pady=(0, 5))
        tk.Label(self.card, text="Módulo de Ventas Atómicas (ACID COMPLIANT)", font=("Segoe UI", 9), 
                 bg=self.colors["card"], fg="#585b70").pack(anchor="w", pady=(0, 20))

        self.id_entry = self.create_input_capsule("ID PRODUCTO (SKU)")
        self.qty_entry = self.create_input_capsule("CANTIDAD")

        btn = tk.Button(self.card, text="CONFIRMAR VENTA", command=self.make_order, 
                        bg=self.colors["btn_orange"], fg="#0b0b11", font=("Segoe UI Black", 12),
                        bd=0, cursor="hand2", activebackground="#d699b6")
        btn.pack(pady=(40, 0), fill="x", ipady=18)

    def clear_card(self):
        for widget in self.card.winfo_children():
            widget.destroy()

    # --- LÓGICA DE RED (Original) ---
    def send_request(self, mode, data):
        try:
            with socket.create_connection((SERVER_IP, PORT), timeout=5) as s:
                op_bytes = mode.encode('utf-8')
                s.send(struct.pack('!H', len(op_bytes)) + op_bytes)
                if mode == "REGISTRAR_PRODUCTO":
                    n_bytes = data['n'].encode('utf-8')
                    s.send(struct.pack('!H', len(n_bytes)) + n_bytes)
                    s.send(struct.pack('!d', float(data['p'])))
                    s.send(struct.pack('!i', int(data['s'])))
                else:
                    s.send(struct.pack('!i', int(data['id'])))
                    s.send(struct.pack('!i', int(data['q'])))
                header = s.recv(2)
                res_len = struct.unpack('!H', header)[0]
                return s.recv(res_len).decode('utf-8')
        except Exception as e:
            return f"Error de red: {e}"

    def add_product(self):
        res = self.send_request("REGISTRAR_PRODUCTO", {'n': self.name_entry.get(), 'p': self.price_entry.get(), 's': self.stock_entry.get()})
        messagebox.showinfo("Neptuno Node", res)

    def make_order(self):
        res = self.send_request("REALIZAR_PEDIDO", {'id': self.id_entry.get(), 'q': self.qty_entry.get()})
        messagebox.showinfo("Neptuno Node", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeptunoApp(root)
    root.mainloop()