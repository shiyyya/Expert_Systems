; ================================================================
; LOAN ANALYSIS EXPERT SYSTEM
; Rule-based loan affordability analysis using CLIPS.
;
; Academic prototype thresholds:
;   Expense ratio < 40%       = low
;   Expense ratio 40%-60%     = moderate
;   Expense ratio > 60%       = high
;   Existing debt ratio <=30% = low
;   Existing debt ratio >30%  = high
;   New loan payment <=30% of available income = affordable
;
; Loan term assumptions:
;   short  = 12 months
;   medium = 24 months
;   long   = 36 months
;
; 
;
; ================================================================

(deftemplate applicant
   (slot name)
   (slot age)
   (slot employment-status)
   (slot employment-length)
   (slot monthly-income)
   (slot monthly-expenses)
   (slot existing-loan-payments)
   (slot payment-history)
   (slot requested-loan-amount)
   (slot loan-term))

(deftemplate expense-level
   (slot level))

(deftemplate available-income
   (slot amount))

(deftemplate debt-level
   (slot level))

(deftemplate loan-term-months
   (slot months))

(deftemplate estimated-payment
   (slot amount))

(deftemplate recommendation
   (slot decision)
   (slot amount)
   (slot reason))


; ================================================================
; EXPENSE ASSESSMENT
; ================================================================

(defrule assess-low-expenses
   (declare (salience 50))
   (applicant
      (monthly-income ?income)
      (monthly-expenses ?expenses))
   (test (> ?income 0))
   (test (< (/ ?expenses ?income) 0.40))
   (not (expense-level))
   =>
   (assert
      (expense-level
         (level low))))


(defrule assess-moderate-expenses
   (declare (salience 50))
   (applicant
      (monthly-income ?income)
      (monthly-expenses ?expenses))
   (test (> ?income 0))
   (test
      (and
         (>= (/ ?expenses ?income) 0.40)
         (<= (/ ?expenses ?income) 0.60)))
   (not (expense-level))
   =>
   (assert
      (expense-level
         (level moderate))))


(defrule assess-high-expenses
   (declare (salience 50))
   (applicant
      (monthly-income ?income)
      (monthly-expenses ?expenses))
   (test (> ?income 0))
   (test (> (/ ?expenses ?income) 0.60))
   (not (expense-level))
   =>
   (assert
      (expense-level
         (level high))))


; ================================================================
; AVAILABLE INCOME
; ================================================================

(defrule calculate-available-income
   (declare (salience 45))
   (applicant
      (monthly-income ?income)
      (monthly-expenses ?expenses)
      (existing-loan-payments ?payments))
   (not (available-income))
   =>
   (bind ?available
      (- ?income ?expenses ?payments))

   (assert
      (available-income
         (amount ?available))))


; ================================================================
; EXISTING DEBT ASSESSMENT
; ================================================================

(defrule assess-low-existing-debt
   (declare (salience 40))
   (applicant
      (monthly-income ?income)
      (existing-loan-payments ?payments))
   (test (> ?income 0))
   (test (<= (/ ?payments ?income) 0.30))
   (not (debt-level))
   =>
   (assert
      (debt-level
         (level low))))


(defrule assess-high-existing-debt
   (declare (salience 40))
   (applicant
      (monthly-income ?income)
      (existing-loan-payments ?payments))
   (test (> ?income 0))
   (test (> (/ ?payments ?income) 0.30))
   (not (debt-level))
   =>
   (assert
      (debt-level
         (level high))))


; ================================================================
; LOAN TERM
; ================================================================

(defrule short-loan-term
   (declare (salience 35))
   (applicant
      (loan-term short))
   (not (loan-term-months))
   =>
   (assert
      (loan-term-months
         (months 12))))


(defrule medium-loan-term
   (declare (salience 35))
   (applicant
      (loan-term medium))
   (not (loan-term-months))
   =>
   (assert
      (loan-term-months
         (months 24))))


(defrule long-loan-term
   (declare (salience 35))
   (applicant
      (loan-term long))
   (not (loan-term-months))
   =>
   (assert
      (loan-term-months
         (months 36))))


; ================================================================
; ESTIMATED MONTHLY PAYMENT
; ================================================================
; Simplified academic calculation:
;
; Requested Loan Amount / Loan Term in Months
;
; Interest and lender-specific fees are not included.
; ================================================================

