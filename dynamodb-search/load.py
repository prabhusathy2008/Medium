import re, json
import boto3

dataFile = 'customer_details.json'  # Path to the JSON file containing the customer data
table = 'customer_details'  # Name of the DynamoDB table to insert data into

# Initialize the DynamoDB target table
dynamodb = boto3.resource('dynamodb').Table(table)

with open(dataFile, 'r') as fl:
    for item in fl:
        
        item = json.loads(item)
        
        # Create a new field 'keyword' by extracting only alphanumeric characters from 
        # the 'name' and 'date_of_birth' fields, and then converting the result to uppercase
        item['keyword'] = ''.join(re.findall('[A-Za-z0-9]+', item['name'] + item['date_of_birth'])).upper()
        
        dynamodb.put_item(Item=item)