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

INSERT INTO roles(id,nome) VALUES(1,'ADMIN DO SISTEMA');
INSERT INTO roles(id,nome) VALUES(2,'MORADORES');
INSERT INTO roles(id,nome) VALUES(3,'SINDICOS');
INSERT INTO roles(id,nome) VALUES(4,'ADMIN DO CONDOMINIO');

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(1,1);
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

INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,4);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,9);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,10);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,11);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,12);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,15);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,17);
INSERT INTO permissoes_roles(role_id,permissao_id) VALUES(4,20);

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('alves.bill@gmail.com','pbkdf2:sha1:1000$KYl6HeL0$9dfed60d4b31e7533f529a2b3da65c3002c69995',2,
		'William','Alves','19-06-1983','M'); -- senha baleia302

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('bicuda@gmail.com','pbkdf2:sha1:1000$FMeVVA7l$fc308f7797fb05e714467075b6fb9ec06ff25f60',3,
		'Estela','Bicuda','19-01-1955','F');-- senha caracas

INSERT INTO usuarios(id,hash_senha,role_id,nome,sobrenome,dt_nascimento,genero)
VALUES ('superman@gmail.com','pbkdf2:sha1:1000$MNTOcpCz$77954fd0c6161a52efba94b99c1a0aca63d7155b',1,
		'Kal','El','17-05-1910','M'); -- senha crypton

INSERT INTO morador(num_ap,bloco,usuario_id)
VALUES (183,'C1','alves.bill@gmail.com');

INSERT INTO morador(num_ap,bloco,usuario_id)
VALUES (51,'B1','bicuda@gmail.com');

INSERT INTO morador(num_ap,bloco,usuario_id)
VALUES (273,'A1','alves.bill@gmail.com');