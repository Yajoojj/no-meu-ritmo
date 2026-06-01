insert into public.usuarios_app (username, senha_hash)
values ('aluno', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')
on conflict (username) do nothing;

alter table public.materias
  add column if not exists usuario_id bigint references public.usuarios_app(id);

alter table public.sessoes_estudo
  add column if not exists usuario_id bigint references public.usuarios_app(id);

alter table public.planos_estudo
  add column if not exists usuario_id bigint references public.usuarios_app(id);

update public.materias
set usuario_id = (select id from public.usuarios_app where username = 'aluno')
where usuario_id is null;

update public.sessoes_estudo
set usuario_id = (select id from public.usuarios_app where username = 'aluno')
where usuario_id is null;

update public.planos_estudo
set usuario_id = (select id from public.usuarios_app where username = 'aluno')
where usuario_id is null;

alter table public.materias
  alter column usuario_id set not null;

alter table public.sessoes_estudo
  alter column usuario_id set not null;

alter table public.planos_estudo
  alter column usuario_id set not null;

alter table public.materias
  drop constraint if exists materias_nome_key;

create unique index if not exists materias_usuario_nome_key
  on public.materias (usuario_id, nome);

create index if not exists sessoes_estudo_usuario_id_idx
  on public.sessoes_estudo (usuario_id);

create index if not exists planos_estudo_usuario_id_idx
  on public.planos_estudo (usuario_id);
