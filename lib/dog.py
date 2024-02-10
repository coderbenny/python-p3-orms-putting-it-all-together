import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    # Initialization
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    # Creating a table
    @classmethod
    def create_table(cls):
        sql = """CREATE TABLE IF NOT EXISTS dogs (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       breed TEXT
        ) 
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Deleting a table if it exists
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Saving to the database
    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed) VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
            CONN.commit()
            return self
        else:
            print("Data already exists!")


    # Persisting an instance to the database
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        sql = """SELECT last_insert_rowid()"""
        dog.id = CURSOR.execute(sql).fetchone()[0]
        return dog
    
    # Retrieve all instances of the class from the database
    @classmethod
    def new_from_db(cls, row):
        if row is not None:
            dog = Dog(row[1], row[2])
            dog.id = row[0]
            return dog
        else:
            return None

    # Get all instance of the class saved in the database
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        dogs = CURSOR.execute(sql).fetchall()
        cls.alldogs = [cls.new_from_db(row) for row in dogs]
        return cls.alldogs

    # Get specific instance of the class by its name
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM dogs 
            WHERE name = ? 
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)

    # Get a specific instance of the class by its ID
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM dogs 
            WHERE id = ? 
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)

    # Search if a record exists, if not then add the record to the database        
    @classmethod
    def find_or_create_by(cls,name,breed):
        sql = """
            SELECT * FROM dogs 
            WHERE name=? AND breed=?
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if not dog:
            return cls.create(name,breed)
        else:
            print("Dog already exists!")
            return dog

    # Update a certain instance to match a record in the database
    def update(self): 
            sql = """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()
        
