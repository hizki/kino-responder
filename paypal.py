import paypalrestsdk as paypal
import logging
import json
import os

def get_all_payments():
	payment_history = paypal.Payment.all({"count": 2})
	print(payment_history)


def generate_paypal_invoice():
	invoice = paypal.Invoice({
		"merchant_info": {
			"email": "jaypatel512-facilitator@hotmail.com",  # You must change this to your sandbox email account
			"first_name": "Dennis",
			"last_name": "Doctor",
			"business_name": "Medical Professionals, LLC",
			"phone": {
				"country_code": "001",
				"national_number": "5032141716"
			},
			"address": {
				"line1": "1234 Main St.",
				"city": "Portland",
				"state": "OR",
				"postal_code": "97217",
				"country_code": "US"
			}
		},
		"billing_info": [{"email": "example@example.com"}],
		"items": [
			{
				"name": "Sutures",
				"quantity": 100,
				"unit_price": {
					"currency": "USD",
					"value": 5
				}
			}
		],
		"note": "Medical Invoice 16 Jul, 2013 PST",
		"payment_term": {
			"term_type": "NET_45"
		},
		"shipping_info": {
			"first_name": "Sally",
			"last_name": "Patient",
			"business_name": "Not applicable",
			"phone": {
				"country_code": "001",
				"national_number": "5039871234"
			},
			"address": {
				"line1": "1234 Broad St.",
				"city": "Portland",
				"state": "OR",
				"postal_code": "97216",
				"country_code": "US"
			}
		},
		"shipping_cost": {
			"amount": {
				"currency": "USD",
				"value": 10
			}
		}
	})

	if invoice.create():
		print(json.dumps(invoice.to_dict(), sort_keys=False, indent=4))
	
	else:
		print(invoice.error)

if __name__ == "__main__":
	new_api = paypal.Api(
		mode="sandbox", 
		client_id="AXSAb66kuPoz5xmhAVtUnK6w3ow7MxvTT2We8svaDUfKOtcdaQtVzcbSbQ_cDRXBRoT1GrQACxPEEOjF", 
		client_secret="EGY18J47ktUeNe-qCkzYaWxuPnUy1dSv_AV5KBTOuxM0lQfxHjX8OzEUgY0NwPQWIzCIq1wQU2TvNh7E")

	os.environ["PAYPAL_CLIENT_ID"]=new_api.client_id
	os.environ["PAYPAL_CLIENT_SECRET"]=new_api.client_secret

	logging.basicConfig(level=logging.INFO)

	auth = new_api.get_refresh_token

	try:
		get_all_payments()
	except Exception as e:
		print(e.content)