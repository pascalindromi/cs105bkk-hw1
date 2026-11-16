"""HW1: a Bangkok food-delivery order. Practises Sessions 1-3: aliasing and defaults, comprehensions,
classes with a guarded property, __repr__ and __eq__, inheritance with super(), composition and duck typing."""


class MenuItem:
    """A dish on a restaurant's menu. The price is a whole number of baht."""

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    @property
    def price(self) -> int:
        """Provided: the price in baht."""
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        if value <= 0:
            raise ValueError
        self._price = value

    def __repr__(self) -> str:
        return f"MenuItem({repr(self.name)}, {self.price})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MenuItem):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def cost(self, quantity: int) -> int:
        return self.price * quantity


class PromoItem(MenuItem):
    """A dish on a "buy 2, get 1 free" promotion: every third one is free."""

    def __init__(self, name: str, price: int):
        super().__init__(name, price)

    def cost(self, quantity: int) -> int:
        return self.price * (quantity - (quantity // 3))


class Order:

    delivery_fee = 30  # Provided: baht added to every order with food in it
    free_delivery_from = 300  # Provided: food worth this much or more is delivered free

    def __init__(self, customer: str, lines: list[tuple[MenuItem, int]] | None = None):
        self.customer = customer
        self.lines = list(lines) if lines is not None else []
        self.order = list(self.lines)

    def add(self, item: MenuItem, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError

        found = False
        new_lines = []
        for existing_item, existing_quantity in self.lines:
            if existing_item == item:
                new_lines.append((existing_item, existing_quantity + quantity))
                found = True
            else:
                new_lines.append((existing_item, existing_quantity))

        if not found:
            new_lines.append((item, quantity))

        self.lines = new_lines

    def total(self) -> int:
        subtotal = sum(item.cost(quantity) for item, quantity in self.lines)
        if subtotal == 0:
            return 0
        if subtotal >= self.free_delivery_from:
            return subtotal
        return subtotal + self.delivery_fee

    def summary(self) -> list[str]:
        return [f"{quantity} x {item.name}" for item, quantity in self.lines]


def cheapest(options: list) -> object | None:
    if not options:
        return None

    smallest_price = None
    cheapest_item = None
    for order in options:
        current_total = order.total()
        if smallest_price is None or current_total < smallest_price:
            smallest_price = current_total
            cheapest_item = order
    return cheapest_item
