# models.py
from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId

class Recipe:
    def __init__(self, name: str, ingredients: List[str], instructions: List[str], 
                 metadata: Optional[Dict] = None, _id: Optional[ObjectId] = None, 
                 is_favorite: bool = False, status: str = "want_to_try"):
        """
        🍳 Recipe model class
        
        Args:
            name: Recipe name
            ingredients: List of ingredients
            instructions: List of cooking instructions
            metadata: Additional recipe info (prep_time, cook_time, servings, etc.)
            _id: MongoDB ObjectId (auto-generated if not provided)
            is_favorite: Whether recipe is marked as favorite
            status: Recipe status - "want_to_try", "tried", "made_before"
        """
        self._id = _id
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.metadata = metadata or {}
        self.is_favorite = is_favorite
        self.status = status  # "want_to_try", "tried", "made_before"
        
        # 📅 Auto-add timestamps if not in metadata
        if 'created_at' not in self.metadata:
            self.metadata['created_at'] = datetime.now()
        if 'updated_at' not in self.metadata:
            self.metadata['updated_at'] = datetime.now()
    
    def to_dict(self) -> Dict:
        """🔄 Convert recipe to dictionary for MongoDB storage"""
        recipe_dict = {
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'metadata': self.metadata,
            'is_favorite': self.is_favorite,
            'status': self.status
        }
        
        if self._id:
            recipe_dict['_id'] = self._id
            
        return recipe_dict
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Recipe':
        """🏗️ Create Recipe instance from dictionary"""
        return cls(
            name=data['name'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            metadata=data.get('metadata', {}),
            _id=data.get('_id'),
            is_favorite=data.get('is_favorite', False),
            status=data.get('status', 'want_to_try')
        )
    
    def update_timestamp(self):
        """⏰ Update the 'updated_at' timestamp"""
        self.metadata['updated_at'] = datetime.now()
    
    def get_status_emoji(self) -> str:
        """🎯 Get emoji for recipe status"""
        status_emojis = {
            'want_to_try': '🤔',
            'tried': '👍', 
            'made_before': '⭐'
        }
        return status_emojis.get(self.status, '🤔')
    
    def get_status_text(self) -> str:
        """📝 Get readable text for recipe status"""
        status_text = {
            'want_to_try': 'Want to Try',
            'tried': 'Tried Once',
            'made_before': 'Made Before'
        }
        return status_text.get(self.status, 'Want to Try')
    
    def get_favorite_emoji(self) -> str:
        """❤️ Get emoji for favorite status"""
        return "❤️" if self.is_favorite else "🤍"
    
    def toggle_favorite(self):
        """🔄 Toggle favorite status"""
        self.is_favorite = not self.is_favorite
        self.update_timestamp()
    
    def set_status(self, new_status: str) -> bool:
        """📝 Set recipe status with validation"""
        valid_statuses = ['want_to_try', 'tried', 'made_before']
        if new_status in valid_statuses:
            self.status = new_status
            self.update_timestamp()
            return True
        return False
    
    def get_display_info(self) -> Dict:
        """📊 Get formatted display information"""
        return {
            'name': self.name,
            'favorite_emoji': self.get_favorite_emoji(),
            'status_emoji': self.get_status_emoji(),
            'status_text': self.get_status_text(),
            'ingredients_count': len(self.ingredients),
            'instructions_count': len(self.instructions),
            'cuisine': self.metadata.get('cuisine', 'N/A'),
            'difficulty': self.metadata.get('difficulty', 'N/A'),
            'servings': self.metadata.get('servings', 'N/A'),
            'prep_time': self.metadata.get('prep_time', 'N/A'),
            'cook_time': self.metadata.get('cook_time', 'N/A')
        }
    
    def is_complete_recipe(self) -> bool:
        """✅ Check if recipe has all required information"""
        return (
            bool(self.name) and 
            bool(self.ingredients) and 
            bool(self.instructions)
        )
    
    def get_total_time(self) -> str:
        """⏱️ Calculate total time if prep and cook times are available"""
        prep = self.metadata.get('prep_time', '')
        cook = self.metadata.get('cook_time', '')
        
        if not prep or not cook:
            return 'N/A'
        
        try:
            # Simple parsing for times like "20 minutes", "1 hour 30 minutes"
            def parse_time(time_str):
                time_str = time_str.lower()
                minutes = 0
                
                if 'hour' in time_str:
                    hours = int(''.join(filter(str.isdigit, time_str.split('hour')[0])))
                    minutes += hours * 60
                    remaining = time_str.split('hour')[1] if 'hour' in time_str else time_str
                else:
                    remaining = time_str
                
                if 'minute' in remaining:
                    mins = int(''.join(filter(str.isdigit, remaining.split('minute')[0])))
                    minutes += mins
                
                return minutes
            
            prep_mins = parse_time(prep)
            cook_mins = parse_time(cook)
            total_mins = prep_mins + cook_mins
            
            if total_mins >= 60:
                hours = total_mins // 60
                mins = total_mins % 60
                if mins > 0:
                    return f"{hours}h {mins}m"
                else:
                    return f"{hours}h"
            else:
                return f"{total_mins}m"
                
        except:
            return 'N/A'
    
    def get_difficulty_level(self) -> int:
        """📊 Get numeric difficulty level (1-3)"""
        difficulty_levels = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        return difficulty_levels.get(self.metadata.get('difficulty', 'medium'), 2)
    
    def add_tag(self, tag: str):
        """🏷️ Add a tag to recipe metadata"""
        if 'tags' not in self.metadata:
            self.metadata['tags'] = []
        
        if tag not in self.metadata['tags']:
            self.metadata['tags'].append(tag)
            self.update_timestamp()
    
    def remove_tag(self, tag: str):
        """🗑️ Remove a tag from recipe metadata"""
        if 'tags' in self.metadata and tag in self.metadata['tags']:
            self.metadata['tags'].remove(tag)
            self.update_timestamp()
    
    def get_tags(self) -> List[str]:
        """🏷️ Get list of tags"""
        return self.metadata.get('tags', [])
    
    def __str__(self) -> str:
        """📝 String representation of recipe"""
        status_emoji = self.get_status_emoji()
        favorite_emoji = self.get_favorite_emoji()
        return f"{favorite_emoji} {self.name} {status_emoji} ({len(self.ingredients)} ingredients, {len(self.instructions)} steps)"
    
    def __repr__(self) -> str:
        return self.__str__()