from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    accountid = Column(String, primary_key=True)
    balance = Column(Integer)

    def __repr__(self):
        return f'Account(acountid={self.accountid})'


class TrustLine(Base):
    __tablename__ = 'trustlines'

    accountid = Column(String, primary_key=True)
    asset = Column(String, primary_key=True)
    ledgerentry = Column(String)

    def __repr__(self):
        return f'TrustLine(accountid={self.accountid}, asset={self.asset})'


class LiquidityPool(Base):
    __tablename__ = 'liquiditypool'

    poolasset = Column(String, primary_key=True)
    asseta = Column(String)
    assetb = Column(String)
    ledgerentry = Column(String)

    def __repr__(self):
        return f'LiquidityPool(poolasset={self.poolasset})'


class ClaimableBalance(Base):
    __tablename__ = 'claimablebalance'

    balanceid = Column(String, primary_key=True)
    ledgerentry = Column(String)

    def __repr__(self):
        return f'ClaimableBalance(balanceid={self.balanceid})'
