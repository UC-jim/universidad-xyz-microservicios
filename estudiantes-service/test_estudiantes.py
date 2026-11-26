import sys, os, importlib.util
from fastapi.testclient import TestClient

SERVICE_DIR = os.path.dirname(os.path.abspath(__file__))
for mod in ["main", "repository", "models", "database"]:
    sys.modules.pop(mod, None)
if SERVICE_DIR not in sys.path:
    sys.path.insert(0, SERVICE_DIR)

spec = importlib.util.spec_from_file_location("est_main", os.path.join(SERVICE_DIR, "main.py"))
est_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est_main)

client = TestClient(est_main.app)

def test_crud_completo_estudiante():
    uid = os.getpid()
    payload = {
        "codigo": f"EST{uid}",
        "nombres": "Ana",
        "apellidos": "Torres",
        "correo": f"ana.{uid}@universidad.edu.pe",
        "carrera": "Ingenieria de Sistemas"
    }
    res_post = client.post("/estudiantes", json=payload)
    assert res_post.status_code == 201
    est_id = res_post.json()["id"]

    res_get = client.get(f"/estudiantes/{est_id}")
    assert res_get.status_code == 200
    assert res_get.json()["codigo"] == f"EST{uid}"

    res_put = client.put(f"/estudiantes/{est_id}", json={
        "codigo": f"EST{uid}",
        "nombres": "Ana Maria",
        "apellidos": "Torres",
        "correo": f"ana.{uid}@universidad.edu.pe",
        "carrera": "Ingenieria de Software"
    })
    assert res_put.status_code == 200

    res_del = client.delete(f"/estudiantes/{est_id}")
    assert res_del.status_code == 200
    assert client.get(f"/estudiantes/{est_id}").status_code == 404