(defrule calculate-estimated-payment
   (declare (salience 30))
   (applicant
      (requested-loan-amount ?loan))
   (loan-term-months
      (months ?months))
   (not (estimated-payment))
   =>
   (bind ?payment
      (/ ?loan ?months))

   (assert
      (estimated-payment
         (amount ?payment))))


; ================================================================
; FINAL RECOMMENDATIONS
; ================================================================
;
; Higher salience rules have priority.
; Only one recommendation is produced.
; ================================================================


; ------------------------------------------------
; Rule 1: Unemployed applicant
; ------------------------------------------------

(defrule recommend-not-recommended-unemployed
   (declare (salience 100))
   (applicant
      (employment-status unemployed))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision not-recommended)
         (amount 0)
         (reason
            "The applicant is currently unemployed, so the system cannot recommend an additional loan based on the available employment information."))))


; ------------------------------------------------
; Rule 2: Poor payment history
; ------------------------------------------------

(defrule recommend-lower-poor-history
   (declare (salience 90))
   (applicant
      (payment-history poor)
      (requested-loan-amount ?loan))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.70))
         (reason
            "The applicant has a poor payment history, so a lower loan amount is recommended."))))


; ------------------------------------------------
; Rule 3: High expenses
; ------------------------------------------------

(defrule recommend-lower-high-expenses
   (declare (salience 80))
   (applicant
      (requested-loan-amount ?loan))
   (expense-level
      (level high))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.80))
         (reason
            "Monthly expenses are high compared with income, so a lower loan amount is recommended."))))


; ------------------------------------------------
; Rule 4: High existing debt
; ------------------------------------------------

(defrule recommend-lower-high-existing-debt
   (declare (salience 75))
   (applicant
      (requested-loan-amount ?loan))
   (debt-level
      (level high))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.80))
         (reason
            "Existing monthly loan payments are high compared with income, so a lower loan amount is recommended."))))


; ------------------------------------------------
; Rule 5: No remaining income
; ------------------------------------------------

(defrule recommend-no-remaining-income
   (declare (salience 70))
   (available-income
      (amount ?available))
   (test (<= ?available 0))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision not-recommended)
         (amount 0)
         (reason
            "The applicant has no remaining income after expenses and existing loan payments."))))


; ------------------------------------------------
; Rule 6: New payment too high
; ------------------------------------------------

(defrule recommend-lower-insufficient-income
   (declare (salience 65))
   (applicant
      (requested-loan-amount ?loan))
   (available-income
      (amount ?available))
   (estimated-payment
      (amount ?payment))
   (test (> ?payment (* ?available 0.30)))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.80))
         (reason
            "The estimated monthly payment is high compared with the applicant's available income, so a lower loan amount is recommended."))))


; ------------------------------------------------
; Rule 7: Fair payment history
; ------------------------------------------------

(defrule recommend-lower-fair-history
   (declare (salience 60))
   (applicant
      (payment-history fair)
      (requested-loan-amount ?loan))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.90))
         (reason
            "The applicant has a fair payment history, so the system recommends a slightly lower loan amount."))))


; ------------------------------------------------
; Rule 8: Favorable applicant
; ------------------------------------------------

(defrule recommend-favorable
   (declare (salience 10))
   (applicant
      (employment-length long)
      (payment-history good)
      (requested-loan-amount ?loan))
   (or
      (applicant
         (employment-status employed))
      (applicant
         (employment-status self-employed)))
   (or
      (expense-level
         (level low))
      (expense-level
         (level moderate)))
   (debt-level
      (level low))
   (available-income
      (amount ?available))
   (estimated-payment
      (amount ?payment))
   (test (> ?available 0))
   (test (<= ?payment (* ?available 0.30)))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision favorable)
         (amount ?loan)
         (reason
            "The applicant has stable employment, good payment history, manageable financial obligations, and enough available income for the estimated payment."))))


; ================================================================
; FALLBACK RULE
; ================================================================

(defrule recommend-cautious-default
   (declare (salience 1))
   (applicant
      (requested-loan-amount ?loan))
   (not (recommendation))
   =>
   (assert
      (recommendation
         (decision lower)
         (amount (* ?loan 0.80))
         (reason
            "The applicant does not meet all favorable conditions in the knowledge base, so a cautious lower amount is recommended."))))