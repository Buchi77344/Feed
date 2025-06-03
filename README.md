

## 📄  Documentation

This project contains several core views that manage user authentication and the homepage logic for the campaign platform. Below is a detailed breakdown of each view and its responsibilities.

---

### 🔸 `index(request)`

**Purpose**: Renders the homepage with featured, trending, and recent campaigns. Also handles newsletter subscription.

**Key Features**:

* Fetches top 3 featured campaigns.
* Fetches top 3 trending campaigns that are still active and launched.
* Fetches top 3 general campaigns.
* Calculates the total donation amount and funding percentage for each campaign.
* Handles newsletter subscription with email duplication check.
* Loads social media links (if available).

**Template Rendered**: `index.html`

**Context Provided**:

* `featured_campaigns`
* `trending_campaigns`
* `campaigns`
* `campaigns_with_percentage` – For featured campaigns.
* `campaigns_with_percentages` – For general campaigns.
* `social` – Social media handles.

---

### 🔸 `signup(request)`

**Purpose**: Handles user registration for new accounts.

**Method**: `POST`

**Validation Steps**:

* Checks if both passwords match.
* Verifies that email and phone number are unique.
* Creates a new `CustomUser` account using the provided form data.

**Redirects**:

* On success: Redirects to `login` with a success message.
* On failure: Redirects back to `signup` with appropriate error messages.

**Template Rendered**: `signup.html` (for GET requests)

---

### 🔸 `login(request)`

**Purpose**: Authenticates users based on email and password.

**Method**: `POST`

**Logic**:

* Uses Django's `auth.authenticate()` to validate credentials.
* Logs the user in and redirects to their profile with a welcome message.
* On failure, shows an error and redirects back to `login`.

**Template Rendered**: `login.html` (for GET requests)

---

### 🔸 `logout(request)`

**Purpose**: Logs the currently authenticated user out of the session.

**Redirects**:

* Redirects to `login` page with a success message on logout.

---

### 🛠 Models Involved

* `CustomUser` – Custom user model handling registration and login.
* `Campaign` – Represents fundraising campaigns.
* `Newsletter` – Stores newsletter subscriber emails.
* `SocialMedia` – Stores social media links related to the platform.

---



## 📧 **Password Reset Functionality**

### 1. `forget(request)`

**Purpose:**
Sends a password reset email with a tokenized link to the user.

**Workflow:**

* Accepts a POST request with an email address.
* Verifies that a user with the given email exists.
* Generates a secure UID and token using Django’s `default_token_generator`.
* Constructs a reset URL like `/reset-password/<uidb64>/<token>/`.
* Sends the reset link via email using `send_mail()`.
* Displays a success or error message using Django’s `messages`.

**Key Concepts Used:**

* `CustomUser` (custom auth model via `get_user_model()`)
* `urlsafe_base64_encode(force_bytes(user.pk))`
* `default_token_generator.make_token(user)`
* `send_mail()` for sending reset instructions

---

### 2. `reset_password(request, uidb64, token)`

**Purpose:**
Verifies the token from the password reset link and allows the user to set a new password.

**Workflow:**

* Decodes the user ID from `uidb64`.
* Checks if the token is valid for the user.
* On POST, verifies password and confirmation match.
* Hashes and sets the new password with `make_password()`.
* Redirects to the login page if successful, otherwise shows error.

**Key Concepts Used:**

* `urlsafe_base64_decode(uidb64)`
* `default_token_generator.check_token()`
* `make_password(new_password)`
* Flash messaging (`messages.success` / `messages.error`)

---

## 📢 **Campaign Creation Functionality**

### 3. `start_campaign(request)`

**Purpose:**
Allows authenticated users to create a fundraising campaign via a form submission.

**Workflow:**

* Accepts form input (POST), including text fields, dates, file/image uploads.
* Performs **form validation**, checking:

  * Required fields
  * Proper formatting (like valid `video_url`)
  * Logical consistency (e.g., non-zero `monetary` target)
* Saves the campaign to the database if valid.
* Renders error messages and re-renders form with validation feedback if invalid.

**Additional Features:**

* Uses `get_object_or_404(SocialMedia)` to retrieve associated social links.
* Uses `django_countries.countries` to provide a country selection dropdown.
* Uses Django’s built-in flash `messages` for feedback.
* Redirects to the user’s profile upon success.

---

