from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Dados2(UserMixin, db.Model):  # tabela recebimentos

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String)
    conta_devedora = db.Column(db.String)
    conta_credora = db.Column(db.String)
    historico = db.Column(db.String)
    doc_deposito = db.Column(db.String)
    valor = db.Column(db.String)


class Dados(db.Model):  # tabela pagamentos

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String)
    conta_devedora = db.Column(db.String)
    conta_credora = db.Column(db.String)
    historico = db.Column(db.String)
    cpl_historico = db.Column(db.String)
    valor = db.Column(db.String)
    nat_despesa = db.Column(db.String)


class Entidade(db.Model):  # tabela entidade

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_entidade = db.Column(db.String)
    cnpj = db.Column(db.String)
    rua = db.Column(db.String)
    numero = db.Column(db.String)
    bairro = db.Column(db.String)
    cep = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)


class Convenio(db.Model):  # tabela convenio

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_convenio = db.Column(db.String)
    orgao_concessor = db.Column(db.String)
    num_contrato = db.Column(db.String)
    data_rec_recurso = db.Column(db.String)
    vr_total_convenio = db.Column(db.String)
    ano_exercicio = db.Column(db.String)
    saldo_anterior = db.Column(db.String)


class Lancamentos(db.Model):  # tabela lancamentos

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_lancamento = db.Column(db.String)
    data = db.Column(db.String)
    cod1_conta_devedora = db.Column(db.String)
    cod2_conta_devedora = db.Column(db.String)
    descricao_conta_devedora = db.Column(db.String)
    cod1_conta_credora = db.Column(db.String)
    cod2_conta_credora = db.Column(db.String)
    descricao_conta_credora = db.Column(db.String)
    cod_historico = db.Column(db.String)
    descricao_historico = db.Column(db.String)
    cpl_historico = db.Column(db.String)
    doc_deposito = db.Column(db.String)
    nat_despesa = db.Column(db.String)
    valor = db.Column(db.String)
