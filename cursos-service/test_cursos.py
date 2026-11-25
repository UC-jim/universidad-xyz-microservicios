from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crud_completo_curso():
    # 1. Crear curso
    payload = {
        "codigo": "CUR999",
        "nombre": "Base de Datos Avanzadas",
        "creditos": 4,
        "docente": "Mg. Laura Torres",
    }
    res_create = client.post("/cursos", json=payload)
    assert res_create.status_code == 201
    data = res_create.json()
    curso_id = data["id"]
    assert data["codigo"] == "CUR999"

    # 2. Obtener por ID
    res_get = client.get(f"/cursos/{curso_id}")
    assert res_get.status_code == 200
    assert res_get.json()["nombre"] == "Base de Datos Avanzadas"

    # 3. Actualizar
    payload["creditos"] = 5
    res_put = client.put(f"/cursos/{curso_id}", json=payload)
    assert res_put.status_code == 200
    assert res_put.json()["creditos"] == 5

    # 4. Eliminar
    res_del = client.delete(f"/cursos/{curso_id}")
    assert res_del.status_code == 200

    # 5. Verificar que ya no existe
    res_not_found = client.get(f"/cursos/{curso_id}")
    assert res_not_found.status_code == 404