from tabulate import tabulate

class TourCalculator:
    def __init__(self):
        self.costs = [{'cost': 0, 'excursions': ''}]
        self.results = []

    def calculate_cost(self, excursions):
        for day, excursion in enumerate(excursions):
            if excursion['tag'] == 'AND':
                self.add_and_cost(excursion['prices'], excursion['name'], day)
            elif excursion['tag'] == 'OR':
                self.add_or_cost(excursion['prices'], excursion['name'], day)

    def add_and_cost(self, prices, name, day):
        for i, cost in enumerate(self.costs):
            new_cost = cost['cost'] + sum(prices)
            new_excursions = cost['excursions'] + (', ' if cost['excursions'] else '') + name
            self.costs[i] = {'cost': new_cost, 'excursions': new_excursions}
            self.results.append([day, name, 'AND', cost['cost'], new_cost, new_excursions])

    def add_or_cost(self, prices, name, day):
        new_costs = []
        for i, cost in enumerate(self.costs):
            for j, price in enumerate(prices):
                new_cost = cost['cost'] + price
                new_excursions = cost['excursions'] + (', ' if cost['excursions'] else '') + f"{name}.{j+1}"
                new_costs.append({'cost': new_cost, 'excursions': new_excursions})
                self.results.append([day, f"{name}.{j+1}", 'OR', cost['cost'], new_cost, new_excursions])
        self.costs = new_costs

    def get_costs(self):
        return self.costs

    def print_results(self):
        headers = ['Day', 'Excursion', 'Tag', 'Previous Cost', 'New Cost', 'Excursions']
        print(tabulate(self.results, headers, tablefmt='orgtbl'))

    def print_final_costs(self):
        headers = ['Cost', 'Excursions']
        print(tabulate([[cost['cost'], cost['excursions']] for cost in self.costs], headers, tablefmt='orgtbl'))

    def print_last_day_results(self, excursions):
        last_day = len(excursions) - 1
        last_day_results = [result for result in self.results if result[0] == last_day]
        excursions_set = set(result[1] for result in last_day_results)
        headers = ['Excursions'] + [excursion for excursion in excursions_set]
        table = []
        for result in last_day_results:
            row = [result[5]]
            for excursion in excursions_set:
                if excursion in result[1]:
                    row.append(result[4])
                else:
                    row.append('-')
            table.append(row)
        print(tabulate(table, headers, tablefmt='orgtbl'))

# Example usage:
excursions = [ 
    {"name":"Tour","tag": "AND", "prices": [630]},
    {"name":"Day 1","tag": "AND", "prices": [0]},
    {"name":"Day 1 Supper","tag": "AND", "prices": [45]},
    {"name":"Day 2 Lunch","tag": "AND", "prices": [20]},
    {"name":"Day 2","tag": "AND", "prices": [0]},
    {"name":"Day 3","tag": "OR", "prices": [17, 14, 14]},
    {"name":"Day 4","tag": "OR", "prices": [65, 75, 27]},
    {"name":"Day 5","tag": "OR", "prices": [27,0]},
    {"name":"Day 6","tag": "OR", "prices": [120,0]},
    {"name":"Day 7","tag": "AND", "prices": [60]},
    {"name":"Day 7 Supper","tag": "AND", "prices": [43]},
    {"name":"Day 8 Lunch","tag": "AND", "prices": [19]},
    {"name":"Excursion","tag": "OR", "prices": [15,0]},
    {"name":"Visa","tag": "AND", "prices": [165]},
    {"name":"Visa Support","tag": "AND", "prices": [30]},
    {"name":"Tour service","tag": "AND", "prices": [45]},
    {"name":"Select place in bus","tag": "AND", "prices": [10]}
]

    # ✗ Визовая поддержка 100 рублей;
    # ✗ Консульский сбор 90 евро (для граждан РБ) + 75 евро сервисный сбор визового центра;
    # ✗ Туристическая услуга 150 рублей;
    # ✗ Медицинская страховка;
    # ✗ Выбор места в автобусе 10 евро (по желанию);
    # ✗ Наушники для экскурсий – 3 евро/экскурсионный день;
    # ✗ Ужины на пароме – взрослые 43/ дети 19 евро (по желанию);
    # ✗ Дополнительные экскурсии по программе (по желанию). -Народный музей Осло Взрослые 20 у.е. Дети до 17 лет б.п. -Круизx на кораблике (~2 ч.) по Люсефьорду + подъем на «Кафедру проповедника» Взрослые 90 у.е. Дети до 16 лет 80 у.е. -Фуникулер на обзорную площадку горы Флейен взрослые, от 20 у.е. дети до 15 лет 10 у.е. -Круиз на кораблике по Неройфьорду (~2 ч.) Взрослые 49 у.е. Дети до 16 лет 40 у.е. -Железная дорога Флом Взрослые 71 у.е. Дети до 16 лет 41 у.е. -Экскурсия в Ратушу Стокгольма Взрослый 25 у.е. Дети до 17 лет 19 у.е. -Музей корабля «Васа» Взрослые 25 у.е. Дети до 18 лет б.п.
    # ✗ Завтрак на пароме: взрослые 19/ дети 12 евро (по желанию);
    # ✗ Доплата за размещение в 2-х местной каюте - 75 евро с человека.

calculator = TourCalculator()
calculator.calculate_cost(excursions)
calculator.print_last_day_results(excursions)