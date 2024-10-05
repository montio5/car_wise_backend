from apps.reminder.models import CarCompany, CarModel


def run():
    # Car models data categorized by country of origin
    german_models = {
        "Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "GLS"],
        "BMW": ["3 Series", "5 Series", "7 Series", "X3", "X5", "X7", "other"],
        "Opel": ["Corsa", "Astra", "Insignia", "Crossland X", "Grandland X"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Touareg", "Arteon", "other"],
    }

    # Additional countries
    italian_models = {...}  # Skipping repetition for brevity
    french_models = {...}
    japanese_models = {...}
    korean_models = {...}
    persian_models = {...}
    chinese_models = {...}
    other_models = {"other": ["other"]}

    # Combine all car model dictionaries into a single list
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
        CarModel.objects.filter(
            car_company=company_object, name__in=models_to_delete
        ).delete()

        # Add new models if they don’t exist
        for model in models_to_add:
            CarModel.objects.create(car_company=company_object, name=model)
