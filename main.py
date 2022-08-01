# import modules
import pandas as pd
import requests

# Data dictionary making global
global data_dict

# condition to break while loop
condition = True

# while loop to check different pages with reviews.
while condition:

    # data dictionary to store extracted data
    data_dict = {"Id": [],
                 "Name": [],
                 "Date": [],
                 "Title": [],
                 "Rating": [],
                 "Review": [],
                 }

    # URL
    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"

    # ASIN of Amazon Product, you can change it here
    asin = ["B09WTQR3LT"]
    #  Product_ID 1 ASIN B091HQNRRD
    #  PRODUCT_ID 2 was B09WTQR3LT
    # PRODUCT_ID 3 was B09MHP42DS
    # PRODUCT_ID 4 was B089JY8M8Y
    # PRODUCT_ID 5 was B087M8BWL6

    # For Range loop to change the page in querystring
    for page in range(1, 50):
        if not condition:
            break
        querystring = {"asin": asin, "country": "GB", "variants": "1", "top": "0", "page": str(page)}

        headers = {"X-RapidAPI-Key": "f10e7173c1msh3c4a3080b1bf02dp1702cbjsnf7bf41d788c5",
                   "X-RapidAPI-Host": "amazon-product-reviews-keywords.p.rapidapi.com"
                   }

        response = requests.request("GET", url, headers=headers, params=querystring)
        # need = product reviews columns like data, name, title, star, review.
        data = (response.json())

        # Checking data of reviews with if statement.
        if len(data["reviews"]) == 0:
            print("API endpoint have no such data to show")
            condition = False

        # Extracting data from json

        for i in data["reviews"]:
            data_dict["Id"].append(i["id"])
            data_dict["Name"].append(i["name"])
            data_dict["Date"].append(i["date"]["date"])
            data_dict["Title"].append(i["title"])
            data_dict["Rating"].append(str(i["rating"]))
            data_dict["Review"].append(i["review"])

# Printing Data dictionary Extracted and stored
print(data_dict)

# Generating CSV file
df = pd.DataFrame.from_dict(data_dict, orient='index')
df = df.transpose()
df.to_csv(r'amazon_reviews.csv', index=False, header=True)
