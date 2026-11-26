from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud_completo_estudiante():
    payload = {
        "codigo": "TEST999",
        "nombres": "Ana",
        "apellidos": "Torres",
        "correo": "ana.torres.test@universidad.edu.pe",
        "carrera": "Ingenieria de Sistemas"
    }
    res_post = client.post("/estudiantes", json=payload)
    assert res_post.status_code == 201
    est_id = res_post.json()["id"]

    res_get = client.get(f"/estudiantes/{est_id}")
    assert res_get.status_code == 200
    assert res_get.json()["codigo"] == "TEST999"

    res_put = client.put(f"/estudiantes/{est_id}", json={
        "nombres": "Ana Maria",
        "apellidos": "Torres",
        "correo": "ana.torres.test@universidad.edu.pe",
        "carrera": "Ingenieria de Software"
    })
    assert res_put.status_code == 200

    res_del = client.delete(f"/estudiantes/{est_id}")
    assert res_del.status_code == 200
    assert client.get(f"/estudiantes/{est_id}").status_code == 404
