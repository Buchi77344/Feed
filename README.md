

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





