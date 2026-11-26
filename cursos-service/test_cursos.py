from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud_completo_curso():
    payload = {
        "codigo": "CUR999",
        "nombre": "Arquitectura de Microservicios",
        "creditos": 4,
        "docente": "Dr. Carlos Mendoza"
    }
    res_post = client.post("/cursos", json=payload)
    assert res_post.status_code == 201
    curso_id = res_post.json()["id"]

    res_get = client.get(f"/cursos/{curso_id}")
    assert res_get.status_code == 200
    assert res_get.json()["codigo"] == "CUR999"

    res_put = client.put(f"/cursos/{curso_id}", json={
        "nombre": "Arquitectura de Software Avanzada",
        "creditos": 4,
        "docente": "Dr. Carlos Mendoza"
    })
    assert res_put.status_code == 200

    res_del = client.delete(f"/cursos/{curso_id}")
    assert res_del.status_code == 200
    assert client.get(f"/cursos/{curso_id}").status_code == 404