### 4. `create_campaign(request)`

**Purpose:**
Provides an **API-style endpoint** (likely used via AJAX/JavaScript frontend) to create campaigns.

**Workflow:**

* Accepts POST request.
* Extracts campaign details from `request.POST` and `request.FILES`.
* Saves a new `Campaign` instance.
* Returns a JSON response with the newly created campaign’s token.

**Return:**

```json
{
  "id": "<campaign_token>"
}
```

**Error Response:**

```json
{
  "error": "Invalid request method"
}
```

---

## ✅ Technologies and Tools Used

| Tool / Concept                | Role                                     |
| ----------------------------- | ---------------------------------------- |
| `send_mail()`                 | Sends reset email with link              |
| `default_token_generator`     | Creates secure token for password reset  |
| `urlsafe_base64_encode`       | Encodes user ID to safely embed in URL   |
| `make_password()`             | Hashes the password securely             |
| `Campaign.objects.create()`   | Saves new campaign instance              |
| `@login_required`             | Restricts access to logged-in users only |
| `messages` framework          | Provides user feedback (success/errors)  |
| `JsonResponse`                | Used in API-style campaign creation      |
| `get_user_model()`            | Supports custom user models              |
| `django_countries`            | Provides list of countries               |
| `request.FILES.get('images')` | Handles image uploads                    |

---

## 🔐 Security & Best Practices

* All sensitive actions (like resetting passwords) validate tokens and user identity.
* Campaign creation is restricted via `@login_required`.
* All POST operations check for method and data validation.
* Email headers are safely checked with `BadHeaderError`.
* SMTP errors are gracefully caught and reported.

---


---

## 📄 `edit_campaign` View

### URL Pattern

```python
path('campaign/edit/<str:token>/', views.edit_campaign, name='edit_campaign')
```

### Description

This view allows a logged-in user to **edit an existing campaign**. The campaign is identified by a unique token. It supports both `GET` and `POST` methods.

* **GET**: Renders a pre-filled form (`edit_campaign.html`) with the current campaign details.
* **POST**: Updates the campaign with the submitted form data.

### Imports Used

```python
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Campaign
```

### Parameters

* `request`: Django `HttpRequest` object.
* `token`: Unique token that identifies the campaign.

### Behavior

* Ensures user is authenticated.
* Retrieves the `Campaign` object using the token.
* If the method is `POST`, it updates the campaign fields with form values.
* On success, returns a JSON response containing the campaign's token.
* On `GET`, renders the form with current values.

### Response

