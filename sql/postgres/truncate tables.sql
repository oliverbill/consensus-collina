truncate permissoes_roles CASCADE;
truncate permissoes CASCADE;
truncate anexos CASCADE;
truncate votos CASCADE;
truncate itemspautas CASCADE;
truncate sugestoes_itempauta CASCADE;
truncate usuarios CASCADE;
truncate comentarios CASCADE;
truncate roles CASCADE;
truncate opcoes_voto CASCADE;
truncate assembleias CASCADE;
truncate alembic_version;

alter sequence permissoes_id_seq restart;
alter sequence anexos_num_seq  restart;
alter sequence anexos_temp_num_seq  restart;
alter sequence votos_num_seq  restart;
alter sequence itemspautas_num_seq restart;
alter sequence sugestoes_itempauta_num_seq  restart;
alter sequence roles_id_seq  restart;
alter sequence opcoes_voto_num_seq restart;
alter sequence assembleias_num_seq restart;
alter sequence comentarios_num_seq restart;
alter sequence moradores_num_seq restart;
 

