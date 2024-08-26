create table clientes (
    clienteid serial primary key,
    nome varchar(100) not null,
    email varchar(100) not null,
    datanascimento date not null,
    cidade varchar(50) not null
);

create table produtos (
    produtoid serial primary key,
    nomeproduto varchar(100) not null,
    categoria varchar(50) not null,
    preco decimal(10, 2) not null,
    estoque int not null
);

create table pedidos (
    pedidoid serial primary key,
    clienteid int references clientes(clienteid),
    datapredido date not null,
    valortotal decimal(10, 2) not null
);

create table itenspedido (
    itemid serial primary key,
    pedidoid int references pedidos(pedidoid),
    produtoid int references produtos(produtoid),
    quantidade int not null,
    precounitario decimal(10, 2) not null
);

-- lista 01 - pedro ramon

-- questões sobre funções (functions)

-- 1:
create or replace function calcularidade(datanascimento date)
returns int as $$
begin
    return extract(year from age(datanascimento));
end;
$$ language plpgsql;

-- 2:
create or replace function verificar_estoque(produtoid int)
returns int as $$
declare
    quantidadeestoque int;
begin
    select estoque into quantidadeestoque
    from produtos
    where produtoid = produtoid;
    return quantidadeestoque;
end;
$$ language plpgsql;

-- 3:
create or replace function calcular_desconto(produtoid int, percentualdesconto numeric)
returns numeric as $$
declare
    precofinal numeric;
    preçooriginal numeric;
begin
    select preco into preçooriginal
    from produtos
    where produtoid = produtoid;
    precofinal = preçooriginal - (preçooriginal * (percentualdesconto / 100));
    return precofinal;
end;
$$ language plpgsql;

-- 4:
create or replace function obter_nome_cliente(clienteid int)
returns varchar as $$
declare
    nomecliente varchar(100);
begin
    select nome into nomecliente
    from clientes
    where clienteid = clienteid;
    return nomecliente;
end;
$$ language plpgsql;

-- 5:
create or replace function calcular_frete(valortotal numeric, cidadecliente varchar)
returns numeric as $$
declare
    frete numeric;
begin
    if cidadecliente = 'são paulo' then
        frete = valortotal * 0.05;
    else
        frete = valortotal * 0.10;
    end if;
    return frete;
end;
$$ language plpgsql;

-- 6:
create or replace function calcular_pontos(clienteid int)
returns int as $$
declare
    totalpontos int default 0;
    valortotal numeric;
begin
    for valortotal in 
        select valortotal from pedidos where clienteid = clienteid
    loop
        if valortotal > 100 then
            totalpontos := totalpontos + 10;
        else
            totalpontos := totalpontos + 5;
        end if;
    end loop;
    return totalpontos;
end;
$$ language plpgsql;

-- questões sobre procedimentos armazenados (stored procedures)

-- 1:
create or replace procedure atualizar_estoque_em_massa(produtoids int[], quantidadeadicionar int)
language plpgsql
as $$
declare
    produtoid int;
begin
    foreach produtoid in array produtoids
    loop
        update produtos
        set estoque = estoque + quantidadeadicionar
        where produtoid = produtoid;
    end loop;
end;
$$;

-- 2:
create or replace procedure inserir_cliente(nome varchar, email varchar, datanascimento date, cidade varchar)
language plpgsql
as $$
begin
    insert into clientes (nome, email, datanascimento, cidade)
    values (nome, email, datanascimento, cidade);
end;
$$;

-- 3:
create or replace procedure realizar_pedido(clienteid int, datapredido date, itens jsonb)
language plpgsql
as $$
declare
    pedidoid int;
    item jsonb;
begin
    insert into pedidos (clienteid, datapredido, valortotal) 
    values (clienteid, datapredido, 0)
    returning pedidoid into pedidoid;

    for item in select * from jsonb_array_elements(itens)
    loop
        insert into itenspedido (pedidoid, produtoid, quantidade, precounitario)
        values (pedidoid, (item->>'produtoid')::int, (item->>'quantidade')::int, (item->>'precounitario')::numeric);

        update pedidos 
        set valortotal = valortotal + (item->>'quantidade')::int * (item->>'precounitario')::numeric
        where pedidoid = pedidoid;
    end loop;
end;
$$;

-- 4:
create or replace procedure excluir_cliente(clienteid int)
language plpgsql
as $$
begin
    delete from itenspedido where pedidoid in (select pedidoid from pedidos where clienteid = clienteid);
    delete from pedidos where clienteid = clienteid;
    delete from clientes where clienteid = clienteid;
end;
$$;

-- 5:
create or replace procedure atualizar_preço_produto(produtoid int, novopreco numeric)
language plpgsql
as $$
begin
    update produtos
    set preco = novopreco
    where produtoid = produtoid;
end;
$$;

-- 6:
create or replace procedure inserir_cliente_com_verificacao(nome varchar, email varchar, datanascimento date, cidade varchar)
language plpgsql
as $$
declare
    emailexiste int;
begin
    select count(*) into emailexiste from clientes where email = email;
    if emailexiste > 0 then
        raise exception 'erro: o email já existe na base de dados.';
    else
        insert into clientes (nome, email, datanascimento, cidade)
        values (nome, email, datanascimento, cidade);
    end if;
end;
$$;
