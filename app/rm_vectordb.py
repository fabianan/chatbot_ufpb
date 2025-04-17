
import shutil
import os

pasta = "vector_db"

if os.path.exists(pasta):
    try:
        shutil.rmtree(pasta)
        print("✅ Pasta vector_db removida com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao tentar apagar a pasta: {e}")
