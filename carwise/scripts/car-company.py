from apps.reminder.models import CarCompany, CarModel


def run():
    german_models = {
        "Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS"],
        "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "X7", "other"],
        "Opel": ["Corsa", "Astra", "Insignia", "Crossland X", "Grandland X"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Touareg", "Arteon", "other"],
    }

    italian_models = {
        "Ferrari": ["488 GTB", "812 Superfast", "SF90 Stradale", "Portofino"],
        "Fiat": ["500", "Panda", "Tipo", "500X", "500L"],
        "Lamborghini": ["Huracán", "Aventador", "Urus"],
        "Maserati": ["Ghibli", "Quattroporte", "Levante"],
    }

    french_models = {
        "Peugeot": [
            "405",
            "206",
            "207",
            "208",
            "308",
            "508",
            "2008",
            "3008",
            "5008",
            "other",
        ],
        "Renault": [
            "L90",
            "Sandro",
            "Clio",
            "Captur",
            "Mégane",
            "Scénic",
            "Kadjar",
            "Talisman",
        ],
        "Bugatti": ["Chiron", "Veyron"],
        "Citroën": ["C3", "C4", "C5", "Berlingo", "Cactus"],
    }

    japanese_models = {
        "Toyota": [
            "Yaris",
            "Corolla",
            "Camry",
            "RAV4",
            "Highlander",
            "Prius",
            "Land Cruiser",
            "other",
        ],
        "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Pilot", "Odyssey", "other"],
        "Nissan": [
            "Altima",
            "Maxima",
            "Sentra",
            "Rogue",
            "Murano",
            "Pathfinder",
            "other",
        ],
        "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "Crosstrek"],
        "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "other"],
        "Suzuki": ["Swift", "Jimny", "Vitara", "S-Cross", "Ignis", "other"],
    }

    korean_models = {
        "Hyundai": [
            "Elantra",
            "Sonata",
            "Santa Fe",
            "Tucson",
            "Kona",
            "Palisade",
            "other",
        ],
        "Kia": ["Rio", "Forte", "Optima", "Sportage", "Sorento", "Telluride", "other"],
        "Genesis": ["G70", "G80", "G90", "other"],
        "SsangYong": ["Tivoli", "Korando", "Rexton", "Musso", "other"],
    }

    persian_models = {
        "Saipa": ["Pride", "Tiba", "Saina", "Quick", "Shahin", "other"],
        "Irankhodro": ["Samand", "Dena", "Runna", "Peykan", "other"],
        "Parskhodro": ["Xantia", "Pickup", "H230", "other"],
    }

    chinese_models = {
        "Chery": ["Tiggo 5", "Tiggo 7", "Arrizo 5", "Arrizo 6", "Tiggo 8", "other"],
        "Lifan": ["X60", "X50", "820", "620", "520", "other"],
        "Great Wall Motors": ["Haval H2", "Haval H6", "Wingle 5", "Wingle 6", "other"],
        "Geely": ["Emgrand 7", "Emgrand X7", "GC6", "other"],
        "Foton": ["Tunland", "Aumark", "View CS2", "other"],
        "JAC": ["S3", "S5", "T6", "J4", "J5", "S7", "other"],
    }

    other_models = {"other": ["other"]}

    # Combine all car model dictionaries
    cars_list = []
    cars_list.extend(german_models.items())
    cars_list.extend(italian_models.items())
    cars_list.extend(french_models.items())
    cars_list.extend(japanese_models.items())
    cars_list.extend(korean_models.items())
    cars_list.extend(persian_models.items())
    cars_list.extend(chinese_models.items())
    cars_list.extend(other_models.items())

    # Iterate over each car company and its models
    for company, models in cars_list:
        # Get or create the car company
        company_object, created = CarCompany.objects.get_or_create(name=company)

        # Fetch all existing models for the car company
        existing_models = CarModel.objects.filter(car_company=company_object)
        existing_model_names = set(existing_models.values_list("name", flat=True))

        # Compare existing models with the new incoming models
        new_model_names = set(models)

        # Determine which models to delete and which to add
        models_to_delete = existing_model_names - new_model_names
        models_to_add = new_model_names - existing_model_names

        # Delete outdated models
        CarModel.objects.filter(car_company=company_object, name__in=models_to_delete).delete()

        # Add new models if they don’t exist
        for model in models_to_add:
            CarModel.objects.create(car_company=company_object, name=model)
