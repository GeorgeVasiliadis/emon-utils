import configparser
import getpass

def generate_config(CONFIG_FILE):
    config = configparser.ConfigParser(interpolation=None)
    config["Emon"] = {}
    config["DB"] = {}

    ### EmonIO Section
    print("--- Configure EmonIO ---")

    # IP
    default = "127.0.0.1"
    temp = input(f"IP of EmonPi ({default}): ")
    emon_ip = temp if temp else default

    # Bearer Credentials
    bearer_credentials = input("EmonPi Bearer Credentials (only the hash): ")
    if not bearer_credentials:
        bearer_credentials = "REPLACE_ME"
        print("Bearer Credentials cannot be omitted. This will cause trouble!")
        print(f"Please refer to http://{emon_ip}/feed/api, look up for the API-Key")
        print("and replace it in the generated config file.")
        input("Press enter to continue...")

    ### DBIO
    print("--- Configure DBIO ---")

    # IP
    default = "127.0.0.1"
    temp = input(f"IP of CouchDB Server ({default}): ")
    db_ip = temp if temp else default

    # Port
    default = "5984"
    temp = input(f"Port of CouchDB Server ({default}): ")
    db_port = temp if temp else default

    # Database Name
    db_name = input("CouchDB Database Name: ")
    if not db_name:
        db_name = "REPLACE_ME"
        print("Database Name cannot be omitted. This will cause trouble!")
        print("Please specify the predefined database")
        print("and replace it in the generated config file.")
        input("Press enter to continue...")

    # Document Name
    document_name = input("CouchDB Document Name: ")
    if not document_name:
        document_name = "REPLACE_ME"
        print("Document Name cannot be omitted. This will cause trouble!")
        print("Please specify the predefined document")
        print("and replace it in the generated config file.")
        input("Press enter to continue...")

    # Username and Password
    username = input("CouchDB Username: ")
    password = getpass.getpass("CouchDB Password: ")

    config["Emon"]["endpoint"] = f"http://{emon_ip}"
    config["Emon"]["bearer_credentials"] = bearer_credentials
    config["DB"]["endpoint"] = f"http://{db_ip}:{db_port}"
    config["DB"]["db_name"] = db_name
    config["DB"]["document_name"] = document_name
    config["DB"]["username"] = username
    config["DB"]["password"] = password

    with open(CONFIG_FILE, "w", encoding="utf8") as f_out:
        config.write(f_out)

    print(f"Config file was successfully generated at: {CONFIG_FILE}")
