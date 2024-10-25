
class Price(float):
    def __new__(cls, value, unit):
        instance = super().__new__(cls, value)
        instance.unit = unit
        return instance

    @property
    def value(self):
        return float(self)

    def __repr__(self):
        return f"Price(value={self.value}, unit='{self.unit}')"

    def __str__(self):
        return f"{self.value:,.2f} {self.unit}"
