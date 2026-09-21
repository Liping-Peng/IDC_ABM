## **Modified Files**

### **1. parameters.py**

#### 1.1 New Parameters

| **Parameter** | **Description** |
| :--- | :--- |
| `LP_Disease` | Target viral pathogen or variant identifier for the simulation. |
| `LP_trans_index_prop` | Infectiousness-Dependence Coefficient (IDC); proportion of the index case's peak infectiousness inherited by the secondary case (0.0 = independent). |
| `LP_symDur_index_prop` | Correlation weight (0 to 1) for symptom duration between the index and secondary cases.|
| `LP_infDur_index_prop` | Correlation weight (0 to 1) for infectious duration between the index and secondary cases. |
| `LP_corr_layer` | Contact layer(s) where trait correlations are enforced (e.g., 'all' for all settings, 'h' for household only). |
| `LP_coef_InfSym` | Coefficient scaling the impact of peak infectiousness (viral load) on the probability of developing symptoms. |
| `LP_symp_probs` | Age-specific probabilities of symptom manifestation (array of length 5). |
| `LP_sus_ORs` | Age-specific susceptibility odds ratios (array of length 5). |
| `LP_trans_ORs` | Age-specific intrinsic transmissibility odds ratios (array of length 5). |
| `LP_param_vg` | Targeted vaccination group policy (e.g., `vg0` for no expansion, `vg5` for universal). |
| `LP_param_vc` | Increase in vaccine coverage (percentage points) administered above baseline data. |
| `LP_base_tip` | Baseline daily probability of population adherence to stay-at-home interventions. |
| `LP_param_tip` | Incremental increase in stay-at-home adherence probability applied during interventions. |
| `LP_end_tida` | Early termination duration for stay-at-home compliance (days before clinical recovery). |
| `LP_imprinting` | Boolean flag for simulating historical immune imprinting effects. Set `False` in current IDC study. |
| `LP_preHAI` | Boolean flag for pre-assigning baseline Hemagglutination Inhibition (HAI) titers at initialization. Set `False` in current IDC study.|


#### 1.2 New Helper Functions & Data Dependencies

Added three utility functions to load and map empirical immunological data onto the synthetic population. Not used in current IDC study.
* **`get_imprt_data()`**: Loads immune imprinting probabilities.
* **`get_preHAI_data()`**: Loads baseline HAI titer distributions.
* **`randomize_imprt()`**: Stochastically overrides imprinting statuses based on defined protection ratios.

<br>

### **2. sim.py**
#### 2.1 Overview
The module was modified to implement the **infectiousness-dependence mechanism (IDC)** . These updates enable the simulation of correlated biological traits across transmission pairs while maintaining a strictly controlled baseline population.

#### 2.2 Key Epidemiological Updates
* **Custom Baseline Parameterization:** 
  Overrode the default population initialization in `init_people()` to accept explicitly pre-calculated, age-stratified arrays (`LP_symp_probs`, `LP_trans_ORs`, `LP_sus_ORs`). 
* **Absolute Reinfection Protection:** 
  Modified the `step()` method to assign 100% susceptibility immunity (`sus_imm = 1.0`) to any previously exposed (`naive == False`) agent. This eliminates confounding reinfection events, isolating the dynamics of a single epidemic wave.
* **Centered Log-Linear Infectiousness Correlation (IDC):** 
  Introduced a mathematical mechanism during the transmission step that correlates a secondary case's peak infectiousness (`rel_trans`) to its index case. The model maps intrinsic traits to a log space, applies a mean-centered linear correlation based on the specified network layer and IDC weight, and exponentiates back. This ensures transmission-pair correlation without disrupting population-level parameter distributions.

#### 2.3 Enhanced Data Analytics
* **Transmission Network Logging:** 
  Initialized a custom tracking array (`self.people.LP_trans_log`) that records a Pandas DataFrame for every transmission event. It logs the exact UIDs, ages, contact layers, and dynamic peak infectiousness values of both the source and target.
* **Robust Generation Time Metrics:** 
  Extended the `compute_gen_time()` output to include median statistics (`true_median` and `clinical_median`), providing analytics that are resilient to skewed transmission intervals.


