# AI Agent Design: AutoRefund-Agent

## 1. Goal
Automatically evaluate and process eligible customer refund requests for an e-commerce platform without requiring human intervention.

---

## 2. Inputs
* **Customer Email:** `customer@example.com`
* **Order ID:** `ORD-98765`
* **Refund Reason:** "Item arrived damaged"

---

## 3. Tools
1. `get_order_details(order_id)` — Fetches purchase date, delivery date, return eligibility window, total amount, and item status.
2. `issue_refund(order_id, amount)` — Processes money return via payment gateway (Stripe API) and returns transaction status.
3. `send_customer_email(email, subject, body)` — Sends automated email notification to the customer.
4. `escalate_to_human(order_id, reason)` — Routes complex edge cases to a support ticket queue for human review.

---

## 4. Output
Refund processed via Stripe API + confirmation email delivered to customer (or escalation ticket created if ineligible).

---

## 5. Decision-Making Process (ReAct Loop)

```text
[START] Goal: Process refund request for Order #ORD-98765

THOUGHT: I need to check the delivery date and policy eligibility for Order #ORD-98765.
ACTION: get_order_details(order_id="ORD-98765")
OBSERVATION: Delivered 5 days ago; Return Policy Window: 30 days; Total Amount: $45.00.

THOUGHT: The order was delivered 5 days ago (within the 30-day window) and the reason is item damage. This request is eligible for an instant automated refund.
ACTION: issue_refund(order_id="ORD-98765", amount=45.00)
OBSERVATION: Payment Status: Success | Transaction ID: tx_3n98274

THOUGHT: The refund processed successfully. I must now send a confirmation email to the customer.
ACTION: send_customer_email(
  email="customer@example.com",
  subject="Refund Confirmation: Order #ORD-98765",
  body="Your refund of $45.00 for Order #ORD-98765 has been successfully processed."
)
OBSERVATION: Email Status: Delivered

THOUGHT: All tasks completed.
FINAL ANSWER: Order #ORD-98765 refunded ($45.00) and confirmation email sent.