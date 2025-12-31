from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server

class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Usar los componentes EXISTENTES del diseñador
    self.label_nombre.text = self.item.get('nombre', 'Sin nombre')
    self.label_precio.text = f"S/ {self.item.get('precio', 0)}"
    self.label_stock.text = f"Stock: {self.item.get('stock', 0)}"

  def seleccionar_btn_click(self, **event_args):
    # Enviar el producto seleccionado al Form2
    self.parent.raise_event(
      'x-producto-seleccionado',
      producto=self.item
    )