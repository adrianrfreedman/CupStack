import decimal

decimal.getcontext().prec = 16


CUP_VOLUME = decimal.Decimal(0.25)

class CupStack:
    def __init__(self, full=0, capacity=CUP_VOLUME, levels=1):
        super().__init__()
        
        self._full      = decimal.Decimal(full)
        self._capacity  = decimal.Decimal(capacity)

        self._l = self.__init__(full, capacity, levels - 1) if levels > 1 else None
        self._r = self.__init__(full, capacity, levels - 1) if levels > 1 else None


    @property
    def full(self): return float(self._full)

    @property
    def capacity(self): return float(self._capacity)

    @property
    def l(self): return self._l
    
    @property
    def r(self): return self._r
    
    def fill(self, amount):
        self._full += decimal.Decimal(amount)

        if self.full > self.capacity:
            overflow = self.full - self.capacity
            self._full = self.capacity

            if self.l is not None: self.l.fill(overflow / 2)
            if self.r is not None: self.r.fill(overflow / 2)