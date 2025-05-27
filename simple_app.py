# simple_app.py - Complete Flask Recipe Management
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from recipe_manager import RecipeManager
from models import Recipe

class RecipeHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.manager = RecipeManager()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.serve_homepage()
        elif self.path == '/recipes':
            self.serve_recipes()
        elif self.path == '/favorites':
            self.serve_favorites()
        elif self.path.startswith('/filter/'):
            status = self.path.split('/')[-1]
            self.serve_filtered_recipes(status)
        elif self.path.startswith('/recipe/'):
            recipe_id = self.path.split('/')[-1]
            self.serve_recipe_detail(recipe_id)
        elif self.path == '/stats':
            self.serve_stats()

        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/add_recipe':
            self.add_recipe()
        elif self.path.startswith('/delete/'):
            recipe_id = self.path.split('/')[-1]
            self.delete_recipe(recipe_id)
        elif self.path.startswith('/toggle_favorite/'):
            recipe_id = self.path.split('/')[-1]
            self.toggle_favorite(recipe_id)
        elif self.path == '/update_status':
            self.update_status()
        elif self.path == '/search':
            self.handle_search()
        else:
            self.send_error(404)
    
    def serve_homepage(self):
        """🏠 Serve homepage with recipe form"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>🍳 Recipe Management System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; }
                .form-group { margin: 15px 0; }
                label { display: block; margin-bottom: 5px; font-weight: bold; color: #34495e; }
                input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; box-sizing: border-box; }
                textarea { height: 100px; resize: vertical; }
                button { background: #3498db; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 5px; }
                button:hover { background: #2980b9; }
                .btn-danger { background: #e74c3c; }
                .btn-danger:hover { background: #c0392b; }
                .btn-success { background: #27ae60; }
                .btn-success:hover { background: #229954; }
                .recipe-card { background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }
                .recipe-title { color: #2c3e50; margin-bottom: 10px; }
                .recipe-meta { color: #7f8c8d; font-size: 14px; }
                .nav { text-align: center; margin-bottom: 30px; }
                .nav a { margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }
                .nav a:hover { background: #ecf0f1; }
                .success { background: #d5edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0; }
                .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0; }
                .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .stat-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #3498db; }
                .checkbox-group { display: flex; align-items: center; margin: 10px 0; }
                .checkbox-group input[type="checkbox"] { width: auto; margin-right: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🍳 Recipe Management System</h1>
                
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/recipes">📋 All Recipes</a>
                    <a href="/favorites">❤️ Favorites</a>
                    <a href="/filter/want_to_try">🤔 Want to Try</a>
                    <a href="/filter/tried">👍 Tried</a>
                    <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                </div>
                
                <h2>➕ Add New Recipe</h2>
                <form method="post" action="/add_recipe">
                    <div class="form-group">
                        <label for="name">🍽️ Recipe Name:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="ingredients">🥘 Ingredients (one per line):</label>
                        <textarea id="ingredients" name="ingredients" placeholder="400g spaghetti&#10;200g pancetta&#10;4 large eggs" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="instructions">📋 Instructions (one per line):</label>
                        <textarea id="instructions" name="instructions" placeholder="Boil water and cook spaghetti&#10;Cook pancetta until crispy" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="cuisine">🌍 Cuisine:</label>
                        <select id="cuisine" name="cuisine">
                            <option value="">Select cuisine...</option>
                            <option value="Italian">Italian</option>
                            <option value="Chinese">Chinese</option>
                            <option value="Mexican">Mexican</option>
                            <option value="Indian">Indian</option>
                            <option value="French">French</option>
                            <option value="American">American</option>
                            <option value="Japanese">Japanese</option>
                            <option value="Thai">Thai</option>
                            <option value="Greek">Greek</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="difficulty">⭐ Difficulty:</label>
                        <select id="difficulty" name="difficulty">
                            <option value="easy">Easy</option>
                            <option value="medium" selected>Medium</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="servings">🍽️ Servings:</label>
                        <input type="number" id="servings" name="servings" min="1" max="20" value="4">
                    </div>
                    
                    <div class="form-group">
                        <label for="prep_time">⏱️ Prep Time:</label>
                        <input type="text" id="prep_time" name="prep_time" placeholder="e.g., 20 minutes">
                    </div>
                    
                    <div class="form-group">
                        <label for="cook_time">🔥 Cook Time:</label>
                        <input type="text" id="cook_time" name="cook_time" placeholder="e.g., 30 minutes">
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="is_favorite" name="is_favorite">
                        <label for="is_favorite">❤️ Mark as Favorite</label>
                    </div>
                    
                    <div class="form-group">
                        <label for="status">📝 Status:</label>
                        <select id="status" name="status">
                            <option value="want_to_try">🤔 Want to Try</option>
                            <option value="tried">👍 Tried Once</option>
                            <option value="made_before">⭐ Made Before</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn-success">✅ Add Recipe</button>
                </form>
                
                <hr style="margin: 40px 0;">
                
                <h2>🔍 Search Recipes</h2>
                <form method="post" action="/search">
                    <div class="form-group">
                        <label for="search_query">Search by name or ingredient:</label>
                        <input type="text" id="search_query" name="search_query" placeholder="e.g., pasta, chicken, chocolate">
                    </div>
                    <button type="submit">🔍 Search</button>
                </form>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_recipes(self):
        """📋 Serve all recipes page"""
        recipes = self.manager.get_all_recipes()
        
        recipe_cards = ""
        for recipe in recipes:
            favorite_icon = "❤️" if recipe.is_favorite else "🤍"
            status_emoji = recipe.get_status_emoji()
            status_text = recipe.get_status_text()
            
            recipe_cards += f"""
            <div class="recipe-card">
                <h3 class="recipe-title">{favorite_icon} {recipe.name} {status_emoji}</h3>
                <div class="recipe-meta">
                    🥘 {len(recipe.ingredients)} ingredients • 
                    📋 {len(recipe.instructions)} steps • 
                    🌍 {recipe.metadata.get('cuisine', 'N/A')} • 
                    ⭐ {recipe.metadata.get('difficulty', 'N/A')} •
                    📝 {status_text} •
                    🍽️ {recipe.metadata.get('servings', 'N/A')} servings
                </div>
                <button onclick="viewRecipe('{recipe._id}')">👁️ View Details</button>
                <button onclick="toggleFavorite('{recipe._id}')">{favorite_icon} Favorite</button>
                <select onchange="updateStatus('{recipe._id}', this.value)" style="padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #ddd;">
                    <option value="">Change Status...</option>
                    <option value="want_to_try" {'selected' if recipe.status == 'want_to_try' else ''}>🤔 Want to Try</option>
                    <option value="tried" {'selected' if recipe.status == 'tried' else ''}>👍 Tried Once</option>
                    <option value="made_before" {'selected' if recipe.status == 'made_before' else ''}>⭐ Made Before</option>
                </select>
                <button class="btn-danger" onclick="deleteRecipe('{recipe._id}')">🗑️ Delete</button>
            </div>
            """
        
        if not recipe_cards:
            recipe_cards = "<p>📭 No recipes found! <a href='/'>Add some recipes</a> to get started.</p>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>📋 All Recipes - Recipe Management</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .recipe-card {{ background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }}
                .recipe-title {{ color: #2c3e50; margin-bottom: 10px; }}
                .recipe-meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }}
                button {{ background: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin: 5px 5px 5px 0; }}
                button:hover {{ background: #2980b9; }}
                .btn-danger {{ background: #e74c3c; }}
                .btn-danger:hover {{ background: #c0392b; }}
                .nav {{ text-align: center; margin-bottom: 30px; }}
                .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                .nav a:hover {{ background: #ecf0f1; }}
            </style>
            <script>
                function viewRecipe(id) {{
                    window.location.href = '/recipe/' + id;
                }}
                function toggleFavorite(id) {{
                    fetch('/toggle_favorite/' + id, {{ method: 'POST' }})
                    .then(() => location.reload());
                }}
                function updateStatus(id) {{
                    var status = prompt("Choose new status:\\n\\n1. want_to_try (🤔 Want to Try)\\n2. tried (👍 Tried Once)\\n3. made_before (⭐ Made Before)\\n\\nEnter: want_to_try, tried, or made_before");
                    if (status && ['want_to_try', 'tried', 'made_before'].includes(status)) {{
                        fetch('/update_status', {{ 
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                            body: 'recipe_id=' + id + '&status=' + status
                        }}).then(() => location.reload());
                    }} else if (status) {{
                        alert('Invalid status! Please use: want_to_try, tried, or made_before');
                    }}
                }}
                function deleteRecipe(id) {{
                    if (confirm('Are you sure you want to delete this recipe?')) {{
                        fetch('/delete/' + id, {{ method: 'POST' }})
                        .then(() => location.reload());
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>📋 All Recipes ({len(recipes)})</h1>
                
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/recipes">📋 All Recipes</a>
                    <a href="/favorites">❤️ Favorites</a>
                    <a href="/filter/want_to_try">🤔 Want to Try</a>
                    <a href="/filter/tried">👍 Tried</a>
                    <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                </div>
                
                {recipe_cards}
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_favorites(self):
        """❤️ Serve favorite recipes page"""
        favorites = self.manager.get_favorite_recipes()
        
        recipe_cards = ""
        for recipe in favorites:
            status_emoji = recipe.get_status_emoji()
            status_text = recipe.get_status_text()
            
            recipe_cards += f"""
            <div class="recipe-card">
                <h3 class="recipe-title">❤️ {recipe.name} {status_emoji}</h3>
                <div class="recipe-meta">
                    🥘 {len(recipe.ingredients)} ingredients • 
                    📋 {len(recipe.instructions)} steps • 
                    🌍 {recipe.metadata.get('cuisine', 'N/A')} • 
                    ⭐ {recipe.metadata.get('difficulty', 'N/A')} •
                    📝 {status_text} •
                    🍽️ {recipe.metadata.get('servings', 'N/A')} servings
                </div>
                <button onclick="viewRecipe('{recipe._id}')">👁️ View Details</button>
                <button onclick="toggleFavorite('{recipe._id}')">💔 Remove Favorite</button>
                <select onchange="updateStatus('{recipe._id}', this.value)" style="padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #ddd;">
                    <option value="">Change Status...</option>
                    <option value="want_to_try" {'selected' if recipe.status == 'want_to_try' else ''}>🤔 Want to Try</option>
                    <option value="tried" {'selected' if recipe.status == 'tried' else ''}>👍 Tried Once</option>
                    <option value="made_before" {'selected' if recipe.status == 'made_before' else ''}>⭐ Made Before</option>
                </select>
            </div>
            """
        
        if not recipe_cards:
            recipe_cards = "<p>💔 No favorite recipes yet! <a href='/recipes'>Browse recipes</a> and mark some as favorites.</p>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>❤️ Favorite Recipes</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .recipe-card {{ background: #fff0f0; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #e74c3c; }}
                .recipe-title {{ color: #2c3e50; margin-bottom: 10px; }}
                .recipe-meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }}
                button {{ background: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin: 5px 5px 5px 0; }}
                button:hover {{ background: #2980b9; }}
                .nav {{ text-align: center; margin-bottom: 30px; }}
                .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                .nav a:hover {{ background: #ecf0f1; }}
            </style>
            <script>
                function viewRecipe(id) {{ window.location.href = '/recipe/' + id; }}
                function toggleFavorite(id) {{
                    fetch('/toggle_favorite/' + id, {{ method: 'POST' }})
                    .then(() => location.reload());
                }}
                function updateStatus(id) {{
                    var status = prompt("Choose new status:\\n\\n1. want_to_try (🤔 Want to Try)\\n2. tried (👍 Tried Once)\\n3. made_before (⭐ Made Before)\\n\\nEnter: want_to_try, tried, or made_before");
                    if (status && ['want_to_try', 'tried', 'made_before'].includes(status)) {{
                        fetch('/update_status', {{ 
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                            body: 'recipe_id=' + id + '&status=' + status
                        }}).then(() => location.reload());
                    }} else if (status) {{
                        alert('Invalid status! Please use: want_to_try, tried, or made_before');
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>❤️ Favorite Recipes ({len(favorites)})</h1>
                
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/recipes">📋 All Recipes</a>
                    <a href="/favorites">❤️ Favorites</a>
                    <a href="/filter/want_to_try">🤔 Want to Try</a>
                    <a href="/filter/tried">👍 Tried</a>
                    <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                </div>
                
                {recipe_cards}
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_filtered_recipes(self, status):
        """📊 Serve recipes filtered by status"""
        recipes = self.manager.get_recipes_by_status(status)
        
        status_info = {
            'want_to_try': ('🤔', 'Want to Try'),
            'tried': ('👍', 'Tried Once'), 
            'made_before': ('⭐', 'Made Before')
        }
        
        emoji, title = status_info.get(status, ('📋', 'Recipes'))
        
        recipe_cards = ""
        for recipe in recipes:
            favorite_icon = "❤️" if recipe.is_favorite else "🤍"
            
            recipe_cards += f"""
            <div class="recipe-card">
                <h3 class="recipe-title">{favorite_icon} {recipe.name} {emoji}</h3>
                <div class="recipe-meta">
                    🥘 {len(recipe.ingredients)} ingredients • 
                    📋 {len(recipe.instructions)} steps • 
                    🌍 {recipe.metadata.get('cuisine', 'N/A')} • 
                    ⭐ {recipe.metadata.get('difficulty', 'N/A')} •
                    🍽️ {recipe.metadata.get('servings', 'N/A')} servings
                </div>
                <button onclick="viewRecipe('{recipe._id}')">👁️ View Details</button>
                <button onclick="toggleFavorite('{recipe._id}')">{favorite_icon} Favorite</button>
                <select onchange="updateStatus('{recipe._id}', this.value)" style="padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #ddd;">
                    <option value="">Change Status...</option>
                    <option value="want_to_try" {'selected' if recipe.status == 'want_to_try' else ''}>🤔 Want to Try</option>
                    <option value="tried" {'selected' if recipe.status == 'tried' else ''}>👍 Tried Once</option>
                    <option value="made_before" {'selected' if recipe.status == 'made_before' else ''}>⭐ Made Before</option>
                </select>
            </div>
            """
        
        if not recipe_cards:
            recipe_cards = f"<p>📭 No recipes with status '{title}' yet!</p>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{emoji} {title} Recipes</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .recipe-card {{ background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }}
                .recipe-title {{ color: #2c3e50; margin-bottom: 10px; }}
                .recipe-meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }}
                button {{ background: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin: 5px 5px 5px 0; }}
                button:hover {{ background: #2980b9; }}
                .nav {{ text-align: center; margin-bottom: 30px; }}
                .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                .nav a:hover {{ background: #ecf0f1; }}
            </style>
            <script>
                function viewRecipe(id) {{ window.location.href = '/recipe/' + id; }}
                function toggleFavorite(id) {{
                    fetch('/toggle_favorite/' + id, {{ method: 'POST' }})
                    .then(() => location.reload());
                }}
                function updateStatus(id) {{
                    var status = prompt("Choose new status:\\n\\n1. want_to_try (🤔 Want to Try)\\n2. tried (👍 Tried Once)\\n3. made_before (⭐ Made Before)\\n\\nEnter: want_to_try, tried, or made_before");
                    if (status && ['want_to_try', 'tried', 'made_before'].includes(status)) {{
                        fetch('/update_status', {{ 
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                            body: 'recipe_id=' + id + '&status=' + status
                        }}).then(() => location.reload());
                    }} else if (status) {{
                        alert('Invalid status! Please use: want_to_try, tried, or made_before');
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <h1>{emoji} {title} Recipes ({len(recipes)})</h1>
                
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/recipes">📋 All Recipes</a>
                    <a href="/favorites">❤️ Favorites</a>
                    <a href="/filter/want_to_try">🤔 Want to Try</a>
                    <a href="/filter/tried">👍 Tried</a>
                    <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                </div>
                
                {recipe_cards}
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_recipe_detail(self, recipe_id):
        """👁️ Serve recipe detail page"""
        recipe = self.manager.get_recipe_by_id(recipe_id)
        
        if not recipe:
            self.send_error(404, "Recipe not found")
            return
        
        # Format ingredients
        ingredients_html = ""
        for i, ingredient in enumerate(recipe.ingredients, 1):
            ingredients_html += f"<li>{ingredient}</li>"
        
        # Format instructions
        instructions_html = ""
        for i, instruction in enumerate(recipe.instructions, 1):
            instructions_html += f"<li><strong>Step {i}:</strong> {instruction}</li>"
        
        favorite_icon = "❤️" if recipe.is_favorite else "🤍"
        status_emoji = recipe.get_status_emoji()
        status_text = recipe.get_status_text()
        total_time = recipe.get_total_time()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🍽️ {recipe.name} - Recipe Details</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; }}
                .meta-info {{ background: #ecf0f1; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                .meta-item {{ display: inline-block; margin: 5px 15px 5px 0; color: #34495e; }}
                ul, ol {{ line-height: 1.6; }}
                li {{ margin: 8px 0; }}
                .nav {{ text-align: center; margin-bottom: 30px; }}
                .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                .nav a:hover {{ background: #ecf0f1; }}
                button {{ background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }}
                button:hover {{ background: #2980b9; }}
                .btn-danger {{ background: #e74c3c; }}
                .btn-danger:hover {{ background: #c0392b; }}
                .action-buttons {{ text-align: center; margin: 20px 0; }}
                .status-badge {{ background: #f39c12; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; }}
            </style>
            <script>
                function toggleFavorite() {{
                    fetch('/toggle_favorite/{recipe._id}', {{ method: 'POST' }})
                    .then(() => location.reload());
                }}
                function updateStatus() {{
                    var status = prompt("Choose new status:\\n\\n1. want_to_try (🤔 Want to Try)\\n2. tried (👍 Tried Once)\\n3. made_before (⭐ Made Before)\\n\\nEnter: want_to_try, tried, or made_before");
                    if (status && ['want_to_try', 'tried', 'made_before'].includes(status)) {{
                        fetch('/update_status', {{ 
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                            body: 'recipe_id={recipe._id}&status=' + status
                        }}).then(() => location.reload());
                    }} else if (status) {{
                        alert('Invalid status! Please use: want_to_try, tried, or made_before');
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="container">
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/recipes">📋 All Recipes</a>
                    <a href="/favorites">❤️ Favorites</a>
                    <a href="/filter/want_to_try">🤔 Want to Try</a>
                    <a href="/filter/tried">👍 Tried</a>
                    <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                    <a href="/random">🎲 Random Recipe</a>
                </div>
                
                <h1>{favorite_icon} {recipe.name} {status_emoji}</h1>
                <div style="text-align: center; margin-bottom: 20px;">
                    <span class="status-badge">{status_text}</span>
                </div>
                
                <div class="meta-info">
                    <span class="meta-item">🥘 <strong>{len(recipe.ingredients)}</strong> ingredients</span>
                    <span class="meta-item">📋 <strong>{len(recipe.instructions)}</strong> steps</span>
                    <span class="meta-item">🌍 <strong>{recipe.metadata.get('cuisine', 'N/A')}</strong></span>
                    <span class="meta-item">⭐ <strong>{recipe.metadata.get('difficulty', 'N/A')}</strong></span>
                    <span class="meta-item">🍽️ <strong>{recipe.metadata.get('servings', 'N/A')}</strong> servings</span>
                    {f'<span class="meta-item">⏱️ <strong>{recipe.metadata.get("prep_time", "N/A")}</strong> prep</span>' if recipe.metadata.get('prep_time') else ''}
                    {f'<span class="meta-item">🔥 <strong>{recipe.metadata.get("cook_time", "N/A")}</strong> cook</span>' if recipe.metadata.get('cook_time') else ''}
                    {f'<span class="meta-item">⏰ <strong>{total_time}</strong> total</span>' if total_time != 'N/A' else ''}
                </div>
                
                <div class="action-buttons">
                    <button onclick="toggleFavorite()">{favorite_icon} {'Remove from' if recipe.is_favorite else 'Add to'} Favorites</button>
                    <select onchange="updateStatusDetail(this.value)" style="padding: 10px; margin: 10px 5px; border-radius: 5px; border: 1px solid #ddd;">
                        <option value="">Change Status...</option>
                        <option value="want_to_try" {'selected' if recipe.status == 'want_to_try' else ''}>🤔 Want to Try</option>
                        <option value="tried" {'selected' if recipe.status == 'tried' else ''}>👍 Tried Once</option>
                        <option value="made_before" {'selected' if recipe.status == 'made_before' else ''}>⭐ Made Before</option>
                    </select>
                    <button onclick="window.history.back()">⬅️ Go Back</button>
                </div>
                
                <h2>🥘 Ingredients</h2>
                <ul>
                    {ingredients_html}
                </ul>
                
                <h2>📋 Instructions</h2>
                <ol>
                    {instructions_html}
                </ol>
                
                {f'<h2>🏷️ Tags</h2><p>{", ".join(recipe.metadata.get("tags", []))}</p>' if recipe.metadata.get('tags') else ''}
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_stats(self):
        """📊 Serve statistics page"""
        stats = self.manager.get_recipe_stats()
        
        if not stats:
            html = """
            <!DOCTYPE html>
            <html>
            <head><title>📊 Statistics</title></head>
            <body><h1>📊 No statistics available</h1><p>Add some recipes first!</p></body>
            </html>
            """
        else:
            # Format cuisine distribution
            cuisine_cards = ""
            for cuisine, count in stats.get('cuisines', {}).items():
                percentage = round((count / stats['total_recipes']) * 100, 1)
                cuisine_cards += f"""
                <div class="stat-card">
                    <h3>🌍 {cuisine}</h3>
                    <p>{count} recipes ({percentage}%)</p>
                </div>
                """
            
            # Format difficulty distribution
            difficulty_cards = ""
            for difficulty, count in stats.get('difficulties', {}).items():
                percentage = round((count / stats['total_recipes']) * 100, 1)
                emoji = {'easy': '😊', 'medium': '🤔', 'hard': '😰'}.get(difficulty, '⭐')
                difficulty_cards += f"""
                <div class="stat-card">
                    <h3>{emoji} {difficulty.title()}</h3>
                    <p>{count} recipes ({percentage}%)</p>
                </div>
                """
            
            # Format status distribution
            status_cards = ""
            status_emojis = {'want_to_try': '🤔', 'tried': '👍', 'made_before': '⭐'}
            for status, count in stats.get('status_counts', {}).items():
                percentage = round((count / stats['total_recipes']) * 100, 1)
                emoji = status_emojis.get(status, '📝')
                readable_status = status.replace('_', ' ').title()
                status_cards += f"""
                <div class="stat-card">
                    <h3>{emoji} {readable_status}</h3>
                    <p>{count} recipes ({percentage}%)</p>
                </div>
                """
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>📊 Recipe Statistics</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                    h1 {{ color: #2c3e50; text-align: center; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
                    .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #3498db; }}
                    .stat-card h3 {{ margin: 0 0 10px 0; color: #2c3e50; }}
                    .stat-card p {{ margin: 0; color: #7f8c8d; }}
                    .nav {{ text-align: center; margin-bottom: 30px; }}
                    .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                    .nav a:hover {{ background: #ecf0f1; }}
                    .highlight {{ background: #e8f5e8; border-left-color: #27ae60; }}
                    .section {{ margin: 30px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 Recipe Statistics</h1>
                    
                    <div class="nav">
                        <a href="/">🏠 Home</a>
                        <a href="/recipes">📋 All Recipes</a>
                        <a href="/favorites">❤️ Favorites</a>
                        <a href="/filter/want_to_try">🤔 Want to Try</a>
                        <a href="/filter/tried">👍 Tried</a>
                        <a href="/filter/made_before">⭐ Made Before</a>
                    <a href="/stats">📊 Statistics</a>
                    </div>
                    
                    <div class="section">
                        <h2>📈 Overview</h2>
                        <div class="stats-grid">
                            <div class="stat-card highlight">
                                <h3>📚 Total Recipes</h3>
                                <p>{stats['total_recipes']} recipes</p>
                            </div>
                            <div class="stat-card highlight">
                                <h3>❤️ Favorites</h3>
                                <p>{stats['favorites_count']} ({stats['favorites_percentage']}%)</p>
                            </div>
                            <div class="stat-card">
                                <h3>🥘 Avg Ingredients</h3>
                                <p>{stats['avg_ingredients']} per recipe</p>
                            </div>
                            <div class="stat-card">
                                <h3>📋 Avg Instructions</h3>
                                <p>{stats['avg_instructions']} steps</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>📝 Recipe Status</h2>
                        <div class="stats-grid">
                            {status_cards}
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>🌍 Cuisines</h2>
                        <div class="stats-grid">
                            {cuisine_cards}
                        </div>
                        <p><strong>Most Popular:</strong> {stats['most_popular_cuisine']}</p>
                    </div>
                    
                    <div class="section">
                        <h2>⭐ Difficulty Levels</h2>
                        <div class="stats-grid">
                            {difficulty_cards}
                        </div>
                        <p><strong>Most Common:</strong> {stats['most_common_difficulty']}</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def add_recipe(self):
        """➕ Add new recipe"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            # Extract form data
            name = data['name'][0]
            ingredients = [ing.strip() for ing in data['ingredients'][0].split('\n') if ing.strip()]
            instructions = [inst.strip() for inst in data['instructions'][0].split('\n') if inst.strip()]
            
            # Optional metadata
            metadata = {}
            if 'cuisine' in data and data['cuisine'][0]:
                metadata['cuisine'] = data['cuisine'][0]
            if 'difficulty' in data:
                metadata['difficulty'] = data['difficulty'][0]
            if 'servings' in data:
                try:
                    metadata['servings'] = int(data['servings'][0])
                except:
                    pass
            if 'prep_time' in data and data['prep_time'][0]:
                metadata['prep_time'] = data['prep_time'][0]
            if 'cook_time' in data and data['cook_time'][0]:
                metadata['cook_time'] = data['cook_time'][0]
            
            # Extract favorite and status
            is_favorite = 'is_favorite' in data
            status = data.get('status', ['want_to_try'])[0]
            
            # Create and save recipe
            recipe = Recipe(name, ingredients, instructions, metadata, None, is_favorite, status)
            self.manager.add_recipe(recipe)
            
            # Redirect to recipes page
            self.send_response(302)
            self.send_header('Location', '/recipes')
            self.end_headers()
            
        except Exception as e:
            self.send_error(500, f"Error adding recipe: {str(e)}")
    
    def delete_recipe(self, recipe_id):
        """🗑️ Delete recipe"""
        try:
            success = self.manager.delete_recipe(recipe_id)
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"success": true}')
            else:
                self.send_error(404, "Recipe not found")
        except Exception as e:
            self.send_error(500, f"Error deleting recipe: {str(e)}")
    
    def toggle_favorite(self, recipe_id):
        """❤️ Toggle favorite status"""
        try:
            success = self.manager.toggle_favorite(recipe_id)
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"success": true}')
            else:
                self.send_error(404, "Recipe not found")
        except Exception as e:
            self.send_error(500, f"Error toggling favorite: {str(e)}")
    
    def update_status(self):
        """📝 Update recipe status"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            recipe_id = data['recipe_id'][0]
            new_status = data['status'][0]
            
            success = self.manager.update_recipe_status(recipe_id, new_status)
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"success": true}')
            else:
                self.send_error(400, "Failed to update status")
                
        except Exception as e:
            self.send_error(500, f"Error updating status: {str(e)}")
    
    def handle_search(self):
        """🔍 Handle search requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            query = data.get('search_query', [''])[0]
            
            if query:
                results = self.manager.search_recipes(query)
                
                recipe_cards = ""
                for recipe in results:
                    favorite_icon = "❤️" if recipe.is_favorite else "🤍"
                    status_emoji = recipe.get_status_emoji()
                    status_text = recipe.get_status_text()
                    
                    recipe_cards += f"""
                    <div class="recipe-card">
                        <h3 class="recipe-title">{favorite_icon} {recipe.name} {status_emoji}</h3>
                        <div class="recipe-meta">
                            🥘 {len(recipe.ingredients)} ingredients • 
                            📋 {len(recipe.instructions)} steps • 
                            🌍 {recipe.metadata.get('cuisine', 'N/A')} • 
                            ⭐ {recipe.metadata.get('difficulty', 'N/A')} •
                            📝 {status_text}
                        </div>
                        <button onclick="viewRecipe('{recipe._id}')">👁️ View Details</button>
                        <button onclick="toggleFavorite('{recipe._id}')">{favorite_icon} Favorite</button>
                        <select onchange="updateStatus('{recipe._id}', this.value)" style="padding: 8px; margin: 5px; border-radius: 5px; border: 1px solid #ddd;">
                            <option value="">Change Status...</option>
                            <option value="want_to_try" {'selected' if recipe.status == 'want_to_try' else ''}>🤔 Want to Try</option>
                            <option value="tried" {'selected' if recipe.status == 'tried' else ''}>👍 Tried Once</option>
                            <option value="made_before" {'selected' if recipe.status == 'made_before' else ''}>⭐ Made Before</option>
                        </select>
                    </div>
                    """
                
                if not recipe_cards:
                    recipe_cards = f"<p>😞 No recipes found for '{query}'. Try a different search term!</p>"
                
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>🔍 Search Results</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        h1 {{ color: #2c3e50; text-align: center; }}
                        .recipe-card {{ background: #ecf0f1; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #3498db; }}
                        .recipe-title {{ color: #2c3e50; margin-bottom: 10px; }}
                        .recipe-meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }}
                        button {{ background: #3498db; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin: 5px 5px 5px 0; }}
                        button:hover {{ background: #2980b9; }}
                        .nav {{ text-align: center; margin-bottom: 30px; }}
                        .nav a {{ margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; padding: 8px 12px; border-radius: 5px; }}
                        .nav a:hover {{ background: #ecf0f1; }}
                    </style>
                    <script>
                        function viewRecipe(id) {{ window.location.href = '/recipe/' + id; }}
                        function toggleFavorite(id) {{
                            fetch('/toggle_favorite/' + id, {{ method: 'POST' }})
                            .then(() => location.reload());
                        }}
                        function updateStatus(id) {{
                            var status = prompt("Choose new status:\\n\\n1. want_to_try (🤔 Want to Try)\\n2. tried (👍 Tried Once)\\n3. made_before (⭐ Made Before)\\n\\nEnter: want_to_try, tried, or made_before");
                            if (status && ['want_to_try', 'tried', 'made_before'].includes(status)) {{
                                fetch('/update_status', {{ 
                                    method: 'POST',
                                    headers: {{ 'Content-Type': 'application/x-www-form-urlencoded' }},
                                    body: 'recipe_id=' + id + '&status=' + status
                                }}).then(() => location.reload());
                            }} else if (status) {{
                                alert('Invalid status! Please use: want_to_try, tried, or made_before');
                            }}
                        }}
                    </script>
                </head>
                <body>
                    <div class="container">
                        <h1>🔍 Search Results for "{query}"</h1>
                        <p>Found {len(results)} recipe(s)</p>
                        
                        <div class="nav">
                            <a href="/">🏠 Home</a>
                            <a href="/recipes">📋 All Recipes</a>
                            <a href="/favorites">❤️ Favorites</a>
                            <a href="/filter/want_to_try">🤔 Want to Try</a>
                            <a href="/filter/tried">👍 Tried</a>
                            <a href="/filter/made_before">⭐ Made Before</a>
                            <a href="/stats">📊 Statistics</a>
                        </div>
                        
                        {recipe_cards}
                    </div>
                </body>
                </html>
                """
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            else:
                # Redirect back to home if empty query
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                
        except Exception as e:
            self.send_error(500, f"Error searching recipes: {str(e)}")

def run_server():
    """🚀 Start the web server"""
    print("🍳 Starting Recipe Management Web Server...")
    print("🌐 Server running at: http://localhost:8080")
    print("⚡ Press Ctrl+C to stop the server")
    
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RecipeHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
        httpd.server_close()

if __name__ == "__main__":
    run_server()