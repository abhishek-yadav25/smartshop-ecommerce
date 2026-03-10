import requests
from products.models import Product

url = "https://dummyjson.com/products?limit=50"

response = requests.get(url)
data = response.json()

for item in data['products']:

    Product.objects.get_or_create(
        name=item['title'],
        defaults={
            "price": item['price'],
            "description": item['description'],
            "image": item['thumbnail']
        }
    )

print("Products imported successfully")