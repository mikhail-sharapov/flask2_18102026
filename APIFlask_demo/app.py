from apiflask import APIFlask, EmptySchema, HTTPError
from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf


app = APIFlask(__name__, title="Example API", version="1.0")
app.tags = ["pets"]


class PetIn(Schema):
    name = String(required=True, validate=Length(3,10))
    category = String(required=True, validate=OneOf(["dog", "cat"]))


class PetOut(Schema):
    id = Integer()
    name = String()
    category = String()


@app.get("/pets/<int:pet_id>")
@app.output(PetOut)
@app.doc(summary="Get pet by id", description="Get pet dy id", tags=["pets"])
def get_pet_by_id(pet_id):
    if pet_id == 2:
        raise HTTPError(404, f"Pet with id={pet_id} not found")
    return {
        "id": pet_id,
        "name": "Coco",
        "category": "dog"
    }


@app.get("/pets")
@app.output(PetOut(many=True))
@app.doc(summary="Get all pets", description="Get all pets", tags=["pets"])
def get_all_pets():
    return [{
        "id": 1,
        "name": "Coco",
        "category": "dog"
    }]


@app.post("/pets")
@app.input(PetIn, location="json", arg_name="pet")
@app.output(PetOut, status_code=201)
@app.doc(summary="Create new pets", description="Create new pets", tags=["pets"])
def create_pet(pet):
    pet.update({"id": 101})
    return pet


@app.delete("/pets/<int:pet_id>")
@app.output(EmptySchema, status_code=204)
@app.doc(summary="Detete pet by id", description="Detete pet by id", tags=["pets"])
def delete_pet_by_id(pet_id):
    return ""