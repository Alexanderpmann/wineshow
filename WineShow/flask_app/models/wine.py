from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# if in models folder, no need to add .name_of_model before import
from flask_app.models import sommelier


class Wine:
    def __init__(self, data):
        self.id = data["id"]

        self.name = data["name"]
        self.type = data["type"]
        self.age = data["age"]
        self.description = data["description"]
        self.sommelier_id = data["sommelier_id"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

# placeholder of empty sommelier for get all_wines query
        self.sommelier = {}

# sommelier_id is not needed to be validated as it should be in session already
    @staticmethod
    def validate_wine(data):
        is_valid = True
        if len(data["name"]) < 2:
            flash("Wine name must be at least 2 characters long!")
            is_valid = False
        if len(data["type"]) < 3:
            flash("Wine type must be at least 2 characters long!")
            is_valid = False
        if data["age"] == "":
            flash("Please enter an age for the wine!")
            is_valid = False
        elif int(data["age"]) < 0:
            flash("Wine age cannot be negative!")
            is_valid = False
        if len(data["description"]) < 10:
            flash("Wine description must be at least 10 characters long!")
            is_valid = False

        return is_valid

    @classmethod
    def create_wine(cls, data):
        query = "INSERT INTO wines (name, type, age, description, sommelier_id, created_at) VALUES (%(name)s, %(type)s, %(age)s, %(description)s, %(sommelier_id)s, NOW());"
        results = connectToMySQL("wine_schema").query_db(query, data)
        return results

# left join on the line that connects the 1 to many relationship in the erd
# wines tables -> sommelier_id + sommelier table -> id = wines.sommelier_id = sommeliers.id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM wines LEFT JOIN sommeliers ON wines.sommelier_id = sommeliers.id;"
        results = connectToMySQL("wine_schema").query_db(query)

        # time to parse
        # any overlapping fields with the 2nd model needs to be specified via ____.created_at, etc
        all_wines = []
        for row in results:
            wine = cls(row)
            sommelier_data = {
                "id": row["sommeliers.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["sommeliers.created_at"],
                "updated_at": row["sommeliers.updated_at"]
            }
# if in models folder - must reference the model name then class name
# if in controllers folder - can reference just the class name
            wine.sommelier = sommelier.Sommelier(sommelier_data)
            all_wines.append(wine)

        return all_wines

    @classmethod
    def get_wine_with_sommelier(cls, data):
        query = "SELECT * FROM wines LEFT JOIN sommeliers ON wines.sommelier_id = sommeliers.id WHERE wines.id = %(wine_id)s;"
        results = connectToMySQL("wine_schema").query_db(query, data)

        wine = cls(results[0])

        sommelier_data = {
            "id": results[0]["sommeliers.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["sommeliers.created_at"],
            "updated_at": results[0]["sommeliers.updated_at"]
        }
        wine.sommelier = sommelier.Sommelier(sommelier_data)
        return wine

    @classmethod
    def update_wine_info(cls, data):
        query = "UPDATE wines SET name = %(name)s, type = %(type)s, age = %(age)s, description = %(description)s, updated_at = NOW() WHERE id = %(wine_id)s;"
        results = connectToMySQL("wine_schema").query_db(query, data)
        return
        # update queries return nothing unless updated in site. no need to include a return here

    @classmethod
    def delete_wine(cls, data):
        query = "DELETE FROM wines WHERE id = %(wine_id)s;"
        results = connectToMySQL("wine_schema").query_db(query, data)
        return
