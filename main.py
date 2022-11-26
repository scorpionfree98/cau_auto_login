from reconnect_network import main
from utils.config import Config

if __name__ == "__main__":
    username, password, device_username = Config().process_user_profile_config()
    main(username, password, device_username)
