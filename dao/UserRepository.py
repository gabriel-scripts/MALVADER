database = []

# testando os requisitos funcionais com um banco de dados em memória

class UserRepository:
    def __init__(self):
        self.database = database

    def SaveUser(self, user):
        try:
            self.database.append(user)
            return print("User saved successfully!")
        
        except ValueError as e:
            print(f"Error: {e}")
    
    def Savecliente(self, user):
        try:
            self.database.append(user)
            return print("User saved successfully!")
        
        except ValueError as e:
            print(f"Error: {e}")

        return print("Cliente saved successfully!")

    def ListClientes(self):
        try:
            if not self.database:
                raise ValueError("No users found in the database.")
            
            for user in self.database:
                print(user)
        
        except ValueError as e:
            print(f"Error: {e}")

    def GetClienteById(self, id_cliente):
        try:
            for user in self.database:
                if user.id_cliente == id_cliente:
                    return user
            raise ValueError("User not found.")
        
        except ValueError as e:
            print(f"Error: {e}")

    def SaveUser(user):
        try:
            database.append(user)
            return print("User saved successfully!")
        
        except ValueError as e:
            print(f"Error: {e}")
        
    def Savecliente(user):
        try:
            database.append(user)
            return print("User saved successfully!")
        
        except ValueError as e:
            print(f"Error: {e}")

        return print("Cliente saved successfully!")

    def ListClientes():
        try:
            if not database:
                raise ValueError("No users found in the database.")
            
            for user in database:
                print(user)
        
        except ValueError as e:
            print(f"Error: {e}")

    def GetClienteById(id_cliente):
        try:
            for user in database:
                if user.id_cliente == id_cliente:
                    return user
            raise ValueError("User not found.")
        
        except ValueError as e:
            print(f"Error: {e}")