import ARKit
import SwiftUI

class ScannerEngine: NSObject, ARSessionDelegate, ObservableObject {
    @Published var vertexCount: Int = 0
    private let session = ARSession()

    func start() {
        let config = ARFaceTrackingConfiguration()
        session.delegate = self
        session.run(config)
    }

    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        guard let face = anchors.first as? ARFaceAnchor else { return }
        DispatchQueue.main.async {
            self.vertexCount = face.geometry.vertices.count
            // Vertices are ready for Vaulting or gRPC transmission to WOS10 Node
        }
    }
}