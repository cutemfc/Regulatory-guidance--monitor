# Regulatory-guidance-monitor

# 🌍 Goal: 
This application is a Proof of Concept (Demo). The regulatory data provided within the default database is for illustrative purposes. It is designed to demonstrate how Regulatory Affairs (RA) professionals can leverage automation to streamline their monitoring workflows.
# 📌 Project Overview
The ATMP Regulatory Intelligence Monitor is a specialized dashboard for Advanced Therapy Medicinal Products (ATMP). It bridges the gap between massive, unstructured regulatory updates from global agencies (FDA, EMA, PMDA) and professional strategic interpretation.
This demo uses TCR T-cell Therapy as the primary example to showcase how specific technical hurdles are tracked through the regulatory lifecycle.
# 🧬 What is TCR T-cell Therapy?
TCR T-cell Therapy (T-Cell Receptor Engineered T-cell Therapy) is a form of immunotherapy used primarily in oncology.

The Mechanism: Patient T-cells are genetically engineered to express a specific T-cell receptor (TCR) that can recognize tumor-specific antigens.

TCR vs. CAR-T: Unlike CAR-T cells (which recognize surface proteins), TCR-Ts can recognize intracellular proteins presented by the HLA (Human Leukocyte Antigen) complex.

Regulatory Complexity: Because TCR-T is HLA-restricted, it faces unique regulatory scrutiny regarding off-target toxicity and cross-reactivity (where the TCR might accidentally attack healthy tissues with similar HLA-peptide complexes). This dashboard is designed to monitor these specific high-stakes requirements.
# ⚙️ Core Logic & Workflow
Automated Scouting: Scans live RSS feeds from FDA (CBER) and EMA, filtering for keywords like TCR, T-cell, and Gene Therapy.

Gap Analysis Support: Provides a structured interface for RA experts to document "Past Requirements" vs. "Latest Updates," turning raw news into actionable strategy.

Knowledge Base: Automatically builds a local repository (master_regulations.csv) of all professional interpretations for long-term audit trails.

# ☘️Result


<img width="1854" height="943" alt="image" src="https://github.com/user-attachments/assets/b1912cf4-2154-4402-af12-cd01840b51ea" />
