-- Criar a primeira ONG
INSERT INTO organizations (id, name) 
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'ONG Sabor do Bem');

-- Criar a segunda ONG
INSERT INTO organizations (id, name) 
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'ONG Mãos que Tecem');

-- 
-- Criar um usuário admin para a ONG 1 (Sabor do Bem)
-- Senha é 'senha123'
--
INSERT INTO users (id, email, password_hash, organization_id)
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'admin@sabordobem.org', '$2a$10$fP2i9iG5.gL3.W1K5y.wFe.3y.gC/qY.W/3y.gC/qY.W/3y.gC/q', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');

-- 
-- Criar um usuário admin para a ONG 2 (Mãos que Tecem)
-- Senha é 'senha123'
--
INSERT INTO users (id, email, password_hash, organization_id)
VALUES ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44', 'admin@maosquetecem.org', '$2a$10$fP2i9iG5.gL3.W1K5y.wFe.3y.gC/qY.W/3y.gC/qY.W/3y.gC/q', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22');


--
-- Produtos para a ONG 1 (Sabor do Bem) [Alimentos]
--
INSERT INTO products (name, description, price, category, stock_qty, weight_grams, organization_id)
VALUES 
('Bolo de Fubá Caseiro', 'Delicioso bolo de fubá com erva-doce, receita da vovó.', 35.50, 'Doces', 10, 500, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
('Pão de Mel Recheado', 'Pão de mel artesanal com recheio de doce de leite.', 8.00, 'Doces', 30, 80, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
('Geleia de Morango', 'Geleia 100% natural, sem conservantes.', 22.00, 'Conservas', 15, 250, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
('Biscoito de Polvilho', 'Pacote de biscoito de polvilho azedo.', 12.00, 'Salgados', 25, 150, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
('Cesta de Orgânicos Pequena', 'Mix de vegetais e frutas da estação.', 55.00, 'Orgânicos', 5, 2000, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11');

--
-- Produtos para a ONG 2 (Mãos que Tecem) [Artesanato/Vestuário]
--
INSERT INTO products (name, description, price, category, stock_qty, weight_grams, organization_id)
VALUES 
('Bolsa de Crochê (Colorida)', 'Bolsa de ombro feita à mão em crochê com linhas coloridas.', 120.00, 'Acessórios', 8, 300, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'),
('Caminho de Mesa Bordado', 'Lindo caminho de mesa bordado à mão.', 95.00, 'Casa', 5, 400, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'),
('Camiseta Tingimento Natural', 'Camiseta de algodão com tingimento natural (tie-dye).', 75.00, 'Vestuário', 12, 180, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'),
('Brinco de Capim Dourado', 'Par de brincos leves feitos de capim dourado.', 45.00, 'Acessórios', 20, 20, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22'),
('Rede de Descanso', 'Rede de descanso de casal em algodão cru.', 180.00, 'Casa', 3, 1500, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22');