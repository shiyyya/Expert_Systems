import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import clips

BASE_DIR = Path(__file__).resolve().parent
CLIPS_FILE = BASE_DIR / "loan_analysis.clp"

BG = "#F4F6F8"
CARD = "#FFFFFF"
TEXT = "#1F2937"
MUTED = "#6B7280"
BORDER = "#E5E7EB"
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
DARK = "#111827"
SOFT = "#F8FAFC"
SUCCESS = "#166534"
SUCCESS_BG = "#DCFCE7"
WARNING = "#92400E"
WARNING_BG = "#FEF3C7"
DANGER = "#991B1B"
DANGER_BG = "#FEE2E2"


class LoanAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Analysis Expert System")
        self.root.geometry("1040x760")
        self.root.minsize(900, 680)
        self.root.configure(bg=BG)

        self.environment = clips.Environment()
        self.load_clips()

        self.create_styles()
        self.create_variables()
        self.create_ui()

    def load_clips(self):
        if not CLIPS_FILE.exists():
            raise FileNotFoundError(
                f"Could not find loan_analysis.clp.\n\n"
                f"Put loan_analysis.clp in the same folder as main.py.\n\n"
                f"Expected location:\n{CLIPS_FILE}"
            )
        self.environment.load(str(CLIPS_FILE))

    def create_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TCombobox", padding=9, font=("Segoe UI", 10))
        style.configure("TEntry", padding=9, font=("Segoe UI", 10))
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10),
            foreground="white",
            background=PRIMARY,
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", PRIMARY_HOVER), ("pressed", PRIMARY_HOVER)],
            foreground=[("disabled", "#9CA3AF")],
        )
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=(16, 10),
            foreground=TEXT,
            background="#FFFFFF",
            bordercolor=BORDER,
        )
        style.map("Secondary.TButton", background=[("active", "#F3F4F6")])

    def create_variables(self):
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.employment_status_var = tk.StringVar(value="Employed")
        self.employment_length_var = tk.StringVar(value="Long")
        self.income_var = tk.StringVar()
        self.expenses_var = tk.StringVar()
        self.existing_payments_var = tk.StringVar()
        self.payment_history_var = tk.StringVar(value="Good")
        self.requested_loan_var = tk.StringVar()
        self.loan_term_var = tk.StringVar(value="Medium")

    def create_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main = tk.Frame(self.root, bg=BG)
        main.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)

        header = tk.Frame(main, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))

        tk.Label(
            header,
            text="Loan Analysis",
            font=("Segoe UI", 27, "bold"),
            bg=BG,
            fg=DARK,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Expert System",
            font=("Segoe UI", 12),
            bg=BG,
            fg=PRIMARY,
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            header,
            text="Enter the applicant's information",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w")

        self.create_steps(main)

        card = tk.Frame(
            main,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.grid(row=2, column=0, sticky="nsew")
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(card, bg=CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        form = tk.Frame(canvas, bg=CARD)

        form_window = canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_form(event):
            canvas.itemconfigure(form_window, width=event.width)

        form.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_form)
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))

        canvas.grid(row=0, column=0, sticky="nsew", padx=(1, 0), pady=1)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=12)

        content = tk.Frame(form, bg=CARD)
        content.pack(fill="both", expand=True, padx=34, pady=30)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        self.add_section_title(content, 0, "Applicant Information", "Basic details and employment stability")

        self.add_entry(content, 1, 0, "Applicant Name", self.name_var, "e.g. Juan Dela Cruz")
        self.add_entry(content, 1, 1, "Age", self.age_var, "18–100")

        self.add_combo(content, 2, 0, "Employment Status", self.employment_status_var,
                       ["Employed", "Self-employed", "Unemployed"])
        self.add_combo(content, 2, 1, "Length of Employment", self.employment_length_var,
                       ["Short", "Medium", "Long"])

        self.add_section_title(content, 3, "Financial Information", "Monthly income and existing obligations")

        self.add_entry(content, 4, 0, "Monthly Income (₱)", self.income_var, "e.g. 35000")
        self.add_entry(content, 4, 1, "Monthly Expenses (₱)", self.expenses_var, "e.g. 15000")
        self.add_entry(content, 5, 0, "Existing Loan Payments (₱)", self.existing_payments_var, "e.g. 5000")
        self.add_combo(content, 5, 1, "Payment History", self.payment_history_var,
                       ["Good", "Fair", "Poor"])

        self.add_section_title(content, 6, "Loan Request", "Specify the amount and repayment period")

        self.add_entry(content, 7, 0, "Requested Loan Amount (₱)", self.requested_loan_var, "e.g. 100000")
        self.add_combo(content, 7, 1, "Loan Term", self.loan_term_var,
                       ["Short", "Medium", "Long"])

        actions = tk.Frame(content, bg=CARD)
        actions.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(26, 0))

        ttk.Button(
            actions,
            text="Analyze Loan",
            style="Primary.TButton",
            command=self.analyze_loan,
        ).pack(side="right")

        ttk.Button(
            actions,
            text="Clear",
            style="Secondary.TButton",
            command=self.clear_form,
        ).pack(side="right", padx=(0, 10))

    def create_steps(self, parent):
        steps = tk.Frame(parent, bg=BG)
        steps.grid(row=1, column=0, sticky="ew", pady=(0, 18))

        items = [
            ("01", "Applicant"),
            ("02", "Finances"),
            ("03", "Loan Request"),
            ("04", "Analysis"),
        ]

        for index, (number, label) in enumerate(items):
            box = tk.Frame(steps, bg=BG)
            box.pack(side="left", padx=(0, 26))

            tk.Label(
                box,
                text=number,
                font=("Segoe UI", 9, "bold"),
                bg=PRIMARY,
                fg="white",
                width=4,
                pady=4,
            ).pack(side="left")

            tk.Label(
                box,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=BG,
                fg=TEXT,
            ).pack(side="left", padx=(7, 0))

    def add_section_title(self, parent, row, title, subtitle):
        frame = tk.Frame(parent, bg=CARD)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 14 if row else 18))

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED,
        ).pack(anchor="w", pady=(2, 0))

    def add_entry(self, parent, row, column, label, variable, hint):
        frame = tk.Frame(parent, bg=CARD)
        frame.grid(row=row, column=column, sticky="ew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0), pady=7)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 5))

        entry = ttk.Entry(frame, textvariable=variable)
        entry.pack(fill="x", ipady=1)

        tk.Label(
            frame,
            text=hint,
            font=("Segoe UI", 8),
            bg=CARD,
            fg=MUTED,
        ).pack(anchor="w", pady=(3, 0))

    def add_combo(self, parent, row, column, label, variable, values):
        frame = tk.Frame(parent, bg=CARD)
        frame.grid(row=row, column=column, sticky="ew", padx=(0 if column == 0 else 10, 10 if column == 0 else 0), pady=7)

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w", pady=(0, 5))

        ttk.Combobox(
            frame,
            textvariable=variable,
            values=values,
            state="readonly",
        ).pack(fill="x")

    @staticmethod
    def validate_number(value, field_name, allow_zero=False):
        try:
            number = float(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number.")

        if allow_zero:
            if number < 0:
                raise ValueError(f"{field_name} cannot be negative.")
        elif number <= 0:
            raise ValueError(f"{field_name} must be greater than 0.")

        return number

    def analyze_loan(self):
        try:
            name = self.name_var.get().strip()
            if not name:
                raise ValueError("Applicant Name is required.")

            try:
                age = int(self.age_var.get())
            except ValueError:
                raise ValueError("Age must be a valid whole number.")

            if age < 18 or age > 100:
                raise ValueError("Age must be between 18 and 100.")

            income = self.validate_number(self.income_var.get(), "Monthly Income")
            expenses = self.validate_number(self.expenses_var.get(), "Monthly Expenses", True)
            existing = self.validate_number(
                self.existing_payments_var.get(),
                "Existing Monthly Loan Payments",
                True,
            )
            requested = self.validate_number(
                self.requested_loan_var.get(),
                "Requested Loan Amount",
            )

            if expenses + existing > income * 2:
                raise ValueError(
                    "Expenses and existing payments are unusually high compared with income."
                )

            employment_status = self.employment_status_var.get().lower()
            employment_length = self.employment_length_var.get().lower()
            payment_history = self.payment_history_var.get().lower()
            loan_term = self.loan_term_var.get().lower()

            self.environment.reset()

            applicant_template = self.environment.find_template("applicant")
            if applicant_template is None:
                raise RuntimeError("The CLIPS template 'applicant' was not found.")

            applicant_template.assert_fact(
                name=name,
                age=age,
                **{"employment-status": clips.Symbol(employment_status)},
                **{"employment-length": clips.Symbol(employment_length)},
                **{"monthly-income": income},
                **{"monthly-expenses": expenses},
                **{"existing-loan-payments": existing},
                **{"payment-history": clips.Symbol(payment_history)},
                **{"requested-loan-amount": requested},
                 **{"loan-term": clips.Symbol(loan_term)},
            )

            self.environment.run()
            result = self.get_result()

            if result is None:
                raise RuntimeError(
                    "The CLIPS engine did not produce a recommendation. "
                    "Check the rules in loan_analysis.clp."
                )

            self.show_result(name, income, expenses, existing, requested, result)

        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))
        except clips.CLIPSError as error:
            messagebox.showerror("CLIPS Error", str(error))
        except Exception as error:
            messagebox.showerror("System Error", str(error))

    def get_result(self):
        for fact in self.environment.facts():
            if fact.template.name == "recommendation":
                return {
                    "decision": str(fact["decision"]),
                    "amount": float(fact["amount"]),
                    "reason": str(fact["reason"]),
                }
        return None

    def get_assessment(self, template_name, slot_name):
        for fact in self.environment.facts():
            if fact.template.name == template_name:
                return str(fact[slot_name])
        return None

    def show_result(self, name, income, expenses, existing, requested, result):
        available = income - expenses - existing
        expense_level = self.get_assessment("expense-level", "level") or "unknown"
        debt_level = self.get_assessment("debt-level", "level") or "unknown"
        payment = self.get_assessment("estimated-payment", "amount")

        window = tk.Toplevel(self.root)
        window.title("Analysis Result")
        window.geometry("900x690")
        window.minsize(760, 600)
        window.configure(bg=BG)
        window.transient(self.root)
        window.grab_set()

        main = tk.Frame(window, bg=BG)
        main.pack(fill="both", expand=True, padx=26, pady=24)

        top = tk.Frame(main, bg=BG)
        top.pack(fill="x", pady=(0, 18))

        tk.Label(
            top,
            text="Analysis Result",
            font=("Segoe UI", 24, "bold"),
            bg=BG,
            fg=DARK,
        ).pack(side="left")

        tk.Label(
            top,
            text=f"Applicant: {name}",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED,
        ).pack(side="right", pady=8)

        decision = result["decision"]
        if decision == "favorable":
            title = "Requested amount may be affordable"
            bg_color, fg_color = SUCCESS_BG, SUCCESS
        elif decision == "lower":
            title = "Consider a lower loan amount"
            bg_color, fg_color = WARNING_BG, WARNING
        else:
            title = "Loan is not recommended"
            bg_color, fg_color = DANGER_BG, DANGER

        banner = tk.Frame(main, bg=bg_color)
        banner.pack(fill="x", pady=(0, 16))

        tk.Label(
            banner,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=bg_color,
            fg=fg_color,
        ).pack(anchor="w", padx=20, pady=(15, 3))

        tk.Label(
            banner,
            text="Decision generated from the CLIPS knowledge base and inference rules.",
            font=("Segoe UI", 9),
            bg=bg_color,
            fg=fg_color,
        ).pack(anchor="w", padx=20, pady=(0, 15))

        stats = tk.Frame(main, bg=BG)
        stats.pack(fill="x", pady=(0, 16))
        stats.grid_columnconfigure((0, 1, 2), weight=1)

        self.add_stat_card(stats, 0, "Requested Loan", self.format_currency(requested))
        self.add_stat_card(stats, 1, "Recommended Amount", self.format_currency(result["amount"]))
        self.add_stat_card(stats, 2, "Available Income", self.format_currency(available))

        details = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        details.pack(fill="x", pady=(0, 16))

        tk.Label(
            details,
            text="Financial Assessment",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w", padx=20, pady=(17, 10))

        rows = [
            ("Estimated Monthly Payment", self.format_currency(float(payment)) if payment is not None else "N/A"),
            ("Expense Level", expense_level.title()),
            ("Existing Debt Level", debt_level.title()),
            ("Payment History", self.payment_history_var.get()),
            ("Employment", self.employment_status_var.get()),
            ("Employment Length", self.employment_length_var.get()),
        ]

        for label, value in rows:
            row = tk.Frame(details, bg=CARD)
            row.pack(fill="x", padx=20, pady=4)

            tk.Label(row, text=label, font=("Segoe UI", 9), bg=CARD, fg=MUTED).pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg=CARD, fg=TEXT).pack(side="right")

        reason = tk.Frame(main, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        reason.pack(fill="both", expand=True)

        tk.Label(
            reason,
            text="Why this result?",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w", padx=20, pady=(17, 6))

        tk.Label(
            reason,
            text=result["reason"],
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED,
            justify="left",
            wraplength=800,
            anchor="nw",
        ).pack(fill="both", expand=True, padx=20, pady=(0, 12))

        ttk.Button(
            main,
            text="Close",
            style="Secondary.TButton",
            command=window.destroy,
        ).pack(anchor="e", pady=(14, 0))

    @staticmethod
    def add_stat_card(parent, column, label, value):
        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 6 if column < 2 else 0))

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 8, "bold"),
            bg=CARD,
            fg=MUTED,
        ).pack(anchor="w", padx=16, pady=(13, 3))

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 15, "bold"),
            bg=CARD,
            fg=TEXT,
        ).pack(anchor="w", padx=16, pady=(0, 13))

    @staticmethod
    def format_currency(amount):
        return f"₱{amount:,.2f}"

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.employment_status_var.set("Employed")
        self.employment_length_var.set("Long")
        self.income_var.set("")
        self.expenses_var.set("")
        self.existing_payments_var.set("")
        self.payment_history_var.set("Good")
        self.requested_loan_var.set("")
        self.loan_term_var.set("Medium")


def main():
    root = tk.Tk()
    try:
        LoanAnalysisApp(root)
    except Exception as error:
        root.withdraw()
        messagebox.showerror("Unable to Start", str(error))
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()
