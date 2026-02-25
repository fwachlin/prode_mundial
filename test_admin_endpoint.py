from app import app

with app.test_client() as client:
    response = client.get('/secret-create-admin-xyz123')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.data.decode()}")
