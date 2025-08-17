# File: hello_algolia.py
from algoliasearch.search.client import SearchClientSync

app_id = "ALGOLIA_APPLICATION_ID"
# API key with `addObject` and `search` ACL
api_key = "ALGOLIA_API_KEY"
index_name = "test-index"


if __name__ == "__main__":
    client = SearchClientSync(app_id, api_key)
    record = {"objectID": "object-1", "name": "test record"}

    # Add record to an index
    save_resp = client.save_object(
        index_name=index_name, body=record,
    )

    # Wait until indexing is done
    client.wait_for_task(
        index_name=index_name,
        task_id=save_resp.task_id,
    )

    # Search for 'test'
    results = client.search(
       {
           "requests": [
               {
                   "indexName": index_name,
                   "query": "test"
               }
           ]
       }
    )

    print(results.to_json())
