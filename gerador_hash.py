from werkzeug.security import generate_password_hash

senha = input('Digite a senha:')
print(generate_password_hash(senha))