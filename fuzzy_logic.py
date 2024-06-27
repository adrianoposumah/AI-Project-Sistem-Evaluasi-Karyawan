import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def evaluate_performance(productivity, quality, discipline, initiative):
    # Define fuzzy variables
    productivity_lv = ctrl.Antecedent(np.arange(0, 11, 1), 'productivity')
    quality_lv = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
    discipline_lv = ctrl.Antecedent(np.arange(0, 11, 1), 'discipline')
    initiative_lv = ctrl.Antecedent(np.arange(0, 11, 1), 'initiative')
    performance_lv = ctrl.Consequent(np.arange(0, 101, 1), 'performance')

    # Define membership functions
    names = ['low', 'average', 'high']
    for var in [productivity_lv, quality_lv, discipline_lv, initiative_lv]:
        var.automf(names=names)

    performance_lv['poor'] = fuzz.trimf(performance_lv.universe, [0, 0, 50])
    performance_lv['good'] = fuzz.trimf(performance_lv.universe, [0, 50, 100])
    performance_lv['excellent'] = fuzz.trimf(performance_lv.universe, [50, 100, 100])

    # Define rules
    rules = [
        ctrl.Rule(productivity_lv['high'] & quality_lv['high'] & discipline_lv['high'] & initiative_lv['high'], performance_lv['excellent']),
        ctrl.Rule(productivity_lv['average'] & quality_lv['average'] & discipline_lv['average'] & initiative_lv['average'], performance_lv['good']),
        ctrl.Rule(productivity_lv['low'] | quality_lv['low'] | discipline_lv['low'] | initiative_lv['low'], performance_lv['poor'])
    ]

    # Create control system
    performance_ctrl = ctrl.ControlSystem(rules)
    performance = ctrl.ControlSystemSimulation(performance_ctrl)

    # Pass inputs to the control system
    performance.input['productivity'] = productivity
    performance.input['quality'] = quality
    performance.input['discipline'] = discipline
    performance.input['initiative'] = initiative

    # Compute the result
    performance.compute()
    return performance.output['performance']
