# astro

Apache Airflow runs in containers so it requires Docker or an equivalent container management engine. I prefer a Daemon-less solution so I used Podman for this project. The installation/ set-up steps for this project (on Windows OS) are below:

1. Install WSL (allows containers to run on Windows): https://learn.microsoft.com/en-us/windows/wsl/install
2. Install Podman Desktop: https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md
3. Install Astro CLI: https://www.astronomer.io/docs/astro/cli/install-cli?tab=windows#install-the-astro-cli
4. Configure Astro CLI to use Podman: https://www.astronomer.io/docs/astro/cli/use-podman?tab=windows#configure-the-astro-cli-to-use-podman
5. Pull repository into your C:\\Users\\[username here] directory
6. Open VS Code (https://code.visualstudio.com/docs/?dv=win64user for download)
7. Install Python and Python Debugger extensions in VS Code
8. Open project folder in VS Code Explorer tab
9. Update the paths in the compose.yaml and docker-compose.override.yml files to match your directory (C:\\Users\\[username here] instead of C:\\Users\\sky031891\\)
10. Open a Terminal window within VS Code
11. Run: podman machine init
12. Run: podman machine start
13. Run: astro dev start (or ./astro dev start)
14. Airflow should launch at this URL in your web browser: http://localhost:8080
    (URL may return Err_Empty_Response for first couple mins)
15. Enter "admin" in the username and password fields and login
