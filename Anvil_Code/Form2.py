from ._anvil_designer import Form2Template
from anvil import *
import anvil.server

class Form2(Form2Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # =========================
    # ESTADO
    # =========================
    self.producto_seleccionado = None

    # =========================
    # EVENTOS DEL REPEATING PANEL
    # =========================
    self.products_panel.set_event_handler(
      'x-producto-seleccionado',
      self.producto_seleccionado_handler
    )

    # =========================
    # EVENTOS DE BOTONES
    # =========================
    self.agregar_btn.set_event_handler('click', self.agregar_btn_click)
    self.actualizar_btn.set_event_handler('click', self.actualizar_btn_click)
    self.eliminar_btn.set_event_handler('click', self.eliminar_btn_click)
    self.limpiar_btn.set_event_handler('click', self.limpiar_btn_click)

    # 🔹 BOTÓN FILTRAR (button_1)
    self.button_1.set_event_handler('click', self.button_1_click)

    # =========================
    # CARGA INICIAL
    # =========================
    self.cargar_generos()
    self.cargar_productos()

  # =========================
  # CARGA DE DATOS
  # =========================
  def cargar_generos(self):
    generos = anvil.server.call('obtener_generos') or []

    self.drop_down_1.items = ["Todos"] + generos
    self.drop_down_1.selected_value = "Todos"

    self.drop_down_2.items = [
      "Nombre",
      "Precio (menor a mayor)",
      "Precio (mayor a menor)"
    ]
    self.drop_down_2.selected_value = "Nombre"

    self.genero_form_dropdown.items = generos or ["Rock"]
    self.genero_form_dropdown.selected_value = self.genero_form_dropdown.items[0]

  def cargar_productos(self):
    productos = anvil.server.call(
      'buscar_productos',
      self.buscar_box.text or "",
      self.drop_down_1.selected_value or "Todos",
      self.obtener_parametro_orden(),
      100
    )
    self.products_panel.items = productos

  def obtener_parametro_orden(self):
    opcion = self.drop_down_2.selected_value

    if opcion == "Precio (menor a mayor)":
      return "precio_asc"
    elif opcion == "Precio (mayor a menor)":
      return "precio_desc"
    return "nombre"

  # =========================
  # FILTRAR
  # =========================
  def button_1_click(self, **event_args):
    self.cargar_productos()

  # =========================
  # SELECCIÓN DESDE ITEMTEMPLATE
  # =========================
  def producto_seleccionado_handler(self, producto, **event_args):
    self.producto_seleccionado = producto

    self.nombre_box.text = producto['nombre']
    self.precio_box.text = str(producto['precio'])
    self.stock_box.text = str(producto['stock'])
    self.genero_form_dropdown.selected_value = producto['genero']
    self.formato_dropdown.selected_value = producto['formato']

  # =========================
  # CRUD
  # =========================
  def agregar_btn_click(self, **event_args):
    if not self.nombre_box.text.strip():
      alert("Nombre obligatorio")
      return

    try:
      precio = float(self.precio_box.text)
      stock = int(self.stock_box.text or 0)
    except:
      alert("Precio o stock inválido")
      return

    res = anvil.server.call(
      'crear_producto',
      self.nombre_box.text.strip(),
      self.genero_form_dropdown.selected_value,
      precio,
      stock,
      self.formato_dropdown.selected_value
    )

    if res.get("success"):
      alert("Producto agregado")
      self.limpiar_formulario()
      self.cargar_productos()

  def actualizar_btn_click(self, **event_args):
    if not self.producto_seleccionado:
      alert("Selecciona un producto")
      return

    datos = {
      "nombre": self.nombre_box.text.strip(),
      "genero": self.genero_form_dropdown.selected_value,
      "precio": float(self.precio_box.text),
      "stock": int(self.stock_box.text or 0),
      "formato": self.formato_dropdown.selected_value
    }

    res = anvil.server.call(
      'actualizar_producto',
      self.producto_seleccionado['_id'],
      datos
    )

    if res.get("success"):
      alert("Producto actualizado")
      self.limpiar_formulario()
      self.cargar_productos()

  def eliminar_btn_click(self, **event_args):
    if not self.producto_seleccionado:
      alert("Selecciona un producto")
      return

    if confirm("¿Eliminar producto?"):
      res = anvil.server.call(
        'eliminar_producto',
        self.producto_seleccionado['_id']
      )

      if res.get("success"):
        alert("Producto eliminado")
        self.limpiar_formulario()
        self.cargar_productos()

  # =========================
  # LIMPIAR
  # =========================
  def limpiar_btn_click(self, **event_args):
    self.limpiar_formulario()

  def limpiar_formulario(self):
    self.producto_seleccionado = None
    self.nombre_box.text = ""
    self.precio_box.text = ""
    self.stock_box.text = ""
    self.formato_dropdown.selected_value = "Vinilo"
    self.genero_form_dropdown.selected_value = self.genero_form_dropdown.items[0]

  # =========================
  # VOLVER
  # =========================
  def volver_btn_click(self, **event_args):
    open_form('Form1')