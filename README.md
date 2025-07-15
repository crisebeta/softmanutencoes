# SoftManutenções

Sistema de Gerenciamento de Manutenções de Software desenvolvido com Django.

## Funcionalidades

- Sistema de autenticação completo (login, registro, recuperação de senha)
- Perfil de usuário com foto
- Interface responsiva com Bootstrap 5
- Gerenciamento de manutenções de software

## Tecnologias Utilizadas

- Python 3.13
- Django 5.1.5
- Bootstrap 5
- SQLite3

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/softmanutencoes.git
cd softmanutencoes
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

O sistema estará disponível em http://127.0.0.1:8000/

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 