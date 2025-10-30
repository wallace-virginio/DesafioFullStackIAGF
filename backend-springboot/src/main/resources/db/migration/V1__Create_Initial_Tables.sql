-- Tabela para as ONGs (Organizações)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para os Usuários (da staff da ONG)
-- Esta tabela é essencial para a segurança multi-tenancy
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Chave estrangeira que liga o usuário a UMA organização
    organization_id UUID NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_organization
        FOREIGN KEY(organization_id) 
        REFERENCES organizations(id)
);

-- Tabela de Produtos
-- Esta tabela também deve ter o organization_id para garantir a tenancy 
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Requisitos do CRUD [cite: 10]
    price DECIMAL(10, 2) NOT NULL, -- Suporta decimais para preços
    category VARCHAR(100),
    image_url VARCHAR(1024),
    stock_qty INT NOT NULL DEFAULT 0, -- Quantidade em estoque
    weight_grams INT, -- Peso em gramas
    
    -- Chave estrangeira que liga o produto à ONG dona
    organization_id UUID NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_product_organization
        FOREIGN KEY(organization_id) 
        REFERENCES organizations(id)
);

-- Tabela de Pedidos (Estrutura mínima)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Poderia ter um customer_id ou dados do cliente
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Itens do Pedido (Estrutura mínima)
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL, -- Preço no momento da compra
    
    -- Essencial para saber de qual ONG era o item
    organization_id UUID NOT NULL,
    
    CONSTRAINT fk_order
        FOREIGN KEY(order_id) 
        REFERENCES orders(id),
        
  -- referência dos produtos.
    
    CONSTRAINT fk_item_organization
        FOREIGN KEY(organization_id) 
        REFERENCES organizations(id)
);

-- Índices para otimizar consultas comuns
CREATE INDEX idx_products_organization_id ON products(organization_id);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_users_organization_id ON users(organization_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);