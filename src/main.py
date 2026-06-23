from dataclasses import dataclass
from argparse import ArgumentParser

@dataclass
class User:
    name: str
    role: str

    def __post_init__(self):
        valid_roles = ["Operations Manager", "Admin", "Guest"]
        if self.role not in valid_roles:
            raise AttributeError("Invalid role")

def get_user_info(user: User) -> dict:
    """Return user info as a dictionary."""
    return {"name": user.name, "role": user.role}

def main():
    parser = ArgumentParser(description="Cannabis Ops Sync")
    parser.add_argument("--name", help="User name")
    parser.add_argument("--role", help="User role")
    args = parser.parse_args()
    try:
        user = User(args.name, args.role)
        print(get_user_info(user))
    except AttributeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
