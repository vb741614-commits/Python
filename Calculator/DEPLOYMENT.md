# Deploying the calculator to Render

The `render.yaml` blueprint configures this calculator as a public web service.

1. Push `calculator.py` and `render.yaml` to a GitHub repository.
2. Sign in to [Render](https://render.com/), choose **New** → **Blueprint**, and connect that repository.
3. Review the `python-calculator` service and deploy it.
4. Open the HTTPS URL Render assigns to the service to use the calculator from any device.

The service listens on Render's assigned port and network interface. No third-party
Python packages are required. The calculator is public and does not have sign-in;
anyone with its URL can use it.


