from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Enable logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Sample recipe data
recipes = [
    {
        "id": 1,
        "name": "Pasta Carbonara",
        "ingredients": ["pasta", "eggs", "parmesan cheese", "bacon", "black pepper"],
        "instructions": "Boil pasta. Mix eggs and cheese. Cook bacon. Combine everything."
    },
    {
        "id": 2,
        "name": "Chicken Salad",
        "ingredients": ["chicken breast", "lettuce", "tomato", "cucumber", "olive oil"],
        "instructions": "Grill chicken. Chop vegetables. Mix everything with olive oil."
    }
]


# Search recipes by name or ingredients
@app.route('/api/recipes', methods=['GET'])
def search_recipes():
    query = request.args.get('query', '').lower()
    result = []

    for recipe in recipes:
        # Search by name or ingredients
        if query in recipe['name'].lower() or any(query in ingredient.lower() for ingredient in recipe['ingredients']):
            result.append(recipe)

    if result:
        return jsonify(result), 200
    else:
        return jsonify({"message": "No recipes found matching your query."}), 404


# Get specific recipe by ID
@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return jsonify(recipe), 200
    return jsonify({"message": "Recipe not found."}), 404


# Add a new recipe
@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    logging.debug(f"Headers: {request.headers}")
    logging.debug(f"Data: {request.data}")

    if not request.is_json:
        return jsonify({"message": "Request body must be JSON"}), 400

    new_recipe = request.json
    if not new_recipe.get('name') or not new_recipe.get('ingredients') or not new_recipe.get('instructions'):
        return jsonify({"message": "Invalid data. Please provide name, ingredients, and instructions."}), 400

    new_id = max(recipe['id'] for recipe in recipes) + 1
    new_recipe['id'] = new_id
    recipes.append(new_recipe)

    return jsonify({"message": "Recipe added successfully!", "recipe": new_recipe}), 201


# Update an existing recipe
@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    logging.debug(f"Headers: {request.headers}")
    logging.debug(f"Data: {request.data}")
    logging.debug(f"Is JSON: {request.is_json}")

    if not request.is_json:
        return jsonify({"message": "Request body must be JSON"}), 400

    updated_data = request.json
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            recipe['name'] = updated_data.get('name', recipe['name'])
            recipe['ingredients'] = updated_data.get('ingredients', recipe['ingredients'])
            recipe['instructions'] = updated_data.get('instructions', recipe['instructions'])
            return jsonify({"message": "Recipe updated successfully!", "recipe": recipe}), 200
    return jsonify({"message": "Recipe not found."}), 404


# Delete a recipe by ID
@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            recipes.remove(recipe)
            return jsonify({"message": "Recipe deleted successfully!"}), 200
    return jsonify({"message": "Recipe not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
