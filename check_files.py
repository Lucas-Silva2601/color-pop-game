import os

# Caminhos que o jogo está tentando encontrar
font_modern_path = 'assets/fonts/ModernFont.ttf'
font_pixel_path = 'assets/fonts/PixelFont.ttf'

print("--- Verificando a existência dos arquivos de fonte ---")

# Verifica o primeiro arquivo
if os.path.exists(font_modern_path):
    print(f"✅ SUCESSO: O arquivo '{font_modern_path}' foi encontrado.")
else:
    print(f"❌ FALHA: O arquivo '{font_modern_path}' NÃO foi encontrado.")
    print(f"   Python está procurando em: {os.path.abspath(font_modern_path)}")

print("-" * 20)

# Verifica o segundo arquivo
if os.path.exists(font_pixel_path):
    print(f"✅ SUCESSO: O arquivo '{font_pixel_path}' foi encontrado.")
else:
    print(f"❌ FALHA: O arquivo '{font_pixel_path}' NÃO foi encontrado.")
    print(f"   Python está procurando em: {os.path.abspath(font_pixel_path)}")

print("\nSe algum arquivo falhou, verifique se o caminho acima está 100% correto.")