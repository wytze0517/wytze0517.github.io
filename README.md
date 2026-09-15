# Ask My Local LLM — GitHub Pages + ngrok + local LLM

A tiny test project: a GitHub Pages site with a text box, where the question
gets answered by an LLM running on your own machine, tunneled out via ngrok.

## Files
- `index.html` — the page to publish on GitHub Pages.
- `server.py` — local Flask server, forwards questions to your local LLM (Ollama).
- `requirements.txt` — Python deps for the server.

## 1. Set up the local LLM (LM Studio)
1. Install LM Studio: https://lmstudio.ai
2. In LM Studio, download/load the model `google/gemma-4-e4b`.
3. Go to the **Developer** tab and click **Start Server** (default `http://localhost:1234`).

## 2. Run the proxy server
```
pip install -r requirements.txt
python server.py
```
This starts a server on `http://localhost:5000` with an `/ask` endpoint.

## 3. Expose it with ngrok
```
ngrok http 5000
```
ngrok will print a public URL like:
```
https://abcd1234.ngrok-free.app
```
Keep this terminal (and `python server.py`, and Ollama) running the whole time
you want the page to work — ngrok tunnels only work while your machine is on
and connected.

## 4. Publish the page on GitHub Pages
1. Create a new GitHub repo (e.g. `ask-my-llm`).
2. Push `index.html` to it (root of the repo, or a `docs/` folder).
3. In the repo: Settings → Pages → set source to the branch/folder containing `index.html`.
4. GitHub gives you a URL like `https://yourname.github.io/ask-my-llm/`.

## 5. Use it
1. Open your GitHub Pages URL.
2. Paste the ngrok URL from step 3 into the "ngrok server URL" box.
3. Type a question, hit Ask.

## Notes
- CORS is wide open and there's no auth — fine for a quick test, not for anything real.
- ngrok's free tier generates a **new URL every time you restart it**, so you'll
  need to paste the new URL into the page each time you restart ngrok.
- To use a different local model, change `MODEL_NAME` in `server.py` to match
  the exact model name shown in LM Studio's Developer tab.
- To use a different local LLM runtime instead of LM Studio (e.g. Ollama, llama.cpp
  server), just point `LM_STUDIO_URL` in `server.py` at that server's API instead.
