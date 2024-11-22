from index import handler

# Search with keyword
event = {
    "keyword": "12"
}
print(handler(event, None))

"""
{'items': [{'loyalty_status': 'Gold', 'address': '321 Maple Road, Gotham, CA, 90210, USA', 'date_of_birth': '1982-09-12', 'id': '4', 'email': 'michael.johnson@example.com', 'phone': '+1-555-3456', 'name': 'Michael Johnson', 'keyword': 'MICHAELJOHNSON19820912'}, {'loyalty_status': 'Bronze', 'address': '123 Pine Avenue, Coast City, CA, 94016, USA', 'date_of_birth': '1992-12-01', 'id': '8', 'email': 'david.anderson@example.com', 'phone': '+1-555-5566', 'name': 'David Anderson', 'keyword': 'DAVIDANDERSON19921201'}], 'consumed_capacity': 1.0, 'next_token': {'loyalty_status': None, 'keyword': '12', 'last_evaluated_key': None}}
"""

# Search with keyword and loyalty status
event = {
    "keyword": "12",
    "loyalty_status": "Gold"
}
print(handler(event, None))

"""
{'items': [{'loyalty_status': 'Gold', 'address': '321 Maple Road, Gotham, CA, 90210, USA', 'date_of_birth': '1982-09-12', 'id': '4', 'email': 'michael.johnson@example.com', 'phone': '+1-555-3456', 'name': 'Michael Johnson', 'keyword': 'MICHAELJOHNSON19820912'}], 'consumed_capacity': 0.5, 'next_token': {'loyalty_status': 'Gold', 'keyword': '12', 'last_evaluated_key': None}}
"""

# Search with keyword and MINIMUM_RESULT = 1
event = {
    "keyword": "12"
}
print(handler(event, None))

"""
{'items': [{'loyalty_status': 'Bronze', 'address': '123 Pine Avenue, Coast City, CA, 94016, USA', 'date_of_birth': '1992-12-01', 'id': '8', 'email': 'david.anderson@example.com', 'phone': '+1-555-5566', 'name': 'David Anderson', 'keyword': 'DAVIDANDERSON19921201'}], 'consumed_capacity': 1.5, 'next_token': {'loyalty_status': None, 'keyword': '12', 'last_evaluated_key': {'id': {'N': '8'}, 'loyalty_status': {'S': 'Bronze'}}}}
"""

# Search with keyword and MINIMUM_RESULT = 1 and next_token
event = {
    "keyword": "12",
    "next_token": {
        "loyalty_status": None,
        "keyword": "12",
        "last_evaluated_key": {
            "id": {
                "N": "8"
            },
            "loyalty_status": {
                "S": "Bronze"
            }
        }
    }
}
print(handler(event, None))

"""
{'items': [{'loyalty_status': 'Gold', 'address': '321 Maple Road, Gotham, CA, 90210, USA', 'date_of_birth': '1982-09-12', 'id': '4', 'email': 'michael.johnson@example.com', 'phone': '+1-555-3456', 'name': 'Michael Johnson', 'keyword': 'MICHAELJOHNSON19820912'}], 'consumed_capacity': 3.0, 'next_token': {'loyalty_status': None, 'keyword': '12', 'last_evaluated_key': {'id': {'N': '4'}, 'loyalty_status': {'S': 'Gold'}}}}
"""