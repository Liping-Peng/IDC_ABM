# **IDC_ABM**

IDC_ABM is an agent-based modeling framework adapted from Covasim (v3.1.4) to investigate the **Infectiousness-Dependence Coefficient (IDC)** mechanism in infectious disease transmission. It evaluates how the peak infectiousness (viral load) of secondary cases correlate with their index cases within specific contact networks. The framework is calibrated to simulate and compare transmission dynamics across diverse viral profiles, including **Influenza A, Ancestral SARS-CoV-2, and the Omicron variant**.

---

## **Structure**

```text
IDC_ABM/
├── README.md                            # Project overview
├── Covasim_IDC_Modification/            # Modified Covasim framework for IDC
│   ├── MODIFICATIONS.md                 # Detailed change log
│   ├── parameters.py                    # IDC parameters and baseline calibration
│   ├── sim.py                           # Central IDC execution and network logging
│   ├── people.py                        # Trait inheritance and duration correlations
│   ├── population.py                    # Age-stratified baseline initialization
│   └── immunity.py                      # Pathogen-specific immunity algorithms
├── example/                             # Example simulation directory
│   ├── code/                            # Example scripts for running simulations 
│   │   ├── README.md                    # Instructions for example usage
│   │   ├── run_example.py               # Main simulation script
│   │   ├── base_func.py                 # Utility and analytical functions
│   │   └── base_data.py                 # Data for diverse viral profiles
│   └── result/                          # Output directories for simulation results
│       ├── README.md                    # Result overview   
│       ├── save_sim                     # Aggregated epidemiological metrics (Rt, attack rates, intervals)
│       ├── sims_detail                  # Standard Covasim macro-level state summaries
│       └── tree_detail                  # Agent-level network logs, individual R, and infectiousness pairs
└── source_data/                         # Source data for paper figures (Figures 3–7)
    ├── README.md                        # Overview of figure source datasets
    ├── SourceData_Figure3_(Lyh).xlsx    # Baseline metrics (Household only)
    ├── SourceData_Figure4_(Lyall).xlsx  # Baseline metrics (All settings)
    ├── SourceData_Figure5a_(Lyh).xlsx   # Matched baselines (Household only)
    ├── SourceData_Figure5b_(Lyall).xlsx # Matched baselines (All settings)
    ├── SourceData_Figure6.xlsx          # Intervention effectiveness grid
    ├── SourceData_Figure7a_(Lyh).xlsx   # Strategy effectiveness in matched AR groups (Household only)
    └── SourceData_Figure7b_(Lyall).xlsx # Strategy effectiveness in matched AR groups (All settings)
```

---

## **Features**

- **Infectiousness-Dependence Coefficient (IDC) Mechanism:** Implements a mean-centered, log-linear correlation model allowing secondary cases to inherit peak infectiousness (viral load proxies) from their index cases.
- **Network-Specific Correlation:** Enforces network-specific correlation weights (e.g., household-only vs. all-settings) between transmission pairs.
- **Granular Network Analytics:** Automatically logs comprehensive generational transmission metadata, capturing precise infectiousness values and demographic traits at the exact moment of transmission.
- **Multi-Pathogen Standardization:** Provides robust baseline parameterizations to isolate structural transmission dynamics for Influenza A, Ancestral SARS-CoV-2, and the Omicron variant by removing clinical progression confounders.
- **Targeted Interventions (NPIs):** Supports the simulation and evaluation of testing, self-isolation, and contact tracing strategies within correlated transmission networks.

---

## **Getting Started**

### 1. Install Covasim
Install the original Covasim package (v3.1.4):
```bash
git clone [https://github.com/InstituteforDiseaseModeling/covasim.git](https://github.com/InstituteforDiseaseModeling/covasim.git)
cd covasim
pip install -e .
```

### 2. Apply Modifications
Replace the following core files in the original Covasim installation with the modified versions provided in this repository:
- `parameters.py`
- `sim.py`
- `people.py`
- `population.py`
- `immunity.py`

### 3. Run Example Simulations
Navigate to the example code folder to execute baseline and correlated transmission scenarios:
```bash
cd example/code
python run_example.py
```
Modify parameters, scenarios, or interventions directly in `run_example.py` as needed.

---

## **License**

**Original Covasim:**
- Covasim 3.1.4 (2022-10-22) — © 2020–2022 Institute for Disease Modeling (IDM).
- All unmodified files remain under the original Covasim license.

**Modifications in this repository:**
- Only a subset of files are modified: `parameters.py`, `sim.py`, `people.py`, `population.py`, and `immunity.py`.
- Modifications are documented with the `# LP_mod:` prefix for transparency.
- These modifications are authored by Liping Peng and may be cited in academic work.

---

## **Citation**

If you use this repository in research, please cite both the original Covasim framework and this repository:

**1. Original Covasim:**
> Kerr CC, Stuart RM, Mistry D, Abeysuriya RG, Rosenfeld R, Hart G, Núñez RC, Cohen JA, Selvaraj P, Hagedorn B, George L, Jastrzębski M, Izzo A, Fowler G, Palmer A, Delport D, Scott N, Kelly S, Bennette C, Wagner B, Chang S, Oron AP, Wenger E, Panovska-Griffiths J, Famulare M, Klein DJ (2021). Covasim: an agent-based model of COVID-19 dynamics and interventions. *PLOS Computational Biology* **17** (7): e1009149. doi: [10.1371/journal.pcbi.1009149](https://doi.org/10.1371/journal.pcbi.1009149).

**2. This repository:**
> Peng L, Zhang C, Adam DC, Chan KH, Peiris M, Cowling BJ, Ip DKM, Tsang TK. Correlated infectiousness within transmission pairs shapes epidemic characteristics of respiratory viruses

---

## **Acknowledgements**

This work builds upon **Covasim**, developed by the Institute for Disease Modeling (IDM). All credit for the original model goes to the Covasim development team.
