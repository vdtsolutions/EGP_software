def Erf(self):
    length_of_defect_L = 24
    od_of_pipe_D = 323
    pipe_thickness_T = 6.35
    depth_of_defect_d = 2.8575
    specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS = 2498.3
    flow_stress = 1.1 * specified_minimum_yield_strength_of_material_at_ambient_condition_SMYS
    print("Sflow", flow_stress)

    z_factor = (length_of_defect_L * length_of_defect_L) / (od_of_pipe_D * pipe_thickness_T)
    print("Z_factor", z_factor)

    x = 1 + 0.8 * z_factor
    Building_stress_magmification_factor_M = pow(x, 1 / 2)
    print("Building_stress_magmification_factor_M", Building_stress_magmification_factor_M)
    y = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T
    z = 1 - 2 / 3 * depth_of_defect_d / pipe_thickness_T / Building_stress_magmification_factor_M
    k = y / z
    print(y)
    print(z)
    print(k)

    if z_factor <= 20:
        Estimated_failure_stress_level_SF = flow_stress * k
        print("estimated_failure_stress", Estimated_failure_stress_level_SF)
    else:
        Estimated_failure_stress_level_SF = flow_stress * (1 - depth_of_defect_d / pipe_thickness_T)
        print("estimated_failure_stress", Estimated_failure_stress_level_SF)
    estimate_failure_pressure = (2 * Estimated_failure_stress_level_SF * pipe_thickness_T) / od_of_pipe_D
    print("estimate_failure_pressure", estimate_failure_pressure)
    safety_factor_SF = 1.39
    safe_operating_pressure_of_corroded_area_Ps = estimate_failure_pressure / safety_factor_SF
    print("safe_operating_pressure_of_corroded_area_Ps", safe_operating_pressure_of_corroded_area_Ps)
    MAOP = 11
    ERF = MAOP / safe_operating_pressure_of_corroded_area_Ps
    print("Estimate Repair Factor", ERF)