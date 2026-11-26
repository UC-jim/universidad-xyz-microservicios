import sys, os, importlib.util
from fastapi.testclient import TestClient

SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
for mod in ["main", "repository", "models", "database"]:
    sys.modules.pop(mod, None)
if SERVICE_DIR not in sys.path:
    sys.path.insert(0, SERVICE_DIR)

spec = importlib.util.spec_from_file_location("cur_main", os.path.join(SERVICE_DIR, "main.py"))
cur_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cur_main)

client = TestClient(cur_main.app)

def test_crud_completo_curso():
    payload = {
        "codigo": f"CUR{os.getpid()}",
        "nombre": "Arquitectura de Microservicios",
        "creditos": 4,
        "docente": "Dr. Carlos Mendoza"
    }
    res_post = client.post("/cursos", json=payload)
    assert res_post.status_code == 201
    curso_id = res_post.json()["id"]

    res_get = client.get(f"/cursos/{curso_id}")
    assert res_get.status_code == 200
    assert res_get.json()["codigo"] == f"CUR{os.getpid()}"

    res_put = client.put(f"/cursos/{curso_id}", json={
        "codigo": f"CUR{os.getpid()}",
        "nombre": "Arquitectura de Software Avanzada",
        "creditos": 4,
        "docente": "Dr. Carlos Mendoza"
    })
    assert res_put.status_code == 200

    res_del = client.delete(f"/cursos/{curso_id}")
    assert res_del.status_code == 200
    assert client.get(f"/cursos/{curso_id}").status_code == 404
