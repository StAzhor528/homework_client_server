import json
from chardet import detect


def write_order_to_json(item, quantity, price, buyer, date):
    data = {'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
            }

    with open('orders.json', 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']

    with open('orders.json', encoding=encoding) as f:
        orders = json.load(f)
    orders['orders'].append(data)

    with open('orders.json', 'w', encoding='utf-8') as f:
        dict_as_str = json.dumps(orders, indent=4, ensure_ascii=False)
        f.write(dict_as_str)


write_order_to_json('Стол', '1', '200', 'Иванов И.И.', '02.02.2023')
write_order_to_json('Стул', '10', '100', 'Петров П.П.', '03.04.2023')
write_order_to_json('Диван', '2', '2000', 'Сидоров С.С.', '03.27.2023')
write_order_to_json('Кресло', '4', '500', 'Смирнов С.С.', '04.10.2023')

with open('orders.json', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']

with open('orders.json', encoding=encoding) as f:
    OBJ = f.read()
print(OBJ)
