#!/usr/bin/env python
# -*- coding: utf-8 -*-

# future proof py2 vs py3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from derpy import bond as bd
import unittest


class TestBond(unittest.TestCase):

    def test_bond_ytm(self):
        px = 139.87
        mat = 12
        cpn_frq = 2
        cpn_rate = 6.25
        face_val = 99.94

        bond = bd.Bond(price=px, maturity=mat, cpn_freq=cpn_frq, cpn_rate=cpn_rate, face_value=face_val)
        expected_result = 0.023985917390473392
        self.assertAlmostEqual(bond.calc_ytm(), expected_result)


if __name__ == '__main__':
    unittest.main()
