# JuniorOmega
**JuniorOmega** is a high-fidelity, low-power spatial data processing and fabrication pipeline engineered explicitly for **Apple Silicon (M4/M1)**. 

Designed by JuniorCloud LLC, this SDK bridges the gap between raw optical/FSD imaging, manifold SVD topology generation, and CNC/robotic fabrication. It leverages Apple's `mlx.core` and `MPS` (Metal Performance Shaders) to execute high-density point cloud tensor math without relying on cloud-compute or traditional PyTorch overhead.

## Core Architecture

The pipeline consists of five primary nodes:
1. **Input (Optical/FSD):** Ingests real camera or LiDAR-style datasets, extracting sparse point clouds.
2. **Sandbox (Mid-Engine):** An interactive layer allowing for threshold customization and BitNet/LLM agentic overrides before fabrication.
3. **Core (MLX SVD):** Executes native Anisotropic Tensor Decomposition ($A = U \Sigma V^T$) to extract surface normals, curvature, and topological void detection.
4. **Fabrication (G-Code):** Translates the optimized topological mesh directly into standard 3-axis G-code for CNC milling or 3D printing of "optimal pads."
5. **Output (Metal Render):** Headless Blender integration utilizing the Metal API to shade and export final `.glb` artifacts.

## Requirements
* **Hardware:** Apple Silicon (M1/M2/M3/M4) highly recommended for MPS acceleration.
* **OS:** macOS 14.0+ (Sonoma/Sequoia).
* **Python:** 3.10+
* **Dependencies:** `mlx`, `numpy`, `gradio`, `opencv-python`, `Pillow`.

## Installation

```bash
git clone [https://github.com/YourOrg/JuniorOmega.git](https://github.com/YourOrg/JuniorOmega.git)
cd JuniorOmega
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
