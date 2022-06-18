from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .models import Dados, Dados2, Entidade, Convenio, Lancamentos
from . import db
import datetime

data_e_hora_atuais = datetime.datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/entidade')
@login_required
def entidade():
    return render_template('entidade.html', name=current_user.name)


@main.route('/entidade', methods=['GET', 'POST'])
@login_required
def entidade_post():
    if request.method == 'POST':
        nome_entidade = request.form.get('nome_entidade')
        cnpj = request.form.get('cnpj')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cep = request.form.get('cep')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        # cadastra uma nova entidade.
        entidade = Entidade(nome_entidade=nome_entidade, cnpj=cnpj, rua=rua,
                            numero=numero, bairro=bairro, cep=cep,
                            cidade=cidade, estado=estado, email=email,
                            telefone=telefone)

        # adiciona uma nova entidade no database "diario" na tabela "entidade"
        db.session.add(entidade)
        db.session.commit()
        return redirect(url_for('main.entidade'))


@main.route('/convenio')
@login_required
def convenio():
    return render_template('convenio.html', name=current_user.name)


@main.route('/convenio', methods=['GET', 'POST'])
@login_required
def convenio_post():
    if request.method == 'POST':
        nome_convenio = request.form.get('nome_convenio')
        orgao_concessor = request.form.get('orgao_concessor')
        num_contrato = request.form.get('num_contrato')
        data_rec_recurso = request.form.get('data_rec_recurso')
        vr_total_convenio = request.form.get('vr_total_convenio')
        ano_exercicio = request.form.get('ano_exercicio')
        saldo_anterior = request.form.get('saldo_anterior')

        # cadastra um novo convenio.
        convenio = Convenio(nome_convenio=nome_convenio, orgao_concessor=orgao_concessor,
                            num_contrato=num_contrato, data_rec_recurso=data_rec_recurso,
                            vr_total_convenio=vr_total_convenio, ano_exercicio=ano_exercicio,
                            saldo_anterior=saldo_anterior)

        # adiciona um novo convenio no database "diario" na tabela "convenio"
        db.session.add(convenio)
        db.session.commit()
        return redirect(url_for('main.convenio'))


@main.route('/pagamentos')
@login_required
def pagamentos():
    return render_template('pagamentos.html', name=current_user.name)


@main.route('/pagamentos', methods=['GET', 'POST'])
@login_required
def pagamentos_post():
    if request.method == 'POST':
        data = request.form.get('data')
        conta_devedora = request.form.get('conta_devedora')
        conta_credora = request.form.get('conta_credora')
        historico = request.form.get('historico')
        cpl_historico = request.form.get('cpl_historico')
        valor = request.form.get('valor')
        if '.' in valor:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        if ',' in valor:
            valor = valor.replace(',', '.')
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        else:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        nat_despesa = request.form.get('nat_despesa')

        # cria um novo pagamento.
        dados = Dados(data=data, conta_credora=conta_credora,
                      conta_devedora=conta_devedora,
                      historico=historico, cpl_historico=cpl_historico,
                      valor=valor, nat_despesa=nat_despesa)

        # adiciona um novo pagamento no database "diario" na tabela "dados"
        db.session.add(dados)
        db.session.commit()
        return redirect(url_for('main.pagamentos'))


@main.route('/recebimentos')
@login_required
def recebimentos():
    return render_template('recebimentos.html', name=current_user.name)


@main.route('/recebimentos', methods=['GET', 'POST'])
@login_required
def recebimentos_post():
    if request.method == 'POST':
        data = request.form.get('data')
        conta_devedora = request.form.get('conta_devedora')
        conta_credora = request.form.get('conta_credora')
        historico = request.form.get('historico')
        doc_deposito = request.form.get('doc_deposito')
        valor = request.form.get('valor')
        if '.' in valor:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        if ',' in valor:
            valor = valor.replace(',', '.')
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        else:
            valor = float(valor)
            valor = "{:.2f}".format(valor)

        # cria um novo pagamento.
        dados2 = Dados2(data=data, conta_devedora=conta_devedora,
                        conta_credora=conta_credora, historico=historico,
                        doc_deposito=doc_deposito, valor=valor)

        # adiciona um novo recebimento no database "diario" na tabela "dados2"
        db.session.add(dados2)
        db.session.commit()
        return redirect(url_for('main.recebimentos'))


# abre a tela para seleção de relatórios"
@main.route('/sel_relatorio1')
@login_required
def sel_relatorio1():
    return render_template('sel_relatorio1.html', name=current_user.name)


