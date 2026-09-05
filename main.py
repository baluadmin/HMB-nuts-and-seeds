from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import os
import pandas as pd
import urllib.parse


class HMBNutsApp(App):[cite: 2]

    def build(self):[cite: 2]
        self.title = "HMB Nuts & Spices"[cite: 2]
        self.cart = [][cite: 2]
        self.search_query = ""[cite: 2]
        self.current_view = "Shop"[cite: 2]

        self.load_products()[cite: 2]

        self.root_layout = BoxLayout([cite: 2]
            orientation="vertical", padding=dp(4), spacing=dp(4)
        )
        self.root_layout.canvas.before.clear()[cite: 2]
        from kivy.graphics import Color, Rectangle

        with self.root_layout.canvas.before:[cite: 2]
            Color(0.878, 0.949, 0.996, 1)  # #e0f2fe background color[cite: 2]
            self.bg_rect = Rectangle([cite: 2]
                size=self.root_layout.size, pos=self.root_layout.pos
            )
        self.root_layout.bind(size=self._update_bg, pos=self._update_bg)[cite: 2]

        self.content_area = BoxLayout(orientation="vertical")[cite: 2]
        self.root_layout.add_widget(self.content_area)[cite: 2]

        self.render_shop_view()[cite: 2]
        return self.root_layout[cite: 2]

    def _update_bg(self, instance, value):[cite: 2]
        self.bg_rect.size = instance.size[cite: 2]
        self.bg_rect.pos = instance.pos[cite: 2]

    def load_products(self):[cite: 2]
        csv_url = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"[cite: 2]
        try:
            df = pd.read_csv(csv_url)[cite: 2]
            self.product_records = [][cite: 2]
            for _, row in df.iterrows():[cite: 2]
                if (
                    len(row) > 4
                    and pd.notna(row.iloc[0])
                    and str(row.iloc[0]).strip() != "id"
                ):
                    self.product_records.append({[cite: 2]
                        "id": str(row.iloc[0]),
                        "name": str(row.iloc[1]),
                        "category": str(row.iloc[2]).strip(),
                        "stock": str(row.iloc[3]),
                        "price": str(row.iloc[4]),
                        "description": (
                            str(row.iloc[5])
                            if len(row) > 5 and pd.notna(row.iloc[5])
                            else "1 Pack"
                        ),
                    })
        except Exception:
            self.product_records = [[cite: 2]
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
            ]

    def get_cart_qty(self, prod_name):[cite: 2]
        for item in self.cart:[cite: 2]
            if item.get("product") == prod_name:[cite: 2]
                q_str = str(item.get("quantity", "1 Unit")).split()[0][cite: 2]
                return int(q_str) if q_str.isdigit() else 1[cite: 2]
        return 0[cite: 2]

    def render_shop_view(self):[cite: 2]
        self.content_area.clear_widgets()[cite: 2]

        search_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(4))[cite: 2]
        search_input = TextInput([cite: 2]
            text=self.search_query,
            hint_text="🔍 Search dry fruits, nuts, seeds...",
            multiline=False,
            size_hint_x=0.8,
        )
        search_input.bind(text=lambda ins, val: setattr(self, "search_query", val))[cite: 2]

        clear_btn = Button([cite: 2]
            text="Clear",
            size_hint_x=0.2,
            background_color=(0.988, 0.905, 0.952, 1),
            color=(0.858, 0.152, 0.466, 1),
        )
        clear_btn.bind([cite: 2]
            on_press=lambda x: (
                setattr(self, "search_query", ""),
                self.render_shop_view(),
            )
        )

        search_layout.add_widget(search_input)[cite: 2]
        search_layout.add_widget(clear_btn)[cite: 2]
        self.content_area.add_widget(search_layout)[cite: 2]

        scroll = ScrollView()[cite: 2]
        grid = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)[cite: 2]
        grid.bind(minimum_height=grid.setter("height"))[cite: 2]

        q = self.search_query.strip().lower()[cite: 2]
        filtered = ([cite: 2]
            [
                p
                for p in self.product_records
                if q in p["name"].lower() or q in p["category"].lower()
            ]
            if q
            else self.product_records
        )

        for prod in filtered:[cite: 2]
            card = BoxLayout([cite: 2]
                orientation="vertical",
                size_hint_y=None,
                height=dp(170),
                padding=dp(4),
            )
            card.add_widget([cite: 2]
                Label(
                    text="10 MINS",
                    font_size=dp(9),
                    color=(0.39, 0.45, 0.54, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )
            card.add_widget([cite: 2]
                Label(
                    text=prod["name"],
                    font_size=dp(11),
                    bold=True,
                    color=(0.06, 0.09, 0.16, 1),
                    size_hint_y=None,
                    height=dp(26),
                )
            )
            card.add_widget([cite: 2]
                Label(
                    text=prod["description"],
                    font_size=dp(9),
                    color=(0.39, 0.45, 0.54, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )
            card.add_widget([cite: 2]
                Label(
                    text="10% OFF",
                    font_size=dp(9),
                    bold=True,
                    color=(0.02, 0.58, 0.41, 1),
                    size_hint_y=None,
                    height=dp(14),
                )
            )

            base_price = float([cite: 2]
                "".join([
                    c
                    for c in str(prod["price"])
                    if c.isdigit() or c == "."
                ])
                or 0
            )
            card.add_widget([cite: 2]
                Label(
                    text=f"₹{int(base_price)}",
                    font_size=dp(12),
                    bold=True,
                    color=(0.06, 0.09, 0.16, 1),
                    size_hint_y=None,
                    height=dp(20),
                )
            )

            qty_layout = BoxLayout(size_hint_y=None, height=dp(28), spacing=dp(4))[cite: 2]
            minus_btn = Button([cite: 2]
                text="-",
                background_color=(0.988, 0.905, 0.952, 1),
                color=(0.858, 0.152, 0.466, 1),
            )
            minus_btn.product_name = prod["name"][cite: 2]
            minus_btn.bind(on_press=self.decrement_cart)[cite: 2]

            current_qty = self.get_cart_qty(prod["name"])[cite: 2]
            qty_label = Label([cite: 2]
                text=str(current_qty),
                font_size=dp(12),
                bold=True,
                color=(0.858, 0.152, 0.466, 1),
            )

            plus_btn = Button([cite: 2]
                text="+",
                background_color=(0.988, 0.905, 0.952, 1),
                color=(0.858, 0.152, 0.466, 1),
            )
            plus_btn.product_name = prod["name"][cite: 2]
            plus_btn.bind(on_press=self.increment_cart)[cite: 2]

            qty_layout.add_widget(minus_btn)[cite: 2]
            qty_layout.add_widget(qty_label)[cite: 2]
            qty_layout.add_widget(plus_btn)[cite: 2]
            card.add_widget(qty_layout)[cite: 2]
            grid.add_widget(card)[cite: 2]

        scroll.add_widget(grid)[cite: 2]
        self.content_area.add_widget(scroll)[cite: 2]

        if len(self.cart) > 0:[cite: 2]
            total_qty = sum([[cite: 2]
                int(str(i.get("quantity", "1")).split()[0]) for i in self.cart
            ])
            bottom_bar = BoxLayout([cite: 2]
                size_hint_y=None, height=dp(50), padding=dp(8), spacing=dp(10)
            )
            view_cart_btn = Button([cite: 2]
                text="View Cart 🛒",
                size_hint_x=0.4,
                background_color=(0.145, 0.388, 0.921, 1),
                color=(1, 1, 1, 1),
            )
            view_cart_btn.bind(on_press=lambda x: self.render_cart_view())[cite: 2]
            info_label = Label([cite: 2]
                text=f"{total_qty} Item(s) in Cart\nReady to Checkout",
                font_size=dp(10),
                color=(0.06, 0.09, 0.16, 1),
            )
            bottom_bar.add_widget(view_cart_btn)[cite: 2]
            bottom_bar.add_widget(info_label)[cite: 2]
            self.content_area.add_widget(bottom_bar)[cite: 2]

    def increment_cart(self, instance):[cite: 2]
        p_name = instance.product_name[cite: 2]
        found = False[cite: 2]
        for item in self.cart:[cite: 2]
            if item.get("product") == p_name:[cite: 2]
                q_val = int(str(item.get("quantity", "1")).split()[0])[cite: 2]
                item["quantity"] = f"{q_val + 1} Unit"[cite: 2]
                found = True[cite: 2]
                break
        if not found:[cite: 2]
            self.cart.append({"product": p_name, "quantity": "1 Unit"})[cite: 2]
        self.render_shop_view()[cite: 2]

    def decrement_cart(self, instance):[cite: 2]
        p_name = instance.product_name[cite: 2]
        for idx, item in enumerate(self.cart):[cite: 2]
            if item.get("product") == p_name:[cite: 2]
                q_val = int(str(item.get("quantity", "1")).split()[0])[cite: 2]
                if q_val > 1:[cite: 2]
                    item["quantity"] = f"{q_val - 1} Unit"[cite: 2]
                else:
                    self.cart.pop(idx)[cite: 2]
                break
        self.render_shop_view()[cite: 2]

    def render_cart_view(self):[cite: 2]
        self.content_area.clear_widgets()[cite: 2]
        scroll = ScrollView()[cite: 2]
        layout = BoxLayout([cite: 2]
            orientation="vertical",
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(10),
        )
        layout.bind(minimum_height=layout.setter("height"))[cite: 2]

        layout.add_widget([cite: 2]
            Label(
                text="Your Shopping Cart & Checkout",
                font_size=dp(16),
                bold=True,
                size_hint_y=None,
                height=dp(30),
                color=(0.06, 0.09, 0.16, 1),
            )
        )

        if not self.cart:[cite: 2]
            layout.add_widget([cite: 2]
                Label(
                    text="Your cart is empty.",
                    size_hint_y=None,
                    height=dp(40),
                    color=(0.06, 0.09, 0.16, 1),
                )
            )
        else:
            for idx, item in enumerate(self.cart):[cite: 2]
                row = BoxLayout(size_hint_y=None, height=dp(35), spacing=dp(10))[cite: 2]
                row.add_widget([cite: 2]
                    Label(
                        text=f"{item.get('product')} ({item.get('quantity')})",
                        color=(0.06, 0.09, 0.16, 1),
                    )
                )
                rem_btn = Button([cite: 2]
                    text="Remove",
                    size_hint_x=0.3,
                    background_color=(0.988, 0.905, 0.952, 1),
                    color=(0.858, 0.152, 0.466, 1),
                )
                rem_btn.idx = idx[cite: 2]
                rem_btn.bind([cite: 2]
                    on_press=lambda ins: (
                        self.cart.pop(ins.idx),
                        self.render_cart_view(),
                    )
                )
                row.add_widget(rem_btn)[cite: 2]
                layout.add_widget(row)[cite: 2]

            layout.add_widget([cite: 2]
                Label(
                    text="Secure Checkout Form",
                    font_size=dp(14),
                    bold=True,
                    size_hint_y=None,
                    height=dp(30),
                    color=(0.06, 0.09, 0.16, 1),
                )
            )
            self.address_input = TextInput([cite: 2]
                hint_text="Delivery Address:",
                size_hint_y=None,
                height=dp(70),
            )
            self.contact_input = TextInput([cite: 2]
                hint_text="Alternative Contact Number:",
                size_hint_y=None,
                height=dp(40),
                multiline=False,
            )
            layout.add_widget(self.address_input)[cite: 2]
            layout.add_widget(self.contact_input)[cite: 2]

            checkout_btn = Button([cite: 2]
                text="Complete Order",
                size_hint_y=None,
                height=dp(40),
                background_color=(0.137, 0.772, 0.368, 1),
                color=(1, 1, 1, 1),
            )
            checkout_btn.bind(on_press=self.complete_order)[cite: 2]
            layout.add_widget(checkout_btn)[cite: 2]

        back_btn = Button([cite: 2]
            text="Return to Shop",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.145, 0.388, 0.921, 1),
            color=(1, 1, 1, 1),
        )
        back_btn.bind(on_press=lambda x: self.render_shop_view())[cite: 2]
        layout.add_widget(back_btn)[cite: 2]

        scroll.add_widget(layout)[cite: 2]
        self.content_area.add_widget(scroll)[cite: 2]

    def complete_order(self, instance):[cite: 2]
        addr = self.address_input.text.strip()[cite: 2]
        contact = self.contact_input.text.strip()[cite: 2]
        if addr and contact:[cite: 2]
            cart_summary = ", ".join([[cite: 2]
                f"{i.get('quantity')} of {i.get('product')}" for i in self.cart
            ])
            wa_message = f"*New Order - HMB Nuts & Seeds*\n\n*Items:* {cart_summary}\n*Address:* {addr}\n*Contact:* {contact}"[cite: 2]
            encoded_message = urllib.parse.quote(wa_message)[cite: 2]
            wa_link = f"https://api.whatsapp.com/send?phone=919840450113&text={encoded_message}"[cite: 2]
            import webbrowser

            webbrowser.open(wa_link)[cite: 2]
            self.cart = [][cite: 2]
            self.render_shop_view()[cite: 2]


if __name__ == "__main__":[cite: 2]
    HMBNutsApp().run()[cite: 2]
