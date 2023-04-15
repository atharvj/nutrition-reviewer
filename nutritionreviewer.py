# Nutrition Reviewer

import requests as rq

# Initializing variables and lists
total_carbs = 0
total_protein = 0
total_fat = 0
total_amount = 0
bad_amount = []
carb_amounts_for_food = []
protein_amounts_for_food = []
fat_amounts_for_food = []


def main():
    # Input foods
    meal = input(
        """Input the name of the foods you are going to eat in your next meal below (separated by commas) 
Example: cheese pizza, caesar salad
--> """
    ).split(", ")

    ingredients = []

    # Input ingredients for each food
    for food in meal:
        ingredients.append(
            input(
                f"Please enter the ingredients it takes to make {food} (separated by commas): "
            ).split(", ")
        )

    score = 3

    # Using function on all lists of ingredients
    for i in range(len(meal)):
        add_nutrient_info(meal[i], ingredients[i])

    # Finding score
    if total_carbs == 0:
        score -= 1
        bad_amount.append("carbohydrates")
    elif ((total_carbs / total_amount) < 0.45) or ((total_carbs / total_amount) > 0.65):
        score -= 1
        bad_amount.append("carbohydrates")

    if total_protein == 0:
        score -= 1
        bad_amount.append("protein")
    elif ((total_protein / total_amount) < 0.10) or (
        (total_protein / total_amount) > 0.35
    ):
        score -= 1
        bad_amount.append("protein")

    if total_fat == 0:
        score -= 1
        bad_amount.append("fat")
    elif ((total_fat / total_amount) < 0.20) or ((total_fat / total_amount) > 0.35):
        score -= 1
        bad_amount.append("fat")

    # Finding which food was the best source of each macronutrient
    carb_foods = [x[0] for x in carb_amounts_for_food]
    carb_amounts = [x[1] for x in carb_amounts_for_food]

    protein_foods = [x[0] for x in protein_amounts_for_food]
    protein_amounts = [x[1] for x in protein_amounts_for_food]

    fat_foods = [x[0] for x in fat_amounts_for_food]
    fat_amounts = [x[1] for x in fat_amounts_for_food]

    best_carb = carb_foods[carb_amounts.index(max(carb_amounts))]
    best_protein = protein_foods[protein_amounts.index(max(protein_amounts))]
    best_fat = fat_foods[fat_amounts.index(max(fat_amounts))]

    # Using score to find nutritional value (output)
    match score:
        case 3:
            print(
                f"This meal is very nutritious: {best_carb} is a good source of carbohydrates, {best_protein} is a good source of protein, and {best_fat} is a good source of fat."
            )
        case 2:
            print(
                f"This meal is somewhat nutritious. It either has an excess or deficiency of {bad_amount[0]}."
            )
        case 1:
            print(
                f"This meal is not nutritious. It either has an excess or deficiency of {bad_amount[0]} and {bad_amount[1]}."
            )
        case 0:
            print(
                f"This meal is not nutritious. It either has an excess or deficiency of {bad_amount[0]}, {bad_amount[1]}, and {bad_amount[2]}."
            )


def add_nutrient_info(food, ingredients):
    global total_carbs
    global total_protein
    global total_fat
    global total_amount

    carb_amt = 0
    protein_amt = 0
    fat_amt = 0

    for ingredient in ingredients:
        options = {
            "app_id": "b26c6684",
            "app_key": "e09078d99f6cde8bcdf44ade32178966",
            "ingr": ingredient,
        }
        req = rq.get("https://api.edamam.com/api/nutrition-data", options).json()

        # Running algorithm if nutrient information is available
        if all(
            nutrient in req["totalNutrients"]
            for nutrient in ["FAT", "CHOCDF", "PROCNT"]
        ):
            fat = req["totalNutrients"]["FAT"]["quantity"]
            carbs = req["totalNutrients"]["CHOCDF"]["quantity"]
            protein = req["totalNutrients"]["PROCNT"]["quantity"]

            total_fat += fat
            fat_amt += fat

            total_carbs += carbs
            carb_amt += carbs

            total_protein += protein
            protein_amt += protein

            total_amount = total_carbs + total_protein + total_fat
        else:
            print(
                "Error: Nutrient information not available for one or more ingredients."
            )
            run_again()

    carb_amounts_for_food.append([food, carb_amt])
    protein_amounts_for_food.append([food, protein_amt])
    fat_amounts_for_food.append([food, fat_amt])


def run_again():
    choice = input("Do you want to try again? (y/n): ")
    if choice == "y":
        main()
    else:
        quit()


main()
