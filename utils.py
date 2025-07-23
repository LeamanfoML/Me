import hashlib

def generate_token_hash(token: str) -> str:
    """Генерация хеша для безопасного хранения токенов"""
    return hashlib.sha256(token.encode()).hexdigest()

def validate_nft_data(item: dict) -> bool:
    """Валидация данных NFT для обоих маркетплейсов"""
    # Обязательные поля для Portals
    portals_required = {'id', 'name', 'current_bid', 'end_time'}
    
    # Обязательные поля для Tonnel
    tonnel_required = {'id', 'name', 'current_price', 'end_time'}
    
    # Проверяем наличие хотя бы одного набора
    if all(field in item for field in portals_required):
        return True
    
    if all(field in item for field in tonnel_required):
        return True
    
    return False
