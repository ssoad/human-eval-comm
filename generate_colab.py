import json
import textwrap


UPSTREAM_REMOTE = "https://github.com/ssoad/human-eval-comm.git"
UPSTREAM_REF = "beta"
RESULTS_DIR = "/content/results"


def md(text: str):
    text = textwrap.dedent(text).strip() + "\n"
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(True),
    }


def code(text: str, title: str = ""):
    text = text.strip("\n")
    lines = text.splitlines()
    first_non_empty = next((line for line in lines if line.strip()), "")
    leading = len(first_non_empty) - len(first_non_empty.lstrip())
    if leading:
        prefix = " " * leading
        lines = [line[len(prefix):] if line.startswith(prefix) else line for line in lines]
    text = "\n".join(lines).strip() + "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"cellView": "form"} if title else {},
        "outputs": [],
        "source": text.splitlines(True),
    }


nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": [],
    "metadata": {
        "colab": {
            "name": "HumanEvalComm_V2_Ollama_Benchmark.ipynb",
            "provenance": [],
            "gpuType": "T4",
        },
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3",
        },
        "language_info": {
            "name": "python",
        },
        "accelerator": "GPU",
    },
}

nb["cells"] = [

    # ── Intro ──────────────────────────────────────────────────────────────────
    md("""
    # HumanEvalComm V2 — Ollama Benchmark on Colab

    Runs the HumanEvalComm V2 benchmark pipeline entirely with **local Ollama models**
    on a Colab GPU instance.

    ## How to use
    1. Select **Runtime → Change runtime type → T4 GPU**.
    2. Run cells **top-to-bottom**.  Each section header tells you what it does.
    3. To run only one model for a quick smoke test, set `SINGLE_MODEL_SMOKE = True`
       in the **Configuration** cell.

    ## Default models (all fit comfortably on a free T4)

    | Alias | Ollama tag | VRAM (approx) |
    |---|---|---|
    | `qwen25_coder_7b` | `qwen2.5-coder:7b` | ~4 GB |
    | `deepseek_coder_6b` | `deepseek-coder:6.7b` | ~4 GB |
    | `codegemma_7b` | `codegemma:7b` | ~4 GB |
    | `starcoder2_7b` | `starcoder2:7b` | ~4 GB |
    | `codellama_7b` | `codellama:7b-instruct` | ~4 GB |

    > **Tip:** pulling and evaluating all five models takes a long time.
    > Start with `SINGLE_MODEL_SMOKE = True` to validate the pipeline, then
    > set it to `False` for the full run.
    """),

    # ── Configuration ─────────────────────────────────────────────────────────
    code(f"""
        #@title ⚙️ Configuration — run this first
        # ── Repository ──────────────────────────────────────────────────────
        UPSTREAM_REMOTE_URL = "{UPSTREAM_REMOTE}"
        UPSTREAM_REF        = "{UPSTREAM_REF}"
        REPO_DIR            = "/content/human-eval-comm-v2"

        # ── Results storage ─────────────────────────────────────────────────
        # Default: local /content (lost when session ends).
        # After mounting Drive (next cell) this is overridden automatically.
        RESULTS_ROOT = "{RESULTS_DIR}"

        # ── Benchmark limits ────────────────────────────────────────────────
        SMOKE_MAX_PROBLEMS      = 2      # problems for the quick smoke test
        STANDARD_MAX_PROBLEMS   = 1000
        UNFEASIBLE_MAX_PROBLEMS = 1000

        # ── Ollama settings ─────────────────────────────────────────────────
        LOCAL_API_BASE = "http://localhost:11434/v1"
        # Per-request timeout in seconds.  Keep >=300 for local models — the
        # first inference call includes model loading which can be slow.
        MODEL_TIMEOUT  = 300

        # ── Model list ───────────────────────────────────────────────────────
        # All 5 models fit on a free T4 (16 GB VRAM) individually.
        OLLAMA_MODELS = [
            {{"name": "qwen25_coder_7b",   "ollama": "qwen2.5-coder:7b"}},
            {{"name": "deepseek_coder_6b", "ollama": "deepseek-coder:6.7b"}},
            {{"name": "codegemma_7b",      "ollama": "codegemma:7b"}},
            {{"name": "starcoder2_7b",     "ollama": "starcoder2:7b"}},
            {{"name": "codellama_7b",      "ollama": "codellama:7b-instruct"}},
        ]

        # Set True to only benchmark the first model — useful for a quick sanity check.
        SINGLE_MODEL_SMOKE = False
        if SINGLE_MODEL_SMOKE:
            OLLAMA_MODELS = OLLAMA_MODELS[:1]

        print(f"Repo    : {{UPSTREAM_REMOTE_URL}} @ {{UPSTREAM_REF}}")
        print(f"Results : {{RESULTS_ROOT}}")
        print(f"Timeout : {{MODEL_TIMEOUT}}s per request")
        print(f"Models  : {{', '.join(m['ollama'] for m in OLLAMA_MODELS)}}")
        """),

    # ── Drive mount (optional) ────────────────────────────────────────────────
    code("""
        #@title 💾 Mount Google Drive (optional — skip if not needed)
        # If Drive mounts successfully, RESULTS_ROOT is updated so results
        # survive after the Colab session ends.
        try:
            from google.colab import drive
            drive.mount("/content/drive")
            RESULTS_ROOT = "/content/drive/MyDrive/HumanEvalComm_V2_Results"
            print(f"Drive mounted. Results → {RESULTS_ROOT}")
        except Exception as e:
            print(f"Drive not mounted ({e}). Using local path: {RESULTS_ROOT}")
        """),

    # ── Clone / update repo ───────────────────────────────────────────────────
    code("""
        #@title 📦 Clone / update repository
        import os
        import subprocess
        from pathlib import Path


        def run(cmd, cwd=None, check=True):
            print("$", " ".join(cmd))
            result = subprocess.run(cmd, cwd=cwd, check=check, text=True,
                                    capture_output=True)
            if result.stdout:
                print(result.stdout.rstrip())
            if result.stderr:
                print(result.stderr.rstrip())
            return result


        repo_path = Path(REPO_DIR)
        if repo_path.exists():
            print(f"Repo exists at {repo_path}. Fetching latest {UPSTREAM_REF}...")
            run(["git", "remote", "remove", "upstream"], cwd=repo_path, check=False)
            run(["git", "remote", "add",    "upstream", UPSTREAM_REMOTE_URL], cwd=repo_path)
            run(["git", "fetch", "--depth", "1", "upstream", UPSTREAM_REF], cwd=repo_path)
            run(["git", "checkout", "-B", "colab-run", "FETCH_HEAD"], cwd=repo_path)
        else:
            run(["git", "init", str(repo_path)])
            run(["git", "remote", "add", "upstream", UPSTREAM_REMOTE_URL], cwd=repo_path)
            run(["git", "fetch", "--depth", "1", "upstream", UPSTREAM_REF], cwd=repo_path)
            run(["git", "checkout", "-B", "colab-run", "FETCH_HEAD"], cwd=repo_path)

        os.chdir(repo_path)
        run(["git", "rev-parse", "--short", "HEAD"], cwd=repo_path)
        print(f"Working directory: {os.getcwd()}")
        """),

    # ── Python dependencies ───────────────────────────────────────────────────
    code("""
        #@title 🐍 Install Python dependencies
        import sys
        import subprocess
        from pathlib import Path

        req = Path("requirements_v2.txt")
        if not req.exists():
            req = Path("requirement.txt")

        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
                       check=True)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q",
             "python-dotenv", "nbformat", "plotly", "kaleido", "statsmodels"],
            check=True,
        )
        print(f"✅ Dependencies installed from {req}")
        """),

    # ── Install Ollama ────────────────────────────────────────────────────────
    code("""
        #@title 🦙 Install Ollama
        import subprocess

        print("Installing Ollama...")
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh",
                       shell=True, check=True)
        print("✅ Ollama installed.")
        """),

    # ── Start Ollama server ───────────────────────────────────────────────────
    code("""
        #@title ▶️ Start Ollama server
        import os
        import subprocess
        import time
        import requests

        os.environ["LOCAL_API_BASE"] = LOCAL_API_BASE
        os.environ["OLLAMA_HOST"]    = "127.0.0.1:11434"

        ollama_log = open("/tmp/ollama.log", "w")
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=ollama_log,
            stderr=subprocess.STDOUT,
            env=os.environ.copy(),
        )

        print("Waiting for Ollama to be ready...")
        ready = False
        for _ in range(60):
            try:
                if requests.get("http://localhost:11434/api/tags", timeout=2).status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
            time.sleep(2)

        if ready:
            print("✅ Ollama server is ready.")
        else:
            print("❌ Ollama did not start. Check /tmp/ollama.log:")
            print(open("/tmp/ollama.log").read())
            raise RuntimeError("Ollama startup failed")
        """),

    # ── Pull models ───────────────────────────────────────────────────────────
    code("""
        #@title ⬇️ Pull Ollama models
        import subprocess

        for m in OLLAMA_MODELS:
            print(f"\\nPulling {m['ollama']}...")
            subprocess.run(["ollama", "pull", m["ollama"]], check=True)

        print("\\n✅ Models available:")
        subprocess.run(["ollama", "list"], check=True)
        """),

    # ── Pre-flight API test ───────────────────────────────────────────────────
    code("""
        #@title 🔍 Pre-flight: verify Ollama API responds
        # Sends one real chat request to the first model before the benchmark.
        # If this fails, fix Ollama before proceeding.
        import json
        import requests

        test_model = OLLAMA_MODELS[0]["ollama"]
        print(f"Testing API with model: {test_model}")

        resp = requests.post(
            "http://localhost:11434/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": test_model,
                "messages": [{"role": "user", "content": "Reply only with the word: OK"}],
                "max_tokens": 10,
                "temperature": 0.0,
            },
            timeout=MODEL_TIMEOUT,
        )
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"].strip()
        print(f"✅ API response: {reply!r}")
        """),

    # ── Build benchmark args + streaming helper ───────────────────────────────
    code("""
        #@title 🔧 Build benchmark arguments + streaming helper
        import os
        import subprocess
        from pathlib import Path

        Path(RESULTS_ROOT).mkdir(parents=True, exist_ok=True)

        # Format: name|ollama_tag|provider|max_tokens|temperature
        # Using | as separator avoids ambiguity with colons inside Ollama model tags
        # (e.g. "qwen2.5-coder:7b" contains a colon that would confuse : splitting).
        MODEL_ARGS = []
        for m in OLLAMA_MODELS:
            MODEL_ARGS.extend(["--models", f"{m['name']}|{m['ollama']}|local|1024|0.1"])

        def run_benchmark(cmd, env=None):
            \"\"\"Run a benchmark command and stream its stdout/stderr in real-time.\"\"\"
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                bufsize=1,
                universal_newlines=True,
            )
            for line in proc.stdout:
                print(line, end="", flush=True)
            proc.wait()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd)

        print("Models configured:")
        for m in OLLAMA_MODELS:
            print(f"  {m['name']} → {m['ollama']}")
        print(f"\\nResults root : {RESULTS_ROOT}")
        print(f"Model timeout: {MODEL_TIMEOUT}s")
        print("run_benchmark() helper ready.")
        """),

    # ── Smoke test ────────────────────────────────────────────────────────────
    code("""
        #@title 🧪 [SMOKE TEST] Run 2 problems — verify pipeline end-to-end
        import os
        from pathlib import Path

        smoke_dir = Path(RESULTS_ROOT) / "smoke_test"
        smoke_dir.mkdir(parents=True, exist_ok=True)

        print(f"Running smoke test ({SMOKE_MAX_PROBLEMS} problems)...\\n")

        cmd = [
            "python3", "-u", "src/v2_benchmark.py",
            "--dataset-path",  "Benchmark/HumanEvalComm_v2.jsonl",
            "--api-provider",  "local",
            "--max-problems",  str(SMOKE_MAX_PROBLEMS),
            "--request-delay", "0",
            "--model-timeout", str(MODEL_TIMEOUT),
            "--output-dir",    str(smoke_dir),
            *MODEL_ARGS,
        ]

        env = os.environ.copy()
        env["LOCAL_API_BASE"] = LOCAL_API_BASE

        run_benchmark(cmd, env=env)
        print(f"\\n✅ Smoke test done. Results → {smoke_dir}")
        """),

    # ── Standard benchmark ────────────────────────────────────────────────────
    code("""
        #@title 📊 [FULL] Run standard V2 benchmark
        import os
        from pathlib import Path

        standard_dir = Path(RESULTS_ROOT) / "standard_benchmark"
        standard_dir.mkdir(parents=True, exist_ok=True)

        print(f"Running full benchmark ({STANDARD_MAX_PROBLEMS} problems)...\\n")

        cmd = [
            "python3", "-u", "src/v2_benchmark.py",
            "--dataset-path",  "Benchmark/HumanEvalComm_v2.jsonl",
            "--api-provider",  "local",
            "--max-problems",  str(STANDARD_MAX_PROBLEMS),
            "--request-delay", "0",
            "--model-timeout", str(MODEL_TIMEOUT),
            "--output-dir",    str(standard_dir),
            *MODEL_ARGS,
        ]

        env = os.environ.copy()
        env["LOCAL_API_BASE"] = LOCAL_API_BASE

        run_benchmark(cmd, env=env)
        print(f"\\n✅ Full benchmark done. Results → {standard_dir}")
        """),

    # ── Unfeasible benchmark ──────────────────────────────────────────────────
    code("""
        #@title 🚧 [PUSHBACK] Run unfeasible-requirements benchmark
        import os
        from pathlib import Path

        unfeasible_dir = Path(RESULTS_ROOT) / "unfeasible_benchmark"
        unfeasible_dir.mkdir(parents=True, exist_ok=True)

        print(f"Running unfeasible benchmark ({UNFEASIBLE_MAX_PROBLEMS} problems)...\\n")

        cmd = [
            "python3", "-u", "src/v2_benchmark.py",
            "--dataset-path",  "Benchmark/HumanEvalComm_Unfeasible.jsonl",
            "--api-provider",  "local",
            "--max-problems",  str(UNFEASIBLE_MAX_PROBLEMS),
            "--request-delay", "0",
            "--model-timeout", str(MODEL_TIMEOUT),
            "--output-dir",    str(unfeasible_dir),
            *MODEL_ARGS,
        ]

        env = os.environ.copy()
        env["LOCAL_API_BASE"] = LOCAL_API_BASE

        run_benchmark(cmd, env=env)
        print(f"\\n✅ Unfeasible benchmark done. Results → {unfeasible_dir}")
        """),

    # ── Display leaderboards ──────────────────────────────────────────────────
    code("""
        #@title 🏆 Display results leaderboards
        import glob
        import os
        import pandas as pd
        from pathlib import Path
        from IPython.display import display

        def show_leaderboard(title, folder):
            path = Path(RESULTS_ROOT) / folder
            files = glob.glob(str(path / "v2_fixed_leaderboard_*.csv"))
            print(f"\\n{'='*60}")
            print(f"  {title}")
            print('='*60)
            if not files:
                print(f"  No results found in {folder}")
                return
            latest = max(files, key=os.path.getctime)
            print(f"  File: {os.path.basename(latest)}")
            df = pd.read_csv(latest)
            display(df)

        show_leaderboard("SMOKE TEST",          "smoke_test")
        show_leaderboard("STANDARD BENCHMARK",  "standard_benchmark")
        show_leaderboard("UNFEASIBLE PUSHBACK",  "unfeasible_benchmark")
        """),

    # ── Zip & download ────────────────────────────────────────────────────────
    code("""
        #@title 📥 Zip and download results
        import shutil
        from pathlib import Path
        from google.colab import files

        archive = "/content/HumanEvalComm_V2_Ollama_Results"
        shutil.make_archive(archive, "zip", RESULTS_ROOT)
        print(f"Archive: {archive}.zip")

        # Uncomment to trigger browser download:
        # files.download(f"{archive}.zip")
        """),
]


with open("HumanEvalComm_V2_Colab.ipynb", "w") as f:
    json.dump(nb, f, indent=2)
    f.write("\n")

print("Generated HumanEvalComm_V2_Colab.ipynb")
