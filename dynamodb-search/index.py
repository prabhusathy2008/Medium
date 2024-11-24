import re
import boto3

# Constants for table and index names, and minimum result count
TABLE_NAME = 'customer_details'
INDEX_NAME = 'index_search'
MINIMUM_RESULT = 10

# Initialize DynamoDB client
client = boto3.client('dynamodb')

def search_keyword(loyalty_status=None, keyword=None, next_token=None):
    """
    Searches for items based on loyalty_status and keyword with pagination support.
    """

    # Prepare the query parameters for the DynamoDB search
    queryParam = {
        'TableName': TABLE_NAME,
        'IndexName': INDEX_NAME,
        'FilterExpression': 'contains(keyword, :keyword)',
        'ExpressionAttributeValues': {
            ':keyword': {
                'S': re.sub('[^a-zA-Z0-9]+', '', keyword or '').upper()
            }
        },
        'ReturnConsumedCapacity': 'INDEXES',
        'Limit': MINIMUM_RESULT  # This is not required. It's used here for testing pagination and limits the number of items scanned per search.
    }

    # Check if there's a next token (for pagination) and set the start key
    if next_token is not None and next_token['last_evaluated_key'] is not None:
        if loyalty_status == next_token['loyalty_status'] and keyword == next_token['keyword']:
            queryParam['ExclusiveStartKey'] = next_token['last_evaluated_key']

    # If loyalty_status is provided, perform a query; otherwise, perform a scan
    if loyalty_status is not None:
        queryParam['KeyConditionExpression'] = 'loyalty_status = :loyalty_status'
        queryParam['ExpressionAttributeValues'][':loyalty_status'] = {
                'S': loyalty_status
        }
        response = client.query(**queryParam) # Execute query
    else:
        response = client.scan(**queryParam) # Execute scan if no loyalty_status provided

    # Prepare and return the search results, including the keys of matched items
    return {
        'keys': [item['id']['N'] for item in response['Items']], # Extract IDs of the matched items
        'consumed_capacity': response['ConsumedCapacity']['CapacityUnits'], # Return consumed read capacity
        'next_token': {
            'loyalty_status': loyalty_status,
            'keyword': keyword,
            'last_evaluated_key': response['LastEvaluatedKey'] if 'LastEvaluatedKey' in response else None
        } # Next key for pagination
    }

def get_items(keys):
    """
    Retrieves customer details based on a list of keys (customer ids).
    """

    # If no keys are provided, return an empty list
    if len(keys) == 0:
        return []

    # Prepare the request parameters and execute the batch get item request
    queryParam = {}
    queryParam['RequestItems'] = {}
    queryParam['RequestItems'][TABLE_NAME] = {
        'Keys': [{'id': {'N': key}} for key in keys]
    }
    response = client.batch_get_item(**queryParam)

    # Process the response and extract the items
    items = [] 
    for item in response['Responses']['customer_details']:
        # Convert DynamoDB response format to a plain dictionary
        items.append({key: value['N'] if 'N' in value else value['S'] for key, value in item.items()})

    return items # Return the list of customer details

def handler(event, context):
    """
    Main handler function that processes the search request, handles pagination, and returns results.
    """

    # Extract parameters from the incoming event
    keyword = event['keyword'] if 'keyword' in event else None
    loyalty_status = event['loyalty_status'] if 'loyalty_status' in event else None
    next_token = event['next_token'] if 'next_token' in event else None

    keys = [] # List to store matching customer ids
    consumed_capacity = 0 # Track consumed capacity
    while True:

        # Perform the keyword search and get search results
        searchResult = search_keyword(loyalty_status=loyalty_status, keyword=keyword, next_token=next_token)

        keys.extend(searchResult['keys']) # Append the found keys to the keys list
        consumed_capacity += searchResult['consumed_capacity'] # Add to the total consumed capacity
        next_token = searchResult['next_token'] # Update the next token for pagination

        # Break if minimum results are reached or if there's no last_evaluated_key
        if len(keys) >= MINIMUM_RESULT or searchResult['next_token']['last_evaluated_key'] is None:
            break            

    # Return the final result with customer details, consumed capacity, and pagination token
    return {
        'items': get_items(keys), # Fetch the customer details for the matched ids
        'consumed_capacity': consumed_capacity, # Total consumed capacity for the search operation
        'next_token': next_token # Pagination token for the next batch of results (if any)
    }