@main.route('/sel_relatorio1', methods=['GET', 'POST'])
def sel_relatorio1_post():
    global recurso, ano, mes, data_e_hora_em_texto, soma1, soma2, tot1, tot2

    dados = Dados.query.all()
    soma1 = 0
    tot1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        recurso = request.form.get('recurso')

    for i in dados:
        if ano == i.data[0:4] and mes == i.data[5:7] and i.conta_credora != 'Caixa':
            x = float(i.valor)
            soma1 += x
            tot1 += 1

    dados2 = Dados2.query.all()
    soma2 = 0
    tot2 = 0

    for i in dados2:
        if ano == i.data[0:4] and mes == i.data[5:7] and i.conta_devedora != 'Caixa':
            x = float(i.valor)
            soma2 += x
            tot2 += 1
    convenio = Convenio.query.all()
    entidade = Entidade.query.all()

    return render_template('relatorio1.html', name=current_user.name, dados=dados, dados2=dados2,
                           recurso=recurso, ano=ano, mes=mes, convenio=convenio, entidade=entidade,
                           data_e_hora_em_texto=data_e_hora_em_texto,
                           soma1=soma1, soma2=soma2, tot1=tot1, tot2=tot2)


@main.route('/relatorio1', methods=['GET', 'POST'])
@login_required
def relatorio1():
    return render_template('relatorio1.html', name=current_user.name)


@main.route('/sel_relatorio2')
@login_required
def sel_relatorio2():
    return render_template('sel_relatorio2.html', name=current_user.name)


@main.route('/sel_relatorio2', methods=['GET', 'POST'])
def sel_relatorio2_post():
    global recurso, ano, mes, data_e_hora_em_texto, soma1, soma2, tot1, tot2

    dados = Dados.query.all()
    soma1 = 0
    tot1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        recurso = request.form.get('recurso')

    for i in dados:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso == i.conta_credora[0:5]:
            x = float(i.valor)
            soma1 += x
            tot1 += 1

    dados2 = Dados2.query.all()
    soma2 = 0
    tot2 = 0
    for i in dados2:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso == i.conta_devedora[0:5]:
            x = float(i.valor)
            soma2 += x
            tot2 += 1

    convenio = Convenio.query.all()
    entidade = Entidade.query.all()

    return render_template('relatorio2.html', name=current_user.name, dados=dados, dados2=dados2,
                           recurso=recurso, ano=ano, mes=mes, convenio=convenio, entidade=entidade,
                           data_e_hora_em_texto=data_e_hora_em_texto,
                           soma1=soma1, soma2=soma2, tot1=tot1, tot2=tot2)


@main.route('/relatorio2', methods=['GET', 'POST'])
@login_required
def relatorio2():
    return render_template('relatorio2.html', name=current_user.name)


 # abre a tela para seleção consulta lançamentos de pagamentos e recebimentos
@main.route('/sel_consulta1')
@login_required
def sel_consulta1():
    return render_template('sel_consulta1.html', name=current_user.name)


@main.route('/sel_consulta1', methods=['GET', 'POST'])
def consultas_pagamentos():
    global ano, mes, soma1
    dados = Dados.query.all()
    soma1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    for i in dados:
        if ano == i.data[0:4] and mes == i.data[5:7]:
            x = float(i.valor)
            soma1 += x

    return render_template('consulta1.html', name=current_user.name, dados=dados,
                           ano=ano, mes=mes, soma1=soma1)


@main.route('/consulta1')  # renderiza o formulario da consulta de pagamentos
@login_required
def consulta1():
    return render_template('consulta1.html', name=current_user.name)


@main.route('/sel_consulta2')
@login_required
def sel_consulta2():
    return render_template('sel_consulta2.html', name=current_user.name)


@main.route('/sel_consulta2', methods=['GET', 'POST'])
def consultas_recebimentos():
    global ano, mes, soma2
    dados2 = Dados2.query.all()
    soma2 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    for i in dados2:
        if ano == i.data[0:4] and mes == i.data[5:7]:
            x = float(i.valor)
            soma2 += x

    return render_template('consulta2.html', name=current_user.name, dados2=dados2,
                           ano=ano, mes=mes, soma2=soma2)


@main.route('/consulta2')  # renderiza o formulario da consulta de recebimentos
@login_required
def consulta2():
    return render_template('consulta2.html', name=current_user.name)


@main.route('/consulta3')  # consulta a entidade
@login_required
def consulta3():
    entidade = Entidade.query.all()
    return render_template('consulta3.html', name=current_user.name, entidade=entidade)


@main.route('/consulta4')  # consulta o convenio
@login_required
def consulta4():
    convenio = Convenio.query.all()
    return render_template('consulta4.html', name=current_user.name, convenio=convenio)


@main.route('/sel_exportar1')
@login_required
def sel_exportar1():
    return render_template('sel_exportar1.html', name=current_user.name)


@main.route('/sel_exportar1', methods=['GET', 'POST'])
def exportar_dados1():
    global ano, mes
    lancamentos = Lancamentos.query.all()

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    return render_template('exportar1.html', name=current_user.name, lancamentos=lancamentos,
                           ano=ano, mes=mes)


