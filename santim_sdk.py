import time

import httpx
import jwt

PRODUCTION_BASE_URL = "https://services.santimpay.com/api/v1/gateway"
TEST_BASE_URL = "https://testnet.santimpay.com/api/v1/gateway"


class SantimPaySdk:
    def __init__(self, merchant_id: str, private_key: str, test_mode: bool = False):
        self.merchant_id = merchant_id
        self.private_key = private_key
        self.base_url = PRODUCTION_BASE_URL

        if test_mode:
            self.base_url = TEST_BASE_URL

    def __signES256(self, data: dict, private_key: str) -> str:
        return jwt.encode(data, private_key, algorithm="ES256")

    def generateSignedTokenForInitialPayment(self, amount: float, payment_reason: str):
        generated_time = int(time.time())

        payload = {
            "amount": amount,
            "paymentReason": payment_reason,
            "merchantId": self.merchant_id,
            "generated": generated_time,
        }

        val = self.__signES256(payload, self.private_key)
        return val

    async def generate_payment_url(
        self,
        id: str,
        amount: float,
        payment_reason: str,
        success_redirect_url: str,
        failure_redirect_url: str,
        notify_url: str,
        phone_number: str = None,
    ) -> str:
        try:
            token = self.generateSignedTokenForInitialPayment(amount, payment_reason)
            payload = {
                "id": id,
                "amount": amount,
                "reason": payment_reason,
                "merchantId": self.merchant_id,
                "signedToken": token,
                "successRedirectUrl": success_redirect_url,
                "failureRedirectUrl": failure_redirect_url,
                "notifyUrl": notify_url,
            }

            if phone_number is not None:
                payload["phoneNumber"] = phone_number

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/initiate-payment",
                    json=payload,
                )
                if response.status_code == 200:
                    return response.json()["url"]

                reason = response.json()
                raise Exception("Failed to initiate payment", reason)
        except Exception:
            raise
