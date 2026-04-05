import Foundation
import Combine
import GRPC
import NIO

#if os(iOS)
import ARKit
#elseif os(macOS)
import Vision
import AVFoundation
#endif

class OmniScannerEngine: NSObject, ObservableObject {
    @Published var vertexCount: Int = 0
    private var channel: ClientConnection?
    private var client: Facial_FacialServiceNIOClient?
    
    #if os(iOS)
    private let session = ARSession()
    #endif

    override init() {
        super.init()
        // Initialize Sovereign gRPC connection to M4 local node
        let group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
        self.channel = ClientConnection.insecure(group: group)
            .connect(host: "localhost", port: 50051)
        self.client = Facial_FacialServiceNIOClient(channel: self.channel!)
    }

    func engageScanner() {
        #if os(iOS)
        guard ARFaceTrackingConfiguration.isSupported else { 
            print("[ENGINE] TrueDepth architecture not available.")
            return 
        }
        let config = ARFaceTrackingConfiguration()
        session.delegate = self
        session.run(config, options: [.resetTracking, .removeExistingAnchors])
        print("[SWIFT] iOS ARKit TrueDepth Engaged. BitNet Edge Node Ready.")
        #elseif os(macOS)
        print("[SWIFT] macOS Vision Framework Bypass (Awaiting Native Matrix).")
        #endif
    }
    
    deinit {
        try? channel?.close().wait()
    }
}

#if os(iOS)
extension OmniScannerEngine: ARSessionDelegate {
    func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
        guard let faceAnchor = anchors.compactMap({ $0 as? ARFaceAnchor }).first else { return }
        
        let vertices = faceAnchor.geometry.vertices
        
        DispatchQueue.main.async {
            self.vertexCount = vertices.count
        }
        
        // Construct gRPC Payload for JuniorOmega Sandbox
        var request = Facial_FacialMesh()
        request.vertices = vertices.flatMap { [$0.x, $0.y, $0.z] }
        
        // Transmit to Python ledger
        _ = self.client?.sendFacialMesh(request).response.always { result in
            switch result {
            case .success(let response):
                print("[gRPC] Pipeline Status: \(response.status) | G-Code: \(response.gcodePath)")
            case .failure(let error):
                print("[gRPC] Transmission Failure: \(error)")
            }
        }
    }
}
#endif
