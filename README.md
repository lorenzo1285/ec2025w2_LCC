# EC2025W2 - MAXSAT Evolutionary Algorithm Solver 🧠

This project implements an **Improved Binary Genetic Algorithm (IBGA)** to solve **Weighted MAXSAT** problems using heuristic initialization and optional Lagrangian penalty ranking.

---

## 📂 Project Structure
```
EC2025W2_LCC/
├── Code/
│   ├── eda_105.ipynb            # Jupyter notebook for EDA or experiments
│   ├── IBGA.py                  # Improved Binary Genetic Algorithm implementation
│   ├── main.py                  # Main execution script
│   ├── maxsat.py                # MAXSAT problem definition and evaluation
├── Data/
│   ├── sbox_4.wcnf              # Example Weighted CNF instance (WCNF format)
├── Docs/
│   ├── images/                  # Images for report or visualization
│   ├── maxsat_report.pdf        # Final report on MAXSAT results
│   ├── optuna_eda104_lagrangian_results.csv  # Results of hyperparameter tuning or EDA
├── requirements.txt             # Python dependencies for pip installation
├── LICENSE.TXT                  # Project license (MIT or similar)
└── README.md                    # Project documentation
```


---

## ⚙️ Requirements
- Python 3.12+
- Recommended: Run inside a Conda environment

### ✅ Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Project (Locally)
### ✅ Step 1: Activate your environment
```bash
conda activate env_evo
```

### ✅ Step 2: Navigate to the Code folder
```bash
cd Code
```

### ✅ Step 3: Run the evolutionary algorithm with your WCNF instance
```bash
python main.py --path ../Data/sbox_4.wcnf
```

✅ You can also provide an **absolute path** if preferred:
```bash
python main.py --path C:\Users\loren\Documents\ec2025w2\Data\sbox_4.wcnf
```

---

## 📈 Expected Output
- Percentage of satisfied clauses
- Best individual (binary string)
- Fitness score (number of satisfied clauses)
- Detailed DataFrame showing clause satisfaction

Example:
```
Percentage of Satisfied Clauses: 98.75%
Best Individual: [1, 0, 1, 1, 0, 1, ...]
Number of Satisfied Clauses: 395
```

---

## 📝 How to Export Environment Dependencies
### ✅ Export `requirements.txt`
```bash
conda activate env_evo
pip freeze > requirements.txt
```

---

## 📜 Author
Lorenzo - MSc Artificial Intelligence and Machine Learning  
University of Birmingham | 2025

---

## 🗒️ License
MIT License
