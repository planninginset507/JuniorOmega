
---

# JuniorOmega SDK
### Sovereign Spatial Engineering & Fabrication Pipeline
**Engineered for Apple Silicon (M4/M1) | Powered by MLX & MPS**

JuniorOmega is a high-fidelity, low-power spatial data orchestration engine. It bridges the gap between raw edge-sensor ingestion (TrueDepth/LiDAR), manifold SVD topology generation, and automated fabrication (G-code). By leveraging Apple’s `mlx.core`, JuniorOmega executes high-density tensor math on-device, eliminating cloud latency and traditional PyTorch overhead.

---

## 🛠 Core Architecture

The SDK is organized into five sovereign nodes, now expanded for decentralized edge compute:

* **1. Ingestion (Omni-Vision):** Multi-modal data capture across iPad Pro (TrueDepth), MacBook (FaceTime HD), and OAK-D spatial microprocessors.
* **2. Transport (gRPC/NIO):** A decentralized "Nervous System" using gRPC to stream 1220-vertex facial/spatial manifolds from Swift-based mobile nodes to the M4 compute core.
* **3. Core (MLX SVD):** Executes native Anisotropic Tensor Decomposition ($A = U \Sigma V^T$) to extract surface normals, curvature, and topological stability.
* **4. Sandbox (Mid-Engine):** An interactive layer for BitNet/LLM agentic overrides, allowing real-time adjustment of anomaly thresholds before fabrication.
* **5. Fabrication (G-Code):** Translates optimized meshes into topology-aware, 3-axis G-code toolpaths using adaptive feedrate and spline interpolation.

---

## 🖥 Command Center UI

JuniorOmega now includes a **TradingView-style Web Dashboard** for real-time monitoring:
* **Live SVD Audit:** View stability metrics and curvature coefficients.
* **3D Manifold Preview:** Interactive Plotly-driven 3D visualization of incoming point clouds.
* **Metal Rendering:** Headless Blender integration for high-contrast "Sovereign Gold" artifact shading.

---

## 📋 Requirements

* **Hardware:** Apple Silicon (M4/M3/M2/M1) | iPad Pro/iPhone (for TrueDepth features).
* **OS:** macOS 14.0+ (Sonoma/Sequoia) | iOS 17.0+.
* **Python:** 3.10+ (Optimized for 3.12).
* **Key Dependencies:** `mlx`, `grpcio`, `gradio`, `scipy`, `trimesh`, `mediapipe`.

---

## 🚀 Installation & Deployment

### 1. Clone & Environment
```bash
git clone https://github.com/JuniorCloudLLC/JuniorOmega.git
cd JuniorOmega
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### 2. Launching the Sovereign Node
To start the gRPC receiver (WOS10 Edge Node) and the Command Center:
```bash
# Terminal A: Start the gRPC Listener
python3 omega_orchestrator.py --grpc

# Terminal B: Start the Web Dashboard
python3 ui_controller.py
```

### 3. Swift App Deployment
Navigate to `swift_app/` and open `Package.swift` in Xcode. Deploy to a TrueDepth-capable iPhone/iPad to begin streaming spatial data to your local node.

---

## 🔐 Security & Harvester Protocol

JuniorOmega utilizes the **Enterprise Harvester** for public releases. This ensures:
* **IP Protection:** Proprietary MLX math kernels are automatically scrubbed and replaced with Community Stubs in public branches.
* **Vaulting:** Non-manifest artifacts and test data are moved to `Vaults/Quarantine` to maintain repository hygiene.
* **Auditability:** Every harvest generates a JSON audit log for regulatory and engineering compliance.

---

**Identity:** Generated for the Lead Architect of JuniorCloud LLC.  
**Tone:** Logic-dense engineering rigor. No fluff. Finalized for Public Release.
