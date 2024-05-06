from apps.reminder.models import CarCompany, CarModel
    
def run():

    german_models = {
        "Banz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS"],
        "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "X7"],
        "Opel": ["Corsa", "Astra", "Insignia", "Crossland X", "Grandland X"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Touareg", "Arteon"]
    }

    italian_models = {
        "Ferrari": ["488 GTB", "812 Superfast", "SF90 Stradale", "Portofino"],
        "Fiat": ["500", "Panda", "Tipo", "500X", "500L"],
        "Lamborghini": ["Huracán", "Aventador", "Urus"],
        "Maserati": ["Ghibli", "Quattroporte", "Levante"]
    }

    french_models = {
        "Peugeot": ["208", "308", "508", "2008", "3008", "5008"],
        "Renault": ["Clio", "Captur", "Mégane", "Scénic", "Kadjar", "Talisman"],
        "Bugatti": ["Chiron", "Veyron"],
        "Citroën": ["C3", "C4", "C5", "Berlingo", "Cactus"]
    }

    japanese_models = {
        "Toyota": ["Corolla", "Camry", "RAV4", "Highlander", "Prius", "Land Cruiser"],
        "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Pilot", "Odyssey"],
        "Nissan": ["Altima", "Maxima", "Sentra", "Rogue", "Murano", "Pathfinder"],
        "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "Crosstrek"],
        "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9"],
        "Suzuki": ["Swift", "Jimny", "Vitara", "S-Cross", "Ignis"]
    }

    korean_models = {
        "Hyundai": ["Elantra", "Sonata", "Santa Fe", "Tucson", "Kona", "Palisade"],
        "Kia": ["Rio", "Forte", "Optima", "Sportage", "Sorento", "Telluride"],
        "Genesis": ["G70", "G80", "G90"],
        "SsangYong": ["Tivoli", "Korando", "Rexton", "Musso"]
    }

    persian_models = {
        "Saipa": ["Pride", "Tiba", "Saina", "Quick"],
        "Irankhodro": ["Samand", "Dena", "Runna", "Peykan"],
        "Parskhodro": ["Xantia", "Pickup", "H230"]
    }

    cars_list = []
    cars_list.extend(german_models.items())
    cars_list.extend(italian_models.items())
    cars_list.extend(french_models.items())
    cars_list.extend(japanese_models.items())
    cars_list.extend(korean_models.items())
    cars_list.extend(persian_models.items())

    for car in cars_list:
        company = car[0]
        models = car[1]
        company_object,_= CarCompany.objects.get_or_create( name=company) 
        for model in models:
            CarModel.objects.get_or_create(car_company=company_object, name =model) 
    
        