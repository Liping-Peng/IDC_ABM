"""
This module contains data for three simulated virus profiles.

Author: Liping Peng
Institution: The University of Hong Kong
Date: 22 September 2026
"""


# =============================================================================
# COMMON DATA FOR SIMULATED VIRUS PROFILES
# =============================================================================


### Disease Progression Parameters
dis_prog_FluA = dict(exp2inf=dict(dist='lognormal_int', par1=1.5, par2=0.64),
                inf2sym=dict(dist='lognormal_int', par1=0, par2=0),  # Infectiousness to symptom onset
                asym2rec=dict(dist='lognormal_int', par1=4.8, par2=0.5),  # Assumed same duration as symptomatic cases
                mild2rec=dict(dist='lognormal_int', par1=4.8, par2=0.5),
                sym2sev=dict(dist='lognormal_int', par1=6.6, par2=4.9),
                sev2crit=dict(dist='lognormal_int', par1=1.5, par2=2.0),
                sev2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2die=dict(dist='lognormal_int', par1=10.7, par2=4.8), )


dis_prog_Cov = dict(exp2inf=dict(dist='lognormal_int', par1=4.9, par2=2.5),   # ref: https://academic.oup.com/cid/article/74/9/1678/6359063#supplementary-data
                inf2sym=dict(dist='lognormal_int', par1=1.4, par2=0.9),     # ref: https://academic.oup.com/cid/article/74/9/1678/6359063#supplementary-data
                asym2rec=dict(dist='lognormal_int', par1=8.0, par2=2.0),  # Assumed same duration as symptomatic cases
                mild2rec=dict(dist='lognormal_int', par1=8.0, par2=2.0),
                sym2sev=dict(dist='lognormal_int', par1=6.6, par2=4.9),
                sev2crit=dict(dist='lognormal_int', par1=1.5, par2=2.0),
                sev2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2die=dict(dist='lognormal_int', par1=10.7, par2=4.8), )


dis_prog_Omicron = dict(exp2inf=dict(dist='lognormal_int', par1=2.5, par2=1.5),   # ref: https://pmc.ncbi.nlm.nih.gov/articles/PMC10916204/
                inf2sym=dict(dist='lognormal_int', par1=0.9, par2=0.5),     # ref:https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2795489
                asym2rec=dict(dist='lognormal_int', par1=8.0, par2=4.4),
                mild2rec=dict(dist='lognormal_int', par1=8.0, par2=4.4),
                sym2sev=dict(dist='lognormal_int', par1=6.6, par2=4.9),
                sev2crit=dict(dist='lognormal_int', par1=1.5, par2=2.0),
                sev2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2rec=dict(dist='lognormal_int', par1=18.1, par2=6.3),
                crit2die=dict(dist='lognormal_int', par1=10.7, par2=4.8), )




### Hong Kong population data
HK_pop_2009 = {    # https://www.censtatd.gov.hk/tc/web_table.html?id=110-01001#
    '0-4': 226000,
    '5-9': 262900,
    '10-19': 806000,
    '20-29': 986600,
    '30-39': 1107500,
    '40-49': 1267700,
    '50-59': 1082100,
    '60-69': 559000,
    '70-79': 435000,
    '80+': 240000,}

HK_pop_2020 = {
    '0-4': 255200,
    '5-9': 307900,
    '10-19': 567000,
    '20-29': 868300,
    '30-39': 1161000,
    '40-49': 1172900,
    '50-59': 1232800,
    '60-69': 1054900,
    '70-79': 517100,
    '80+': 383400, }

HK_pop_2022 = {
    '0-4': 213100,
    '5-9': 270900,
    '10-19': 558900,
    '20-29': 739000,
    '30-39': 1073200,
    '40-49': 1151300,
    '50-59': 1182700,
    '60-69': 1151600,
    '70-79': 616100,
    '80+': 389300, }


HK_pop_2015 = {
    '0-4': 259700,
    '5-9': 248100,
    '10-19': 694400,
    '20-29': 974000,
    '30-39': 1131600,
    '40-49': 1185300,
    '50-59': 1223300,
    '60-69': 737700,
    '70-79': 423300,
    '80+': 301500,}

