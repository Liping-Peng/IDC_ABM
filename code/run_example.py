"""
Infectiousness-Dependence Coefficient (IDC) ABM Simulation
==========================================================
Main Execution Script for IDC ABM Simulation. Execute this file to start the simulation.

==========================================================
This module implements an agent-based model for infectious disease transmission
using the customized Covasim framework. It is specifically designed to investigate
the Infectiousness-Dependence Coefficient (IDC) mechanism, exploring how peak viral
load correlates between index and secondary cases.

Key features:
- Mathematical execution of the IDC mechanism across specified contact layers
- Age-structured population based on Hong Kong demographics
- Multiple transmission networks (household, school, workplace, community)
- Pathogen-specific parameterization with age-stratified susceptibility and transmissibility
- High-resolution logging of generational transmission trees and individual reproduction numbers
- Evaluation of Non-Pharmaceutical Interventions (NPIs) including testing, isolation, and contact tracing


Author: Liping Peng
Institution: The University of Hong Kong
Date: 22 September 2026

"""

import copy
import datetime
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as pl
import covasim as cv
import os
import sciris as sc
import optuna
from statistics import mean
import random
import re
import itertools

import base_func as bfc
from base_func import fun_tree_indi_R, func_combine_data
from base_data import dis_prog_FluA, dis_prog_Cov, dis_prog_Omicron, HK_pop_2009, HK_pop_2020, HK_pop_2015, HK_pop_2022
from covasim import utils as cvu
from covasim import misc as cvm
from covasim import interventions as cvi
from covasim import plotting as cvpl
from covasim import run as cvr



def main_simulation(begin_seed, N):
    """
    Execute the core simulation loop across specified random seeds, compile detailed
    agent-level transmission networks, and export the simulation results.
    """
    sims = []
    sims_seed = []

    # Single scenario execution and agent-level detail extraction
    for n in range(begin_seed, begin_seed + N):
        # Create people
        # with sc.timer('creating'):
        #     sim_base = cv.Sim(pars_base, label=scenario,
        #                   interventions=scen_intervention,
        #                   rand_seed=n
        #                   ).init_people()
        # sim_base.people.save(f'result/load_people/example_ppl_{Disease}.ppl')

        # load the created population, if people have been created
        with sc.timer('loading'):
            sim_base = cv.Sim(pars_base, label=scenario,
                              interventions=scen_intervention,
                              rand_seed=n,
                              popfile=f'result/load_people/example_ppl_{Disease}.ppl').init_people()

        sim_base.run(verbose=False)

        # Reconstruct the transmission tree
        tt = sim_base.make_transtree(to_networkx=True)

        # Export detailed agent-level transmission log
        tree_detail = tt.detailed
        tree_detail = tree_detail[
            ['source', 'target', 'date', 'layer', 'trg_age', 'src_age', 'trg_date_exposed', 'src_date_exposed']]
        tree_detail.to_excel(f"%s/tree_detail/tree%s.xlsx" % (output_path, n))

        # Calculate and export the individual reproduction number (R)
        individual_r = fun_tree_indi_R(tree_detail)
        individual_r.to_excel(f"%s/tree_detail/Individual_R%s.xlsx" % (output_path, n))

        # Export specific infectiousness of index and secondary cases
        test1 = sim_base.people.LP_trans_log
        test1 = pd.concat([x for x in test1])
        test1.to_excel(f"%s/tree_detail/Infectiousness%s.xlsx" % (output_path, n), index=False)

        # Process and compile final simulation data
        func_combine_data(sim=sim_base, output_path=output_path, n=n)

        # Output overall summary of the simulation run
        sim_base.to_excel("%s/sims_detail/sim%s.xlsx" % (output_path, n))



