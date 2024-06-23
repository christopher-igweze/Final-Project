import yaml
from sqlalchemy import create_engine, Column, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Path to the uploaded YAML file
yaml_file_path = r'C:\Users\USER\Documents\Important Files\Final Project\Version 3.0\Frontend\config.yaml'

# Path to the SQLite database file
db_path = r'sqlite:///C:\Users\USER\Documents\Important Files\Final Project\Version 3.0\class_schedule-02.db'  # Change this to your desired path

# Define the database update function
def update_database():
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    # Extract user data from the specific YAML structure
    users = data.get('credentials', {}).get('usernames', {})

    engine = create_engine(db_path)
    metadata = MetaData()

    users_table = Table(
        'users', metadata,
        Column('username', String, primary_key=True),
        Column('name', String),
        Column('email', String),
        Column('password', String)
    )

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    conn = engine.connect()
    for username, user_info in users.items():
        existing_user = conn.execute(users_table.select().where(users_table.c.username == username)).fetchone() # type: ignore
        if existing_user:
            update = users_table.update().where(users_table.c.username == username).values( # type: ignore
                name=user_info['name'],
                email=user_info['email'],
                password=user_info['password']
            )
            conn.execute(update)
        else:
            try:
                ins = users_table.insert().values(  # type: ignore
                    username=username,
                    name=user_info['name'],
                    email=user_info['email'],
                    password=user_info['password']
                )
                conn.execute(ins)
            except IntegrityError as e:
                print(f"Error inserting user {username}: {e}")

    conn.close()    # type: ignore
    print("Database updated successfully!")


