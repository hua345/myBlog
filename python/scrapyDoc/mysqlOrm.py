from sqlalchemy import Column, create_engine, String, Integer, DateTime, BigInteger, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:


class Book(Base):
    # 表的名字:
    __tablename__ = 'book'

    # 表的结构:
    id = Column(BigInteger(), primary_key=True)
    book_name = Column(String(32), comment='书名')
    price = Column(DECIMAL(10, 2), comment='价格')
    create_at = Column(DateTime(timezone=True),
                       default=func.now(), comment='创建时间')
    update_at = Column(DateTime(timezone=True),
                       onupdate=func.now(), comment='修改时间')


testBookName = "python+mysql"
# 初始化数据库连接:
# echo=True,打印执行语句
engine = create_engine(
    'mysql+mysqlconnector://root:xxx@192.168.137.128:3306/fang', echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# 创建新User对象:
newBook = Book(book_name=testBookName, price='21')
# 添加到session:
session.add(newBook)
# 查询语句,filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# .first()
books = session.query(Book).filter(Book.book_name == testBookName).all()
for book in books:
    print(book.id, book.book_name, book.price, book.create_at, book.update_at)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()
