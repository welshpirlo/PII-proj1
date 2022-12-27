import unittest
import model
import mamdani_inference
import numpy as np
import std_mfs
import itertools
import operations
import fuzzifier
import defuzzifier
import type_reducer
import sm

class TestMethods(unittest.TestCase):
    mamdani_inference.preprocessing(model.input_lvs, model.output_lv)

    def test_excellent(self):
        crisps = (10, 100, 1, 9)
        res = mamdani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisps)
        self.assertEqual(res[1], 'excellent')

    def test_awful(self):
        crisps = (190, 1900, 9, 1)
        res = mamdani_inference.process(model.input_lvs, model.output_lv, model.rule_base, crisps)
        self.assertEqual(res[1], 'awful')

    def test_activated_riles(self):
        crisps = (190, 1900, 9, 1)
        fuzzy_values = fuzzifier.fuzzification(crisps, model.input_lvs)
        act_rules = mamdani_inference.activated_rules(fuzzy_values, model.rule_base)
        print(act_rules)
        self.assertEqual(act_rules, [(('huge', 'extremely high', 'lengthy', 'little'), 'awful'),
                                     (('huge', 'extremely high', 'lengthy', 'enough'), 'awful')])



if __name__ == '__main__':
    unittest.main()