if __name__ == "__main__":

    # ---------------------------------------------------------
    # System path and global execution timer initialization
    # ---------------------------------------------------------
    time1 = datetime.datetime.now()
    path = "D:/ABM trans/"
    os.chdir(path)

    # ---------------------------------------------------------
    # Baseline demographic and epidemiological configurations
    # ---------------------------------------------------------
    begin_seed = 0
    run_times = 1

    Disease = 'FluA'  # Target viral pathogen
    dis_prog = dis_prog_FluA  # Disease progression parameters
    HK_pop = HK_pop_2009  # Demographic baseline (Hong Kong population structure)
    total_pop = sum([HK_pop[key] for key in HK_pop])

    # Pathogen-specific clinical and transmission parameters
    LP_trans_ORs = np.array([1.6, 0.8, 0.8, 0.8, 0.8], dtype=float)
    LP_sus_ORs = np.array([1.3, 1.3, 1.0, 0.9, 1.4], dtype=float)
    LP_symp_probs = np.array([0.75, 0.75, 0.75, 0.75, 0.75], dtype=float)
    viral_dist = dict(frac_time=0.4, load_ratio=8, high_cap=3)
    quar_period = 7  # Quarantine duration (e.g., 7 days for influenza, 14 for COVID-19)


    # ---------------------------------------------------------
    # Scenario definitions and batch execution
    # ---------------------------------------------------------
    list_Scenario = ['test_S0_Lyh_IDC0_NP1_NI500_Isd120_Bt125_TI0_QR0']
    print(len(list_Scenario))

    for scenario in list_Scenario:
        print("--------------Now begin running %s:【" % Disease, scenario, "】--------------")
        output_path = f'result/result_{Disease}/{scenario}'

        # Create localized directory structure for simulation outputs
        bfc.func_create_folder(output_path, 'figure')
        bfc.func_create_folder(output_path, 'sims_detail')
        bfc.func_create_folder(output_path, 'sims_multisim')
        bfc.func_create_folder(output_path, 'save_sim')
        bfc.func_create_folder(output_path, 'tree_detail')

        # ---------------------------------------------------------
        # Dynamic parameter extraction via regular expressions
        # ---------------------------------------------------------
        param_value = re.search("(S\\d+)_Ly(\\w+)_IDC(\\d+)_NP(\\d+)_NI(\\d+)_Isd(\\d+)_Bt(\\d+)_TI(\\d+)_QR(\\d+)",
                                scenario)
        scen_N = param_value.group(1)
        param_corr_layer = param_value.group(2)
        param_IDC = float(param_value.group(3)) * 0.01
        param_NPop = float(param_value.group(4)) * 0.01
        param_NInf = int(param_value.group(5))
        param_Isd = float(param_value.group(6)) * 0.01
        param_beta = float(param_value.group(7)) * 0.0001
        param_tip = float(param_value.group(8)) * 0.01
        param_qr = float(param_value.group(9)) * 0.01

        # ---------------------------------------------------------
        # Non-Pharmaceutical Interventions (NPIs) initialization
        # ---------------------------------------------------------
        if scen_N == "S0":
            scen_intervention = []
        elif scen_N == "S1":
            # Testing and self-isolation (behavioral compliance reduces transmissibility)
            intv_TI = cv.test_prob(symp_prob=param_tip, asymp_prob=0, start_day=0, test_delay=1)
            scen_intervention = [intv_TI]
        elif scen_N == "S2":
            intv_TI = cv.test_prob(symp_prob=param_tip, asymp_prob=0, start_day=0, test_delay=1)
            intv_QR = cv.contact_tracing(trace_probs=dict(h=param_qr, s=0, w=0, c=0), trace_time=1, start_day=0, quar_period=quar_period)
            scen_intervention = [intv_TI, intv_QR]
        elif scen_N == "S3":
            intv_TI = cv.test_prob(symp_prob=param_tip, asymp_prob=0, start_day=0, test_delay=1)
            intv_QR = cv.contact_tracing(trace_probs=dict(h=param_qr, s=param_qr, w=param_qr, c=0), trace_time=1, start_day=0, quar_period=quar_period)
            scen_intervention = [intv_TI, intv_QR]

        # ---------------------------------------------------------
        # Base parameter dictionary for Covasim instantiation
        # ---------------------------------------------------------
        pars_base = dict(
            location='Hong Kong',
            pop_type='hybrid',
            pop_scale=1,
            pop_size=round(total_pop * param_NPop, 0),
            pop_infected=param_NInf,
            beta=param_beta,
            start_day='2009-06-20',
            end_day='2010-02-20',
            dur=dis_prog,
            LP_Disease=Disease,
            LP_sus_ORs=LP_sus_ORs,
            LP_trans_ORs=LP_trans_ORs,
            LP_symp_probs=LP_symp_probs,
            LP_param_tip=param_tip,
            LP_trans_index_prop=param_IDC,
            LP_corr_layer=param_corr_layer,
            beta_dist=dict(dist='lognormal', par1=1.0, par2=param_Isd),
            asymp_factor=0.5,
            viral_dist=viral_dist
        )

        # Execute simulation for the current scenario
        main_simulation(begin_seed, run_times)

    time2 = datetime.datetime.now()
    print("Total Running Time: ", time2 - time1)



