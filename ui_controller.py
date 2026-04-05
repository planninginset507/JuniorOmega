# ui_controller.py
import gradio as gr
import numpy as np
import plotly.graph_objects as go
from omega_orchestrator import execute_pipeline
from core.sandbox_customizer import MidEngineSandbox

def generate_manifold_plot(vertices):
    """Renders M4 SVD output as a 3D topological mesh."""
    if vertices is None or len(vertices) == 0:
        return go.Figure()
        
    v_array = np.array(vertices)
    x, y, z = v_array[:, 0], v_array[:, 1], v_array[:, 2]
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=2, 
            color=z, 
            colorscale='Viridis', 
            opacity=0.8
        )
    )])
    
    # TradingView Dark Aesthetic
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True, zerolinecolor="gray"),
            yaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True, zerolinecolor="gray"),
            zaxis=dict(backgroundcolor="rgb(20, 20, 20)", gridcolor="gray", showbackground=True, zerolinecolor="gray"),
            bgcolor="rgb(10, 10, 10)"
        ),
        paper_bgcolor="rgb(10, 10, 10)",
        font=dict(color="#D4AF37"), # Sovereign Gold
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

def run_dashboard_pipeline(input_file, target_z, anomaly_thresh, bitnet_toggle, hardware_select):
    """Executes the Omni-Vision to G-Code orchestration layer."""
    overrides = {
        "bitnet_agent": bitnet_toggle,
        "anomaly_detection": True,
        "curvature_weight": anomaly_thresh,
        "gcode_feedrate": 1500 if bitnet_toggle else 1200
    }
    
    file_path = input_file.name if input_file else None
    
    # Execute backend logic
    gcode_path, mesh_data = execute_pipeline(
        input_path=file_path, 
        hardware_target=hardware_select
    )
    
    # Audit Metrics extraction
    stability = mesh_data.get('svd_stability', 0.0)
    curvature = mesh_data.get('curvature', 0.0)
    status = "OPTIMAL_PAD" if stability > 0.9 else "TOPOLOGICAL_FLUID"
    
    report = f"""--- JUNIOROMEGA AUDIT ---
NODE STATUS: {status}
SVD STABILITY: {stability:.6f}
MANIFOLD CURVATURE: {curvature:.6f}
G-CODE ARTIFACT: {gcode_path}"""
    
    # Generate 3D visualization
    fig = generate_manifold_plot(mesh_data.get("vertices", []))
    
    return gcode_path, report, fig

# UI Architecture
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# JUNIOROMEGA COMMAND CENTER")
    gr.Markdown("### Sovereign Spatial Engine | JuniorCloud LLC | M4 MPS Compute")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 1. DATA INGEST")
            hardware = gr.Dropdown(
                ["none", "macbook", "iphone", "ipad", "oak_d_edge"], 
                label="Omni-Vision Hardware Target", value="none"
            )
            file_input = gr.File(label="Manual Payload (.ply, .stl, .jpg)")
            elevation = gr.Slider(0, 50, value=0, label="Target Z (mm)")
            
        with gr.Column(scale=1):
            gr.Markdown("## 2. SANDBOX CONTROLS")
            bitnet_agent = gr.Checkbox(label="Enable BitNet Agent", value=True)
            anomaly_threshold = gr.Slider(0.05, 0.5, value=0.3, label="Curvature Weight")
            run_btn = gr.Button("🚀 EXECUTE PIPELINE", variant="primary")
            
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 3. 3D TOPOLOGY PREVIEW")
            plot_out = gr.Plot(label="SVD Manifold Verification")
            
        with gr.Column(scale=1):
            gr.Markdown("## 4. FABRICATION EXPORT")
            gcode_out = gr.File(label="Optimized G-code Toolpath")
            metrics_out = gr.Textbox(label="Audit Report", lines=8)

    run_btn.click(
        run_dashboard_pipeline, 
        inputs=[file_input, elevation, anomaly_threshold, bitnet_agent, hardware],
        outputs=[gcode_out, metrics_out, plot_out]
    )

if __name__ == "__main__":
    print("[UI] JuniorOmega Command Center Online. Forwarding to Private 7860.")
    demo.launch(server_name="0.0.0.0", server_port=7860)
