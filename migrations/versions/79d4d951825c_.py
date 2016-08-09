"""empty message

Revision ID: 79d4d951825c
Revises: None
Create Date: 2016-07-29 17:01:18.925721

"""

# revision identifiers, used by Alembic.
revision = '79d4d951825c'
down_revision = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('permissoes_roles',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('permissao_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permissao_id'], ['permissoes.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )
    op.create_table('usuarios',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('nome', sa.String(length=20), nullable=False),
    sa.Column('sobrenome', sa.String(length=20), nullable=False),
    sa.Column('idade', sa.String(length=3), nullable=False),
    sa.Column('genero', sa.String(length=1), nullable=False),
    sa.Column('hash_senha', sa.String(length=128), nullable=False),
    sa.Column('confirmado', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sugestoes_itempauta',
    sa.Column('num', sa.BigInteger(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('status_aprovado', sa.String(length=1), nullable=True),
    sa.Column('justif_reprovacao', sa.String(length=255), nullable=True),
    sa.Column('email_autor', sa.String(length=70), nullable=False),
    sa.Column('opcao_voto', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['email_autor'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['opcao_voto'], ['opcoes_voto.num'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('anexos',
    sa.Column('num', sa.BigInteger(), nullable=False),
    sa.Column('path', sa.String(length=50), nullable=False),
    sa.Column('usuario_google_drive', sa.String(length=70), nullable=True),
    sa.Column('sugestao_itempauta', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['sugestao_itempauta'], ['sugestoes_itempauta.num'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('itemspautas',
    sa.Column('num', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.String(length=70), server_default='APROVADO', nullable=True),
    sa.Column('num_assembleia', sa.BigInteger(), nullable=False),
    sa.Column('num_sugestao', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['num_assembleia'], ['assembleias.num'], ),
    sa.ForeignKeyConstraint(['num_sugestao'], ['sugestoes_itempauta.num'], ),
    sa.PrimaryKeyConstraint('num')
    )
    op.create_table('votos',
    sa.Column('num', sa.BigInteger(), nullable=False),
    sa.Column('nome', sa.String(length=70), nullable=False),
    sa.Column('email_autor', sa.String(length=70), nullable=False),
    sa.Column('num_itempauta', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['email_autor'], ['usuarios.id'], ),
    sa.ForeignKeyConstraint(['num_itempauta'], ['itemspautas.num'], ),
    sa.PrimaryKeyConstraint('num')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votos')
    op.drop_table('itemspautas')
    op.drop_table('anexos')
    op.drop_table('sugestoes_itempauta')
    op.drop_table('usuarios')
    op.drop_table('permissoes_roles')
    op.drop_table('roles')
    ### end Alembic commands ###
