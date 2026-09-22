# **Source Data Overview**

This directory contains the source data files used to generate Figures 3 through 7 in the associated study. The datasets are extracted from the Infectiousness-Dependence Coefficient (IDC) agent-based model and are systematically organized based on their analytical purpose. 

*(Note: The `Lyh` and `Lyall` suffixes in the filenames indicate whether the IDC mechanism was applied exclusively to household networks or across all contact settings, respectively.)*

---

## **1. Baseline Transmission Dynamics (Figures 3 & 4)**
Contains epidemiological metrics for baseline scenarios without non-pharmaceutical interventions (Strategy `S0`).
* **`SourceData_Figure3_(Lyh).xlsx`**: Baseline dynamics when the IDC mechanism is restricted to household contacts.
* **`SourceData_Figure4_(Lyall).xlsx`**: Baseline dynamics when the IDC mechanism operates across all contact layers.

---

## **2. Matched Baselines (Figure 5)**
Contains baseline scenarios filtered via the Adaptive Matched Attack Rate method to isolate structural transmission differences from baseline incidence confounders.
* **`SourceData_Figure5a_(Lyh).xlsx`** & **`SourceData_Figure5b_(Lyall).xlsx`**: Datasets grouping different IDC values that yield comparable overall attack rates (`Matched AR Group`), enabling standardized comparisons.

---

## **3. Intervention Effectiveness (Figures 6 & 7)**
Contains evaluation metrics for non-pharmaceutical interventions (testing, isolation, and contact tracing) across the correlated transmission networks.
* **`SourceData_Figure6.xlsx`**: A comprehensive grid dataset evaluating overall intervention effectiveness across continuous IDC and transmission probability ($\beta$) gradients for both network settings.
* **`SourceData_Figure7a_(Lyh).xlsx`** & **`SourceData_Figure7b_(Lyall).xlsx`**: Strategy-specific effectiveness (relative reductions in attack rates and peak incidence) within the matched attack rate groups.