# A Little Love

A small Python web app for the interactive love page.

## Add Darling's photos

Put your pictures in this folder, using these names:

- `photos/darling-1.jpg`
- `photos/darling-2.jpg`
- `photos/darling-3.jpg`

JPG/JPEG, PNG, and WebP images are allowed. If your files use `.png` or `.webp`, change the matching `.jpg` filename in `index.html` and `script.js` to match. Each gallery picture opens with its own love note; the surprise button opens all three pictures with secret messages. Edit the notes in `script.js` and the captions/messages in `index.html` to make them personal.

## Run locally

From this folder, install the dependencies and start the server:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:8000> in your browser. To make it reachable by other devices on your local network, run `python app.py --host 0.0.0.0` and use your computer's local IP address.

## Publish it online

The root-level `render.yaml` is a Render Blueprint. Push this repository to GitHub, create a new Blueprint Instance in Render, and select the repository. Render will build the app and provide a public HTTPS URL that can be opened from anywhere.

The public URL is available after deployment; running the app on your computer alone does not publish it to the internet. The free hosting plan may spin down after inactivity.
