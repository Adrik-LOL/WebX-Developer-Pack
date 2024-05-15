import sys
import requests
import json

def print_color(text, color):
    """
    Print text in specified color.
    """
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "end": "\033[0m"
    }
    print(f"{colors[color]}{text}{colors['end']}")

def fetch_tlds():
    url = "http://api.buss.lol/tlds"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print_color(f"An error occurred while fetching TLDs: {e}", "red")
        return None

def register_domain(tld, domain_name, ip):
    url = "http://api.buss.lol/domain"
    body = {
        "tld": tld,
        "name": domain_name,
        "ip": ip
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=body)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print_color(f"An error occurred while registering the domain: {e}", "red")
        return None

def delete_domain(key):
    url = f"http://api.buss.lol/domain/{key}"
    try:
        response = requests.delete(url)
        return response.status_code
    except Exception as e:
        print_color(f"An error occurred while deleting the domain: {e}", "red")
        return None

def main():
    if len(sys.argv) < 2:
        print_color("Usage: python apibuss.py [domain] [--register] [--debug] [--delete <key>]", "yellow")
        return
    
    # Check if --register, --debug, or --delete flag is provided
    register_mode = "--register" in sys.argv
    debug_mode = "--debug" in sys.argv
    delete_mode = "--delete" in sys.argv

    if delete_mode:
        delete_index = sys.argv.index("--delete")
        delete_key = sys.argv[delete_index + 1]
        result = delete_domain(delete_key)
        if result == 200:
            print_color("Domain deleted successfully.", "green")
        else:
            print_color("Failed to delete domain.", "red")
        return
    
    if "--register" in sys.argv and "--debug" in sys.argv:
        # Remove --register and --debug from arguments to get domain
        args = sys.argv[1:-2]
    elif "--register" in sys.argv:
        # Remove --register from arguments to get domain
        args = sys.argv[1:-1]
    elif "--debug" in sys.argv:
        # Remove --debug from arguments to get domain
        args = sys.argv[1:-1]
    else:
        args = sys.argv[1:]  # Only domain
    
    for arg in args:
        if arg.startswith("-"):
            print_color(f"Unknown option: {arg}", "red")
            return
        
        domain = arg
        domain_name, tld = domain.split('.', 1) if '.' in domain else (domain, '')
        print_color(f"============================", "white")
        print_color(f"{'':^28}", "white")
        print_color(f"    Welcome to APIBuss!    ", "cyan")
        print_color(f"{'':^28}", "white")
        print_color(f"============================", "white")
        print_color(f"Provided domain: {arg}", "green")
        if debug_mode:
            print_color("----    DEBUGGING INFOS    ----", "purple")
            print_color(f"Domain name: {domain_name}", "blue")
            print_color(f"Top level domain: {tld}", "blue")
            print_color("---- ********************* ----", "purple")
        url = f"https://api.buss.lol/domain/{domain_name}/{tld}"
        
        if register_mode:
            print_color(f"{'':^28}", "white")
            # Prompt for IP address if --register is enabled
            ip = input("Enter IP address: ")
            result = register_domain(tld, domain_name, ip)
            if result:
                if "secret_key" in result:
                    print_color(
                        f"{'':^28}\nSuccess! Your key is: {result['secret_key']}\n\nMAKE SURE TO SAVE IT! You will need it to update/delete your domain.",
                        "green"
                    )
                elif "status" in result and result["status"] == 429:
                    print_color("Failed due to ratelimit.", "red")
                else:
                    print_color(f"Failed due to error: {result.get('status', 'unknown')}", "red")
        else:
            print_color(f"API URL: {url}", "cyan")
            try:
                response = requests.get(url)
    
                if response.status_code == 200:
                    print_color("Response from API:", "green")
                    # Parse the JSON response
                    data = json.loads(response.text)
                    print_color("Parsed JSON data:", "cyan")
                    print(json.dumps(data, indent=4))
                else:
                    print_color(f"Error: {response.status_code}", "red")
            except Exception as e:
                print_color(f"An error occurred: {e}", "red")


if __name__ == "__main__":
    main()
