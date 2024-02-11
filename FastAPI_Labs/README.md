## Install FASTAPI and Uvicorn

You will need to install fastapi and uvicorn to proceed ahead

1. `pip install fastapi`
2. `pip install uvicorn[standard]`

## FASTAPI Syntax
The instance of FASTAPI class can be defined as `app = FASTAPI()` When you run a FastAPI application, you often pass this app instance to an ASGI server uvicorn. The server then uses the app instance to handle incoming web requests and send responses based on the routes and logic you’ve defined in your FastAPI application.

To run a FASTAPI application
```
uvicorn myapp:app --reload
```

In this command, myapp is the name of the Python file containing your app instance (without the .py extension), and app is the name of the instance itself. The --reload flag tells uvicorn to restart the server whenever code changes are detected, which is useful during development and should not be used in production.

All the functions which should be used as API should be prefixed by `@app.get("/followed_by_endpoint_name")` or `@app.post("/followed_by_endpoint_name")` This particular syntax is used to define route handlers(which function should handle an incoming request based on the URL and HTTP method), which are the functions responsible for responding to client requests to a given endpoint

1. Decorator (@): This symbol is used to define a decorator, which is a way to dynamically add functionality to functions or methods. In FastAPI, decorators are used to associate a function with a particular HTTP method and path.
2. App Instance (app): This represents an instance of the FastAPI class. It is the core of your application and maintains the list of defined routes, request handlers, and other configurations.
3. HTTP Method (get, post, etc.): The HTTP method specifies the type of HTTP request the route will respond to. For example, get is used for retrieving data, and post is used for sending data to the server. FastAPI provides a decorator for each standard HTTP method, such as @app.put, @app.delete, @app.patch, and @app.options, allowing you to define handlers for different types of client requests. For detailed info refer to this webiste by [Mdn](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
4. Path/Endpoint ("/endpoint_name"): This is the URL path where the API will be accessible. When a client makes a request to this path using the specified HTTP method, FastAPI will execute the associated function and return the response.

Using `async` in FastAPI allows for non-blocking operations, enabling the server to handle other requests while waiting for I/O tasks, like database queries or model loading, to complete. This leads to improved concurrency and resource utilization, enhancing the application's ability to manage multiple simultaneous requests efficiently

## Data Models in FASTAPI
```Python
class IrisData(BaseModel):
    petal_length: float
    sepal_length:float
    petal_width:float
    sepal_width:float
```
The `IrisData` class is a [Pydantic model](https://docs.pydantic.dev/latest/concepts/models/) which defines the expected structure of the data for a request body. When you use it as a type annotation for a route operation parameter, FastAPI will perform the following actions:

- Request Body Reading: FastAPI will read the request body as JSON.
- Data Conversion: It will convert the corresponding types, if necessary.
- Data Validation: It will validate the data. If the data is invalid, it will return a 422 Unprocessable Entity error response with details about what was incorrect.

```Python
class IrisResponse(BaseModel):
    response:int
```
The `IrisResponse` class is another Pydantic model that defines the structure of the response data for an endpoint. When you specify response_model=IrisResponse in a route operation, it tells FastAPI to:

- Serialize the Output: Convert the output data to JSON format according to the IrisResponse model.
- Document the API: Include the IrisResponse model in the generated API documentation, so API consumers know what to expect in the response.

### Request Body Reading
---
When a client sends a request to a FastAPI endpoint, the request can include a body with data. For routes that expect data (commonly POST, PUT, or PATCH requests), this data is often in JSON format. FastAPI automatically reads the request body by checking the Content-Type header, which should be set to application/json for JSON payloads.

### Data Conversion
---
Once the request body is read, FastAPI utilizes Pydantic models to parse the JSON data. Pydantic attempts to construct an instance of the specified model using the data from the request body. During this instantiation, Pydantic converts the JSON data into the proper Python data types as declared in the model.

For instance, if the JSON object has a field like petal_length with a value of "5.1" (a string), and the model expects a float, Pydantic will transform the string into a float. If conversion isn't possible (say, the value was "five point one"), Pydantic will raise a validation error.

### Data Validation
---
Pydantic checks that all required fields are present and that the values are of the correct type, adhering to any constraints defined in the model (such as string length or number range). If the validation passes, the endpoint has a verified Python object to work with. If validation fails (due to missing fields, incorrect types, or constraint violations), FastAPI responds with a 422 Unprocessable Entity status. This response includes a JSON body detailing the validation errors, aiding clients in correcting their request data.


## Error Handling 
Error handling in FastAPI can be effectively managed using the HTTPException class. HTTPException is used to explicitly signal an HTTP error status code and return additional details about the error. When an HTTPException is raised within a route, FastAPI will catch the exception and use its content to form the HTTP response.

- Instantiation: The HTTPException class is instantiated with at least two arguments: status_code and detail. The status_code argument is an integer that represents the HTTP status code (e.g., 404 for Not Found, 400 for Bad Request). The detail argument is a string or any JSON-encodable object that describes the error.
- Response: When an HTTPException is raised, FastAPI sends an HTTP response with the status code specified. The detail provided in the HTTPException is sent as the body of the response in JSON format.

```Python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = get_item_by_id(item_id)  # Hypothetical function to fetch an item
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return item
```
In this example, `get_item_by_id` is a function that retrieves an item based on its ID. If no item with the given ID is found, an HTTPException with a 404 Not Found status code is raised, and the detail message is customized to include the ID of the item that was not found.

FastAPI will catch this exception and return a response with a 404 status code and a JSON body like this:
```JSON
{
    "detail": "Item with ID 1 not found"
}
```

For more information on how to handle errors in FASTAPI refer to this [documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/)


## Testing endpoints
To view the documentation of your api model you can use http://127.0.0.1:8000/docs (or) http://localhost:8000/docs after you run you run your FASTAPI app.

![API page](assets/docs.png) 

You can also test out the results of your endpoints by interacting with them. Click on the dropdown button of your endpoint -> Try it out -> Fill the Request body -> Click on Execute button.

![API response](assets/api_response.png)

You can also use other tools like POSTMAN for API testing. 
FAST API detailed video: https://www.youtube.com/watch?v=KReburHqRIQ&list=PLcS4TrUUc53LeKBIyXAaERFKBJ3dvc9GZ&index=5







