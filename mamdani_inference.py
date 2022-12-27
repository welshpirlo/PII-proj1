import numpy as np
import std_mfs
import itertools
import operations
import fuzzifier
import defuzzifier
import type_reducer
import sm

def preprocessing(input_lvs, output_lv):
    for item in input_lvs:
        item['U'] = np.arange(0, 10, 0.01)
    output_lv['U'] = np.arange(0, 10, 0.01)

    for lv in input_lvs:
        for term in lv['terms'].values():
            umf_type, *umf_params = term['umf']
            lmf_type, *lmf_params = term['lmf']
            term['umf'] = getattr(std_mfs, umf_type)(lv['U'], *umf_params)
            term['lmf'] = getattr(std_mfs, lmf_type)(lv['U'], *lmf_params)

    for term in output_lv['terms'].values():
        umf_type, *umf_params = term['umf']
        lmf_type, *lmf_params = term['lmf']
        term['umf'] = getattr(std_mfs, umf_type)(output_lv['U'], *umf_params)
        term['lmf'] = getattr(std_mfs, lmf_type)(output_lv['U'], *lmf_params)


def activated_rules(fuzzy_values, rule_base):
    terms = (item.keys() for item in fuzzy_values.values())
    antecedents = tuple(itertools.product(*terms))
    return [rule for rule in rule_base if rule[0] in antecedents]


def implication(fuzzy_values, activated_rules, output_lv):
    result = []
    for rule in activated_rules:
        antecedent, consequent = rule
        mfs = [fuzzy_values[index][term] for index, term in enumerate(antecedent)]
        lmfs = [lmf for lmf, _ in mfs]
        umfs = [umf for _, umf in mfs]

        tmp = operations.t2_fuzzy_min(output_lv['terms'][consequent], min(lmfs), min(umfs))
        result.append(tmp)
    return result

def aggregation(*fuzzy_sets):
    return operations.t2_fuzzy_union(*fuzzy_sets)


def process(input_lvs, output_lv, rule_base, crisp_values):
    fuzzy_values = fuzzifier.fuzzification(crisp_values, input_lvs)
    act_rules = activated_rules(fuzzy_values, rule_base)
    imp_res = implication(fuzzy_values, act_rules, output_lv)
    t2fs = aggregation(*imp_res)
    result = type_reducer.EKM(output_lv['U'], *t2fs)
    result = defuzzifier.defuzzification(output_lv['U'], result)

    words = []
    for term, mfs in output_lv['terms'].items():
        tmp = sm.jaccard_measure({'lmf': t2fs[0], 'umf': t2fs[1]}, mfs)
        words.append((term, tmp))

    word_result = max(words, key=lambda item: item[1])

    return result, word_result[0]







