# Importa a função create_app do módulo app, que é responsável por criar e configurar o aplicativo Flask.
from app import create_app

# Cria a aplicação Flask chamando a função create_app.
app = create_app()

# Verifica se este arquivo está sendo executado diretamente (e não importado como módulo).
if __name__ == '__main__':
    # Executa o servidor Flask no modo de depuração.
    # O modo debug permite recarregar automaticamente o servidor em caso de alterações no código
    # e exibe mensagens de erro detalhadas no navegador.
    app.run(debug=True)
