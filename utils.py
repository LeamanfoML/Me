import hashlib

def generate_token_hash(token: str) -> str:
    """Генерация хеша для безопасного хранения токенов"""
    return hashlib.sha256(token.encode()).hexdigest()

def validate_nft_data(item: dict) -> bool:
    """Валидация данных NFT"""
    required_fields = {'id', 'name', 'model', 'current_bid', 'end_time'}
    return all(field in item for field in required_fields)
