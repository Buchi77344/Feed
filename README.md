

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
Thank you for the clarification!

## Below is a **comprehensive documentation** for the code you posted, broken down by functionality:

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







