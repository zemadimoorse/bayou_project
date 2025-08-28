# Prompts for UI processing.
classify_links_prompt = """
You are an expert HTML parser and link classifier. Your task is to extract all links (<a> tags) from the provided HTML content and classify them based on their purpose.

Classification Rules:
- **Link Type "account"**: Classify links that contain keywords like "account", "profile", "settings", "login", "logout", or "my-info".
- **Link Type "billing"**: Classify links that contain keywords like "bill", "billing", "payment", "invoice", "pay-now", or "statement".
- **Link Type "energy_usage"**: Classify links that contain keywords like "usage", "consumption", "energy", "data", "stats", or "insights".

For each link, determine if it is external. An external link is any link that starts with "http", "https", or "www". Relative links (e.g., /dashboard, #section-1) 
are not external.

The output structure is a single JSON array, with a single object for each link type. Within each object, the key is the link type and the value is an array of 
link objects. Always return account, billing, and usage objects in alphabetical order.

Each object in the sub-array must have the following structure:
{ 
"link_url": "The full URL from the href attribute",
"external_link": "A boolean, true if the link is external, false otherwise",
"dom_element": The DOM element of the link,
}

Organize the output by link type with a key for each type. Do not include any other text or explanation in your response, only the JSON. Do not include link_urls that are 
already in the array.

Example Input HTML:
<body>
<a href="/account/profile">My Profile</a>
<a href="https://example.com/pay-bill">Pay My Bill</a>
<a href="/energy/usage">View My Usage</a>
<a href="/about-us">About Us</a>
</body>

Example JSON Output:
[
  {
    "account": [
      {
        "link_url": "/account/profile",
        "external_link": false,
        "dom_element": "<a href=\"/account/profile\">My Profile</a>"
      }
    ]
  },
  {
    "billing": [
      {
        "link_url": "https://example.com/pay-bill",
        "external_link": true,
        "dom_element": "<a href=\"https://example.com/pay-bill\">Pay My Bill</a>"
      }
    ]
  },
  {
    "energy_usage": [
      {
        "link_url": "/energy/usage",
        "external_link": false,
        "dom_element": "<a href=\"/energy/usage\">View My Usage</a>"
      }
    ]
  }
]

Now process the following HTML content:
"""

# Prompts for data extraction.
# HTML document extraction.
extract_billing_prompt = """
Analyze the following HTML document for data related to a user's energy bill. Extract and classify the data into a structured format. For each piece of information, 
provide a standardized field name, the value, and the corresponding HTML element (e.g., id, class, or tag) from which the value was extracted. The goal is to 
identify key energy-related metrics like due date, payment amount, energy usage, etc.

Do not include account information such as user name, address or account number.

**Output format:**
Return a JSON array where each object has the following keys:
- `fieldName`: A standardized name for the data (e.g., "total_bill_amount", "due_date", "payment_amount", "energy_type").
- `value`: The extracted value (e.g., "150.5", "$25.75", "January 2024").

Example of Expected Output:
```json
[
  {{
    "fieldName": "total_bill_amount",
    "value": "$500",
  }},
  {{
    "fieldName": "due_date",
    "value": "2025-09-01",
  }},
  {{
    "fieldName": "payment_amount",
    "value": "$100",
  }},
  {{
    "fieldName": "energy_type",
    "value": "Residential",
  }}
]

Now process the following HTML content:
"""

# JSON response extraction.
json_billing_prompt = """
Analyze the following JSON data to extract and summarize billing information.

Instructions:
1.  Extract all data related to billing information, such as account balances, due dates, and payment history.
2.  Format the extracted data into a single JSON array.
3.  Each object in the array must contain:
    -   `account_id`: The identifier for the account.
    -   `amount_due`: The current balance owed.
    -   `due_date`: The date the payment is due.
    -   `past_due_amount`: Any amount that is past due.
    -   `last_payment_date`: The date of the most recent payment.
    -   `last_payment_amount`: The amount of the most recent payment.
4.  Do not include any personal identifying information like names or addresses.
5.  The final output must be a single, valid JSON array.

Example Output:
```json
[
  {
    "account_id": "123456789",
    "amount_due": 150.50,
    "due_date": "2024-06-15",
    "past_due_amount": 0.00,
    "last_payment_date": "2024-05-20",
    "last_payment_amount": 125.75
  },
  {
    "account_id": "987654321",
    "amount_due": 25.00,
    "due_date": "2024-06-20",
    "past_due_amount": 10.00,
    "last_payment_date": "2024-05-18",
    "last_payment_amount": 50.00
  }
]
```

Now process the following json data.
"""