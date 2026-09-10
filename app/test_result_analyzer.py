from app.result_analyzer import ResultAnalyzer


analyzer = ResultAnalyzer()

data = [
    {
        "product_id": 1,
        "product_name": "Laptop",
        "price": 55000
    },
    {
        "product_id": 2,
        "product_name": "Headphones",
        "price": 2500
    }
]

result = analyzer.analyze(data)

print("Analysis:")
print(result)