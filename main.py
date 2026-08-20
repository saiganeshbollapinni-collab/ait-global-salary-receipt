"""
AIT Global - Salary Structure Calculator 
------------------------------------------
Enter the Annual CTC and all salary components are auto-calculated
and filled in, both Yearly and Monthly.

Run with:  python salary_structure_ait_global.py
(Requires Python 3 with Tkinter - included by default on Windows/Mac,
 on Linux install with: sudo apt-get install python3-tk)
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------------------------------------------
# Salary calculation logic
# ---------------------------------------------------------------
def calculate_salary(ctc, insurance_annual=0):
    """
    Given Annual CTC and Insurance, returns a dictionary of all salary components
    (annual values).
    """

    # ---- Fixed annual amounts (company policy - editable) ----
    medical_annual = 15000          # Medical allowance
    travel_annual = 19200           # Travel / Conveyance allowance
    professional_tax_annual = 2400  # Professional Tax (varies by state)

    # Solve for Basic where Basic = 0.40 * Gross
    basic_annual = (0.40 * (ctc - insurance_annual)) / 1.06724

    epf_employer_annual = round(0.12 * basic_annual, 2)
    gratuity_annual = round(0.0481 * basic_annual, 2)

    employer_contrib_total = epf_employer_annual + gratuity_annual + insurance_annual
    gross_salary_annual = ctc - employer_contrib_total

    da_annual = round(0.10 * basic_annual, 2)

    # Special allowance = balancing figure so components add up to Gross
    known_earnings = basic_annual + da_annual + medical_annual + travel_annual
    special_allowance_annual = round(gross_salary_annual - known_earnings, 2)
    if special_allowance_annual < 0:
        special_allowance_annual = 0

    epf_employee_annual = round(0.12 * basic_annual, 2)
    net_take_home_annual = gross_salary_annual - epf_employee_annual - professional_tax_annual

    basic_annual = round(basic_annual, 2)

    return {
        "CTC": ctc,
        "Basic": basic_annual,
        "DA": da_annual,
        "Medical Allowance": medical_annual,
        "Travel Allowance": travel_annual,
        "Special Allowance": special_allowance_annual,
        "Gross Salary": round(gross_salary_annual, 2),
        "EPF (Employer)": epf_employer_annual,
        "Gratuity": gratuity_annual,
        "Insurance (Employer)": insurance_annual,
        "Professional Tax": professional_tax_annual,
        "EPF (Employee)": epf_employee_annual,
        "Net Take Home": round(net_take_home_annual, 2),
    }


# ---------------------------------------------------------------
# GUI
# ---------------------------------------------------------------
class SalaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AIT Global - Salary Receipt")
        self.root.geometry("650x750")
        self.root.configure(bg="#f4f6f8")

        self.result_vars = {}

        self.build_header()
        self.build_input_section()
        self.build_output_table()

    # ---------------- Header ----------------
    def build_header(self):
        header = tk.Frame(self.root, bg="#1f3b57", height=70)
        header.pack(fill="x")
        tk.Label(
            header, text="AIT GLOBAL", font=("Segoe UI", 20, "bold"),
            bg="#1f3b57", fg="white"
        ).pack(pady=(10, 0))
        tk.Label(
            header, text="Salary Receipt", font=("Segoe UI", 12),
            bg="#1f3b57", fg="#cfe0ee"
        ).pack(pady=(0, 10))

    # ---------------- Input Section ----------------
    def build_input_section(self):
        frame = tk.Frame(self.root, bg="#f4f6f8", pady=15)
        frame.pack(fill="x", padx=20)

        # Row 1: CTC Input
        tk.Label(
            frame, text="Enter Annual CTC (₹):", font=("Segoe UI", 12, "bold"),
            bg="#f4f6f8"
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.ctc_entry = tk.Entry(frame, font=("Segoe UI", 12), width=20)
        self.ctc_entry.grid(row=0, column=1, sticky="w")
        self.ctc_entry.bind("<KeyRelease>", lambda event: self.on_calculate())

        # Row 2: Insurance Input
        tk.Label(
            frame, text="Insurance (Employer) (₹):", font=("Segoe UI", 12, "bold"),
            bg="#f4f6f8"
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))

        self.insurance_entry = tk.Entry(frame, font=("Segoe UI", 12), width=20)
        self.insurance_entry.grid(row=1, column=1, sticky="w", pady=(10, 0))
        self.insurance_entry.bind("<KeyRelease>", lambda event: self.on_calculate())

        # Buttons
        calc_btn = tk.Button(
            frame, text="Calculate", font=("Segoe UI", 11, "bold"),
            bg="#2b7a4b", fg="white", activebackground="#245f3c",
            padx=15, pady=4, command=self.on_calculate
        )
        calc_btn.grid(row=0, column=2, padx=(15, 5), rowspan=2)

        clear_btn = tk.Button(
            frame, text="Clear", font=("Segoe UI", 11),
            bg="#c0392b", fg="white", activebackground="#992d22",
            padx=15, pady=4, command=self.on_clear
        )
        clear_btn.grid(row=0, column=3, rowspan=2)

    # ---------------- Output Table ----------------
    def build_output_table(self):
        container = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Table headers
        headers = ["Salary Component", "Yearly (₹)", "Monthly (₹)"]
        header_row = tk.Frame(container, bg="#1f3b57")
        header_row.pack(fill="x")
        for i, h in enumerate(headers):
            tk.Label(
                header_row, text=h, font=("Segoe UI", 11, "bold"),
                bg="#1f3b57", fg="white", width=22 if i == 0 else 15,
                pady=8
            ).grid(row=0, column=i)

        rows_frame = tk.Frame(container, bg="white")
        rows_frame.pack(fill="both", expand=True)

        self.fields = [
            "Basic",
            "DA",
            "Medical Allowance",
            "Travel Allowance",
            "Special Allowance",
            "Gross Salary",
            "EPF (Employer)",
            "Gratuity",
            "Insurance (Employer)",
            "Professional Tax",
            "EPF (Employee)",
            "Net Take Home",
            "CTC",
        ]

        bold_rows = {"Gross Salary", "Net Take Home", "CTC"}

        for idx, field in enumerate(self.fields):
            bg = "#eef3f8" if idx % 2 == 0 else "white"
            if field in bold_rows:
                bg = "#dff0d8"

            row = tk.Frame(rows_frame, bg=bg)
            row.pack(fill="x")

            font_style = ("Segoe UI", 10, "bold" if field in bold_rows else "normal")

            tk.Label(
                row, text=field, font=font_style, bg=bg, anchor="w",
                width=22, padx=10, pady=6
            ).grid(row=0, column=0, sticky="w")

            yearly_var = tk.StringVar(value="-")
            monthly_var = tk.StringVar(value="-")
            self.result_vars[field] = (yearly_var, monthly_var)

            tk.Label(
                row, textvariable=yearly_var, font=font_style, bg=bg,
                width=15, anchor="e"
            ).grid(row=0, column=1)

            tk.Label(
                row, textvariable=monthly_var, font=font_style, bg=bg,
                width=15, anchor="e"
            ).grid(row=0, column=2)

    # ---------------- Actions ----------------
    def on_calculate(self):
        raw_ctc = self.ctc_entry.get().strip().replace(",", "")
        raw_insurance = self.insurance_entry.get().strip().replace(",", "")

        # Parse Insurance
        try:
            insurance = float(raw_insurance) if raw_insurance else 0
            if insurance < 0:
                raise ValueError
        except ValueError:
            insurance = 0

        # Parse CTC
        try:
            ctc = float(raw_ctc) if raw_ctc else None
            if ctc is not None and ctc <= 0:
                ctc = None
        except ValueError:
            ctc = None

        if ctc is None:
            # Clear output table if input is invalid/empty
            for field in self.fields:
                yearly_var, monthly_var = self.result_vars[field]
                yearly_var.set("-")
                monthly_var.set("-")
            return

        results = calculate_salary(ctc, insurance)

        # Update output table
        for field in self.fields:
            yearly_val = results[field]
            monthly_val = yearly_val / 12
            yearly_var, monthly_var = self.result_vars[field]
            yearly_var.set(f"{yearly_val:,.2f}")
            monthly_var.set(f"{monthly_val:,.2f}")

    def on_clear(self):
        self.ctc_entry.delete(0, tk.END)
        self.insurance_entry.delete(0, tk.END)
        for field in self.fields:
            yearly_var, monthly_var = self.result_vars[field]
            yearly_var.set("-")
            monthly_var.set("-")


# ---------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryApp(root)
    root.mainloop()