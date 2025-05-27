# generate_sample_data.py
from recipe_manager import RecipeManager
from models import Recipe

def generate_sample_recipes():
    """🎨 Generate beautiful sample recipes for demo"""
    
    sample_recipes = [
        Recipe(
            name="Classic Margherita Pizza",
            ingredients=[
                "500g pizza dough",
                "200ml tomato sauce",
                "250g fresh mozzarella",
                "Fresh basil leaves",
                "2 tbsp olive oil",
                "Salt and pepper to taste"
            ],
            instructions=[
                "Preheat oven to 250°C (480°F)",
                "Roll out pizza dough on floured surface",
                "Spread tomato sauce evenly",
                "Add torn mozzarella pieces",
                "Drizzle with olive oil",
                "Bake for 10-12 minutes until golden",
                "Garnish with fresh basil before serving"
            ],
            metadata={
                "prep_time": "20 minutes",
                "cook_time": "12 minutes",
                "servings": 4,
                "difficulty": "medium",
                "cuisine": "Italian",
                "tags": ["vegetarian", "classic", "comfort food"]
            }
        ),
        
        Recipe(
            name="Chicken Tikka Masala",
            ingredients=[
                "800g chicken breast, cubed",
                "200ml Greek yogurt",
                "2 tbsp tikka masala paste",
                "400ml coconut milk",
                "400g canned tomatoes",
                "1 large onion, diced",
                "3 cloves garlic, minced",
                "2cm fresh ginger, grated",
                "2 tsp garam masala",
                "1 tsp turmeric",
                "Fresh cilantro",
                "Basmati rice for serving"
            ],
            instructions=[
                "Marinate chicken in yogurt and tikka paste for 2 hours",
                "Heat oil in large pan, cook chicken until golden",
                "Remove chicken, sauté onions until soft",
                "Add garlic, ginger, and spices, cook 1 minute",
                "Add tomatoes, simmer 10 minutes",
                "Stir in coconut milk and cooked chicken",
                "Simmer 15 minutes until sauce thickens",
                "Garnish with cilantro, serve with rice"
            ],
            metadata={
                "prep_time": "30 minutes + 2h marinating",
                "cook_time": "35 minutes",
                "servings": 6,
                "difficulty": "medium",
                "cuisine": "Indian",
                "tags": ["spicy", "creamy", "protein-rich"]
            }
        ),
        
        Recipe(
            name="Chocolate Lava Cake",
            ingredients=[
                "200g dark chocolate",
                "200g butter",
                "4 large eggs",
                "4 egg yolks",
                "100g caster sugar",
                "60g plain flour",
                "Butter for ramekins",
                "Cocoa powder for dusting",
                "Vanilla ice cream for serving"
            ],
            instructions=[
                "Preheat oven to 200°C (400°F)",
                "Butter 6 ramekins and dust with cocoa",
                "Melt chocolate and butter in double boiler",
                "Whisk whole eggs, yolks, and sugar until thick",
                "Fold in chocolate mixture and flour",
                "Fill ramekins 3/4 full",
                "Bake 10-12 minutes until edges are firm",
                "Let cool 2 minutes, turn out onto plates",
                "Serve immediately with ice cream"
            ],
            metadata={
                "prep_time": "25 minutes",
                "cook_time": "12 minutes",
                "servings": 6,
                "difficulty": "medium",
                "cuisine": "French",
                "tags": ["dessert", "chocolate", "impressive"]
            }
        ),
        
        Recipe(
            name="Thai Green Curry",
            ingredients=[
                "500g chicken thigh, sliced",
                "400ml coconut milk",
                "3 tbsp green curry paste",
                "200g Thai eggplant",
                "100g green beans",
                "2 kaffir lime leaves",
                "Thai basil leaves",
                "2 tbsp fish sauce",
                "1 tbsp palm sugar",
                "1 red chili, sliced",
                "Jasmine rice for serving"
            ],
            instructions=[
                "Heat thick coconut cream in wok",
                "Fry curry paste until fragrant",
                "Add chicken, cook until nearly done",
                "Add remaining coconut milk",
                "Add eggplant and green beans",
                "Season with fish sauce and sugar",
                "Add lime leaves and basil",
                "Simmer until vegetables are tender",
                "Garnish with chili and serve with rice"
            ],
            metadata={
                "prep_time": "20 minutes",
                "cook_time": "25 minutes",
                "servings": 4,
                "difficulty": "medium",
                "cuisine": "Thai",
                "tags": ["spicy", "coconut", "aromatic"]
            }
        ),
        
        Recipe(
            name="Classic Caesar Salad",
            ingredients=[
                "2 large romaine lettuce heads",
                "100g parmesan cheese, grated",
                "4 slices day-old bread",
                "4 anchovy fillets",
                "2 cloves garlic, minced",
                "1 egg yolk",
                "2 tbsp lemon juice",
                "1 tsp Dijon mustard",
                "100ml olive oil",
                "Salt and black pepper"
            ],
            instructions=[
                "Cut bread into cubes, toss with oil",
                "Bake croutons at 180°C until golden",
                "Mash anchovies and garlic into paste",
                "Whisk egg yolk, lemon juice, mustard",
                "Slowly add oil while whisking",
                "Mix in anchovy paste",
                "Tear lettuce into bite-sized pieces",
                "Toss with dressing and parmesan",
                "Top with croutons and extra cheese"
            ],
            metadata={
                "prep_time": "20 minutes",
                "cook_time": "10 minutes",
                "servings": 4,
                "difficulty": "easy",
                "cuisine": "American",
                "tags": ["salad", "classic", "healthy"]
            }
        ),
        
        Recipe(
            name="Beef Tacos",
            ingredients=[
                "500g ground beef",
                "8 small corn tortillas",
                "1 onion, diced",
                "2 cloves garlic, minced",
                "2 tsp chili powder",
                "1 tsp cumin",
                "1 tsp paprika",
                "200g cheddar cheese, shredded",
                "2 tomatoes, diced",
                "1 avocado, sliced",
                "Sour cream",
                "Fresh cilantro",
                "Lime wedges"
            ],
            instructions=[
                "Heat oil in large skillet",
                "Cook onion until soft",
                "Add garlic, cook 1 minute",
                "Add ground beef, cook until browned",
                "Season with spices, cook 2 minutes",
                "Warm tortillas in dry pan",
                "Fill tortillas with beef mixture",
                "Top with cheese, tomatoes, avocado",
                "Serve with sour cream and cilantro"
            ],
            metadata={
                "prep_time": "15 minutes",
                "cook_time": "15 minutes",
                "servings": 4,
                "difficulty": "easy",
                "cuisine": "Mexican",
                "tags": ["quick", "family-friendly", "customizable"]
            }
        ),
        
        Recipe(
            name="Japanese Ramen",
            ingredients=[
                "400g fresh ramen noodles",
                "1.5L chicken stock",
                "200ml soy sauce",
                "2 tbsp miso paste",
                "4 soft-boiled eggs",
                "200g pork belly, sliced",
                "2 green onions, sliced",
                "100g bamboo shoots",
                "2 sheets nori seaweed",
                "1 tbsp sesame oil",
                "2 cloves garlic, minced",
                "1 tsp ginger, grated"
            ],
            instructions=[
                "Prepare soft-boiled eggs, peel when cool",
                "Heat oil, cook pork belly until crispy",
                "Sauté garlic and ginger",
                "Add stock, soy sauce, and miso",
                "Simmer broth 20 minutes",
                "Cook noodles according to package",
                "Divide noodles between bowls",
                "Pour hot broth over noodles",
                "Top with eggs, pork, vegetables, nori"
            ],
            metadata={
                "prep_time": "40 minutes",
                "cook_time": "30 minutes",
                "servings": 4,
                "difficulty": "hard",
                "cuisine": "Japanese",
                "tags": ["comfort food", "umami", "warming"]
            }
        ),
        
        Recipe(
            name="Greek Salad",
            ingredients=[
                "4 large tomatoes, chunked",
                "1 cucumber, sliced",
                "1 red onion, thinly sliced",
                "200g feta cheese, cubed",
                "100g Kalamata olives",
                "3 tbsp olive oil",
                "2 tbsp red wine vinegar",
                "1 tsp dried oregano",
                "Salt and pepper",
                "Fresh herbs for garnish"
            ],
            instructions=[
                "Cut tomatoes into large chunks",
                "Slice cucumber and red onion",
                "Combine vegetables in large bowl",
                "Add feta cheese and olives",
                "Whisk oil, vinegar, and oregano",
                "Pour dressing over salad",
                "Season with salt and pepper",
                "Toss gently to combine",
                "Let sit 10 minutes before serving"
            ],
            metadata={
                "prep_time": "15 minutes",
                "cook_time": "0 minutes",
                "servings": 6,
                "difficulty": "easy",
                "cuisine": "Greek",
                "tags": ["healthy", "vegetarian", "fresh", "no-cook"]
            }
        )
    ]
    
    return sample_recipes

def populate_database():
    """🚀 Populate database with sample recipes"""
    print("🎨 Generating sample recipe data...")
    
    manager = RecipeManager()
    sample_recipes = generate_sample_recipes()
    
    added_count = 0
    
    for recipe in sample_recipes:
        try:
            recipe_id = manager.add_recipe(recipe)
            added_count += 1
            print(f"✅ Added: {recipe.name}")
        except ValueError as e:
            print(f"⚠️ Skipped {recipe.name}: {e}")
        except Exception as e:
            print(f"❌ Error adding {recipe.name}: {e}")
    
    print(f"\n🎉 Successfully added {added_count} recipes!")
    print("🚀 Ready to launch Flask app!")

if __name__ == "__main__":
    populate_database()