class card:
    def __init__(self, name: str, price: float):
        self.name = name
        self.prices = []
        if price is not None:
            self.prices.append(price)

    def add_price(self, price: float):
        if price is None:
            return
        self.prices.append(price)
        self.prices = sorted(self.prices)

    def price_range(self) -> list:
        if len(self.prices) == 0:
            return [0, 0]
        return [float(self.prices[0]), float(self.prices[len(self.prices) - 1])]