@main.route("/excluir1/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir1(id):
    dados = Dados.query.filter_by(id=id).first()
    if request.method == 'POST':
        if dados:
            db.session.delete(dados)
            db.session.commit()
            return redirect(url_for('main.consulta1'))
    return render_template('delete.html')


@main.route("/excluir2/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir2(id):
    dados2 = Dados2.query.filter_by(id=id).first()
    if request.method == 'POST':
        if dados2:
            db.session.delete(dados2)
            db.session.commit()
            return redirect(url_for('main.consulta2'))
    return render_template('delete.html')


@main.route("/excluir3/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir3(id):
    entidade = Entidade.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entidade:
            db.session.delete(entidade)
            db.session.commit()
            return redirect(url_for('main.consulta3'))
    return render_template('delete.html')


@main.route("/excluir4/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir4(id):
    convenio = Convenio.query.filter_by(id=id).first()
    if request.method == 'POST':
        if convenio:
            db.session.delete(convenio)
            db.session.commit()
            return redirect(url_for('main.consulta4'))
    return render_template('delete.html')


@main.route("/atualizar1/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar1(id):
    dados = Dados.query.filter_by(id=id).first()
    if request.method == 'POST':
        if dados:
            db.session.delete(dados)
            db.session.commit()

            data = request.form.get('data')
            conta_devedora = request.form.get('conta_devedora')
            conta_credora = request.form.get('conta_credora')
            historico = request.form.get('historico')
            cpl_historico = request.form.get('cpl_historico')
            valor = request.form.get('valor')
            nat_despesa = request.form.get('nat_despesa')

            # cria um novo pagamento.
            dados = Dados(data=data, conta_credora=conta_credora,
                          conta_devedora=conta_devedora,
                          historico=historico, cpl_historico=cpl_historico,
                          valor=valor, nat_despesa=nat_despesa)
            db.session.add(dados)
            db.session.commit()
            return redirect(url_for('main.sel_consulta1'))

    return render_template('atualizar1.html', dados=dados)


@main.route("/atualizar2/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar2(id):
    dados2 = Dados2.query.filter_by(id=id).first()
    if request.method == 'POST':
        if dados2:
            db.session.delete(dados2)
            db.session.commit()

            data = request.form.get('data')
            conta_devedora = request.form.get('conta_devedora')
            conta_credora = request.form.get('conta_credora')
            historico = request.form.get('historico')
            doc_deposito = request.form.get('doc_deposito')
            valor = request.form.get('valor')
            dados2 = Dados2(data=data, conta_devedora=conta_devedora,
                            conta_credora=conta_credora, historico=historico,
                            doc_deposito=doc_deposito, valor=valor)

            db.session.add(dados2)
            db.session.commit()
            return redirect(url_for('main.sel_consulta2'))
    return render_template('atualizar2.html', dados2=dados2)


@main.route("/atualizar3/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar3(id):
    entidade = Entidade.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entidade:
            db.session.delete(entidade)
            db.session.commit()

            nome_entidade = request.form.get('nome_entidade')
            cnpj = request.form.get('cnpj')
            rua = request.form.get('rua')
            numero = request.form.get('numero')
            bairro = request.form.get('bairro')
            cep = request.form.get('cep')
            cidade = request.form.get('cidade')
            estado = request.form.get('estado')
            email = request.form.get('email')
            telefone = request.form.get('telefone')

        entidade = Entidade(nome_entidade=nome_entidade, cnpj=cnpj, rua=rua,
                            numero=numero, bairro=bairro, cep=cep,
                            cidade=cidade, estado=estado, email=email,
                            telefone=telefone)

        db.session.add(entidade)
        db.session.commit()
        return redirect(url_for('main.consulta3'))
    return render_template('atualizar3.html', entidade=entidade)


@main.route("/atualizar4/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar4(id):
    convenio = Convenio.query.filter_by(id=id).first()
    if request.method == 'POST':
        if convenio:
            db.session.delete(convenio)
            db.session.commit()

            nome_convenio = request.form.get('nome_convenio')
            orgao_concessor = request.form.get('orgao_concessor')
            num_contrato = request.form.get('num_contrato')
            data_rec_recurso = request.form.get('data_rec_recurso')
            vr_total_convenio = request.form.get('vr_total_convenio')
            ano_exercicio = request.form.get('ano_exercicio')
            saldo_anterior = request.form.get('saldo_anterior')

            convenio = Convenio(nome_convenio=nome_convenio, orgao_concessor=orgao_concessor,
                                num_contrato=num_contrato, data_rec_recurso=data_rec_recurso,
                                vr_total_convenio=vr_total_convenio, ano_exercicio=ano_exercicio,
                                saldo_anterior=saldo_anterior)

            db.session.add(convenio)
            db.session.commit()
            return redirect(url_for('main.consulta4'))
    return render_template('atualizar4.html', convenio=convenio)
