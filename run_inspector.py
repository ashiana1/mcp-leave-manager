
import subprocess

def main():
    command = "npx -y @modelcontextprotocol/inspector"

    try:
        subprocess.run(
            command,
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Inspector failed with exit code: {e.returncode}")
    except KeyboardInterrupt:
        print("Inspector stopped.")

if __name__ == "__main__":
    main()

# npx -y @modelcontextprotocol/inspector
# this opens the inspector in a browser window, which can be used to inspect the MCP server.
