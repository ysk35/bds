from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import os
# postgresqlのDBの設定
DATABASE = "os.environ['DATABASE_URL']"

# Engineの作成
ENGINE = create_engine(
  DATABASE,
  encoding="utf-8",
  # TrueにするとSQLが実行される度に出力される
  echo=True
)

# Sessionの作成
session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
  sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE
  )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()