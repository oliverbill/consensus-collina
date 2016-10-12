-- datetime_format eh alterado dinamicamente 
-- no select de acordo com a variavel timezone(que recebe o timezone do Sistema Operaconal).
-- Para altera-la, use: 
-- SELECT date_format(dt_hora_criacao,'%d-%m-%Y %h:%i:%s') from assembleias
INSERT INTO `consensus`.`assembleias`
(`dt_hora_inicio`,`dt_hora_fim`)
VALUES
(DATE_FORMAT(NOW(), '%d/%m/%Y %h:%i'),DATE_FORMAT(NOW() + INTERVAL 7 DAY, '%d/%m/%Y %h:%i'));

INSERT INTO `consensus`.`assembleias`
(`dt_hora_inicio`,`dt_hora_fim`)
VALUES
(DATE_FORMAT(NOW() + INTERVAL 14 DAY, '%d/%m/%Y %h:%i'),DATE_FORMAT(NOW() + INTERVAL 21 DAY, '%d/%m/%Y %h:%i'));

 INSERT INTO `consensus`.`opcoes_voto`(nome)
 VALUES('contra/a favor/abster-se');

 INSERT INTO `consensus`.`opcoes_voto`(nome)
 VALUES('aprovado / reprovado / abster-se');

 INSERT INTO `consensus`.`opcoes_voto`(nome)
 VALUES('outras opcoes');

-- CONTROLE DE ACESSO
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('ADMINISTRAR_SISTEMA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('SUGERIR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('RESPONDER_SUGESTAO_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('GERAR_ATA_ASSEMBLEIA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('QUESTIONAR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('EXCLUIR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('ANULAR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('RESPONDER_QUESTIONAMENTO');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('CONVOCAR_ASSEMBLEIA_ONLINE');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('PESQUISAR_RI');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('CRIAR_ENQUETE');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('PUBLICAR_COMUNICADO');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('VOTAR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('COMENTAR_ITEM_PAUTA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('LISTAR_ASSEMBLEIAS');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('CRIAR_ASSEMBLEIA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('ALTERAR_ASSEMBLEIA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('ATRIBUIR_ASSEMBLEIA');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('DESFAZER_REJEICAO');
INSERT INTO `consensus`.`permissoes`(`nome`) VALUES('LISTAR_ITEM_PAUTA');

INSERT INTO `consensus`.`roles`(`nome`) VALUES('ADMIN DO SISTEMA');
INSERT INTO `consensus`.`roles`(`nome`) VALUES('MORADORES');
INSERT INTO `consensus`.`roles`(`nome`) VALUES('SINDICOS');
INSERT INTO `consensus`.`roles`(`nome`) VALUES('ADMIN DO CONDOMINIO');

INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(1,1);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,2);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,5);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,8);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,10);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,11);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,13);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,14);

INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(3,2);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,3);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,4);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,5);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,6);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,7);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,8);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,9);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,10);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,11);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,12);
INSERT INTO `consensus`.`permissoes_roles`(`role_id`,`permissao_id`) VALUES(2,14);

INSERT INTO `consensus`.`usuarios`(`id`,`hash_senha`,`role_id`,`nome`,`sobrenome`,`dt_nascimento`,`genero`)
VALUES ('alves.bill@gmail.com','pbkdf2:sha1:1000$KYl6HeL0$9dfed60d4b31e7533f529a2b3da65c3002c69995',2,
		'William','Alves',DATE_FORMAT(MAKEDATE(1983,170), '%d/%m/%Y'),'M'); -- senha baleia302

INSERT INTO `consensus`.`usuarios`(`id`,`hash_senha`,`role_id`,`nome`,`sobrenome`,`dt_nascimento`,`genero`)
VALUES ('bicuda@gmail.com','pbkdf2:sha1:1000$FMeVVA7l$fc308f7797fb05e714467075b6fb9ec06ff25f60',3,
		'Estela','Bicuda',DATE_FORMAT(MAKEDATE(1901,55), '%d/%m/%Y'),'F');-- senha caracas

INSERT INTO `consensus`.`usuarios`(`id`,`hash_senha`,`role_id`,`nome`,`sobrenome`,`dt_nascimento`,`genero`)
VALUES ('superman@gmail.com','pbkdf2:sha1:1000$MNTOcpCz$77954fd0c6161a52efba94b99c1a0aca63d7155b',1,
		'Kal','El',DATE_FORMAT(MAKEDATE(1735,301), '%d/%m/%Y'),'M'); -- senha crypton

INSERT INTO `consensus`.`morador`(`num_ap`,`bloco`,`usuario_id`)
VALUES (183,'C1','alves.bill@gmail.com');

INSERT INTO `consensus`.`morador`(`num_ap`,`bloco`,`usuario_id`)
VALUES (51,'B1','bicuda@gmail.com');

INSERT INTO `consensus`.`morador`(`num_ap`,`bloco`,`usuario_id`)
VALUES (273,'A1','alves.bill@gmail.com');


