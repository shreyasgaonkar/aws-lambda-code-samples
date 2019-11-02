This will programmatically create subscription filters (here using phone numbers) until you hit the limit. It can be used as a guide to create new subscriptions with the required subscription filters, to leverage selective push messages to a SNS topic.  


Sample payload to set subscription policy:

```
{
   "store": ["example_corp"],
   "event": [{"anything-but": "order_cancelled"}],
   "customer_interests": [
      "rugby",
      "football",
      "baseball"
   ],
   "price_usd": [{"numeric": [">=", 100]}]
}
```
