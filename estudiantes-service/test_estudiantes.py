from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crud_completo_estudiante():
    # 1. Crear estudiante
    payload = {
        "codigo": "TEST999",
        "nombres": "Juan Carlos",
        "apellidos": "Rojas Vega",
        "correo": "juan.rojas@universidad.edu.pe",
        "carrera": "Ingeniería Industrial",
    }
    res_create = client.post("/estudiantes", json=payload)
    assert res_create.status_code == 201
    data = res_create.json()
    est_id = data["id"]
    assert data["codigo"] == "TEST999"

    # 2. Obtener por ID
    res_get = client.get(f"/estudiantes/{est_id}")
    assert res_get.status_code == 200
    assert res_get.json()["nombres"] == "Juan Carlos"

    # 3. Actualizar
    payload["carrera"] = "Ingeniería de Software"
    res_put = client.put(f"/estudiantes/{est_id}", json=payload)
    assert res_put.status_code == 200
    assert res_put.json()["carrera"] == "Ingeniería de Software"

    # 4. Eliminar
    res_del = client.delete(f"/estudiantes/{est_id}")
    assert res_del.status_code == 200

    # 5. Verificar que ya no existe
    res_not_found = client.get(f"/estudiantes/{est_id}")
    assert res_not_found.status_code == 404