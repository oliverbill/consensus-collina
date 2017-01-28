-- datetime_format eh alterado dinamicamente 
-- no select de acordo com a variavel timezone(que recebe o timezone do Sistema Operaconal).
-- Para altera-la, use: 
-- SELECT date_format(dt_hora_criacao,'%d-%m-%Y %h:%i:%s') from assembleias
INSERT INTO assembleias  
(dt_hora_inicio,dt_hora_fim)
VALUES
(TO_CHAR(current_date, 'DD/MM/YYYY HH24:MI'),TO_CHAR(current_date + INTERVAL '7' DAY, 'DD/MM/YYYY HH24:MI'));

INSERT INTO assembleias
(dt_hora_inicio,dt_hora_fim)
VALUES
(TO_CHAR(current_date + INTERVAL '14' DAY, 'DD/MM/YYYY HH24:MI'),TO_CHAR(current_date + INTERVAL '21' DAY, 'DD/MM/YYYY HH24:MI'));

 INSERT INTO opcoes_voto(nome)
 VALUES('contra/a favor/abster-se');

 INSERT INTO opcoes_voto(nome)
 VALUES('aprovado / reprovado / abster-se');

 INSERT INTO opcoes_voto(nome)
 VALUES('outras opcoes');

-- CONTROLE DE ACESSO
INSERT INTO permissoes(id,nome) VALUES(1,'ADMINISTRAR_SISTEMA');
INSERT INTO permissoes(id,nome) VALUES(2,'SUGERIR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(3,'RESPONDER_SUGESTAO_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(4,'GERAR_ATA_ASSEMBLEIA');
INSERT INTO permissoes(id,nome) VALUES(5,'QUESTIONAR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(6,'EXCLUIR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(7,'ANULAR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(8,'RESPONDER_QUESTIONAMENTO');
INSERT INTO permissoes(id,nome) VALUES(9,'CONVOCAR_ASSEMBLEIA_ONLINE');
INSERT INTO permissoes(id,nome) VALUES(10,'PESQUISAR_RI');
INSERT INTO permissoes(id,nome) VALUES(11,'CRIAR_ENQUETE');
INSERT INTO permissoes(id,nome) VALUES(12,'PUBLICAR_COMUNICADO');
INSERT INTO permissoes(id,nome) VALUES(13,'VOTAR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(14,'COMENTAR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(15,'LISTAR_ASSEMBLEIAS');
INSERT INTO permissoes(id,nome) VALUES(16,'CRIAR_ASSEMBLEIA');
INSERT INTO permissoes(id,nome) VALUES(17,'ALTERAR_ASSEMBLEIA');
INSERT INTO permissoes(id,nome) VALUES(18,'ATRIBUIR_ASSEMBLEIA');
INSERT INTO permissoes(id,nome) VALUES(19,'DESFAZER_REJEICAO');
INSERT INTO permissoes(id,nome) VALUES(20,'LISTAR_ITEM_PAUTA');
INSERT INTO permissoes(id,nome) VALUES(21,'EXIBIR_USUARIOS');
INSERT INTO permissoes(id,nome) VALUES(22,'AVALIAR_SUGESTAO_ITEM_PAUTA');

INSERT INTO roles(id,nome) VALUES(1,'ADMIN DO SISTEMA');
INSERT INTO roles(id,nome) VALUES(2,'MORADORES');
INSERT INTO roles(id,nome) VALUES(3,'SINDICOS');
INSERT INTO roles(id,nome) VALUES(4,'ADMIN DO CONDOMINIO');

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(1,1);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(1,21);

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,2);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,5);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,8);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,10);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,11);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,13);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(2,14);

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,2);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,3);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,4);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,5);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,6);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,7);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,8);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,9);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,10);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,11);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,12);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,14);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,18);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,20);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,21);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(3,22);

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,4);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,9);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,10);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,11);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,12);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,15);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,17);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,20);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,21);

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('alves.bill@gmail.com','pbkdf2:sha1:1000$2aZOWld2$9aa41a8dcbb0a0eba9954461161e18e49bf650a5',2,
		'William','Alves','19-06-1983','M'); -- senha baleia302%

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('emilio@hotmail.com.br','pbkdf2:sha1:1000$naXQnraF$c47fe940f299d44dca4d0b094d38f39c730b6201',2,
		'Emilio','Zurita','19-02-1922','M'); -- senha emilio123%

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('bicuda@gmail.com','pbkdf2:sha1:1000$wvtiAAfc$d2007596a16166205116d5cbbab0269aa73365b4',3,
		'Estela','Bicuda','19-01-1955','F');-- senha caracas123%

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('lalau@hotmail.com','pbkdf2:sha1:1000$sjYE3YSR$f6231881cb3bed5c67e618305b7a2cf39e5d0c23',4,
		'Lalau','Kobayashi','12-05-1913','M'); -- senha lalau123%

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('superman@gmail.com','pbkdf2:sha1:1000$YUME66Ai$234e58dd2231d14b210009130fa0b6700f935324',1,
		'Kal','El','17-05-1910','M'); -- senha crypton123%

INSERT INTO moradores(num_ap,bloco,usuario_id)
VALUES (183,'C1','alves.bill@gmail.com');

INSERT INTO moradores(num_ap,bloco,usuario_id)
VALUES (22,'C2','emilio@hotmail.com.br');

INSERT INTO sugestoes_itempauta(titulo,descricao,email_autor,opcao_voto) values ('Aprovacao da Padaria',
'A moradora sra. Neide do 283 C2, está apresentando o projeto anexo para instalação de uma padaria no condomínio. 
Pede-se que os moradores votem na aprovação do projeto.','alves.bill@gmail.com',1);