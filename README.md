

<h1>🧠 MNIST Digit Classifier</h1>
<p>
  An end-to-end ML app to draw handwritten digits (0–9), classify them using a quantized PyTorch model, collect feedback, and display predictions — built with Streamlit and FastAPI.
</p>

<hr>

<h2>🔧 Tech Stack</h2>
<ul>
  <li><strong>Frontend</strong>: Streamlit + streamlit-drawable-canvas</li>
  <li><strong>Backend</strong>: FastAPI</li>
  <li><strong>Model</strong>: Quantized PyTorch (TorchScript)</li>
  <li><strong>Database</strong>: Supabase PostgreSQL</li>
  <li><strong>Deployment</strong>: Docker, GCP Cloud Run, Streamlit Cloud</li>
</ul>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>Draw digit input on canvas</li>
  <li>Fast, quantized inference (&lt;100 ms target latency)</li>
  <li>Confidence score returned with prediction</li>
  <li>Submit feedback with true label</li>
  <li>View recent predictions from Supabase DB</li>
  <li>Decoupled frontend/backend</li>
  <li>Optimized for local and cloud deployment</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>
<div class="project-structure">
<code>
.
├── main.py            # Streamlit UI
├── app.py             # FastAPI backend
├── db.py              # Supabase logging logic
├── model/             # Quantized .pt model
├── Dockerfile
├── requirements.txt
├── .env               # (not committed)
└── README.md
</code>
</div>

<hr>

<h2>⚙️ Local Setup</h2>

<h3>1. Clone and install dependencies</h3>
<pre><code>git clone https://github.com/your-username/PyTorch-mnist-classifier.git
cd PyTorch-mnist-classifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
</code></pre>

<h3>2. Run backend</h3>
<pre><code>uvicorn app:app --reload</code></pre>

<h3>3. Run frontend</h3>
<pre><code>streamlit run main.py</code></pre>

<hr>

<h2>🌐 Environment Variables</h2>
<p>Create a file named <code>.env</code> with the following content:</p>
<pre><code>PREDICTION_API_URL=https://your-api-url/predict

SUPABASE_HOST=your.supabase.db
SUPABASE_DB=postgres
SUPABASE_USER=your_user
SUPABASE_PASSWORD=your_password
SUPABASE_PORT=5432
</code></pre>

<hr>

<h2>🐳 Docker + GCP Deployment</h2>

<h3>1. Build Docker image</h3>
<pre><code>docker build -t gcr.io/YOUR_PROJECT_ID/mnist-api .</code></pre>

<h3>2. Push to GCP</h3>
<pre><code>docker push gcr.io/YOUR_PROJECT_ID/mnist-api</code></pre>

<h3>3. Deploy to Cloud Run</h3>
<pre><code>gcloud run deploy mnist-api \
  --image gcr.io/YOUR_PROJECT_ID/mnist-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
</code></pre>

<hr>

<h2>🔁 API Reference</h2>

<h3>POST <code>/predict</code></h3>
<p>Request body (JSON):</p>
<pre><code>{
  "pixels": [/* 784 grayscale pixel values */],
  "true_label": 7            /* optional */
}
</code></pre>

<p>Response (JSON):</p>
<pre><code>{
  "predicted": 7,
  "confidence": 98.3
}
</code></pre>

<h3>GET <code>/</code></h3>
<p>Health check:</p>
<pre><code>{
  "status": "ok",
  "message": "MNIST model is live and ready!"
}
</code></pre>

<hr>

<h2>🧠 Model Details</h2>
<ul>
  <li>Trained on MNIST</li>
  <li>Quantized to INT8 using PyTorch</li>
  <li>Exported as TorchScript (<code>.pt</code>)</li>
  <li>Loaded with <code>torch.jit.load()</code> for fast inference</li>
  <li>Inference time: &lt; 1 ms (fbgemm engine)</li>
</ul>

<hr>

<h2>📊 Logs & Feedback</h2>
<ul>
  <li>All predictions logged to Supabase DB</li>
  <li>Only predictions with true label feedback shown in UI</li>
  <li>Recent 10 predictions displayed in a styled table</li>
</ul>

<hr>

<h2>👤 Author</h2>
<p>
  <strong>Othniel Obasi</strong><br>
  AI Product Engineer | NLP & ML Solutions | Streamlined Deployment<br>
  <a href="https://linkedin.com/in/othniel-obasi" target="_blank">LinkedIn</a> | 
  <a href="https://github.com/othnielObasi" target="_blank">GitHub</a>
</p>

<hr>

<h2>📄 License</h2>
<p>This project is licensed under the MIT License.</p>
