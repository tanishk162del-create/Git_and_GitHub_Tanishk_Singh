from app import app

client = app.test_client()

api_response = client.get("/api")
assert api_response.status_code == 200
assert isinstance(api_response.get_json(), list)
print("GET /api ->", api_response.status_code)
print("JSON response ->", api_response.get_json())

error_response = client.post("/", data={"name": "", "email": "", "message": ""})
assert error_response.status_code == 400
assert b"All fields are required." in error_response.data
print("POST / with empty fields ->", error_response.status_code)
print("Error handling -> All fields are required.")
