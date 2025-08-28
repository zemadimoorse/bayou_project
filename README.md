# Utility Billing Parser

## 💡 Description and Technical Details

This application is designed to automate the process of extracting billing data from utility company websites.  The system uses **Selenium** and **WebDriver** to navigate and interact with web pages, logging in with provided credentials. 

After logging in, it classifies links into categories like **account**, **billing**, and **usage**. It then sequentially loads each classified URL to parse HTML content and JSON network call responses, ultimately extracting user data. The current implementation is **synchronous**, but future plans include introducing **asynchronous** processing and **batching** of users for improved efficiency. Error handling and retry mechanisms are planned for a later design phase.

-----

## 🚀 How to Run the Application

To run the application, follow these steps:

1.  Clone the implementation from this repo.
2.  If you're targeting a different utility, you'll need to modify lines 17-24 in the `project.py` file to accommodate the new site.
3.  Replace USERNAME and PASSWORD in `project.py` with the PSE utility credentials. Replace API key with Zhila's gemini API key.
3.  Execute `project.py` locally. Note that the application relies on the Gemini API key, which is linked to a specific Google Cloud project. This may require additional configuration.
4.  Once running, be patient—requests to the Gemini API can be time-consuming. The results will be displayed in the console upon completion.

-----

## 🔌 How to Use with a Different Utility

To adapt the application for a new utility, you must update the core logic in `project.py` (specifically lines 17-24). This is where the application's WebDriver and login routines are configured to handle the specific structure of a new utility's website.

-----

## 📄 Example Output

The following is an example of the kind of data the application extracts after parsing a utility's website.

### **Extracted Fields**

  * [cite\_start]**outstanding\_balance**: $0.00 [cite: 1]
  * [cite\_start]**due\_date**: 08/21/2025 [cite: 1]
  * [cite\_start]**current\_bill\_date**: 08/01/2025 [cite: 1]
  * [cite\_start]**previous\_bill\_date**: 07/01/2025 [cite: 1]
  * [cite\_start]**previous\_bill\_total\_charges**: $176.43 [cite: 2]
  * [cite\_start]**previous\_bill\_payment\_received**: -$176.43 [cite: 2]
  * [cite\_start]**current\_period\_electricity\_charges**: $200.09 [cite: 2]
  * [cite\_start]**current\_period\_natural\_gas\_charges**: $39.01 [cite: 2]
  * [cite\_start]**current\_period\_total\_charges**: $239.10 [cite: 2]
  * [cite\_start]**current\_bill\_payment\_received**: -$239.10 [cite: 3]
  * [cite\_start]**total\_payments\_received**: -$239.10 [cite: 3]
  * [cite\_start]**electricity\_meter\_number**: X154394834 [cite: 3]
  * [cite\_start]**electricity\_usage\_kwh**: 1114 [cite: 3]
  * [cite\_start]**natural\_gas\_meter\_number**: 1265869 [cite: 3]
  * [cite\_start]**natural\_gas\_usage\_therms**: 9.9511 [cite: 4]

### **Processed JSON Output**

```json
[
  {
    "account_id": "220035713407",
    "amount_due": 0.0,
    "due_date": "2025-08-21",
    "past_due_amount": 0.0,
    "last_payment_date": null,
    "last_payment_amount": null
  },
  {
    "account_id": "220035713407",
    "amount_due": 0.0,
    "due_date": "2025-08-21",
    "past_due_amount": 0.0,
    "last_payment_date": null,
    "last_payment_amount": null
  }
]
```