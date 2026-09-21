# **Code: Infectiousness-Dependence Coefficient (IDC) ABM Simulation**

This repository contains the simulation code and analytical scripts required to reproduce the agent-based modeling (ABM) results presented in the study. The model is built upon the [Covasim](https://github.com/InstituteforDiseaseModeling/covasim) framework to investigate the **Infectiousness-Dependence Coefficient (IDC)** mechanism within transmission pairs.

---

## **1. Overview**

The provided scripts execute a highly parameterized ABM that models infectious disease transmission (e.g., Influenza A, SARS-CoV-2) across age-stratified populations. 

**Key Methodological Features:**
* **Transmission Pair Correlation:** Mathematically links the peak infectiousness (viral load) of secondary cases to their index cases.
* **Empirical Demographic Integration:** Used Hong Kong's age-structured census data (2009–2022).
* **High-Resolution Network Logging:** Extracts and records generational transmission trees and individual reproduction numbers ($R$) to analyze disease dispersion and superspreading phenomena.
* **NPI Evaluation:** Simulates targeted Non-Pharmaceutical Interventions (NPIs) including testing, isolation, and contact tracing.

---

## **2. Repository Structure**

The execution pipeline consists of three core Python modules:

* `run_example.py`: **Main execution script.** Parses scenario configurations, initializes the synthetic population, applies interventions, executes the simulation loop, and extracts transmission trees.
* `base_func.py`: **Analytical module.** Contains post-simulation utility functions to compute individual reproduction numbers, age-stratified attack rates, cross-layer transmission proportions, and generation intervals.
* `base_data.py`: **Empirical data repository.** Defines disease progression distributions (latent/infectious periods) and baseline demographic arrays.

---

## **3. System Requirements & Installation**


The code requires **Python 3.8+** and the customized Covasim framework provided in the parent directory.