CREATE DATABASE IF NOT EXISTS db_cursos;
USE db_cursos;
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(120) NOT NULL,
    creditos INT NOT NULL,
    docente VARCHAR(120) NOT NULL
);

CREATE INDEX idx_cursos_docente ON cursos(docente);

DELIMITER //

CREATE PROCEDURE sp_crear_curso(
    IN p_codigo VARCHAR(20),
    IN p_nombre VARCHAR(120),
    IN p_creditos INT,
    IN p_docente VARCHAR(120)
)
BEGIN
    INSERT INTO cursos (codigo, nombre, creditos, docente)
    VALUES (p_codigo, p_nombre, p_creditos, p_docente);
    SELECT LAST_INSERT_ID() AS id;
END //

CREATE PROCEDURE sp_listar_cursos()
BEGIN
    SELECT id, codigo, nombre, creditos, docente FROM cursos;
END //

CREATE PROCEDURE sp_obtener_curso(IN p_id INT)
BEGIN
    SELECT id, codigo, nombre, creditos, docente
    FROM cursos
    WHERE id = p_id;
END //

CREATE PROCEDURE sp_actualizar_curso(
    IN p_id INT,
    IN p_codigo VARCHAR(20),
    IN p_nombre VARCHAR(120),
    IN p_creditos INT,
    IN p_docente VARCHAR(120)
)
BEGIN
    UPDATE cursos
    SET codigo = p_codigo,
        nombre = p_nombre,
        creditos = p_creditos,
        docente = p_docente
    WHERE id = p_id;
    SELECT ROW_COUNT() AS affected_rows;
END //

CREATE PROCEDURE sp_eliminar_curso(IN p_id INT)
BEGIN
    DELETE FROM cursos WHERE id = p_id;
    SELECT ROW_COUNT() AS affected_rows;
END //

DELIMITER ;