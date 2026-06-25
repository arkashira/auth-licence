from auth_licence import AuthLicence, License
import pytest

def test_purchase_license():
    auth_licence = AuthLicence()
    license = auth_licence.purchase_license("user@example.com")
    assert isinstance(license, License)
    assert license.key == "LICENSE-user@example.com"
    assert license.email == "user@example.com"
    assert license.purchase_date

def test_purchase_license_payment_failed():
    class StripeCheckout:
        def process_payment(self, email: str) -> bool:
            return False
    auth_licence = AuthLicence()
    auth_licence.stripe_checkout = StripeCheckout()
    with pytest.raises(Exception):
        auth_licence.purchase_license("user@example.com")

def test_generate_license_key():
    auth_licence = AuthLicence()
    license_key = auth_licence.generate_license_key("user@example.com")
    assert license_key == "LICENSE-user@example.com"

def test_send_license_key_via_email():
    auth_licence = AuthLicence()
    auth_licence.send_license_key_via_email("user@example.com", "LICENSE-KEY")
    # No assertion, just checking it doesn't raise an exception
