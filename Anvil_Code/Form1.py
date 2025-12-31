from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # CARGAR DATOS 
    self.rep_productos.items = anvil.server.call('traer_productos')
    self.rep_empleados.items = anvil.server.call('traer_empleados')
    self.rep_clientes.items = anvil.server.call('traer_clientes')
    self.rep_ventas.items = anvil.server.call('traer_ventas')

    self.ocultar_todo()

  def ocultar_todo(self):
    # Tablas
    self.grid_productos.visible = False
    self.grid_empleados.visible = False
    self.grid_clientes.visible = False
    self.grid_ventas.visible = False
    # Títulos (Labels)
    self.lbl_productos.visible = False
    self.lbl_empleados.visible = False
    self.lbl_clientes.visible = False
    self.lbl_ventas.visible = False

  # --- FUNCIÓN DEL BOTÓN CLIENTE ---
  def btn_cliente_click(self, **event_args):
    self.ocultar_todo()

    alert("¡Hola! Aquí tienes nuestro catálogo de música.")
    self.lbl_productos.visible = True
    self.grid_productos.visible = True

  # --- FUNCIÓN DEL BOTÓN VENDEDOR ---
  def btn_vendedor_click(self, **event_args):
    caja_texto = TextBox(hide_text=True, placeholder="Escribe aquí...")

    alerta = alert(content=caja_texto, title="Ingresa la clave de vendedor:")

    if alerta and caja_texto.text == "admin":
      alert("Acceso concedido. Mostrando base de datos completa.")
      # Mostramos TODO
      self.lbl_productos.visible = True
      self.grid_productos.visible = True

      self.lbl_empleados.visible = True
      self.grid_empleados.visible = True

      self.lbl_clientes.visible = True
      self.grid_clientes.visible = True

      self.lbl_ventas.visible = True
      self.grid_ventas.visible = True
    else:
      alert("Clave incorrecta o cancelado.")

  def gestion_btn_click(self, **event_args):
    print("Botón clickeado desde manejador asignado en código")
    open_form('Form2')