* **POST**: `JsonResponse({'token': campaign.token})`
* **GET**: Renders `edit_campaign.html` template with:

  * `campaign`: The campaign object
  * `category`: Category choices from model
  * `event`: Event choices from model
  * `countries`: Presumed list (make sure it's defined)

---

## 📄 `profile` View

### URL Pattern

```python
path('profile/', views.profile, name='profile')
```

### Description

Displays the **user’s profile page**, listing their campaigns, donation data, and profile details. Also allows **profile updates** via `POST`.

### Behavior

* Retrieves all campaigns owned by the user.
* Aggregates total donations per campaign.
* Updates user and profile data on `POST`.
* Fetches optional social media data if available.
* Renders `profile.html` with relevant context.

### Context Passed to Template

* `campaigns`: Campaigns owned by user
* `donations`: Donations made to user's campaigns
* `profile`: User’s profile object
* `social`: (optional) SocialMedia object

---

## 📄 `donate` View

### URL Pattern

```python
path('donate/<str:token>/', views.donate, name='donate')
```

### Description

Displays the donation page for a specific campaign. This is a **GET-only** view.

### Behavior

* Retrieves campaign using token.
* Optionally includes `SocialMedia` object if it exists.
* Renders `donate.html`.

---

## 📄 `paypal_payment_link` View

### URL Pattern

```python
path('paypal-payment/<str:token>/', views.paypal_payment_link, name='paypal_payment_link')
```

### Description

Handles **PayPal payment creation** for a campaign donation. Accepts a `POST` request with donation details.

### Request Body (JSON)

```json
{
  "amount": "20.00",
  "message": "Keep up the good work!"
}
```

### Response

* On success: JSON with `approval_url` and `campaign_token`
* On error: JSON error message

### Behavior

* Validates donation amount.
* Creates a PayPal payment using `paypalrestsdk`.
* Returns approval URL for user redirection.

---

## 📄 `stripe_payment_link` View

### URL Pattern

```python
path('stripe-payment/<str:token>/', views.stripe_payment_link, name='stripe_payment_link')
```

### Description

Creates a **Stripe PaymentIntent** for the campaign donation. Expects a `POST` request with donation data.

### Request Body (JSON)

```json
{
  "amount": "25.00",
  "message": "Happy to help!"
}
```

### Response

* On success: JSON with `client_secret` and `campaign_token`
* On error: JSON error message

### Behavior

* Validates donation amount.
* Converts amount to cents for Stripe.
* Creates a `PaymentIntent`.
* Returns the `client_secret` to frontend for payment completion.

---

## 📝 Notes

* Ensure all models (`Campaign`, `Profile`, `Donation`, `SocialMedia`, `PaymentData`) are correctly defined in `models.py`.
* Always protect `POST` endpoints with CSRF tokens or `@csrf_exempt` when integrating with JavaScript (if needed).
* Replace placeholder API keys (`stripe.api_key`) with secure environment variables in production.
* Make sure `countries` is defined and passed in `edit_campaign`.



## 🔍 `find_campaign(request)`

**Purpose**: Display all active (launched) campaigns with total donations and funding percentage.

**Logic**:

* Filters campaigns with `is_launch=True`.
* For each campaign:

  * Calculates total donations.
  * Computes percentage of goal achieved.
* Optionally gets social media data.
* Renders the `find_campaign.html` template.

**Context Data**:

```python
{
  "campaigns_with_percentage": [
    {
      "campaign": <Campaign>,
      "total_donations": <int>,
      "percentage_achieved": <float>
    },
    ...
  ],
  "social": <SocialMedia|None>
}
```

---

## ℹ️ `about(request)`

**Purpose**: Render the About page with optional social media links.

**Context Data**:

```python
{
  "social": <SocialMedia|None>
}
```

---

## ❓ `faq(request)`

**Purpose**: Renders the FAQ page.

**Template**: `faq.html`

---

## 🔍 `search_campaigns(request)`

**Method**: POST
**Purpose**: Allows frontend search via AJAX by keyword, category, or sector.

**Input (JSON POST body)**:

```json
{
  "keyword": "education",
  "categories": ["health"],
  "sectors": ["ngo"]
}
```

**Logic**:

* Validates if at least one filter is provided.
* Filters campaigns based on provided criteria.

**Returns**: A JSON list of matching campaigns:

```json
[
  {
    "campaign_name": "...",
    "country": "...",
    "story": "...",
    "category": "...",
    "sector": "...",
    "start_date": "...",
    "end_date": "..."
  },
  ...
]
```

**Error**: Returns JSON error on failure or wrong method.

---

## 🤝 `support(request)`

**Purpose**: Renders the support/help page.

**Template**: `support.html`

---

## 📄 `details(request, token)`

**Purpose**: Show the detail view of a campaign identified by a unique `token`.

**Logic**:

* Fetch campaign and related donations.
* Calculate total donations and percentage funded.
* Save goal progress.
* Get donation count.
* Get social media details.

**Context Data**:

```python
{
  "campaign_details": <Campaign>,
  "total_donations": <Decimal>,
  "percentage_achieved": <Decimal>,
  "donation": <QuerySet of Donation>,
  "campaign_with_donations": <Campaign with annotated count>,
  "social": <SocialMedia|None>
}
```

---

## 🖼 `preview(request, token)`

**Decorator**: `@login_required`

**Purpose**: Allows a logged-in user to preview a campaign before publishing.

**Context Data**:

```python
{
  "campaign_details": <Campaign>
}
```

**Redirects**: To login if user is not authenticated.

---

## 💰 `fee_payout(request)`

**Purpose**: Renders a page about platform fees and payout structure.

**Template**: `feeds-payout.html`

---

## ❤️ `donate(request)`

**Purpose**: Renders the donation landing page.

**Template**: `dote.html` (possibly a typo: should it be `donate.html`?)

---

## 🧾 Notes

* Be sure to include `Donation` model where used (e.g., in `details()`).
* Check for undefined variables (e.g., `social` might not exist if the condition is false).
* Improve performance with `.select_related()` or `.prefetch_related()` if needed in views with multiple DB hits.
* Consistently use `get_object_or_404` only when expecting one item, and guard against missing objects gracefully.










