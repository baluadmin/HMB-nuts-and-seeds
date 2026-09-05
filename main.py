from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import urllib.request
import csv
import codecs
import urllib.parse


class HMBNutsApp(App):

    def build(self):
        self.title = "HMB Nuts & Spices"[cite: 2]
        self.cart = []
        self.search_query = ""
        self.current_view = "Shop"[cite: 2]

        self.load_products()

        self.root_layout = BoxLayout(
            orientation="vertical", padding=dp(4), spacing=dp(4)
        )
        self.root_layout.canvas.before.clear()
        from kivy.graphics import Color, Rectangle

        with self.root_layout.canvas.before:
            Color(0.878, 0.949, 0.996, 1)
            self.bg_rect = Rectangle(
                size=self.root_layout.size, pos=self.root_layout.pos
            )
        self.root_layout.bind(size=self._update_bg, pos=self._update_bg)

        self.content_area = BoxLayout(orientation="vertical")
        self.root_layout.add_widget(self.content_area)

        self.render_shop_view()
        return self.root_layout

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def load_products(self):
        csv_url = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"[cite: 2]
        try:
            response = urllib.request.urlopen(csv_url)
            lines = [
                line.decode("utf-8")
                for line in codecs.iterdecode(response, "utf-8")
            ]
            reader = csv.reader(lines)
            self.product_records = []
            for row in reader:
                if (
                    len(row) > 4
                    and row[0].strip()
                    and row[0].strip() != "id"
                ):
                    self.product_records.append({
                        "id": row[0].strip(),
                        "name": row[1].strip(),
                        "category": row[2].strip(),
                        "stock": row[3].strip(),
                        "price": row[4].strip(),
                        "description": (
                            row[5].strip() if len(row) > 5 and row[5].strip() else "1 Pack"[cite: 2]
                        ),
                    })
        except Exception:
            self.product_records = [
                {
                    "id": "ITM001",
                    "name": "Premium California Almonds",
                    "price": "850",
                    "stock": "50",
                    "category": "Nuts",
                    "description": "500g",
                },
                {
                    "id": "ITM002",
                    "name": "W320 Cashew Nuts",
                    "price": "900",
                    "stock": "40",
                    "category": "Nuts",
                    "description": "500g",
                },
                {
                    "id": "ITM003",
                    "name": "Raw Pumpkin Seeds",
                    "price": "350",
                    "stock": "100",
                    "category": "Seeds",
                    "description": "250g",
                },
            ][cite: 2]

    def get_cart_qty(self, prod_name):
        for item in self.cart:
            if item.get("product") == prod_name:
                q_str = str(item.get("quantity", "1 Unit")).split()[0]
                return int(q_str) if q_str.isdigit() else 1
        return 0

    def render_shop_view(self):
        self.content_area.clear_widgets()

        search_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(4))
        search_input = TextInput(
            text=self.search_query,
            hint_text="🔍 Search dry fruits, nuts, seeds...",[cite: 2]
            multiline=False,
            size_hint_x=0.8,
        )
        search_input.bind(text=lambda ins, val: setattr(self, "search_query", val))

        clear_btn = Button(
            text="Clear",
            size_hint_x=0.2,
            background_color=(0.988, 0.905, 0.952, 1),
            color=(0.858, 0.152, 0.466, 1),
        )
        clear_btn.bind(
            on_press=lambda x: (
                setattr(self, "search_query", ""),
                self.render_shop_view(),
            )
        )

        search_layout.add_widget(search_input)
        search_layout.add_widget(clear_btn)
        self.content_area.add_widget(search_layout)

        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        q = self.search_query.strip().lower()
        filtered = (
            [
                p
                for p in self.product_records
                if q in p["name"].lower() or q in p["category"].lower()
            ]
            if q
            else self.product_records
        )

        for prod in filtered:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(170),
                padding=dp(4),
            )
            card.add_widget(
                Label(
                    text="10 MINS",
                    font_size=dp(9),
                    color=(0.39, 0.45, 0.54, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )
            card.add_widget(
                Label(
                    text=prod["name"],
                    font_size=dp(11),
                    bold=True,
                    color=(0.06, 0.09, 0.16, 1),
                    size_hint_y=None,
                    height=dp(26),
                )
            )
            card.add_widget(
                Label(
                    text=prod["description"],
                    font_size=dp(9),
                    color=(0.39, 0.45, 0.54, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )
            card.add_widget(
                Label(
                    text="10% OFF",
                    font_size=dp(9),
                    bold=True,
                    color=(0.02, 0.58, 0.41, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )

            base_price = float(
                "".join([
                    c
                    for c in str(prod["price"])
                    if c.isdigit() or c == "."
                ])
                or 0
            )
            card.add_widget(
                Label(
                    text=f"₹{int(base_price)}",
                    font_size=dp(12),
                    bold=True,
                    color=(0.06, 0.09, 0.16, 1),
                    size_hint_y=None,
                    height=dp(20),
                )
            )

            qty_layout = BoxLayout(size_hint_y=None, height=dp(28), spacing=dp(4))
            minus_btn = Button(
                text="-",
                background_color=(0.988, 0.905, 0.952, 1),
                color=(0.858, 0.152, 0.466, 1),
            )
            minus_btn.product_name = prod["name"]
            minus_btn.bind(on_press=self.decrement_cart)

            current_qty = self.get_cart_qty(prod["name"])
            qty_label = Label(
                text=str(current_qty),
                font_size=dp(12),
                bold=True,
                color=(0.858, 0.152, 0.466, 1),
            )

            plus_btn = Button(
                text="+",
                background_color=(0.988, 0.905, 0.952, 1),
                color=(0.858, 0.152, 0.466, 1),
            )
            plus_btn.product_name = prod["name"]
            plus_btn.bind(on_press=self.increment_cart)

            qty_layout.add_widget(minus_btn)
            qty_layout.add_widget(qty_label)
            qty_layout.add_widget(plus_btn)
            card.add_widget(qty_layout)
            grid.add_widget(card)

        scroll.add_widget(grid)
        self.content_area.add_widget(scroll)

        if len(self.cart) > 0:
            total_qty = sum([
                int(str(i.get("quantity", "1")).split()[0]) for i in self.cart
            ])
            bottom_bar = BoxLayout(
                size_hint_y=None, height=dp(50), padding=dp(8), spacing=dp(10)
            )
            view_cart_btn = Button(
                text="View Cart 🛒",
                size_hint_x=0.4,
                background_color=(0.145, 0.388, 0.921, 1),
                color=(1, 1, 1, 1),
            )
            view_cart_btn.bind(on_press=lambda x: self.render_cart_view())
            info_label = Label(
                text=f"{total_qty} Item(s) in Cart\nReady to Checkout",
                font_size=dp(10),
                color=(0.06, 0.09, 0.16, 1),
            )
            bottom_bar.add_widget(view_cart_btn)
            bottom_bar.add_widget(info_label)
            self.content_area.add_widget(bottom_bar)

    def increment_cart(self, instance):
        p_name = instance.product_name
        found = False
        for item in self.cart:
            if item.get("product") == p_name:
                q_val = int(str(item.get("quantity", "1")).split()[0])
                item["quantity"] = f"{q_val + 1} Unit"
                found = True
                break
        if not found:
            self.cart.append({"product": p_name, "quantity": "1 Unit"})
        self.render_shop_view()

    def decrement_cart(self, instance):
        p_name = instance.product_name
        for idx, item in enumerate(self.cart):
            if item.get("product") == p_name:
                q_val = int(str(item.get("quantity", "1")).split()[0])
                if q_val > 1:
                    item["quantity"] = f"{q_val - 1} Unit"
                else:
                    self.cart.pop(idx)
                break
        self.render_shop_view()

    def render_cart_view(self):
        self.content_area.clear_widgets()
        scroll = ScrollView()
        layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(10),
        )
        layout.bind(minimum_height=layout.setter("height"))

        layout.add_widget(
            Label(
                text="Your Shopping Cart & Checkout",
                font_size=dp(16),
                bold=True,
                size_hint_y=None,
                height=dp(30),
                color=(0.06, 0.09, 0.16, 1),
            )
        )

        if not self.cart:
            layout.add_widget(
                Label(
                    text="Your cart is empty.",
                    size_hint_y=None,
                    height=dp(40),
                    color=(0.06, 0.09, 0.16, 1),
                )
            )
        else:
            for idx, item in enumerate(self.cart):
                row = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(10))
                row.add_widget(
                    Label(
                        text=f"{item.get('product')} ({item.get('quantity')})",
                        color=(0.06, 0.09, 0.16, 1),
                    )
                )
                rem_btn = Button(
                    text="Remove",
                    size_hint_x=0.3,
                    background_color=(0.988, 0.905, 0.952, 1),
                    color=(0.858, 0.152, 0.466, 1),
                )
                rem_btn.idx = idx
                rem_btn.bind(
                    on_press=lambda ins: (
                        self.cart.pop(ins.idx),
                        self.render_cart_view(),
                    )
                )
                row.add_widget(rem_btn)
                layout.add_widget(row)

            layout.add_widget(
                Label(
                    text="Secure Checkout Form",
                    font_size=dp(14),
                    bold=True,
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.06, 0.09, 0.16, 1),
                )
            )
            self.address_input = TextInput(
                hint_text="Delivery Address:",
                size_hint_y=None,
                height=dp(70),
            )
            self.contact_input = TextInput(
                hint_text="Alternative Contact Number:",
                size_hint_y=None,
                height=dp(40),
                multiline=False,
            )
            layout.add_widget(self.address_input)
            layout.add_widget(self.contact_input)

            checkout_btn = Button(
                text="Complete Order",
                size_hint_y=None,
                height=dp(40),
                background_color=(0.137, 0.772, 0.368, 1),
                color=(1, 1, 1, 1),
            )
            checkout_btn.bind(on_press=self.complete_order)
            layout.add_widget(checkout_btn)

        back_btn = Button(
            text="Return to Shop",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.145, 0.388, 0.921, 1),
            color=(1, 1, 1, 1),
        )
        back_btn.bind(on_press=lambda x: self.render_shop_view())
        layout.add_widget(back_btn)

        scroll.add_widget(layout)
        self.content_area.add_widget(scroll)

    def complete_order(self, instance):
        addr = self.address_input.text.strip()
        contact = self.contact_input.text.strip()
        if addr and contact:
            cart_summary = ", ".join([
                f"{i.get('quantity')} of {i.get('product')}" for i in self.cart
            ])
            wa_message = f"*New Order - HMB Nuts & Seeds*\n\n*Items:* {cart_summary}\n*Address:* {addr}\n*Contact:* {contact}"[cite: 2]
            encoded_message = urllib.parse.quote(wa_message)
            wa_link = f"https://api.whatsapp.com/send?phone=919840450113&text={encoded_message}"[cite: 2]
            import webbrowser

            webbrowser.open(wa_link)
            self.cart = []
            self.render_shop_view()


if __name__ == "__main__":
    HMBNutsApp().run()[cite: 2]
