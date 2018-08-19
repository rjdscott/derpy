

class Bond:
    
    def __init__(self, cpn=None, mty=None, px=None, yld=None,  **kwargs):
        self.cpn = cpn
        self.mty = mty
        self.px = px
        self.yld = yld

    def __repr__(self):
        return "Bond(cpn={}, mty={}, px={}, yld={})".format(self.cpn,
                                                            self.mty,
                                                            self.px,
                                                            self.yld)
    