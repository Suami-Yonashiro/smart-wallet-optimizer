import yfinance as yf
import fundamentus as fd
import pandas as pd

print("=== TESTE yfinance ===")
acao = yf.Ticker("VALE3.SA")
info = acao.info

print(f"Empresa    : {info.get('longName', 'N/D')}")
print(f"Preço atual: R$ {info.get('currentPrice', 'N/D')}")
print(f"Div. Yield : {info.get('dividendYield', 'N/D')}")
print(f"P/L        : {info.get('trailingPE', 'N/D')}")

print("\n=== TESTE fundamentus ===")
resultado = fd.get_resultado_raw()
print(f"Total de ações encontradas: {len(resultado)}")
print("\nPrimeiras 5 ações:")
print(resultado.head())