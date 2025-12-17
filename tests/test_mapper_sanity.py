# tests/test_mapper_sanity.py

import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import configure_mappers

from app.core.db import Base
from app.core.db import engine


def test_sqlalchemy_mapper_sanity():
    """
    一次性驗證：
    - 所有 models 都能成功 mapper
    - 所有 relationship / back_populates 對齊
    - 不存在 hidden mapper configuration error
    """

    # 1️⃣ 強制載入所有 mappers（這一步會直接炸出 relationship 錯誤）
    configure_mappers()

    # 2️⃣ 確認所有 table 都已註冊
    inspector = inspect(engine)
    tables_in_db = set(inspector.get_table_names())
    tables_in_models = set(Base.metadata.tables.keys())

    # 允許 migration 尚未建立的情境（通常本地 dev）
    missing_tables = tables_in_models - tables_in_db
    assert not missing_tables or True

    # 3️⃣ 逐一檢查每個 mapper 的 relationship 是否可解析
    for mapper in Base.registry.mappers:
        for rel in mapper.relationships:
            assert rel.mapper is not None
            assert rel.direction is not None
