import colorama
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

class Product:
    def __init__(self, name, price, ratings, reviews):
        self.name = name
        self.price = price
        self.ratings = ratings
        self.reviews = reviews

def get_user_input():
    item_name = input("Enter the item you want: ")
    price_range = float(input("Enter your preferred price range: "))
    ratings = float(input("Enter the minimum ratings you want: "))
    return item_name, price_range, ratings

def search_products(item_name):
    base_url = "https://www.example.com/search?q="
    search_url = base_url + item_name.replace(" ", "+")
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        products = []

        for product_element in soup.find_all("div", class_="product"):
            name = product_element.find("h2").text
            price = float(product_element.find("span", class_="price").text.replace("$", ""))
            ratings = float(product_element.find("span", class_="ratings").text)
            reviews = int(product_element.find("span", class_="reviews").text.replace(" reviews", ""))
            products.append(Product(name, price, ratings, reviews))
        
        return products
    else:
        print("Failed to retrieve product information.")
        return []

def compare_products(products, price_range, min_ratings):
    valid_products = []
    for product in products:
        if product.price <= price_range and product.ratings >= min_ratings:
            valid_products.append(product)
    return valid_products

def display_results(valid_products):
    print("\n" + Fore.GREEN + "Best Product Options:\n" + Style.RESET_ALL)
    for product in valid_products:
        print(f"Product: {product.name}")
        print(f"Price: ${product.price}")
        print(f"Ratings: {product.ratings}")
        print(f"Reviews: {product.reviews}\n")

def main():
    colorama.init(autoreset=True)
    print("Welcome to E-Commerce Product Comparator!")

    item_name, price_range, min_ratings = get_user_input()
    products = search_products(item_name)
    valid_products = compare_products(products, price_range, min_ratings)
    display_results(valid_products)

if __name__ == "__main__":
    main()
