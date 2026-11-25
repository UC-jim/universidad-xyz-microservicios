CREATE DATABASE IF NOT EXISTS db_estudiantes;
USE db_estudiantes;
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    carrera VARCHAR(100) NOT NULL
);

CREATE INDEX idx_estudiantes_carrera ON estudiantes(carrera);

DELIMITER //

CREATE PROCEDURE sp_crear_estudiante(
    IN p_codigo VARCHAR(20),
    IN p_nombres VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_correo VARCHAR(120),
    IN p_carrera VARCHAR(100)
)
BEGIN
    INSERT INTO estudiantes (codigo, nombres, apellidos, correo, carrera)
    VALUES (p_codigo, p_nombres, p_apellidos, p_correo, p_carrera);
    SELECT LAST_INSERT_ID() AS id;
END //

CREATE PROCEDURE sp_listar_estudiantes()
BEGIN
    SELECT id, codigo, nombres, apellidos, correo, carrera FROM estudiantes;
END //

CREATE PROCEDURE sp_obtener_estudiante(IN p_id INT)
BEGIN
    SELECT id, codigo, nombres, apellidos, correo, carrera
    FROM estudiantes
    WHERE id = p_id;
END //

CREATE PROCEDURE sp_actualizar_estudiante(
    IN p_id INT,
    IN p_codigo VARCHAR(20),
    IN p_nombres VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_correo VARCHAR(120),
    IN p_carrera VARCHAR(100)
)
BEGIN
    UPDATE estudiantes
    SET codigo = p_codigo,
        nombres = p_nombres,
        apellidos = p_apellidos,
        correo = p_correo,
        carrera = p_carrera
    WHERE id = p_id;
    SELECT ROW_COUNT() AS affected_rows;
END //

CREATE PROCEDURE sp_eliminar_estudiante(IN p_id INT)
BEGIN
    DELETE FROM estudiantes WHERE id = p_id;
    SELECT ROW_COUNT() AS affected_rows;
END //

DELIMITER ;