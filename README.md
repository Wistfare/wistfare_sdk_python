# Wistfare Python SDK

Official Python SDK for the [Wistfare](https://wistfare.com) API. Build payments, wallets, and business management into your application.

## Installation

```bash
pip install wistfare
```

All service modules are included in a single package. No extra installs needed.

## Quick Start

```python
from wistfare import Wistfare

wf = Wistfare(api_key="wf_live_xxx")

# Collect a payment via MTN Mobile Money
collection = wf.payments.initiate_collection(
    business_id="biz_123",
    wallet_id="wal_456",
    customer_phone="250788000000",
    amount="10000",
    payment_method="mtn",
    currency="RWF",
    description="Invoice #1234",
)

print(collection["transaction_id"], collection["status"])
```

## Configuration

```python
wf = Wistfare(
    api_key="wf_live_xxx",                       # Required — wf_live_* or wf_test_*
    base_url="https://api-production.wistfare.com",         # Optional
    timeout=30.0,                                 # Optional — seconds (default: 30)
    max_retries=2,                                # Optional — retries on 5xx/network errors
)
```

### Test Mode

Use a `wf_test_*` API key for sandbox testing. Check with `wf.is_test_mode`.

### Context Manager

```python
with Wistfare(api_key="wf_live_xxx") as wf:
    balance = wf.wallet.get_balance("wal_123")
# HTTP client is closed automatically
```

## Payments

```python
# Initiate a mobile money collection
result = wf.payments.initiate_collection(
    business_id="biz_123",
    wallet_id="wal_456",
    customer_phone="250788000000",
    amount="5000",
    payment_method="mtn",  # "mtn" or "airtel_Rw"
    currency="RWF",
)

# Create a payment request (QR code / payment link)
payment_request = wf.payments.create_payment_request(
    business_id="biz_123",
    wallet_id="wal_456",
    request_type="one_time",
    amount="5000",
    currency="RWF",
    description="Table 4 — Lunch",
)
print(payment_request["short_code"])  # "PAY-A1B2C3"
print(payment_request["qr_data"])     # QR data string

# Calculate fees
fee = wf.payments.calculate_fee(
    business_id="biz_123",
    amount="10000",
    transaction_type="collection",
)
print(fee["fee_amount"])  # "250"
print(fee["net_amount"])  # "9750"

# Initiate a disbursement (payout)
payout = wf.payments.initiate_disbursement(
    business_id="biz_123",
    wallet_id="wal_456",
    amount="5000",
    destination_type="mobile_money",
    destination_ref="250788000000",
    idempotency_key="disb_unique_123",
)

# List transactions
txns = wf.payments.list_transactions("biz_123", page=1, per_page=20)
```

### All Payments Methods

| Method | Description |
|--------|-------------|
| `set_fee_config(...)` | Configure fees for a business |
| `get_fee_config(business_id, transaction_type)` | Get fee configuration |
| `list_fee_configs(business_id, **pagination)` | List all fee configs |
| `delete_fee_config(fee_config_id)` | Delete a fee config |
| `calculate_fee(...)` | Calculate fee for an amount |
| `create_payment_request(...)` | Create a QR / payment link |
| `get_payment_request(request_id)` | Get a payment request |
| `list_payment_requests(business_id, **pagination)` | List payment requests |
| `cancel_payment_request(request_id)` | Cancel a payment request |
| `initiate_collection(...)` | Charge a customer via mobile money |
| `get_transaction(transaction_id)` | Get a transaction |
| `list_transactions(business_id, **filters)` | List transactions |
| `initiate_disbursement(...)` | Payout to mobile money |
| `get_disbursement(disbursement_id)` | Get a disbursement |
| `list_disbursements(business_id, **pagination)` | List disbursements |

## Wallet

```python
# Create a wallet
w = wf.wallet.create(user_id="usr_123", wallet_type="personal")

# Check balance
balance = wf.wallet.get_balance("wal_456")
print(balance["available_balance"], balance["currency"])  # "15000" "RWF"

# Transfer between wallets
transfer = wf.wallet.transfer(
    from_wallet_id="wal_456",
    to_wallet_id="wal_789",
    amount="5000",
    description="Split dinner",
    idempotency_key="txn_unique_123",
)

# Deposit (fund wallet via mobile money)
deposit = wf.wallet.initiate_deposit(
    wallet_id="wal_456",
    amount="10000",
    payment_method="mtn",
    phone_number="250788000000",
)

# Withdraw (cash out to mobile money)
withdrawal = wf.wallet.initiate_withdrawal(
    wallet_id="wal_456",
    amount="5000",
    destination_type="mobile_money",
    destination_ref="250788000000",
)
```

### Shared Wallet RBAC

```python
# Create a role
role = wf.wallet.create_role(
    wallet_id="wal_456",
    name="viewer",
    permissions=["balance:read", "transactions:read"],
)

# Add a member
wf.wallet.add_member(wallet_id="wal_456", user_id="usr_789", role_id=role["id"])

# List members
members = wf.wallet.list_members("wal_456")
```

## Business

```python
# Create a business
biz = wf.business.create(
    name="Kigali Coffee House",
    business_type="restaurant",
    category="food_beverage",
)

# Invite staff
invitation = wf.business.invite_staff(
    business_id=biz["id"],
    email="manager@example.com",
    role="manager",
)

# Create a team
team = wf.business.create_team(
    business_id=biz["id"],
    name="Kitchen Staff",
)

# Create an API key
api_key = wf.business.create_api_key(
    business_id=biz["id"],
    name="Production Key",
    environment="live",
)
print(api_key["raw_key"])  # Only shown once!
```

## Error Handling

All SDK errors extend `WistfareError`:

```python
from wistfare.errors import WistfareError, AuthenticationError, NotFoundError

try:
    wf.payments.get_transaction("txn_nonexistent")
except NotFoundError:
    print("Transaction not found")
except AuthenticationError:
    print("Bad API key")
except WistfareError as e:
    print(e, e.status, e.code, e.request_id)
```

| Error Class | HTTP Status | Code |
|-------------|-------------|------|
| `AuthenticationError` | 401 | `authentication_error` |
| `PermissionError` | 403 | `permission_error` |
| `NotFoundError` | 404 | `not_found` |
| `ValidationError` | 400/422 | `validation_error` |
| `RateLimitError` | 429 | `rate_limit` |

## Pagination

List methods return a standard dict with pagination fields:

```python
result = wf.payments.list_transactions("biz_123", page=1, per_page=20)

print(result["data"])      # List of items
print(result["total"])     # Total count
print(result["page"])      # Current page
print(result["per_page"])  # Items per page
print(result["has_more"])  # More pages available?
```

## Requirements

- Python 3.10+
- `httpx` (installed automatically)

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## License

MIT
