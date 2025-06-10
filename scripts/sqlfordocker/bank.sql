CREATE DATABASE IF NOT EXISTS MALVADER;
USE MALVADER;

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(15),
    tipo_usuario ENUM('cliente', 'funcionario', 'admin') NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    otp_ativo VARCHAR(6),
    otp_expiracao DATETIME,
    PRIMARY KEY(id_usuario)
);

CREATE TABLE endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    cep VARCHAR(8) NOT NULL,
    local VARCHAR(100) NOT NULL,
    numero_casa VARCHAR(10) NOT NULL,
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    estado CHAR(2) NOT NULL,
    complemento VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNIQUE NOT NULL,
    score_credito INT DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE agencia (
    id_agencia INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo_agencia VARCHAR(20) UNIQUE NOT NULL,
    endereco_id INT NOT NULL,
    FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
);

CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNIQUE NOT NULL,
    codigo_funcionario VARCHAR(20) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    id_supervisor INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_supervisor) REFERENCES funcionario(id_funcionario)
);

CREATE TABLE conta (
    id_conta INT AUTO_INCREMENT PRIMARY KEY,
    numero_conta VARCHAR(20) UNIQUE NOT NULL,
    id_agencia INT NOT NULL,
    saldo DECIMAL(15,2) DEFAULT 0.00,
    tipo_conta ENUM('poupanca', 'corrente', 'investimento') NOT NULL,
    id_cliente INT NOT NULL,
    data_abertura DATE NOT NULL,
    status ENUM('ativa', 'inativa', 'bloqueada') DEFAULT 'ativa',
    FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE conta_poupanca (
    id_conta_poupanca INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE NOT NULL,
    taxa_rendimento DECIMAL(5,4) NOT NULL,
    ultimo_rendimento DATE,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_corrente (
    id_conta_corrente INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE NOT NULL,
    limite DECIMAL(15,2) DEFAULT 0.00,
    data_vencimento DATE,
    taxa_manutencao DECIMAL(5,2),
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_investimento (
    id_conta_investimento INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT UNIQUE NOT NULL,
    perfil_risco ENUM('conservador', 'moderado', 'arrojado') NOT NULL,
    valor_minimo DECIMAL(15,2) NOT NULL,
    taxa_rendimento_base DECIMAL(5,4) NOT NULL,
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE transacao (
    id_transacao INT AUTO_INCREMENT PRIMARY KEY,
    id_conta_origem INT NOT NULL,
    id_conta_destino INT,
    tipo_transacao ENUM('deposito', 'saque', 'transferencia', 'pagamento', 'investimento') NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descricao VARCHAR(255),
    FOREIGN KEY (id_conta_origem) REFERENCES conta(id_conta),
    FOREIGN KEY (id_conta_destino) REFERENCES conta(id_conta)
);

CREATE TABLE emprestimo (
    id_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_conta INT NOT NULL,
    valor_solicitado DECIMAL(15,2) NOT NULL,
    valor_aprovado DECIMAL(15,2),
    taxa_juros DECIMAL(5,2),
    prazo_meses INT,
    status ENUM('PENDENTE', 'APROVADO', 'NEGADO', 'PAGO') DEFAULT 'PENDENTE',
    data_solicitacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_aprovacao DATETIME,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    acao VARCHAR(50) NOT NULL,
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    detalhes TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE relatorio (
    id_relatorio INT AUTO_INCREMENT PRIMARY KEY,
    id_funcionario INT NOT NULL,
    tipo_relatorio VARCHAR(50) NOT NULL,
    data_geracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    conteudo TEXT,
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

DELIMITER $$
CREATE PROCEDURE gerar_otp(IN id_usuario INT)
BEGIN
    DECLARE novo_otp VARCHAR(6);
    SET novo_otp = LPAD(FLOOR(RAND() * 1000000), 6, '0');
    UPDATE usuario SET otp_ativo = novo_otp, otp_expiracao = NOW() + INTERVAL 5 MINUTE
    WHERE id_usuario = id_usuario;
    SELECT novo_otp;
END $$
DELIMITER ;