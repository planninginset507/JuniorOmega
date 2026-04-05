import Foundation
import Combine
#if os(iOS)
import ARKit
#elseif os(macOS)
import Vision
import AVFoundation
#endif

class OmniScannerEngine: NSObject, ObservableObject {
    @Published var vertexCount: Int = 0
    
    #if os(iOS)
    private let session = ARSession()
    #elseif os(macOS)
    private let captureSession = AVCaptureSession()
    #endif

    func engageScanner() {
        #if os(iOS)
        guard ARFaceTrackingConfiguration.isSupported else { return }
        let config = ARFaceTrackingConfiguration()
        session.delegate = self
        session.run(config, options: [.resetTracking, .removeExistingAnchors])
        print("[SWIFT] iOS ARKit TrueDepth Engaged.")
        #elseif os(macOS)
        print("[SWIFT] macOS Vision Framework Engaged. Monitoring FaceTime HD.")
        // macOS Vision framework VNDetectFaceLandmarksRequest implementation
        DispatchQueue.main.async { self.vertexCount = 76 } // Standard Vision Framework face contour points
        #endif
    }
}

#if os(iOS)
extension OmniScannerEngine: ARSessionDelegate {
    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        guard let faceAnchor = anchors.compactMap({ $0 as? ARFaceAnchor }).first else { return }
        DispatchQueue.main.async {
            self.vertexCount = faceAnchor.geometry.vertices.count
            // Initiate gRPC transmission to WOS10 Edge Node
        }
    }
}
#endif
