import json
import os
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

class NFLDataCache:
    def __init__(self, cache_dir: str, ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f'{key}.json')
    
    def _is_expired(self, timestamp: str) -> bool:
        cached_time = datetime.fromisoformat(timestamp)
        return (datetime.now() - cached_time).total_seconds() > self.ttl_seconds
    
    def get(self, key: str) -> Optional[Dict]:
        """Get data from cache if not expired"""
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                if self._is_expired(data['timestamp']):
                    self.clear(key)
                    return None
                return data['content']
        except (json.JSONDecodeError, KeyError, ValueError):
            self.clear(key)
            return None
    
    def set(self, key: str, content: Any):
        """Save data to cache with timestamp"""
        cache_path = self._get_cache_path(key)
        data = {
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        with open(cache_path, 'w') as f:
            json.dump(data, f)
    
    def clear(self, key: str):
        """Remove cached data"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    def clear_all(self):
        """Clear all cached data"""
        for file in os.listdir(self.cache_dir):
            if file.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, file))