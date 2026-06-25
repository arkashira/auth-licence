import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class License:
    key: str
    email: str
    purchase_date: str

class AuthLicence:
    def __init__(self):
        self.licenses = {}
        self.stripe_checkout = StripeCheckout()

    def purchase_license(self, email: str) -> License:
        payment_result = self.stripe_checkout.process_payment(email)
        if payment_result:
            license_key = self.generate_license_key(email)
            self.licenses[license_key] = License(license_key, email, datetime.now().strftime("%Y-%m-%d"))
            self.send_license_key_via_email(email, license_key)
            return self.licenses[license_key]
        else:
            raise Exception("Payment failed")

    def generate_license_key(self, email: str) -> str:
        return f"LICENSE-{email}"

    def send_license_key_via_email(self, email: str, license_key: str) -> None:
        # Simulate sending an email
        print(f"Sending license key {license_key} to {email}")

class StripeCheckout:
    def process_payment(self, email: str) -> bool:
        # Simulate payment processing
        return True

def main():
    auth_licence = AuthLicence()
    license = auth_licence.purchase_license("user@example.com")
    print(license)

if __name__ == "__main__":
    main()
