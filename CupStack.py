import decimal

decimal.getcontext().prec = 16


CUP_VOLUME = decimal.Decimal(0.25)

class CupStack:
    def __init__(self, full=0, capacity=CUP_VOLUME, levels=0):
        super().__init__()
        
        self._full      = decimal.Decimal(full)
        self._capacity  = decimal.Decimal(capacity)

        if levels > 0:
            cups = [
                [
                    CupStack(full=full, capacity=capacity)
                    for j in range(i + 2)
                ]
                for i in range(levels)
            ]
            
            # Make each child find it's 2 parents
            for i in range(levels - 1, 0, -1):
                for j in range(len(cups[i])):
                    if j < i + 1: cups[i-1][j  ]._l = cups[i][j]
                    if j > 0:     cups[i-1][j-1]._r = cups[i][j]

            # Finally, attach the first row
            self._l, self._r = cups[0]

        else:
            self._l = None
            self._r = None

    def __repr__(self):
        return '.'


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