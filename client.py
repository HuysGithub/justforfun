from Login import Login  
from HomePage import HomePage

def main():
    loginWindow = Login()
    try:
        HomePage(loginWindow.user, loginWindow.client_socket)
    except:
        pass

if __name__ == "__main__":
    main()