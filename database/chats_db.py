import sqlite3
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ChatsDatabase:
    def __init__(self, db_path: str = "telegram_bot.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS categories(
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    emoji TEXT)
                """)
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id TEXT NOT NULL,
                    name TEXT NOT NULL,  -- ДОБАВЛЕНО название канала
                    username TEXT NOT NULL UNIQUE,
                    subscribers TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )               
                """)
            
            cursor = conn.execute("PRAGMA table_info(chats)")
            columns = [column[1] for column in cursor.fetchall()]       

            if 'name' not in columns:
                conn.execute("ALTER TABLE chats ADD COLUMN name TEXT NOT NULL DEFAULT 'Channel'")
                logger.info("Добавлена колонка name в таблицу chats")                 
            
            self._seed_categories(conn)
            self._seed_chats(conn)
            
            conn.commit()
        logger.info("База данных инициализирована")

    def _seed_categories(self, conn):
        categories = [
        ('cat_crypto', '🪙 Криптовалюта / TON', '🪙'),
        ('cat_ai', '🧠 Нейросети / AI', '🧠'),
        ('cat_marketing', '📈 Маркетинг / Продвижение', '📈'),
        ('cat_arbitrage', '💰 Арбитраж / Трафик', '💰'),
        ('cat_blogging', '🎥 Блогинг / Контент', '🎥'),
        ('cat_it', '💼 IT / Автоматизация', '💼'),
        ]
        conn.executemany(
            """
            INSERT OR IGNORE INTO categories (id, name, emoji)
            VALUES (?, ?, ?)
            """, categories)

    def _seed_chats(self, conn):
        chats = [
            # КРИПТОВАЛЮТА 
            ('cat_crypto', 'OKX Новости', '@okx_ru', '6204899 подписчиков'),
            ('cat_crypto', 'Crypto Wolf', '@Crypto_Woolf', '3343456 подписчиков'),
            ('cat_crypto', 'Дайте TON!', '@SearcheeBot', '287654 подписчиков'),
            ('cat_crypto', 'Binance Russian', '@binance_russian', '1892345 подписчиков'),
            ('cat_crypto', 'Crypto Pro', '@cryptopro_ru', '1567890 подписчиков'),
            ('cat_crypto', 'Крипто-бык', '@cryptobull_ru', '923456 подписчиков'),
            ('cat_crypto', 'Bitcoin News RU', '@bitcoin_news_rus', '812300 подписчиков'),
            ('cat_crypto', 'Ethereum Russia', '@ethereum_russia', '654321 подписчиков'),
            ('cat_crypto', 'DeFi по-русски', '@defi_rus', '543210 подписчиков'),
            ('cat_crypto', 'NFT Мир', '@nft_world_ru', '432100 подписчиков'),
            ('cat_crypto', 'Bybit Russian', '@BybitRussian', '99236 участников'),
            ('cat_crypto', 'Vseznayka Chat', '@vseznayka_chat', '23683 участников'),
            ('cat_crypto', 'Web Investors', '@web_investors', '23279 участников'),
            ('cat_crypto', 'Cryptanci Chat', '@cryptancichat', '27660 участников'),
            ('cat_crypto', 'Starpets GG', '@starpetsgg_chat', '9258 участников'),
            ('cat_crypto', 'Ton Farm', '@TonFarm4at', '37006 участников'),
            ('cat_crypto', 'Rus CryptEx', '@RusCryptEx', '15909 участников'),
            ('cat_crypto', 'MEXC Russian', '@MEXCRussianOfficial', '25843 участников'),
            ('cat_crypto', 'Mining Irkutsk', '@mining_irkutskk', '12487 участников'),
            ('cat_crypto', 'Crypto Signals', '@crypto_signals_ru', '387654 подписчиков'),
            
            # НЕЙРОСЕТИ / AI 
            ('cat_ai', 'Нейросети | AI', '@neuronseti', '890123 подписчиков'),
            ('cat_ai', 'AI Revolution', '@ai_revolution_ru', '567890 подписчиков'),
            ('cat_ai', 'ChatGPT по-русски', '@chatgpt_rus', '456789 подписчиков'),
            ('cat_ai', 'Midjourney RU', '@midjourney_ru', '345678 подписчиков'),
            ('cat_ai', 'Искусственный Интеллект', '@ai_russia', '234567 подписчиков'),
            ('cat_ai', 'Нейросети для бизнеса', '@ai_business_ru', '198765 подписчиков'),
            ('cat_ai', 'Machine Learning RU', '@ml_rus', '187654 подписчиков'),
            ('cat_ai', 'AI Промпты', '@ai_prompts_ru', '176543 подписчиков'),
            ('cat_ai', 'Нейрографика', '@neurographica_ru', '165432 подписчиков'),
            ('cat_ai', 'AI Новости', '@ai_news_ru', '154321 подписчиков'),
            ('cat_ai', 'Stable Diffusion RU', '@stablediffusion_ru', '143210 подписчиков'),
            ('cat_ai', 'DALL-E Russia', '@dalle_russia', '132109 подписчиков'),
            ('cat_ai', 'AI Кодинг', '@ai_coding_ru', '121098 подписчиков'),
            
            # МАРКЕТИНГ / ПРОДВИЖЕНИЕ 
            ('cat_marketing', 'Трафик и Маркетинг', '@traffic_ru', '1234567 подписчиков'),
            ('cat_marketing', 'SMM Special', '@smmspecial', '789012 подписчиков'),
            ('cat_marketing', 'Контекстная реклама', '@context_rus', '678901 подписчиков'),
            ('cat_marketing', 'Арбитраж трафика', '@arbitrajnik', '567890 подписчиков'),
            ('cat_marketing', 'Email Маркетинг', '@email_marketing_ru', '456789 подписчиков'),
            ('cat_marketing', 'SEO Expert', '@seo_expert_ru', '345678 подписчиков'),
            ('cat_marketing', 'Копирайтинг PRO', '@copywriting_pro', '234567 подписчиков'),
            ('cat_marketing', 'Личный бренд', '@personal_brand_ru', '198765 подписчиков'),
            ('cat_marketing', 'ВКонтакте Маркетинг', '@vk_marketing', '187654 подписчиков'),
            ('cat_marketing', 'Telegram Marketing', '@tg_marketing_ru', '176543 подписчиков'),
            ('cat_marketing', 'Instagram Marketing', '@insta_marketing_ru', '165432 подписчиков'),
            ('cat_marketing', 'YouTube Продвижение', '@youtube_promo', '154321 подписчиков'),
            
            # АРБИТРАЖ / ТРАФИК 
            ('cat_arbitrage', 'Арбитражник', '@arbitrajnik_pro', '543210 подписчиков'),
            ('cat_arbitrage', 'Трафик Монстр', '@traffic_monster', '432109 подписчиков'),
            ('cat_arbitrage', 'CPA Network RU', '@cpa_network_ru', '321098 подписчиков'),
            ('cat_arbitrage', 'Вертикальный арбитраж', '@vertical_arbitrage', '210987 подписчиков'),
            ('cat_arbitrage', 'Трафик из соцсетей', '@social_traffic_ru', '198765 подписчиков'),
            ('cat_arbitrage', 'PPC Арбитраж', '@ppc_arbitrage', '187654 подписчиков'),
            
            # БЛОГИНГ / КОНТЕНТ 
            ('cat_blogging', 'Блогинг PRO', '@blogging_pro_ru', '456789 подписчиков'),
            ('cat_blogging', 'YouTube Мастер', '@youtube_master_ru', '345678 подписчиков'),
            ('cat_blogging', 'Контент-маркетинг', '@content_marketing_ru', '234567 подписчиков'),
            ('cat_blogging', 'Instagram PRO', '@instagram_pro_ru', '198765 подписчиков'),
            ('cat_blogging', 'Сторителлинг', '@storytelling_ru', '187654 подписчиков'),
            
            # IT / АВТОМАТИЗАЦИЯ 
            ('cat_it', 'Python RU', '@python_ru', '543210 подписчиков'),
            ('cat_it', 'JavaScript Russia', '@javascript_russia', '432109 подписчиков'),
            ('cat_it', 'DevOps по-русски', '@devops_rus', '321098 подписчиков'),
            ('cat_it', 'Базы данных', '@databases_ru', '210987 подписчиков'),
            ('cat_it', 'Кибербезопасность', '@cybersecurity_ru', '198765 подписчиков'),
        ]

        conn.executemany(
            """
            INSERT OR IGNORE INTO chats (category_id, name, username, subscribers)
            VALUES (?, ?, ?, ?)
            """, chats)

    def get_all_categories(self) -> List[Dict]:
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT id, name, emoji 
                FROM categories 
                ORDER BY name
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def get_channels_by_category(self, category_id: str, limit: int = 5, offset: int = 0) -> List[Dict]:
        """Получить каналы по категории с пагинацией"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                '''
                SELECT name, username, subscribers
                FROM chats 
                WHERE category_id = ?
                ORDER BY name
                LIMIT ? OFFSET ?
                ''', (category_id, limit, offset))
            return [dict(row) for row in cursor.fetchall()]

    def get_channels_count_by_category(self, category_id: str) -> int:
        """Получить общее количество каналов в категории"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                '''
                SELECT COUNT(*) 
                FROM chats 
                WHERE category_id = ?
                ''', (category_id,))
            return cursor.fetchone()[0]
        
    def get_category_info(self, category_id: str) -> Optional[Dict]:
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                '''
                SELECT id, name, emoji
                FROM categories
                WHERE id = ?
                ''', (category_id,))
            result = cursor.fetchone()
            return dict(result) if result else None


    #Поиск по клюючевым словам
    def search_channels(self, keyword: str, limit: int = 20) -> List[Dict]:
        """Поиск каналов по ключевым словам (без учета регистра)"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            
            # Приводим все к нижнему регистру для поиска
            search_pattern = f'%{keyword.lower()}%'
            
            cursor = conn.execute(
                '''
                SELECT c.name, c.username, c.subscribers, cat.name as category_name, cat.emoji
                FROM chats c
                JOIN categories cat ON c.category_id = cat.id
                WHERE LOWER(c.name) LIKE ? OR LOWER(c.username) LIKE ?
                ORDER BY c.name
                LIMIT ?
                ''', (search_pattern, search_pattern, limit))
            
            return [dict(row) for row in cursor.fetchall()]
            

chats_db = ChatsDatabase()