<br>


### **3. people.py**
#### 3.1 Overview
The `People` class and its core state-updating methods in the Covasim framework have been extended to investigate the epidemiological impact of **correlated traits within transmission pairs**. Aligning with our methodology of modeling infectiousness dependence, the modifications introduce an infectiousness-dependent symptom probability model and establish temporal trait correlations (symptom duration and infectious duration) between index and secondary cases across specific contact layers.

#### 3.2 Enhanced Age-Structured Transmission Tracking
To support age-stratified transmission dynamics and contact pattern analysis, the internal `infection_log` was expanded. 
* **`age_source`**: Logs the age of the **infector** (index case) at the time of transmission.
* **`age_target`**: Logs the age of the **infectee** (secondary case).

#### 3.3 Infectiousness-Dependent Symptom Manifestation
The default static symptom probability model was replaced with a mechanism that couples clinical manifestation with the agent's simulated viral load. 
* **Mechanism:** We introduced a dynamic probability model using a logit transformation. It incorporates the individual's peak infectiousness (`rel_trans`, serving as a proxy for peak viral load) and a scaling coefficient (`LP_coef_InfSym`).
* **Epidemiological Rationale:** This models the biological hypothesis that a higher intrinsic infectiousness (higher peak viral load) statistically increases the likelihood of a secondary case progressing to symptomatic infection, bridging intra-host viral dynamics with population-level case ascertainment.

#### 3.4 Temporal Trait Correlation in Transmission Pairs
Parallel to the Infectiousness-Dependence Coefficient (IDC) used for peak viral load, we extended the model to capture correlations in **disease durations** between directly linked transmission pairs. The `infect()` method was expanded with three key parameters:
* `LP_symDur_index_prop`: The correlation weight (0 to 1) for **symptom duration** between the index case and secondary case.
* `LP_infDur_index_prop`: The correlation weight (0 to 1) for **infectious duration**.
* `LP_corr_layer`: Specifies the network scope where this correlation acts (e.g., 'h' for the **household-only scope**, or 'all' for the **all-settings scope**).

<br>



### **4. population.py**
#### 4.1 Overview
This module was modified to allow the direct injection of pathogen-specific, age-stratified natural history parameters during initialization. 

#### 4.2 Parameter Additions in `make_people()`
To override Covasim's default parameters, `make_people()` now accepts three custom arrays:
* **`LP_sus_ORs`**: Age-specific susceptibility odds ratios.
* **`LP_trans_ORs`**: Age-specific intrinsic transmissibility odds ratios.
* **`LP_symp_probs`**: Age-specific probabilities of symptomatic infection.

<br>


### **5. immunity.py**
#### 5.1 Overview
This module was modified to incorporate pathogen-specific immunological dynamics. While advanced immunological frameworks—such as population-level pre-existing immunity and historical immune imprinting—were developed as part of this module, they were intentionally deactivated for the current study (with both preHAI_bool and imprt_bool flags set to False). 

#### 5.2 Detailed Modifications

|  **Feature**                |  **Modification**                                                                                                                                                                                                    |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  Pre-existing  immunity      |  -  Added hemagglutination inhibition (HAI) titer-based immunity. -  Introduced discrete HAI titers (0–9 scale). -  Added preHAI\_bool parameter to enable/disable pre-assignment of HAI titers at  initialization.  |
|  Immune  imprinting          |  -  Implemented calc\_imprt() to simulate immune imprinting effects. -  Added imprt\_bool flag (currently inactive) for toggling imprinting.                                                                          |
|  Immunity  boosting          |  -  Replaced multiplicative boosting with an additive scheme: peak\_nab +  boost\_factor. -  Standardized to four-fold HAI titer rise upon re-exposure.                                                               |
|  Waning  pattern             |  -  Modified nab\_growth\_decay() function. -  Replaced exponential waning with linear decay at 14% per year.                                                                                                         |
|  Immunity  update functions  |  -  Overhauled immunity update mechanics: •  Modified update\_nab() •  Modified update\_peak\_nab()                                                                                                                 |
    

