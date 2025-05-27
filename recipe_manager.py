# recipe_manager.py
from typing import List, Optional, Dict
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, PyMongoError

from database import db_connection
from models import Recipe

class RecipeManager:
    def __init__(self):
        """🎯 Initialize Recipe Manager with MongoDB connection"""
        self.collection_name = 'recipes'
        self.collection: Optional[Collection] = None
        self._connect_to_db()
    
    def _connect_to_db(self):
        """🔌 Establish database connection"""
        if db_connection.connect():
            self.collection = db_connection.get_collection(self.collection_name)
            # 📇 Create index on recipe name for faster searches
            self.collection.create_index("name", unique=True)
            # 📇 Create indexes for favorite and status filtering
            self.collection.create_index("is_favorite")
            self.collection.create_index("status")
    
    def add_recipe(self, recipe: Recipe) -> str:
        """
        ➕ Add a new recipe to the database
        
        Args:
            recipe: Recipe object to add
            
        Returns:
            str: ID of the inserted recipe
        """
        try:
            recipe_dict = recipe.to_dict()
            result = self.collection.insert_one(recipe_dict)
            print(f"✅ Recipe '{recipe.name}' added successfully!")
            return str(result.inserted_id)
        
        except DuplicateKeyError:
            print(f"❌ Recipe '{recipe.name}' already exists!")
            raise ValueError(f"Recipe '{recipe.name}' already exists!")
        
        except PyMongoError as e:
            print(f"❌ Database error: {e}")
            raise
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        🔍 Get recipe by MongoDB ObjectId
        
        Args:
            recipe_id: String representation of ObjectId
            
        Returns:
            Recipe object or None if not found
        """
        try:
            result = self.collection.find_one({"_id": ObjectId(recipe_id)})
            if result:
                return Recipe.from_dict(result)
            return None
        
        except Exception as e:
            print(f"❌ Error fetching recipe: {e}")
            return None
    
    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        """
        🔍 Get recipe by name
        
        Args:
            name: Recipe name
            
        Returns:
            Recipe object or None if not found
        """
        try:
            result = self.collection.find_one({"name": name})
            if result:
                return Recipe.from_dict(result)
            return None
        
        except Exception as e:
            print(f"❌ Error fetching recipe: {e}")
            return None
    
    def get_all_recipes(self) -> List[Recipe]:
        """
        📋 Get all recipes from database
        
        Returns:
            List of Recipe objects
        """
        try:
            results = self.collection.find()
            return [Recipe.from_dict(doc) for doc in results]
        
        except Exception as e:
            print(f"❌ Error fetching recipes: {e}")
            return []
    
    def update_recipe(self, recipe_id: str, updated_recipe: Recipe) -> bool:
        """
        ✏️ Update an existing recipe
        
        Args:
            recipe_id: ID of recipe to update
            updated_recipe: Updated Recipe object
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            updated_recipe.update_timestamp()
            update_dict = updated_recipe.to_dict()
            
            # Remove _id from update dict to avoid conflicts
            if '_id' in update_dict:
                del update_dict['_id']
            
            result = self.collection.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$set": update_dict}
            )
            
            if result.modified_count > 0:
                print(f"✅ Recipe updated successfully!")
                return True
            else:
                print(f"⚠️ No recipe found with ID: {recipe_id}")
                return False
        
        except Exception as e:
            print(f"❌ Error updating recipe: {e}")
            return False
    
    def delete_recipe(self, recipe_id: str) -> bool:
        """
        🗑️ Delete a recipe from database
        
        Args:
            recipe_id: ID of recipe to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": ObjectId(recipe_id)})
            
            if result.deleted_count > 0:
                print(f"✅ Recipe deleted successfully!")
                return True
            else:
                print(f"⚠️ No recipe found with ID: {recipe_id}")
                return False
        
        except Exception as e:
            print(f"❌ Error deleting recipe: {e}")
            return False
    
    def search_recipes(self, query: str) -> List[Recipe]:
        """
        🔎 Search recipes by name or ingredients
        
        Args:
            query: Search term
            
        Returns:
            List of matching Recipe objects
        """
        try:
            # Search in name and ingredients using regex
            search_filter = {
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"ingredients": {"$regex": query, "$options": "i"}}
                ]
            }
            
            results = self.collection.find(search_filter)
            return [Recipe.from_dict(doc) for doc in results]
        
        except Exception as e:
            print(f"❌ Error searching recipes: {e}")
            return []
    
    def toggle_favorite(self, recipe_id: str) -> bool:
        """
        ❤️ Toggle favorite status of a recipe
        
        Args:
            recipe_id: ID of recipe to toggle
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            recipe = self.get_recipe_by_id(recipe_id)
            if not recipe:
                return False
            
            # Toggle favorite status
            recipe.is_favorite = not recipe.is_favorite
            recipe.update_timestamp()
            
            # Update in database
            result = self.collection.update_one(
                {"_id": ObjectId(recipe_id)}, 
                {"$set": {
                    "is_favorite": recipe.is_favorite, 
                    "metadata.updated_at": recipe.metadata['updated_at']
                }}
            )
            
            if result.modified_count > 0:
                status = "added to" if recipe.is_favorite else "removed from"
                print(f"✅ Recipe {status} favorites!")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error toggling favorite: {e}")
            return False
    
    def update_recipe_status(self, recipe_id: str, new_status: str) -> bool:
        """
        📝 Update recipe status (want_to_try, tried, made_before)
        
        Args:
            recipe_id: ID of recipe to update
            new_status: New status value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            valid_statuses = ['want_to_try', 'tried', 'made_before']
            if new_status not in valid_statuses:
                print(f"❌ Invalid status. Must be one of: {valid_statuses}")
                return False
            
            recipe = self.get_recipe_by_id(recipe_id)
            if not recipe:
                return False
            
            recipe.status = new_status
            recipe.update_timestamp()
            
            # Update in database
            result = self.collection.update_one(
                {"_id": ObjectId(recipe_id)}, 
                {"$set": {
                    "status": new_status, 
                    "metadata.updated_at": recipe.metadata['updated_at']
                }}
            )
            
            if result.modified_count > 0:
                print(f"✅ Recipe status updated to: {recipe.get_status_text()}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error updating status: {e}")
            return False
    
    def get_favorite_recipes(self) -> List[Recipe]:
        """
        ❤️ Get all favorite recipes
        
        Returns:
            List of favorite Recipe objects
        """
        try:
            results = self.collection.find({"is_favorite": True})
            return [Recipe.from_dict(doc) for doc in results]
        except Exception as e:
            print(f"❌ Error fetching favorites: {e}")
            return []
    
    def get_recipes_by_status(self, status: str) -> List[Recipe]:
        """
        📊 Get recipes filtered by status
        
        Args:
            status: Status to filter by ('want_to_try', 'tried', 'made_before')
            
        Returns:
            List of matching Recipe objects
        """
        try:
            results = self.collection.find({"status": status})
            return [Recipe.from_dict(doc) for doc in results]
        except Exception as e:
            print(f"❌ Error fetching recipes by status: {e}")
            return []
    
    def get_recipes_by_metadata(self, metadata_key: str, metadata_value) -> List[Recipe]:
        """
        🏷️ Get recipes filtered by metadata
        
        Args:
            metadata_key: Key in metadata dict
            metadata_value: Value to match
            
        Returns:
            List of matching Recipe objects
        """
        try:
            filter_dict = {f"metadata.{metadata_key}": metadata_value}
            results = self.collection.find(filter_dict)
            return [Recipe.from_dict(doc) for doc in results]
        
        except Exception as e:
            print(f"❌ Error filtering recipes: {e}")
            return []
    
    def get_recipes_by_cuisine(self, cuisine: str) -> List[Recipe]:
        """
        🌍 Get recipes by cuisine type
        
        Args:
            cuisine: Cuisine to filter by
            
        Returns:
            List of matching Recipe objects
        """
        return self.get_recipes_by_metadata("cuisine", cuisine)
    
    def get_recipes_by_difficulty(self, difficulty: str) -> List[Recipe]:
        """
        ⭐ Get recipes by difficulty level
        
        Args:
            difficulty: Difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            List of matching Recipe objects
        """
        return self.get_recipes_by_metadata("difficulty", difficulty)
    
    def get_recipe_stats(self) -> Dict:
        """
        📊 Get comprehensive recipe statistics
        
        Returns:
            Dictionary with various statistics
        """
        try:
            all_recipes = self.get_all_recipes()
            
            if not all_recipes:
                return {}
            
            # Basic counts
            total_recipes = len(all_recipes)
            favorites_count = len([r for r in all_recipes if r.is_favorite])
            
            # Status counts
            status_counts = {
                'want_to_try': len([r for r in all_recipes if r.status == 'want_to_try']),
                'tried': len([r for r in all_recipes if r.status == 'tried']),
                'made_before': len([r for r in all_recipes if r.status == 'made_before'])
            }
            
            # Cuisine distribution
            cuisines = {}
            for recipe in all_recipes:
                cuisine = recipe.metadata.get('cuisine', 'Unknown')
                cuisines[cuisine] = cuisines.get(cuisine, 0) + 1
            
            # Difficulty distribution
            difficulties = {}
            for recipe in all_recipes:
                difficulty = recipe.metadata.get('difficulty', 'Unknown')
                difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
            
            # Average ingredients and instructions
            avg_ingredients = sum(len(r.ingredients) for r in all_recipes) / total_recipes
            avg_instructions = sum(len(r.instructions) for r in all_recipes) / total_recipes
            
            # Most common ingredients (simplified)
            all_ingredients = []
            for recipe in all_recipes:
                all_ingredients.extend([ing.lower().strip() for ing in recipe.ingredients])
            
            from collections import Counter
            common_ingredients = Counter(all_ingredients).most_common(5)
            
            return {
                'total_recipes': total_recipes,
                'favorites_count': favorites_count,
                'favorites_percentage': round((favorites_count / total_recipes) * 100, 1),
                'status_counts': status_counts,
                'cuisines': cuisines,
                'difficulties': difficulties,
                'avg_ingredients': round(avg_ingredients, 1),
                'avg_instructions': round(avg_instructions, 1),
                'common_ingredients': dict(common_ingredients),
                'most_popular_cuisine': max(cuisines.items(), key=lambda x: x[1])[0] if cuisines else 'N/A',
                'most_common_difficulty': max(difficulties.items(), key=lambda x: x[1])[0] if difficulties else 'N/A'
            }
            
        except Exception as e:
            print(f"❌ Error generating stats: {e}")
            return {}
    
    def advanced_search(self, 
                       name_query: str = "", 
                       ingredient_query: str = "",
                       cuisine: str = "",
                       difficulty: str = "",
                       is_favorite: Optional[bool] = None,
                       status: str = "",
                       min_servings: Optional[int] = None,
                       max_servings: Optional[int] = None) -> List[Recipe]:
        """
        🔍 Advanced search with multiple filters
        
        Args:
            name_query: Search in recipe names
            ingredient_query: Search in ingredients
            cuisine: Filter by cuisine
            difficulty: Filter by difficulty
            is_favorite: Filter by favorite status
            status: Filter by recipe status
            min_servings: Minimum servings
            max_servings: Maximum servings
            
        Returns:
            List of matching Recipe objects
        """
        try:
            filters = []
            
            # Name search
            if name_query:
                filters.append({"name": {"$regex": name_query, "$options": "i"}})
            
            # Ingredient search
            if ingredient_query:
                filters.append({"ingredients": {"$regex": ingredient_query, "$options": "i"}})
            
            # Cuisine filter
            if cuisine:
                filters.append({"metadata.cuisine": cuisine})
            
            # Difficulty filter
            if difficulty:
                filters.append({"metadata.difficulty": difficulty})
            
            # Favorite filter
            if is_favorite is not None:
                filters.append({"is_favorite": is_favorite})
            
            # Status filter
            if status:
                filters.append({"status": status})
            
            # Servings filters
            if min_servings is not None:
                filters.append({"metadata.servings": {"$gte": min_servings}})
            
            if max_servings is not None:
                filters.append({"metadata.servings": {"$lte": max_servings}})
            
            # Combine filters
            if filters:
                if len(filters) == 1:
                    query = filters[0]
                else:
                    query = {"$and": filters}
            else:
                query = {}
            
            results = self.collection.find(query)
            return [Recipe.from_dict(doc) for doc in results]
        
        except Exception as e:
            print(f"❌ Error in advanced search: {e}")
            return []
    
    def bulk_update_status(self, recipe_ids: List[str], new_status: str) -> int:
        """
        📝 Update status for multiple recipes
        
        Args:
            recipe_ids: List of recipe IDs to update
            new_status: New status for all recipes
            
        Returns:
            int: Number of recipes updated
        """
        try:
            valid_statuses = ['want_to_try', 'tried', 'made_before']
            if new_status not in valid_statuses:
                print(f"❌ Invalid status. Must be one of: {valid_statuses}")
                return 0
            
            object_ids = [ObjectId(rid) for rid in recipe_ids]
            
            result = self.collection.update_many(
                {"_id": {"$in": object_ids}},
                {"$set": {
                    "status": new_status,
                    "metadata.updated_at": datetime.now()
                }}
            )
            
            print(f"✅ Updated {result.modified_count} recipes to status: {new_status}")
            return result.modified_count
            
        except Exception as e:
            print(f"❌ Error in bulk update: {e}")
            return 0
    
    def export_recipes(self, format_type: str = "dict") -> List:
        """
        📤 Export all recipes in specified format
        
        Args:
            format_type: Export format ('dict', 'json_ready')
            
        Returns:
            List of recipes in specified format
        """
        try:
            recipes = self.get_all_recipes()
            
            if format_type == "dict":
                return [recipe.to_dict() for recipe in recipes]
            elif format_type == "json_ready":
                # Convert ObjectId to string for JSON serialization
                exported = []
                for recipe in recipes:
                    recipe_dict = recipe.to_dict()
                    if '_id' in recipe_dict:
                        recipe_dict['_id'] = str(recipe_dict['_id'])
                    # Convert datetime objects to strings
                    if 'metadata' in recipe_dict:
                        for key, value in recipe_dict['metadata'].items():
                            if hasattr(value, 'isoformat'):
                                recipe_dict['metadata'][key] = value.isoformat()
                    exported.append(recipe_dict)
                return exported
            else:
                return []
                
        except Exception as e:
            print(f"❌ Error exporting recipes: {e}")
            return []
    
    def get_random_recipe(self, filters: Optional[Dict] = None) -> Optional[Recipe]:
        """
        🎲 Get a random recipe, optionally with filters
        
        Args:
            filters: Optional MongoDB filter dict
            
        Returns:
            Random Recipe object or None
        """
        try:
            pipeline = []
            
            if filters:
                pipeline.append({"$match": filters})
            
            pipeline.append({"$sample": {"size": 1}})
            
            results = list(self.collection.aggregate(pipeline))
            
            if results:
                return Recipe.from_dict(results[0])
            return None
            
        except Exception as e:
            print(f"❌ Error getting random recipe: {e}")
            return None