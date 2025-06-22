from flask import Flask, render_template, request
from typing import Dict, Union, List

# --- Create the Flask App ---
app = Flask(__name__)

# --- Paste the Core Logic and Data from the previous step ---

# Fertilizer recipes (grams per 1000 Liters)
FERTILIZER_RECIPES: Dict[str, Dict[str, Dict[str, float]]] = {
    "seedling": {
        "Tank A": {"Calcium Nitrate": 600.0, "Potassium Nitrate": 250.0},
        "Tank B": {"Mono Ammonium Phosphate (MAP)": 200.0, "Potassium Sulphate": 250.0, "Magnesium Sulphate": 300.0}
    },
    "vegetative": {
        "Tank A": {"Calcium Nitrate": 800.0, "Potassium Nitrate": 400.0},
        "Tank B": {"Mono Ammonium Phosphate (MAP)": 150.0, "Potassium Sulphate": 500.0, "Magnesium Sulphate": 400.0}
    },
    "flowering": {
        "Tank A": {"Calcium Nitrate": 900.0, "Potassium Nitrate": 500.0},
        "Tank B": {"Mono Ammonium Phosphate (MAP)": 200.0, "Potassium Sulphate": 600.0, "Magnesium Sulphate": 450.0}
    },
    "fruiting": {
        "Tank A": {"Calcium Nitrate": 800.0, "Potassium Nitrate": 600.0},
        "Tank B": {"Mono Ammonium Phosphate (MAP)": 150.0, "Potassium Sulphate": 700.0, "Magnesium Sulphate": 450.0}
    }
}

def calculate_capsicum_fertigation(growth_stage: str, tank_volume_liters: float) -> Union[Dict, str]:
    """Calculates fertigation recipes. (Docstring omitted for brevity in this file)"""
    normalized_stage = growth_stage.lower()
    if normalized_stage not in FERTILIZER_RECIPES:
        valid_stages: List[str] = list(FERTILIZER_RECIPES.keys())
        return f"Error: Invalid growth_stage '{growth_stage}'. Please use one of: {', '.join(valid_stages)}."
    
    base_recipe = FERTILIZER_RECIPES[normalized_stage]
    scaling_factor = tank_volume_liters / 1000.0
    calculated_recipe: Dict[str, Dict[str, float]] = {"Tank A": {}, "Tank B": {}}

    for tank, fertilizers in base_recipe.items():
        for name, base_amount in fertilizers.items():
            scaled_amount = base_amount * scaling_factor
            calculated_recipe[tank][name] = round(scaled_amount, 2)
    return calculated_recipe

# --- Web Application Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handles both displaying the form (GET) and processing the calculation (POST).
    """
    # These will hold the results and user inputs to re-display them
    result = None
    user_input = {'stage': 'seedling', 'volume': 1000} 

    if request.method == 'POST':
        # Get data from the submitted form
        stage = request.form.get('growth_stage')
        volume_str = request.form.get('tank_volume')
        
        user_input = {'stage': stage, 'volume': volume_str}

        try:
            # Validate and convert the volume to a float
            volume = float(volume_str)
            if volume <= 0:
                result = "Error: Tank volume must be a positive number."
            else:
                # Call our expert function to get the recipe
                result = calculate_capsicum_fertigation(stage, volume)
        except (ValueError, TypeError):
            result = "Error: Please enter a valid number for the tank volume."
            
    # Render the HTML page, passing the result and user inputs to it
    return render_template('index.html', result=result, user_input=user_input)

# --- Run the App ---
if __name__ == '__main__':
    # Setting debug=True allows for auto-reloading when you save the file
    app.run(debug=True)